import bcrypt
from datetime import datetime
from app.controllers.db_controller import DatabaseController
import psycopg2

class UserRepository:
    def __init__(self):
        self.db_controller = DatabaseController()

    def register_user(self, username, email, password, name, phone_number, role_name):
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user_query = """
                INSERT INTO users (username, email, password_hash, name, phone_number)
                VALUES (%s, %s, %s, %s, %s) RETURNING user_id;
            """
            user_result = self.db_controller.execute_query(user_query, (username, email, password_hash, name, phone_number), True)
            if not user_result:
                raise Exception("User registration failed")

            role_query = "SELECT role_id FROM roles WHERE role_name = %s;"
            role_result = self.db_controller.execute_query(role_query, (role_name.lower(),), True)
            if not role_result:
                raise Exception(f"Role '{role_name}' not found")

            self.db_controller.execute_query("INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s);", (user_result[0]['user_id'], role_result[0]['role_id']))

            return True, "User registered successfully"

        except psycopg2.errors.UniqueViolation as e:
            return False, "Username or email already exists"
        except Exception as e:
            return False, str(e)

    def verify_login(self, username, password):
        query = """
            SELECT u.*, r.role_name, r.role_id
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE u.username = %s;
        """
        try:
            result = self.db_controller.execute_query(query, (username,), True)
            if not result:
                return False, "Invalid username or password", None

            user = result[0]
            if user['account_status'] != 'active':
                return False, f"Account is {user['account_status']}", None

            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                self.db_controller.execute_query(
                    "UPDATE users SET last_login = %s WHERE user_id = %s",
                    (datetime.now(), user['user_id'])
                )

                permissions_query = """
                    SELECT p.permission_name
                    FROM role_permissions rp
                    JOIN permissions p ON rp.permission_id = p.permission_id
                    WHERE rp.role_id = %s;
                """
                permissions_result = self.db_controller.execute_query(
                    permissions_query, (user['role_id'],), True
                )
                permissions = [perm['permission_name'] for perm in permissions_result]

                return True, "Login successful", {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'role': user['role_name'],
                    'name': user['name'],
                    'email': user['email'],
                    'phone_number': user['phone_number'],
                    'permissions': permissions
                }
            return False, "Invalid username or password", None

        except Exception as e:
            return False, "Login failed due to an error", None


    def get_user_by_id(self, user_id):
        query = """
            SELECT u.user_id, u.username, u.email, u.name, u.phone_number,
                   u.account_status, u.created_at, u.last_login,
                   r.role_name
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE u.user_id = %s;
        """
        try:
            result = self.db_controller.execute_query(query, (user_id,), True)
            return result[0] if result else None
        except Exception as e:
            return None

    def update_user(self, user_id, name=None, email=None, phone_number=None):
        try:
            update_parts = []
            params = []

            if name is not None:
                update_parts.append("name = %s")
                params.append(name)

            if email is not None:
                update_parts.append("email = %s")
                params.append(email)

            if phone_number is not None:
                update_parts.append("phone_number = %s")
                params.append(phone_number)

            if not update_parts:
                return True, "No updates provided"

            query = f"""
                UPDATE users
                SET {', '.join(update_parts)}
                WHERE user_id = %s;
            """
            params.append(user_id)

            self.db_controller.execute_query(query, tuple(params))
            return True, "User information updated successfully"

        except Exception as e:
            return False, str(e)

    def change_password(self, user_id, current_password, new_password):
        try:
            query = "SELECT password_hash FROM users WHERE user_id = %s;"
            result = self.db_controller.execute_query(query, (user_id,), True)

            if not result:
                return False, "User not found"

            current_hash = result[0]['password_hash']

            if not bcrypt.checkpw(current_password.encode('utf-8'), current_hash.encode('utf-8')):
                return False, "Current password is incorrect"

            new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_query = "UPDATE users SET password_hash = %s WHERE user_id = %s;"
            self.db_controller.execute_query(update_query, (new_hash, user_id))

            return True, "Password changed successfully"

        except Exception as e:
            return False, str(e)
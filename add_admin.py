import bcrypt
import psycopg2

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def add_admin_users():
    admin_users = [
        {
            "username": "admin_1",
            "email": "admin1@nexuslibrary.com",
            "password": "Admin@123",
            "name": "Admin User 1",
            "phone_number": "1234567890"
        },
        {
            "username": "admin_2",
            "email": "admin2@nexuslibrary.com",
            "password": "Admin@123",
            "name": "Admin User 2",
            "phone_number": "1234567891"
        },
        {
            "username": "admin_3",
            "email": "admin3@nexuslibrary.com",
            "password": "Admin@123",
            "name": "Admin User 3",
            "phone_number": "1234567892"
        }
    ]

    try:
        with psycopg2.connect(
            dbname='NexusLibrary',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        ) as conn:
            with conn.cursor() as cursor:

                # Get admin role ID
                cursor.execute("SELECT role_id FROM roles WHERE role_name = 'admin'")
                role_result = cursor.fetchone()
                if not role_result:
                    print("Error: 'admin' role not found in the roles table.")
                    return
                admin_role_id = role_result[0]

                for admin in admin_users:
                    password_hash = hash_password(admin['password'])

                    # Insert admin user
                    cursor.execute(
                        """
                        INSERT INTO users (username, email, password_hash, name, phone_number, account_status)
                        VALUES (%s, %s, %s, %s, %s, 'active')
                        RETURNING user_id;
                        """,
                        (admin['username'], admin['email'], password_hash, admin['name'], admin['phone_number'])
                    )
                    user_id = cursor.fetchone()[0]

                    # Assign admin role
                    cursor.execute(
                        """
                        INSERT INTO user_roles (user_id, role_id, assigned_by)
                        VALUES (%s, %s, NULL);
                        """,
                        (user_id, admin_role_id)
                    )

                    print(f"Admin user '{admin['username']}' added successfully.")

                conn.commit()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    add_admin_users()

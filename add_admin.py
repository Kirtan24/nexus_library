import bcrypt
import psycopg2

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def add_admin_user():
    # username = 'admin_1'
    # email = 'admin1@nexuslibrary.com'
    # password = 'Admin@123'
    # name = 'Admin User 1'
    # phone_number = '1234567890'

    username = 'admin_2'
    email = 'admin2@nexuslibrary.com'
    password = 'Admin@123'
    name = 'Admin User 2'
    phone_number = '1234567890'

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        conn = psycopg2.connect(
            dbname='NexusLibrary',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()

        # Insert Admin User
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, name, phone_number, account_status)
            VALUES (%s, %s, %s, %s, %s, 'active')
            RETURNING user_id;
            """,
            (username, email, password_hash, name, phone_number)
        )
        user_id = cursor.fetchone()[0]

        # Get Admin Role ID
        cursor.execute("SELECT role_id FROM roles WHERE role_name = 'admin'")
        role_id = cursor.fetchone()[0]

        # Assign Admin Role
        cursor.execute(
            """
            INSERT INTO user_roles (user_id, role_id, assigned_by)
            VALUES (%s, %s, NULL);
            """,
            (user_id, role_id)
        )

        # Commit Changes
        conn.commit()
        print(f"Admin user '{username}' added successfully!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    add_admin_user()

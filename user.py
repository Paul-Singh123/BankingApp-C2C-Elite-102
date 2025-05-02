from db_config import connect_db
from utils import hash_password, check_password

def register_user():
    while True:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Create a password: ")

        hashed = hash_password(password)

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (name, email, password_hash, user_type)
                    VALUES (%s, %s, %s, 'customer')
                """, (name, email, hashed))
                conn.commit()
                print("Registration successful.")
                break
            except Exception as err:
                print(f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

        back = input("Press 'b' to go back or any key to try again: ")
        if back.lower() == 'b':
            return

def login_user():
    while True:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, password_hash, account_balance, user_type FROM users WHERE email = %s", (email,))
                result = cursor.fetchone()

                if result:
                    user_id, name, stored_hash, balance, user_type = result
                    if check_password(password, stored_hash):
                        print(f"Welcome back, {name}!")
                        return user_id, name, float(balance), user_type
                    else:
                        print("Incorrect password.")
                else:
                    print("No account found with that email.")

            except Exception as err:
                print(f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

        back = input("Press 'b' to go back or any key to try again: ")
        if back.lower() == 'b':
            return None, None, None, None

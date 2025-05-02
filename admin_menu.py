from db_config import connect_db
from transfer import transfer_money
from colorama import Fore, Style, init

init(autoreset=True)

def admin_menu(admin_id, admin_name):
    while True:
        print(f"\n{Fore.CYAN}Admin {admin_name}, welcome to Singh Bank Admin Portal.")
        print(Fore.YELLOW + "=" * 45)
        print(Fore.GREEN + "         Singh Bank - Admin Menu")
        print(Fore.YELLOW + "=" * 45)
        print(Fore.BLUE + "1. View All Users")
        print("2. Transfer Funds")
        print("3. View My Balance")
        print("4. Deposit to My Account")
        print("5. Withdraw from My Account")
        print("6. Admin Controls")
        print("7. Logout")
        print(Fore.YELLOW + "=" * 45)

        choice = input("Select an option: ").strip()

        if choice == "1":
            view_all_users()
        elif choice == "2":
            transfer_money(admin_id, admin_name, is_admin=True)
        elif choice == "3":
            view_balance(admin_id)
        elif choice == "4":
            deposit(admin_id)
        elif choice == "5":
            withdraw(admin_id)
        elif choice == "6":
            admin_controls()
        elif choice == "7":
            print(Fore.GREEN + "Logging out...")
            break
        else:
            print(Fore.RED + "Invalid option. Try again.")

def admin_controls():
    print(Fore.MAGENTA + "\n--- Admin Controls ---")
    print("1. Delete a User")
    print("2. Modify User Details")
    sub = input("Choose an option: ")

    if sub == "1":
        delete_user()
    elif sub == "2":
        modify_user_details()
    else:
        print(Fore.RED + "Invalid option.")

def view_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, user_type, account_balance FROM users")
    users = cursor.fetchall()

    print(Fore.CYAN + "\nAll Users:")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Type: {user[3]}, Balance: ${user[4]:.2f}")

    cursor.close()
    conn.close()

def delete_user():
    user_id = input("Enter the ID of the user to delete: ")
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    if cursor.rowcount:
        print(Fore.GREEN + "User deleted.")
    else:
        print(Fore.RED + "User not found.")

    conn.commit()
    cursor.close()
    conn.close()

def modify_user_details():
    user_id = input("Enter the ID of the user to modify: ").strip()

    fields = {
        "1": "name",
        "2": "email",
        "3": "password",
        "4": "account_balance"
    }

    print(Fore.MAGENTA + "\nWhat would you like to modify?")
    print("1. Name")
    print("2. Email")
    print("3. Password")
    print("4. Account Balance")
    field_choice = input("Select a field: ").strip()

    if field_choice not in fields:
        print(Fore.RED + "Invalid choice.")
        return

    new_value = input(f"Enter the new value for {fields[field_choice]}: ").strip()

    if fields[field_choice] == "account_balance":
        try:
            new_value = float(new_value)
        except ValueError:
            print(Fore.RED + "Balance must be a number.")
            return

    conn = connect_db()
    cursor = conn.cursor()
    sql = f"UPDATE users SET {fields[field_choice]} = %s WHERE id = %s"
    cursor.execute(sql, (new_value, user_id))

    if cursor.rowcount:
        print(Fore.GREEN + f"{fields[field_choice].capitalize()} updated successfully.")
    else:
        print(Fore.RED + "User not found or update failed.")

    conn.commit()
    cursor.close()
    conn.close()

def view_balance(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT account_balance FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        print(Fore.GREEN + f"Current Balance: ${result[0]:.2f}")
    else:
        print(Fore.RED + "Account not found.")

    cursor.close()
    conn.close()

def deposit(user_id):
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print(Fore.RED + "Amount must be greater than 0.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET account_balance = account_balance + %s WHERE id = %s", (amount, user_id))
        cursor.execute("INSERT INTO transactions (user_id, type, amount, description) VALUES (%s, 'deposit', %s, 'Admin deposit')", (user_id, amount))

        conn.commit()
        print(Fore.GREEN + f"${amount:.2f} deposited successfully.")

    except Exception as e:
        print(Fore.RED + "Error during deposit:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def withdraw(user_id):
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print(Fore.RED + "Amount must be greater than 0.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT account_balance FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()

        if not result:
            print(Fore.RED + "Account not found.")
            return

        current_balance = float(result[0])
        if current_balance < amount:
            print(Fore.RED + "Insufficient balance.")
            return

        cursor.execute("UPDATE users SET account_balance = account_balance - %s WHERE id = %s", (amount, user_id))
        cursor.execute("INSERT INTO transactions (user_id, type, amount, description) VALUES (%s, 'withdrawal', %s, 'Admin withdrawal')", (user_id, amount))

        conn.commit()
        print(Fore.GREEN + f"${amount:.2f} withdrawn successfully.")

    except Exception as e:
        print(Fore.RED + "Error during withdrawal:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

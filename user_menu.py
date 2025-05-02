from db_config import connect_db
from transfer import transfer_money
from colorama import Fore, Style, init

init(autoreset=True)

def user_menu(user_id, name, balance):
    while True:
        print(f"\n{Fore.CYAN}Welcome {name}!")
        print(Fore.YELLOW + "=" * 40)
        print(Fore.GREEN + "      Singh Bank - Customer Menu")
        print(Fore.YELLOW + "=" * 40)
        print(Fore.BLUE + "1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Advanced Options")
        print("6. Logout")
        print(Fore.YELLOW + "=" * 40)

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            print(f"{Fore.GREEN}Your current balance is: ${balance:.2f}")

        elif choice == '2':
            amount = float(input("Enter amount to deposit: "))
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET account_balance = account_balance + %s WHERE id = %s", (amount, user_id))
            cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, 'deposit', %s)", (user_id, amount))
            conn.commit()
            cursor.execute("SELECT account_balance FROM users WHERE id = %s", (user_id,))
            balance = cursor.fetchone()[0]
            print(f"{Fore.GREEN}Deposited ${amount:.2f}. New balance is ${balance:.2f}")
            cursor.close()
            conn.close()

        elif choice == '3':
            amount = float(input("Enter amount to withdraw: "))
            if amount > balance:
                print(Fore.RED + "Insufficient balance.")
            else:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET account_balance = account_balance - %s WHERE id = %s", (amount, user_id))
                cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, 'withdrawal', %s)", (user_id, amount))
                conn.commit()
                cursor.execute("SELECT account_balance FROM users WHERE id = %s", (user_id,))
                balance = cursor.fetchone()[0]
                print(f"{Fore.GREEN}Withdrew ${amount:.2f}. New balance is ${balance:.2f}")
                cursor.close()
                conn.close()

        elif choice == '4':
            transfer_money(user_id, name)

        elif choice == '5':
            print(Fore.MAGENTA + "\n--- Advanced Controls ---")
            print("1. Modify Account Details")
            print("2. Delete Account")
            adv_choice = input("Choose an option: ").strip()

            if adv_choice == '1':
                email = input("Enter new email: ")
                password = input("Enter new password: ")
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET email = %s, password = %s WHERE id = %s", (email, password, user_id))
                conn.commit()
                print(Fore.GREEN + "Account details updated.")
                cursor.close()
                conn.close()

            elif adv_choice == '2':
                confirm = input("Are you sure you want to delete your account? (yes/no): ")
                if confirm.lower() == 'yes':
                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    conn.commit()
                    print(Fore.RED + "Account deleted.")
                    cursor.close()
                    conn.close()
                    break
            else:
                print(Fore.RED + "Invalid option.")

        elif choice == '6':
            print(Fore.GREEN + "Goodbye!")
            break

        else:
            print(Fore.RED + "Invalid choice. Try again.")

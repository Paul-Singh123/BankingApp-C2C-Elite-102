from db_config import connect_db
from colorama import Fore, Style, init

init(autoreset=True)

def transfer_money(sender_id, sender_name, is_admin=False):
    try:
        print(Fore.MAGENTA + "\n--- Fund Transfer ---")
        recipient_id = input("Enter recipient ID: ").strip()
        recipient_name = input("Enter recipient name: ").strip().lower()
        recipient_email = input("Enter recipient email: ").strip().lower()

        try:
            amount = float(input("Enter amount to transfer: "))
            if amount <= 0:
                print(Fore.RED + "Transfer amount must be greater than 0.")
                return
        except ValueError:
            print(Fore.RED + "Invalid amount entered.")
            return

        conn = connect_db()
        cursor = conn.cursor()

        # Fetch sender's balance
        cursor.execute("SELECT account_balance FROM users WHERE id = %s", (sender_id,))
        sender_result = cursor.fetchone()
        if not sender_result:
            print(Fore.RED + "Sender not found.")
            return

        sender_balance = float(sender_result[0])
        if amount > sender_balance:
            print(Fore.RED + "Insufficient balance for transfer.")
            return

        # Fetch and validate recipient
        cursor.execute("""
            SELECT id, account_balance FROM users 
            WHERE id = %s AND LOWER(name) = %s AND LOWER(email) = %s
        """, (recipient_id, recipient_name, recipient_email))
        recipient = cursor.fetchone()

        if not recipient:
            print(Fore.RED + "Recipient not found or incorrect info.")
            return

        # Transfer logic
        cursor.execute("UPDATE users SET account_balance = account_balance - %s WHERE id = %s", (amount, sender_id))
        if cursor.rowcount != 1:
            print(Fore.RED + "Failed to update sender balance.")
            return

        cursor.execute("UPDATE users SET account_balance = account_balance + %s WHERE id = %s", (amount, recipient_id))
        if cursor.rowcount != 1:
            print(Fore.RED + "Failed to update recipient balance.")
            return

        # Log transactions
        cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, description)
            VALUES (%s, 'transfer_out', %s, %s)
        """, (sender_id, amount, f"Transfer to {recipient_name} (ID {recipient_id})"))

        cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, description)
            VALUES (%s, 'transfer_in', %s, %s)
        """, (recipient_id, amount, f"Transfer from {sender_name} (ID {sender_id})"))

        if cursor.rowcount < 1:
            print(Fore.RED + "Failed to log transaction.")
            return

        conn.commit()
        print(Fore.GREEN + f"Transfer complete: ${amount:.2f} sent to {recipient_name.title()} (ID: {recipient_id})")

    except Exception as e:
        print(Fore.RED + "Error during transfer:", e)
        if conn:
            conn.rollback()

    finally:
        if conn:
            cursor.close()
            conn.close()

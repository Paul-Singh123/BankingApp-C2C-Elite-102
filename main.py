from colorama import Fore, Style, init
from user import register_user, login_user
from user_menu import user_menu
from admin_menu import admin_menu
from ui_utils import print_header  # Imports Singh Bank ASCII art

init(autoreset=True)  # Automatically resets color after each print

def main():
    print_header()  # Display Singh Bank header with color

    while True:
        print(Fore.YELLOW + "\n" + "=" * 44)
        print(Fore.CYAN + "           Singh Bank Main Menu           ")
        print(Fore.YELLOW + "=" * 44 + Style.RESET_ALL)

        print(Fore.GREEN + "1." + Style.RESET_ALL + " Register (Customer Only)")
        print(Fore.GREEN + "2." + Style.RESET_ALL + " Login as Customer")
        print(Fore.GREEN + "3." + Style.RESET_ALL + " Login as Admin")
        print(Fore.GREEN + "4." + Style.RESET_ALL + " Exit")

        print(Fore.YELLOW + "=" * 44 + Style.RESET_ALL)

        choice = input(Fore.BLUE + "Choose an option: " + Style.RESET_ALL)

        if choice == '1':
            register_user()

        elif choice == '2':
            user_id, name, balance, user_type = login_user()
            if user_id and user_type.lower() == 'customer':
                user_menu(user_id, name, balance)
            elif user_type.lower() == 'admin':
                print(Fore.RED + "\n You're an admin! Please use the admin login option.")

        elif choice == '3':
            user_id, name, balance, user_type = login_user()
            if user_id and user_type.lower() == 'admin':
                admin_menu(user_id, name)
            elif user_type.lower() == 'customer':
                print(Fore.RED + "\n You're not an admin.")

        elif choice == '4':
            print(Fore.MAGENTA + "\n Thank you for banking with Singh Bank. Goodbye!")
            break

        else:
            print(Fore.RED + "\n Invalid option. Please try again.")

if __name__ == "__main__":
    main()

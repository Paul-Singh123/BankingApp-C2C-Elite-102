from colorama import Fore, Style, init

init(autoreset=True)

def print_header():
    print(Fore.CYAN + "=" * 55)
    print(Fore.CYAN + "  ____  ____    _    _   _ _  __ ")
    print(Fore.CYAN + " / ___|| __ )  / \\  | \\ | | |/ / ")
    print(Fore.CYAN + " \\___ \\|  _ \\ / _ \\ |  \\| | ' /  ")
    print(Fore.CYAN + "  ___) | |_) / ___ \\| |\\  | . \\  ")
    print(Fore.CYAN + " |____/|____/_/   \\_\\_| \\_|_|\\_\\ ")
    print("                                 ")
    print(Fore.GREEN + "                 Welcome to SBank")
    print(Fore.CYAN + "=" * 55 + Style.RESET_ALL)

from datetime import datetime
from colorama import init, Fore, Style

class Logging():

    def __init__(self) -> None:
        init()

    def get_timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")
    
    def error(self, string: str, prefix: str = "[-]") -> None:
        print(Fore.LIGHTRED_EX + f" [{self.get_timestamp()}] {prefix} {string}" + Style.RESET_ALL)

    def success(self, string: str, prefix: str = "[+]") -> None:
        print(Fore.LIGHTGREEN_EX + f" [{self.get_timestamp()}] {prefix} {string}" + Style.RESET_ALL)

    def warning(self, string: str, prefix: str = "[!]") -> None:
        print(Fore.LIGHTYELLOW_EX + f" [{self.get_timestamp()}] {prefix} {string}" + Style.RESET_ALL)

    def magenta(self, string: str) -> None:
        print(Fore.LIGHTMAGENTA_EX + string + Style.RESET_ALL)

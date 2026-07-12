from colorama import Fore, Style


class PhoneLookup:
    def __init__(self):
        self.name = "Telefon Numarası OSINT"

    def run(self, target):
        print(f"{Fore.BLUE}[+] {self.name} çalıştırılıyor...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Hedef: {target}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Bu modül geliştirme aşamasındadır.{Style.RESET_ALL}")

    def check_prefix(self, number):
        pass

    def lookup_number(self, number):
        pass

from colorama import Fore, Style


class SocialMedia:
    def __init__(self):
        self.name = "Sosyal Medya OSINT"

    def run(self, target):
        print(f"{Fore.BLUE}[+] {self.name} çalıştırılıyor...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Hedef: {target}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Bu modül geliştirme aşamasındadır.{Style.RESET_ALL}")

    def search_username(self, username):
        pass

    def search_email_social(self, email):
        pass

from colorama import Fore, Style


class IPDomainLookup:
    def __init__(self):
        self.name = "IP / Domain OSINT"

    def run(self, target):
        print(f"{Fore.BLUE}[+] {self.name} çalıştırılıyor...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Hedef: {target}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Bu modül geliştirme aşamasındadır.{Style.RESET_ALL}")

    def whois_lookup(self, domain):
        pass

    def dns_lookup(self, domain):
        pass

    def ip_geolocation(self, ip):
        pass

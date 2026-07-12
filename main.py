import sys
import argparse
from colorama import init, Fore, Style
from src.modules.social_media import SocialMedia
from src.modules.email import EmailLookup
from src.modules.phone import PhoneLookup
from src.modules.ip_domain import IPDomainLookup

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
  ___  ____ ___ _   _ _____     ___ ___  _   _ _____ 
 / _ \/ ___|_ _| \ | |_   _|   |_ _/ _ \| \ | | ____|
| | | \___ \| ||  \| | | |_____ | | | | |  \| |  _|  
| |_| |___) | || |\  | | |_____| | | |_| | |\  | |___ 
 \___/|____/___|_| \_| |_|     |___\___/|_| \_|_____|
{Style.RESET_ALL}
{Fore.YELLOW}Her Şeyi Kapsayan OSINT Aracı{Style.RESET_ALL}
"""

def main():
    parser = argparse.ArgumentParser(description="OSINT ARACI - Kapsamlı Açık Kaynak İstihbarat Aracı")
    parser.add_argument("-m", "--module", choices=["social", "email", "phone", "ip", "all"],
                        help="Kullanılacak modül")
    parser.add_argument("-t", "--target", help="Hedef (kullanıcı adı, e-posta, telefon, IP/domain)")
    parser.add_argument("--list-modules", action="store_true", help="Mevcut modülleri listele")
    
    args = parser.parse_args()

    if args.list_modules:
        print(f"{Fore.GREEN}Mevcut Modüller:{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}social{Style.RESET_ALL}  - Sosyal Medya OSINT")
        print(f"  {Fore.CYAN}email{Style.RESET_ALL}   - E-posta OSINT")
        print(f"  {Fore.CYAN}phone{Style.RESET_ALL}   - Telefon Numarası OSINT")
        print(f"  {Fore.CYAN}ip{Style.RESET_ALL}      - IP / Domain OSINT")
        print(f"  {Fore.CYAN}all{Style.RESET_ALL}     - Tüm modüller")
        return

    if not args.target:
        print(BANNER)
        print(f"{Fore.RED}Hata:{Style.RESET_ALL} Hedef belirtilmedi. Kullanım: python main.py -m <modül> -t <hedef>")
        print(f"{Fore.YELLOW}Örnek:{Style.RESET_ALL} python main.py -m social -t kullaniciadi")
        return

    print(BANNER)
    print(f"{Fore.GREEN}[*] Hedef: {args.target}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Modül: {args.module or 'tümü'}{Style.RESET_ALL}\n")

    if args.module in ("social", "all"):
        SocialMedia().run(args.target)
    if args.module in ("email", "all"):
        EmailLookup().run(args.target)
    if args.module in ("phone", "all"):
        PhoneLookup().run(args.target)
    if args.module in ("ip", "all"):
        IPDomainLookup().run(args.target)

if __name__ == "__main__":
    main()

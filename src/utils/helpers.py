import re
import requests
from colorama import Fore, Style


def print_info(msg):
    print(f"{Fore.CYAN}[i] {msg}{Style.RESET_ALL}")


def print_success(msg):
    print(f"{Fore.GREEN}[+] {msg}{Style.RESET_ALL}")


def print_error(msg):
    print(f"{Fore.RED}[!] {msg}{Style.RESET_ALL}")


def print_warning(msg):
    print(f"{Fore.YELLOW}[*] {msg}{Style.RESET_ALL}")


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(number):
    cleaned = re.sub(r"\D", "", number)
    return 10 <= len(cleaned) <= 15


def validate_ip(ip):
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, ip) is not None


def validate_domain(domain):
    pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, domain) is not None


def fetch_url(url, timeout=10):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print_error(f"İstek başarısız: {e}")
        return None

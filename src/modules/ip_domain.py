import dns.resolver
import whois
import requests
import re


class IPDomainLookup:
    def __init__(self):
        self.name = "IP / Domain OSINT"

    def run(self, target, callback=None):
        results = []
        results.append(("Bilgi", f"🌐 {self.name} - Hedef: {target}"))

        is_ip = self._is_ip(target)

        if is_ip:
            ip_result = self._ip_geolocation(target)
            results.append(ip_result)
        else:
            domain_result = self._check_domain(target)
            results.append(domain_result)

            whois_result = self._whois_lookup(target)
            results.append(whois_result)

            dns_result = self._dns_lookup(target)
            results.append(dns_result)

            subdomain_result = self._check_common_subdomains(target)
            results.append(subdomain_result)

        if callback:
            callback(results)
        return results

    def _is_ip(self, target):
        pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return re.match(pattern, target) is not None

    def _ip_geolocation(self, ip):
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "success":
                    return ("Başarılı", f"🌍 {data.get('country', '?')}, {data.get('city', '?')} | ISP: {data.get('isp', '?')} | Org: {data.get('org', '?')} | ASN: {data.get('as', '?')} | ZIP: {data.get('zip', '?')}")
                return ("Hata", f"❌ IP bilgisi alınamadı: {data.get('message', '?')}")
            return ("Hata", "❌ IP sorgulama başarısız")
        except Exception as e:
            return ("Hata", f"❌ Hata: {e}")

    def _check_domain(self, domain):
        try:
            resp = requests.get(f"https://{domain}", timeout=10)
            return ("Başarılı", f"✅ Domain erişilebilir (HTTP {resp.status_code})")
        except:
            try:
                resp = requests.get(f"http://{domain}", timeout=10)
                return ("Uyarı", f"⚠️ Domain HTTP üzerinden erişilebilir (HTTP {resp.status_code})")
            except:
                return ("Hata", "❌ Domain erişilemez")

    def _whois_lookup(self, domain):
        try:
            w = whois.whois(domain)
            parts = []
            if w.name: parts.append(f"İsim: {w.name}")
            if w.org: parts.append(f"Kurum: {w.org}")
            if w.country: parts.append(f"Ülke: {w.country}")
            if w.creation_date: parts.append(f"Oluşturulma: {w.creation_date}")
            if w.expiration_date: parts.append(f"Süre Bitiş: {w.expiration_date}")
            if w.name_servers: parts.append(f"NS: {', '.join(w.name_servers[:3])}")
            if parts:
                return ("Başarılı", f"📋 WHOIS | {' | '.join(parts)}")
            return ("Uyarı", "⚠️ WHOIS bilgisi alınamadı")
        except:
            return ("Uyarı", "⚠️ WHOIS sorgusu başarısız")

    def _dns_lookup(self, domain):
        try:
            records = {}
            for qtype in ["A", "AAAA", "MX", "NS", "TXT"]:
                try:
                    answers = dns.resolver.resolve(domain, qtype)
                    records[qtype] = [str(r) for r in answers]
                except:
                    records[qtype] = []

            parts = []
            if records["A"]: parts.append(f"A: {', '.join(records['A'][:3])}")
            if records["AAAA"]: parts.append(f"AAAA: {', '.join(records['AAAA'][:3])}")
            if records["MX"]: parts.append(f"MX: {', '.join(records['MX'][:3])}")
            if records["NS"]: parts.append(f"NS: {', '.join(records['NS'][:3])}")
            if records["TXT"]: parts.append(f"TXT: {', '.join(records['TXT'][:3])}")

            if parts:
                return ("Başarılı", f"📡 DNS | {' | '.join(parts)}")
            return ("Uyarı", "⚠️ DNS kaydı bulunamadı")
        except:
            return ("Uyarı", "⚠️ DNS sorgusu başarısız")

    def _check_common_subdomains(self, domain):
        common = ["www", "mail", "api", "admin", "blog", "dev", "test", "cdn", "static", "app"]
        found = []
        for sub in common:
            try:
                full = f"{sub}.{domain}"
                resp = requests.get(f"https://{full}", timeout=3)
                if resp.status_code < 500:
                    found.append(full)
            except:
                pass
        if found:
            return ("Başarılı", f"🔍 Alt Domainler ({len(found)}): {', '.join(found)}")
        return ("Uyarı", "⚠️ Yaygın alt domain bulunamadı")

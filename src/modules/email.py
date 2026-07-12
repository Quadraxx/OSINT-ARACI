import dns.resolver
import hashlib
import requests
from email_validator import validate_email, EmailNotValidError


class EmailLookup:
    def __init__(self):
        self.name = "E-posta OSINT"

    def run(self, target, callback=None):
        results = []
        results.append(("Bilgi", f"📧 {self.name} - Hedef: {target}"))

        # 1. Email format validation
        valid, info = self._validate_format(target)
        results.append(valid)

        if not info.get("valid"):
            if callback:
                callback(results)
            return results

        # 2. MX record check
        domain = info["domain"]
        mx_result = self._check_mx(domain)
        results.append(mx_result)

        # 3. Breach check
        breach_result = self._check_breach(target)
        results.append(breach_result)

        if callback:
            callback(results)
        return results

    def _validate_format(self, email):
        try:
            val = validate_email(email, check_deliverability=False)
            return ("Başarılı", f"✅ Geçerli format: {val.normalized}"), {"valid": True, "domain": val.domain}
        except EmailNotValidError as e:
            return ("Hata", f"❌ Geçersiz format: {e}"), {"valid": False}

    def _check_mx(self, domain):
        try:
            records = dns.resolver.resolve(domain, "MX")
            mx_list = [str(r.exchange) for r in records]
            return ("Başarılı", f"📡 MX Kayıtları ({len(mx_list)}): {', '.join(mx_list[:5])}")
        except:
            return ("Uyarı", "⚠️ MX kaydı bulunamadı")

    def _check_breach(self, email):
        try:
            hash_obj = hashlib.sha1(email.encode()).hexdigest().upper()
            prefix = hash_obj[:5]
            suffix = hash_obj[5:]
            resp = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=10)
            if resp.status_code == 200:
                for line in resp.text.splitlines():
                    if line.startswith(suffix):
                        count = int(line.split(":")[1])
                        return ("Uyarı", f"⚠️ {count} veri ihlalinde bulundu! (Have I Been Pwned)")
                return ("Başarılı", "✅ Herhangi bir veri ihlali bulunamadı")
            return ("Uyarı", "⚠️ İhlal kontrolü yapılamadı")
        except:
            return ("Uyarı", "⚠️ İhlal kontrolü başarısız")

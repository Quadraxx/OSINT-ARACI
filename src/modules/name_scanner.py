import re
from ddgs import DDGS

CONTEXT_PATTERNS = [
    (r"(?:ad[ıi]|isim|isimli|adlı|kullanıcı|yetkili|irtibat|iletişim)\s*[:\-]?\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,3})", "Orta"),
    (r"sahibi\s*[:\-]?\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,3})", "Orta"),
    (r"ilan\s*[:\-]?\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,3})", "Orta"),
    (r"([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)?)\s*(?:tel|telefon|gsm|cep|num)", "Düşük"),
]

SITE_NAMES = {
    "facebook.com": "Facebook",
    "instagram.com": "Instagram",
    "twitter.com": "X / Twitter",
    "x.com": "X / Twitter",
    "linkedin.com": "LinkedIn",
    "sahibinden.com": "Sahibinden",
    "hepsiburada.com": "Hepsiburada",
    "n11.com": "n11",
    "arabam.com": "Arabam",
    "donanimhaber.com": "DonanımHaber",
    "eksisozluk.com": "Ekşi Sözlük",
    "letgo.com": "Letgo",
    "pinterest.com": "Pinterest",
    "medium.com": "Medium",
}


def _extract(text):
    found = []
    for pattern, confidence in CONTEXT_PATTERNS:
        for m in re.findall(pattern, text, re.IGNORECASE):
            if isinstance(m, tuple):
                m = " ".join(m)
            m = m.strip()
            if 4 < len(m) < 60 and not any(c.isdigit() for c in m):
                found.append((m, confidence))
    return found


def _site_label(url):
    for domain, label in SITE_NAMES.items():
        if domain in url.lower():
            return label
    return None


class NameScanner:
    def __init__(self):
        self.name = "İsim / Kimlik Taraması"

    def scan(self, number_formats, callback=None):
        results = []
        queries = list(dict.fromkeys(number_formats))[:4]
        all_hits = []

        for q in queries:
            try:
                for r in list(DDGS().text(q, max_results=8, timelimit="m")):
                    snippet = f"{r.get('title', '')} {r.get('body', '')}"
                    url = r.get("href", "")
                    site = _site_label(url) or "Genel Web"
                    for name, conf in _extract(snippet):
                        all_hits.append((name, site, url, conf))
            except Exception:
                pass

        seen = set()
        unique = []
        for name, site, url, conf in all_hits:
            key = name.lower()
            if key not in seen:
                seen.add(key)
                unique.append((name, site, url, conf))

        if unique:
            results.append(("Başarılı", f"  ✅ {len(unique)} potansiyel eşleşme"))
            for name, site, url, conf in unique[:8]:
                icon = "🟢" if conf == "Yüksek" else "🟡" if conf == "Orta" else "⚪"
                results.append(("Bilgi", f"  {icon} {name}"))
                results.append(("Bilgi", f"     📍 {site} | Güven: {conf}"))
                if url:
                    results.append(("Bilgi", f"     🔗 {url[:100]}"))
        else:
            results.append(("Uyarı", "  ℹ️ Otomatik aramada sonuç bulunamadı"))
            results.append(("Bilgi", "    • Bu numara web'de halka açık kayıtlarda görünmüyor"))
            results.append(("Bilgi", "    • Aşağıdaki Google bağlantılarını manuel dene"))
            results.append(("Bilgi", "    • Truecaller yüklüyse numarayı orada kontrol et"))

        if callback:
            callback(results)
        return results

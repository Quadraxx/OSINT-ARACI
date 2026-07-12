import re
from ddgs import DDGS


TR_NAME_PATTERNS = [
    (r"([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?: [A-ZÇĞİÖŞÜ][a-zçğıöşü]+)?)", "Ad Soyad"),
]

CONTEXT_PATTERNS = [
    r"(?:ad(?:ı|ı|?)?|isim|isimli|adlı|kullanıcı)\s*[:\-]?\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,3})",
    r"(?:iletişim|yetkili|irtibat)\s*[:\-]?\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,3})",
    r"sahibi\s*[:\-]?\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,3})",
    r"ilan\s*[:\-]?\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+){1,3})",
]

SITE_NAMES = {
    "facebook.com": "Facebook",
    "instagram.com": "Instagram",
    "twitter.com": "Twitter / X",
    "x.com": "Twitter / X",
    "linkedin.com": "LinkedIn",
    "sahibinden.com": "Sahibinden",
    "hepsiburada.com": "Hepsiburada",
    "n11.com": "n11",
    "letgo.com": "Letgo",
    "arabam.com": "Arabam",
    "donanimhaber.com": "DonanımHaber",
    "eksisozluk.com": "Ekşi Sözlük",
}


def _extract_names(text):
    names = []
    for pattern, label in CONTEXT_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            m = m.strip()
            if len(m) > 4 and len(m) < 60:
                names.append((m, label, "Orta"))
    for pattern, label in TR_NAME_PATTERNS:
        matches = re.findall(pattern, text)
        for m in matches:
            full = f"{m[0]} {m[1]}"
            if 5 < len(full) < 60:
                names.append((full, label, "Düşük"))
    return names


def _classify_url(url):
    for domain, label in SITE_NAMES.items():
        if domain in url.lower():
            return label
    return None


class NameScanner:
    def __init__(self):
        self.name = "İsim / Kimlik Taraması"

    def scan(self, number_formats, callback=None):
        results = []

        if not number_formats:
            results.append(("Uyarı", "  ℹ️ Arama yapılamadı: format eksik"))
            if callback:
                callback(results)
            return results

        queries = list(dict.fromkeys(number_formats))
        all_names = []

        for q in queries[:4]:
            try:
                ddgs = DDGS()
                search_results = list(ddgs.text(q, max_results=8, timelimit="m"))
                for r in search_results:
                    title = r.get("title", "")
                    body = r.get("body", "")
                    url = r.get("href", "")
                    snippet = f"{title} {body}"

                    site_label = _classify_url(url) or "Genel Web"

                    found_names = _extract_names(snippet)
                    for name, match_type, confidence in found_names:
                        all_names.append({
                            "name": name,
                            "source": site_label,
                            "url": url,
                            "confidence": confidence,
                            "match": match_type,
                        })
            except Exception:
                pass

        seen = set()
        unique_names = []
        for n in all_names:
            key = n["name"].lower()
            if key not in seen:
                seen.add(key)
                unique_names.append(n)

        if not unique_names:
            results.append(("Uyarı", "  ℹ️ Web aramasında isim bulunamadı"))
            results.append(("Bilgi", "    • Bu numara ile ilgili halka açık kayıt bulunamadı"))
            results.append(("Bilgi", "    • Numarayı tırnak içinde manuel olarak Google'da aratmayı dene"))
        else:
            results.append(("Başarılı", f"  ✅ {len(unique_names)} potansiyel eşleşme bulundu"))
            for n in unique_names[:10]:
                icon = "🟢" if n["confidence"] == "Yüksek" else "🟡" if n["confidence"] == "Orta" else "⚪"
                results.append(("Bilgi", f"  {icon} {n['name']}"))
                results.append(("Bilgi", f"     📍 {n['source']} | Güven: {n['confidence']}"))
                if n.get("url"):
                    short_url = n["url"][:90]
                    results.append(("Bilgi", f"     🔗 {short_url}"))

        if callback:
            callback(results)
        return results

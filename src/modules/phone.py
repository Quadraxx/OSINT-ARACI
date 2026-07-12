import re
import urllib.parse
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from src.data.countries import COUNTRY_DATA, COUNTRY_MAP

SEP = "━" * 48
SEP2 = "─" * 48

NUMBER_TYPES = {
    phonenumbers.PhoneNumberType.FIXED_LINE: "Sabit Hat",
    phonenumbers.PhoneNumberType.MOBILE: "Mobil",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Sabit Hat / Mobil",
    phonenumbers.PhoneNumberType.TOLL_FREE: "Ücretsiz (Toll-Free)",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "Ücretli (Premium)",
    phonenumbers.PhoneNumberType.SHARED_COST: "Paylaşımlı Maliyet",
    phonenumbers.PhoneNumberType.VOIP: "VoIP",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Kişisel Numara",
    phonenumbers.PhoneNumberType.PAGER: "Çağrı Cihazı",
    phonenumbers.PhoneNumberType.UAN: "UAN",
    phonenumbers.PhoneNumberType.VOICEMAIL: "Sesli Mesaj",
    phonenumbers.PhoneNumberType.UNKNOWN: "Bilinmeyen",
}

HAT_SINIFI = {
    "Mobil": "GSM",
    "Sabit Hat": "PSTN",
    "VoIP": "IP Telefon",
    "Sabit Hat / Mobil": "PSTN/GSM",
}

TR_BLOK = {
    "530": "Turkcell", "531": "Turkcell", "532": "Turkcell", "533": "Turkcell",
    "534": "Turkcell", "535": "Turkcell", "536": "Turkcell", "537": "Turkcell",
    "538": "Turkcell", "539": "Turkcell", "561": "Turkcell", "562": "Turkcell",
    "516": "Turkcell", "517": "Turkcell",
    "540": "Vodafone", "541": "Vodafone", "542": "Vodafone", "543": "Vodafone",
    "544": "Vodafone", "545": "Vodafone", "546": "Vodafone", "547": "Vodafone",
    "548": "Vodafone", "549": "Vodafone", "501": "Vodafone", "505": "Vodafone",
    "506": "Vodafone", "507": "Vodafone",
    "550": "Turk Telekom", "551": "Turk Telekom", "552": "Turk Telekom",
    "553": "Turk Telekom", "554": "Turk Telekom", "555": "Turk Telekom",
    "556": "Turk Telekom", "557": "Turk Telekom", "558": "Turk Telekom",
    "559": "Turk Telekom",
}

SITE_ARAMALARI = {
    "Facebook": "site:facebook.com",
    "Instagram": "site:instagram.com",
    "LinkedIn": "site:linkedin.com",
    "X / Twitter": "site:x.com OR site:twitter.com",
}

REPUTASYON = {
    "Tellows": "https://www.tellows.com/num/{}",
    "Sync.me": "https://sync.me/search/?number={}",
    "Who Called Me": "https://who-calledme.com/en/number/{}",
    "Find Who Calls Me": "https://findwhocallsme.com/phone/{}",
}

BELGELER = {
    "Pastebin": "site:pastebin.com",
    "PDF Belgeleri": 'ext:pdf OR ext:doc OR ext:docx OR ext:xls OR ext:csv',
    "Forumlar": 'site:forum.donanimhaber.com OR site:eksisozluk.com OR site:r10.net',
    "İlan Siteleri": 'site:sahibinden.com OR site:hepsiburada.com OR site:n11.com',
}

V = lambda l, v: f"{l:24}: {v}"


def _fmt(n, fmt_type):
    if fmt_type == "e164":
        return phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)
    elif fmt_type == "int":
        return phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    elif fmt_type == "nat":
        return phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.NATIONAL)
    elif fmt_type == "raw":
        return re.sub(r"\D", "", phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.NATIONAL))
    return ""


def _gs_url(q):
    return f"https://www.google.com/search?q={urllib.parse.quote(q)}"


def _q_quoted(s):
    return f'"{s}"'


def _q_raw(s):
    return re.sub(r"\D", "", s)


class PhoneLookup:
    def __init__(self):
        self.name = "Telefon Numarası OSINT"

    def run(self, target, callback=None, country_code=None):
        results = []
        results.append(("section", "📞 PHONE ANALYZER"))
        results.append(("section", SEP))

        try:
            cleaned = re.sub(r"[\s\-\(\)\.\,\#]", "", target)
            parsed = None
            detected = None

            if not cleaned.startswith("+"):
                if country_code:
                    cc_info = COUNTRY_MAP.get(country_code)
                    if cc_info:
                        c2 = cleaned[1:] if cleaned.startswith("0") else cleaned
                        parsed = phonenumbers.parse("+" + cc_info["prefix"] + c2, None)
                        detected = cc_info
                else:
                    try:
                        parsed = phonenumbers.parse(cleaned, None)
                    except phonenumbers.NumberParseException:
                        if cleaned.startswith("0"):
                            parsed = phonenumbers.parse("+90" + cleaned[1:], None)
                            detected = COUNTRY_MAP.get("TR")
                        else:
                            parsed = phonenumbers.parse(cleaned, "TR")
                            detected = COUNTRY_MAP.get("TR")
            else:
                parsed = phonenumbers.parse(cleaned, None)
                for cc in COUNTRY_DATA:
                    if cleaned.startswith("+" + cc["prefix"]):
                        detected = cc
                        break

            is_valid = phonenumbers.is_valid_number(parsed)
            is_possible = phonenumbers.is_possible_number(parsed)

            if not is_valid:
                results.append(("section", ""))
                results.append(("section", "❌ INVALID NUMBER"))
                results.append(("section", SEP2))
                results.append(("Hata", V("📌 Girilen", target)))
                results.append(("Hata", V("❌ Geçerli", "Hayır")))
                if is_possible:
                    results.append(("Uyarı", V("⚠️ Mümkün", "Evet (geçersiz format)")))
                if callback:
                    callback(results)
                return results

            e164 = _fmt(parsed, "e164")
            intl = _fmt(parsed, "int")
            nat = _fmt(parsed, "nat")
            raw = _fmt(parsed, "raw")

            cc_val = parsed.country_code
            flag = detected["flag"] if detected else ""
            cname_en = detected["name"] if detected else (geocoder.description_for_number(parsed, "en") or "?")
            cname_tr = geocoder.description_for_number(parsed, "tr") or cname_en

            num_type = phonenumbers.number_type(parsed)
            type_name = NUMBER_TYPES.get(num_type, "Bilinmeyen")

            # ── TEMEL BİLGİLER ──
            results.append(("section", ""))
            results.append(("section", f"{flag} TEMEL BİLGİLER"))
            results.append(("section", SEP2))
            results.append(("Başarılı", V("📌 Hedef", target)))
            results.append(("Başarılı", V("✅ Geçerli", "Evet")))
            results.append(("Başarılı", V("✅ Mümkün", "Evet")))
            results.append(("Başarılı", V("📱 Numara Türü", type_name)))
            results.append(("Başarılı", V("📡 Hat Sınıfı", HAT_SINIFI.get(type_name, "Bilinmiyor"))))
            results.append(("Başarılı", V(f"{flag} Ülke", f"{flag} {cname_tr} ({cname_en})")))
            results.append(("Başarılı", V("📞 Ülke Kodu", f"+{cc_val}")))

            # Operatör
            blok_operator = ""
            if cc_val == 90:
                prefix = raw[1:4] if len(raw) >= 4 else ""
                blok_operator = TR_BLOK.get(prefix, "")
            c_operator = carrier.name_for_number(parsed, "tr")

            if blok_operator and c_operator and blok_operator == c_operator:
                results.append(("Başarılı", V("🏢 Operatör", blok_operator)))
            else:
                if blok_operator:
                    results.append(("Başarılı", V("🏢 Numara Bloğu", blok_operator)))
                if c_operator:
                    results.append(("Başarılı", V("🔄 Güncel Operatör", c_operator)))
                    results.append(("Uyarı", V("ℹ️ Açıklama", "Numara taşınmış olabilir")))
                elif blok_operator:
                    results.append(("Uyarı", V("🔄 Güncel Operatör", "Bilinmiyor")))
                    results.append(("Uyarı", V("ℹ️ Açıklama", "Numara taşınmış olabilir")))
            if not blok_operator and not c_operator:
                c_operator = carrier.name_for_number(parsed, "en")
                if c_operator:
                    results.append(("Başarılı", V("🏢 Operatör", c_operator)))

            tz_list = timezone.time_zones_for_number(parsed)
            if tz_list:
                results.append(("Başarılı", V("🕐 Zaman Dilimi", ", ".join(tz_list))))

            # ── NUMARA FORMATLARI ──
            results.append(("section", ""))
            results.append(("section", "📞 NUMARA FORMATLARI"))
            results.append(("section", SEP2))
            results.append(("Başarılı", V("📞 E.164", e164)))
            results.append(("Başarılı", V("📞 Uluslararası", intl)))
            results.append(("Başarılı", V("📞 Ulusal", nat)))
            results.append(("Başarılı", V("🔢 Son 4 Hane", raw[-4:])))
            if detected and detected.get("format"):
                results.append(("Bilgi", V("📋 Beklenen Format", detected["format"])))

            # ── OSINT ARAMA BAĞLANTILARI ──
            results.append(("section", ""))
            results.append(("section", "🔗 OSINT ARAMA BAĞLANTILARI"))
            results.append(("section", SEP2))

            # Çoklu format
            formats = [e164, intl, nat, raw]
            formats_quoted = [_q_quoted(f) for f in [intl, nat]]
            formats_raw = [_q_quoted(f) for f in [raw]]
            all_q = formats + formats_quoted + formats_raw
            all_q = list(dict.fromkeys(all_q))

            results.append(("section", "  🌐 GENEL WEB ARAMASI"))
            for q in all_q:
                url = _gs_url(q)
                results.append(("Bilgi", f"    • {q}"[:80]))
                results.append(("Bilgi", f"      {url}"))

            # Site bazlı
            results.append(("section", ""))
            results.append(("section", "  📱 SİTE BAZLI ARAMALAR"))
            for site_name, site_query in SITE_ARAMALARI.items():
                q = f"{site_query} {e164}"
                url = _gs_url(q)
                results.append(("Bilgi", f"    • {site_name}: {url}"))

            # Reputasyon
            results.append(("section", ""))
            results.append(("section", "  ⚠️ İHBAR / REPUTASYON"))
            for name, tpl in REPUTASYON.items():
                url = tpl.format(raw, e164, intl, raw)
                results.append(("Uyarı", f"    • {name}: {url}"))

            # Belgeler
            results.append(("section", ""))
            results.append(("section", "  📄 AÇIK BELGELER VE PAYLAŞIMLAR"))
            for doc_name, doc_query in BELGELER.items():
                q = f"{doc_query} {e164}"
                url = _gs_url(q)
                results.append(("Bilgi", f"    • {doc_name}: {url}"))

            # ── KAYNAK GÜVENİ ──
            results.append(("section", ""))
            results.append(("section", "📚 KAYNAK GÜVENİ"))
            results.append(("section", SEP2))

            trust_items = [
                ("phonenumbers doğrulaması", "Yüksek"),
                ("Ülke / format bilgisi", "Yüksek"),
                ("Operatör bilgisi", "Orta / prefix tabanlı"),
                ("Sosyal medya eşleşmesi", "Doğrulanmadı"),
                ("Reputasyon siteleri", "Kullanıcı bildirimi"),
            ]
            for label, level in trust_items:
                icon = "🟢" if level == "Yüksek" else "🟡" if "Orta" in level else "🔴" if "Doğrulanmadı" in level else "⚪"
                results.append(("Bilgi", f"  {icon} {label:30} {level}"))

        except phonenumbers.NumberParseException as e:
            results.append(("section", ""))
            results.append(("Hata", f"❌ Numara ayrıştırılamadı: {e}"))

        results.append(("section", ""))
        results.append(("section", SEP))
        if callback:
            callback(results)
        return results

import re
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from src.data.countries import COUNTRY_DATA, COUNTRY_MAP, COUNTRY_BY_PREFIX


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

TR_OPERATORS = {
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

SOCIAL_DORKS = {
    "Facebook": "https://www.facebook.com/search/top/?q=\"{}\"",
    "Twitter / X": "https://twitter.com/search?q=\"{}\"",
    "Instagram": "https://www.instagram.com/web/search/topsearch/?query={}",
    "LinkedIn": "https://www.linkedin.com/search/results/all/?keywords=\"{}\"",
    "Google": "https://www.google.com/search?q=\"{}\"",
}

REPUTATION_SITES = {
    "whosenumber.info": "https://whosenumber.info/search/?q={}",
    "findwhocallsme.com": "https://findwhocallsme.com/phone/{}",
    "who-calledme.com": "https://who-calledme.com/en/number/{}",
    "sync.me": "https://sync.me/search/?number={}",
    "tellows": "https://www.tellows.com/num/{}",
}

INDIVIDUAL_SITES = {
    "numinfo.net": "https://numinfo.net/{}",
    "spytox.com": "https://spytox.com/{}",
    "pastebin.com": "https://www.google.com/search?q=site:pastebin.com+\"{}\"",
}

V = lambda l, v: f"{l:24}: {v}"


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
                        cleaned2 = cleaned
                        if cleaned.startswith("0"):
                            cleaned2 = cleaned[1:]
                        parsed = phonenumbers.parse("+" + cc_info["prefix"] + cleaned2, None)
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

            nat_num = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            int_num = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            e164_num = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            nat_clean = re.sub(r"\D", "", nat_num)
            cc_val = parsed.country_code

            flag = detected["flag"] if detected else ""
            country_name = detected["name"] if detected else geocoder.description_for_number(parsed, "en") or "?"
            country_name_tr = geocoder.description_for_number(parsed, "tr") or country_name

            results.append(("section", ""))
            results.append(("section", f"{flag} TEMEL BİLGİLER"))
            results.append(("section", SEP2))

            display_target = target
            results.append(("Başarılı", V("📌 Hedef", display_target)))
            results.append(("Başarılı", V("✅ Geçerli", "Evet")))
            results.append(("Başarılı", V("✅ Mümkün", "Evet")))

            num_type = phonenumbers.number_type(parsed)
            type_name = NUMBER_TYPES.get(num_type, "Bilinmeyen")
            results.append(("Başarılı", V("📱 Numara Türü", type_name)))

            hat = HAT_SINIFI.get(type_name, "Bilinmiyor")
            results.append(("Başarılı", V("📡 Hat Sınıfı", hat)))

            results.append(("Başarılı", V(f"{flag} Ülke", f"{detected['flag'] if detected else ''} {country_name_tr} ({country_name})")))
            results.append(("Başarılı", V("📞 Ülke Kodu", f"+{cc_val}")))

            operator_label = ""
            if cc_val == 90:
                prefix = nat_clean[2:5] if len(nat_clean) >= 5 else ""
                operator_label = TR_OPERATORS.get(prefix, "")
                if operator_label:
                    results.append(("Başarılı", V("🏢 Tahmini Operatör", operator_label)))

            c_operator = carrier.name_for_number(parsed, "tr")
            if c_operator and c_operator != operator_label:
                results.append(("Başarılı", V("🏢 Operatör (carrier)", c_operator)))

            tz_list = timezone.time_zones_for_number(parsed)
            if tz_list:
                results.append(("Başarılı", V("🕐 Zaman Dilimi", ", ".join(tz_list))))

            results.append(("section", ""))
            results.append(("section", "📞 NUMARA FORMATLARI"))
            results.append(("section", SEP2))

            results.append(("Başarılı", V("📞 E.164", e164_num)))
            results.append(("Başarılı", V("📞 Uluslararası", int_num)))
            results.append(("Başarılı", V("📞 Ulusal", nat_num)))
            results.append(("Başarılı", V("🔢 Son 4 Hane", nat_clean[-4:])))

            if detected:
                expected_format = detected.get("format", "")
                if expected_format:
                    results.append(("Bilgi", V("📋 Beklenen Format", expected_format)))

            if is_valid:
                results.append(("section", ""))
                results.append(("section", "🔍 OSINT TARAMALARI"))
                results.append(("section", SEP2))

                results.append(("section", "  📱 SOSYAL MEDYA"))
                for name, url_tpl in SOCIAL_DORKS.items():
                    url = url_tpl.format(e164_num, e164_num, e164_num, int_num, nat_clean)
                    url = url_tpl.format(int_num, e164_num, nat_clean, e164_num, e164_num)
                    results.append(("Başarılı", f"    • {name}: {url}"))

                results.append(("section", ""))
                results.append(("section", "  ⚠️ İHBAR / REPUTASYON"))
                for name, url_tpl in REPUTATION_SITES.items():
                    url = url_tpl.format(nat_clean, e164_num, int_num, e164_num, e164_num)
                    results.append(("Uyarı", f"    • {name}: {url}"))

                results.append(("section", ""))
                results.append(("section", "  👤 BİREYSEL İZ ARAMA"))
                for name, url_tpl in INDIVIDUAL_SITES.items():
                    url = url_tpl.format(e164_num, nat_clean, e164_num)
                    results.append(("Bilgi", f"    • {name}: {url}"))

        except phonenumbers.NumberParseException as e:
            results.append(("section", ""))
            results.append(("Hata", f"❌ Numara ayrıştırılamadı: {e}"))

        results.append(("section", ""))
        results.append(("section", SEP))
        if callback:
            callback(results)
        return results

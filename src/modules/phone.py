import re
import phonenumbers
from phonenumbers import carrier, geocoder, timezone


SEP = "━" * 46
LINE = "─" * 46

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

HAT_SINIFI = {
    "Mobil": "GSM",
    "Sabit Hat": "PSTN",
    "VoIP": "IP Telefon",
}


class PhoneLookup:
    def __init__(self):
        self.name = "Telefon Numarası OSINT"

    def run(self, target, callback=None):
        results = []
        label_val = lambda l, v: f"{l:22}: {v}"

        results.append(("section", f"📞 Telefon Numarası OSINT"))
        results.append(("section", SEP))
        results.append(("section", ""))

        try:
            cleaned = re.sub(r"[\s\-\(\)\.]", "", target)

            try:
                phone = phonenumbers.parse(cleaned, None)
            except phonenumbers.NumberParseException:
                if cleaned.startswith("0"):
                    phone = phonenumbers.parse("+90" + cleaned[1:], None)
                elif cleaned.startswith("00"):
                    phone = phonenumbers.parse("+" + cleaned[2:], None)
                else:
                    phone = phonenumbers.parse(cleaned, "TR")

            is_valid = phonenumbers.is_valid_number(phone)
            is_possible = phonenumbers.is_possible_number(phone)

            if not is_valid:
                results.append(("Hata", label_val("❌ Geçerli", "Hayır")))
                if is_possible:
                    results.append(("Uyarı", label_val("⚠️ Mümkün", "Evet (ama geçersiz)")))
                if callback:
                    callback(results)
                return results

            results.append(("Başarılı", label_val("📌 Hedef", target)))
            results.append(("Başarılı", label_val("✅ Geçerli", "Evet")))
            results.append(("Başarılı", label_val("✅ Mümkün", "Evet")))

            num_type = phonenumbers.number_type(phone)
            type_name = NUMBER_TYPES.get(num_type, "Bilinmeyen")
            results.append(("Başarılı", label_val("📱 Numara Türü", type_name)))

            hat_sinifi = HAT_SINIFI.get(type_name, "Bilinmiyor")
            results.append(("Başarılı", label_val("📡 Hat Sınıfı", hat_sinifi)))

            country = geocoder.description_for_number(phone, "tr")
            if country:
                results.append(("Başarılı", label_val("🌍 Ülke/Bölge", country)))

            cc = phone.country_code
            results.append(("Başarılı", label_val("📞 Ülke Kodu", f"+{cc}")))

            operator_label = ""
            nat_num = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)
            nat_clean = re.sub(r"\D", "", nat_num)

            if cc == 90:
                prefix = nat_clean[2:5] if len(nat_clean) >= 5 else ""
                detected = TR_OPERATORS.get(prefix, "")
                if detected:
                    operator_label = detected
                    results.append(("Başarılı", label_val("🏢 Tahmini Operatör", detected)))

            c_operator = carrier.name_for_number(phone, "tr")
            if c_operator and c_operator != operator_label:
                results.append(("Başarılı", label_val("🏢 Operatör (carrier)", c_operator)))

            tz_list = timezone.time_zones_for_number(phone)
            if tz_list:
                results.append(("Başarılı", label_val("🕐 Zaman Dilimi", ", ".join(tz_list))))

            results.append(("section", ""))
            results.append(("section", SEP))
            results.append(("section", "📞 NUMARA FORMATLARI"))
            results.append(("section", SEP))
            results.append(("section", ""))

            e164 = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            int_num = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            results.append(("Başarılı", label_val("📞 E.164", e164)))
            results.append(("Başarılı", label_val("📞 Uluslararası", int_num)))
            results.append(("Başarılı", label_val("📞 Ulusal", nat_num)))
            results.append(("Başarılı", label_val("🔢 Son 4 Hane", nat_clean[-4:])))

            if cc == 90:
                numara_tasima = "Bilinmiyor"
                results.append(("Uyarı", label_val("🔄 Numara Taşıma", numara_tasima)))
                results.append(("Uyarı", label_val("⚠️ Operatör Güveni", "Prefix tabanlı tahmin")))

        except phonenumbers.NumberParseException as e:
            results.append(("Hata", f"❌ Numara ayrıştırılamadı: {e}"))

        results.append(("section", ""))
        results.append(("section", SEP))
        if callback:
            callback(results)
        return results

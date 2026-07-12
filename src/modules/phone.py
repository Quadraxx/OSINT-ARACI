import re
import phonenumbers
from phonenumbers import carrier, geocoder, timezone


NUMBER_TYPES = {
    phonenumbers.PhoneNumberType.FIXED_LINE: "Sabit Hat",
    phonenumbers.PhoneNumberType.MOBILE: "Mobil (Cep Telefonu)",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Sabit Hat / Mobil",
    phonenumbers.PhoneNumberType.TOLL_FREE: "Ücretsiz (Toll-Free)",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "Ücretli Hat (Premium)",
    phonenumbers.PhoneNumberType.SHARED_COST: "Paylaşımlı Maliyet",
    phonenumbers.PhoneNumberType.VOIP: "VoIP / İnternet Telefonu",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Kişisel Numara",
    phonenumbers.PhoneNumberType.PAGER: "Çağrı Cihazı",
    phonenumbers.PhoneNumberType.UAN: "UAN (Evrensel Erişim)",
    phonenumbers.PhoneNumberType.VOICEMAIL: "Sesli Mesaj",
    phonenumbers.PhoneNumberType.UNKNOWN: "Bilinmeyen Tür",
}


class PhoneLookup:
    def __init__(self):
        self.name = "Telefon Numarası OSINT"

    def run(self, target, callback=None):
        results = []
        results.append(("Bilgi", f"📞 {self.name} - Hedef: {target}"))

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

            if not phonenumbers.is_valid_number(phone):
                results.append(("Hata", "❌ Geçersiz telefon numarası"))
                if callback:
                    callback(results)
                return results

            valid_str = "✅ Geçerli" if phonenumbers.is_valid_number(phone) else "❌ Geçersiz"
            possible_str = "✅ Mümkün" if phonenumbers.is_possible_number(phone) else "❌ İmkansız"
            results.append(("Başarılı", f"{valid_str}, {possible_str}"))

            num_type = phonenumbers.number_type(phone)
            type_name = NUMBER_TYPES.get(num_type, f"Bilinmeyen ({num_type})")
            results.append(("Başarılı", f"📱 Numara Türü: {type_name}"))

            country = geocoder.description_for_number(phone, "tr")
            if country:
                results.append(("Başarılı", f"🌍 Ülke/Bölge: {country}"))

            cc = phone.country_code
            results.append(("Başarılı", f"📞 Ülke Kodu: +{cc}"))

            nat_num = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)
            int_num = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            e164 = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            results.append(("Başarılı", f"📞 E.164 Formatı: {e164}"))
            results.append(("Başarılı", f"📞 Uluslararası: {int_num}"))
            results.append(("Başarılı", f"📞 Ulusal: {nat_num}"))

            if cc == 90 and type_name == "Mobil (Cep Telefonu)":
                prefix = cleaned[-10:-7] if len(cleaned) >= 10 else ""
                operator_map = {
                    "530": "Turkcell", "531": "Turkcell", "532": "Turkcell", "533": "Turkcell", "534": "Turkcell", "535": "Turkcell", "536": "Turkcell", "537": "Turkcell", "538": "Turkcell", "539": "Turkcell",
                    "540": "Vodafone", "541": "Vodafone", "542": "Vodafone", "543": "Vodafone", "544": "Vodafone", "545": "Vodafone", "546": "Vodafone", "547": "Vodafone", "548": "Vodafone", "549": "Vodafone",
                    "550": "Turk Telekom", "551": "Turk Telekom", "552": "Turk Telekom", "553": "Turk Telekom", "554": "Turk Telekom", "555": "Turk Telekom", "556": "Turk Telekom", "557": "Turk Telekom", "558": "Turk Telekom", "559": "Turk Telekom",
                    "561": "Turkcell", "562": "Turkcell",
                    "501": "Vodafone", "505": "Vodafone", "506": "Vodafone", "507": "Vodafone",
                    "516": "Turkcell", "517": "Turkcell",
                }
                detected = operator_map.get(prefix, "")
                if detected:
                    results.append(("Başarılı", f"🏢 Operatör: {detected}"))

            mobile_num = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)
            mobile_clean = re.sub(r"\D", "", mobile_num)
            if cc == 90:
                last4 = mobile_clean[-4:]
                results.append(("Başarılı", f"🔢 Son 4 Haneli: {last4}"))

            operator = carrier.name_for_number(phone, "tr")
            if operator:
                results.append(("Başarılı", f"🏢 Operatör (carrier): {operator}"))

            tz_list = timezone.time_zones_for_number(phone)
            if tz_list:
                results.append(("Başarılı", f"🕐 Zaman Dilimi: {', '.join(tz_list)}"))

        except phonenumbers.NumberParseException as e:
            results.append(("Hata", f"❌ Numara ayrıştırılamadı: {e}"))

        if callback:
            callback(results)
        return results

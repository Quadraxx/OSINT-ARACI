import phonenumbers
from phonenumbers import carrier, geocoder, timezone


class PhoneLookup:
    def __init__(self):
        self.name = "Telefon Numarası OSINT"

    def run(self, target, callback=None):
        results = []
        results.append(("Bilgi", f"📞 {self.name} - Hedef: {target}"))

        try:
            phone = phonenumbers.parse(target, None)

            if not phonenumbers.is_valid_number(phone):
                results.append(("Hata", "❌ Geçersiz telefon numarası"))
                if callback:
                    callback(results)
                return results

            valid_str = "✅ Geçerli" if phonenumbers.is_valid_number(phone) else "❌ Geçersiz"
            possible_str = "✅ Mümkün" if phonenumbers.is_possible_number(phone) else "❌ İmkansız"
            results.append(("Başarılı", f"{valid_str}, {possible_str}"))

            country = geocoder.description_for_number(phone, "tr")
            if country:
                results.append(("Başarılı", f"🌍 Ülke/Bölge: {country}"))

            operator = carrier.name_for_number(phone, "tr")
            if operator:
                results.append(("Başarılı", f"🏢 Operatör: {operator}"))

            tz_list = timezone.time_zones_for_number(phone)
            if tz_list:
                results.append(("Başarılı", f"🕐 Zaman Dilimi: {', '.join(tz_list)}"))

            formatted_int = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            formatted_nat = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)
            results.append(("Başarılı", f"📞 Uluslararası: {formatted_int}"))
            results.append(("Başarılı", f"📞 Ulusal: {formatted_nat}"))

        except phonenumbers.NumberParseException as e:
            results.append(("Hata", f"❌ Numara ayrıştırılamadı: {e}"))

        if callback:
            callback(results)
        return results

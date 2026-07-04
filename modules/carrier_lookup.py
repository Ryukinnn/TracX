import phonenumbers
from phonenumbers import carrier, timezone, geocoder

class CarrierLookup:
    def lookup(self, phone):
        result = {'phone': phone, 'carrier': None, 'country': None, 'timezone': None, 'error': None}
        try:
            parsed = phonenumbers.parse(phone, None)
            if phonenumbers.is_valid_number(parsed):
                result['carrier'] = carrier.name_for_number(parsed, 'en') or 'Tidak diketahui'
                result['country'] = geocoder.description_for_number(parsed, 'en')
                tz_list = timezone.time_zones_for_number(parsed)
                result['timezone'] = list(tz_list)[0] if tz_list else None
                return result
            result['error'] = 'Nomor tidak valid'
            return result
        except Exception as e:
            result['error'] = str(e)
            return result
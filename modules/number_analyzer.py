#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

class NumberAnalyzer:
    def analyze(self, phone):
        result = {'raw': phone, 'error': None, 'valid': False, 'e164': None}
        try:
            parsed = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed):
                result['error'] = 'Nomor tidak valid'
                return result
            result['valid'] = True
            result['e164'] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            result['national'] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            result['country_code'] = phonenumbers.region_code_for_number(parsed)
            result['country_name'] = geocoder.description_for_number(parsed, 'id') or geocoder.description_for_number(parsed, 'en')
            
            # Tipe
            ntype = phonenumbers.number_type(parsed)
            type_map = {
                phonenumbers.PhoneNumberType.MOBILE: 'Mobile (Seluler)',
                phonenumbers.PhoneNumberType.FIXED_LINE: 'Fixed Line',
                phonenumbers.PhoneNumberType.VOIP: 'VoIP',
                phonenumbers.PhoneNumberType.TOLL_FREE: 'Toll Free',
            }
            result['line_type'] = type_map.get(ntype, 'Unknown')
            
            # Timezone
            tz_list = timezone.time_zones_for_number(parsed)
            result['timezone'] = list(tz_list)[0] if tz_list else None
            
            # Operator
            try:
                result['carrier'] = carrier.name_for_number(parsed, 'en')
            except: pass
            return result
        except Exception as e:
            result['error'] = str(e)
            return result
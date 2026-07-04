import phonenumbers
from phonenumbers import geocoder
import requests
import json

class GeoLocator:
    def locate(self, phone):
        result = {
            'phone': phone,
            'country': None,
            'city': None,
            'latitude': None,
            'longitude': None,
            'address_estimate': None,
            'error': None
        }
        try:
            parsed = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed):
                result['error'] = 'Nomor tidak valid'
                return result
            
            # Dapatkan deskripsi lokasi dari phonenumbers
            location = geocoder.description_for_number(parsed, 'en')
            if location:
                result['country'] = location
                # Coba cari koordinat dari OpenStreetMap
                try:
                    geo_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
                    resp = requests.get(geo_url, headers={'User-Agent': 'TracX-OSINT'}, timeout=10)
                    data = resp.json()
                    if data:
                        result['latitude'] = data[0].get('lat')
                        result['longitude'] = data[0].get('lon')
                        result['city'] = data[0].get('display_name', '').split(',')[0]
                        result['address_estimate'] = data[0].get('display_name')
                except:
                    pass
            
            return result
        except Exception as e:
            result['error'] = str(e)
            return result
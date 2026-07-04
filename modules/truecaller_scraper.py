import requests
import re
from bs4 import BeautifulSoup

class TruecallerScraper:
    def scrape(self, phone):
        result = {'phone': phone, 'name': None, 'location': None, 'carrier': None, 'photo_url': None, 'error': None}
        try:
            # Bersihkan nomor
            clean = phone.replace('+', '').replace(' ', '').replace('-', '')
            url = f"https://www.truecaller.com/search/{clean}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                result['error'] = f'HTTP {resp.status_code}'
                return result
            
            # Parse HTML
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Coba cari nama dari tag <h1> atau class tertentu
            name_tag = soup.find('h1', class_='profile-name') or soup.find('div', class_='name')
            if name_tag:
                result['name'] = name_tag.text.strip()
            
            # Lokasi
            location_tag = soup.find('span', class_='location') or soup.find('div', class_='location')
            if location_tag:
                result['location'] = location_tag.text.strip()
            
            # Carrier (jika ada)
            carrier_tag = soup.find('span', class_='carrier')
            if carrier_tag:
                result['carrier'] = carrier_tag.text.strip()
            
            # Foto
            img_tag = soup.find('img', class_='profile-image')
            if img_tag and img_tag.get('src'):
                result['photo_url'] = img_tag['src']
            
            # Jika tidak ditemukan, coba cari di script JSON (Truecaller sering pakai JSON embedded)
            if not result['name']:
                # Coba cari pola JSON
                script_tags = soup.find_all('script')
                for script in script_tags:
                    if script.string and 'window.__INITIAL_STATE__' in script.string:
                        # Ekstrak nama dari JSON (sulit, skip dulu)
                        pass
            
            return result
        except Exception as e:
            result['error'] = str(e)
            return result
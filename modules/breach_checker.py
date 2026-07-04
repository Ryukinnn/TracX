import requests
import urllib.parse
import time
import re

class BreachChecker:
    def check(self, phone):
        result = {
            'phone': phone,
            'found': False,
            'breaches': [],
            'message': 'Tidak ditemukan indikasi kebocoran.',
            'search_urls': []
        }
        clean = phone.replace('+', '').replace(' ', '').replace('-', '')
        
        # Dork untuk mencari kebocoran
        dorks = [
            f'site:pastebin.com "{clean}"',
            f'site:github.com "{clean}" phone',
            f'"{clean}" "leak" "dump"',
            f'"{clean}" "breach" "database"',
            f'"{clean}" "password" "email"'
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        found_any = False
        for dork in dorks:
            encoded = urllib.parse.quote_plus(dork)
            url = f"https://www.google.com/search?q={encoded}"
            result['search_urls'].append(url)
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                # Cek apakah ada hasil
                if 'did not match any documents' not in resp.text and 'tidak ditemukan' not in resp.text:
                    # Ekstrak jumlah hasil
                    match = re.search(r'About ([\d,]+) results', resp.text)
                    if match:
                        count = match.group(1)
                        result['breaches'].append(f"{dork} -> {count} hasil")
                        found_any = True
                time.sleep(0.5)
            except:
                pass
        
        if found_any:
            result['found'] = True
            result['message'] = '⚠️ Terdeteksi potensi jejak bocor!'
        else:
            result['message'] = '✅ Tidak ditemukan indikasi bocor di Google/Pastebin.'
        
        return result
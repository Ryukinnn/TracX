#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import urllib.parse
import time

class BreachChecker:
    def check(self, phone):
        result = {
            'phone': phone,
            'found': False,
            'breaches': [],
            'message': 'Tidak ditemukan indikasi kebocoran.',
            'search_urls': []
        }
        
        clean_phone = phone.replace('+', '').replace(' ', '').replace('-', '')
        
        # Dork spesifik untuk pastebin & github
        dorks = [
            f'site:pastebin.com "{clean_phone}"',
            f'site:github.com "{clean_phone}" phone',
            f'"{clean_phone}" "leak" "dump"',
            f'"{clean_phone}" "breach" "database"'
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        found_any = False
        for dork in dorks:
            encoded = urllib.parse.quote_plus(dork)
            url = f"https://www.google.com/search?q={encoded}"
            result['search_urls'].append(url)
            
            # Coba cek apakah ada hasil (dengan memparsing jumlah hasil, simpel)
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                if 'did not match any documents' not in resp.text and 'tidak ditemukan' not in resp.text:
                    if 'hasil' in resp.text or 'results' in resp.text:
                        found_any = True
                        result['breaches'].append(f"Potensi ditemukan: {url}")
                time.sleep(0.5) # Hindari block
            except:
                pass
        
        if found_any:
            result['found'] = True
            result['message'] = '⚠️ Terdeteksi potensi jejak bocor! Periksa link.'
        else:
            result['message'] = '✅ Tidak ditemukan indikasi bocor di Google/Pastebin.'
        
        return result
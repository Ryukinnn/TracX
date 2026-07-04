#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import urllib.parse

class SocialScraper:
    def search(self, phone, number_info):
        result = {'social_media': {}, 'search_links': []}
        clean_phone = phone.replace('+', '').replace(' ', '').replace('-', '')
        
        # 1. Cek WhatsApp (Real HTTP)
        wa_url = f"https://wa.me/{clean_phone}"
        try:
            resp = requests.get(wa_url, timeout=5, allow_redirects=False)
            if resp.status_code in [200, 302]:
                result['social_media']['WhatsApp'] = {'exists': True, 'url': wa_url}
            else:
                result['social_media']['WhatsApp'] = {'exists': False}
        except:
            result['social_media']['WhatsApp'] = {'exists': False, 'error': 'Timeout'}

        # 2. Cek Telegram (Real HTTP - cek apakah redirect ke login)
        tg_url = f"https://t.me/{clean_phone}"
        try:
            resp = requests.get(tg_url, timeout=5)
            if 'tgme_page_extra' in resp.text and 'If you have Telegram' in resp.text:
                result['social_media']['Telegram'] = {'exists': False}
            elif 'tgme_page' in resp.text:
                result['social_media']['Telegram'] = {'exists': True, 'url': tg_url}
            else:
                result['social_media']['Telegram'] = {'exists': False}
        except:
            result['social_media']['Telegram'] = {'exists': False}

        # 3. Cek Truecaller (scraping halaman pencarian)
        tc_url = f"https://www.truecaller.com/search/{clean_phone}"
        result['search_links'].append({'platform': 'Truecaller', 'url': tc_url})

        # 4. Siapkan link pencarian Google untuk jejak lain
        platforms = {
            'Facebook': f"https://www.facebook.com/search/top?q={clean_phone}",
            'Instagram': f"https://www.instagram.com/web/search/top/?q={clean_phone}",
            'Twitter': f"https://twitter.com/search?q={clean_phone}",
            'LinkedIn': f"https://www.linkedin.com/search/results/people/?keywords={clean_phone}",
            'GitHub': f"https://github.com/search?q={clean_phone}",
        }
        for p, url in platforms.items():
            result['search_links'].append({'platform': p, 'url': url})
        
        return result
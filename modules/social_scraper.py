import requests
import urllib.parse

class SocialScraper:
    def search(self, phone):
        result = {'social_media': {}, 'search_links': []}
        clean = phone.replace('+', '').replace(' ', '').replace('-', '')
        encoded = urllib.parse.quote_plus(phone)
        
        # Daftar platform dengan metode pengecekan
        platforms = {
            'WhatsApp': {
                'url': f'https://wa.me/{clean}',
                'check_method': 'status_code',
                'status_ok': [200, 302]
            },
            'Telegram': {
                'url': f'https://t.me/{clean}',
                'check_method': 'text_contains',
                'text_ok': ['tgme_page']
            },
            'Facebook': {
                'url': f'https://www.facebook.com/search/top/?q={encoded}',
                'check_method': 'always_link'
            },
            'Instagram': {
                'url': f'https://www.instagram.com/web/search/top/?q={encoded}',
                'check_method': 'always_link'
            },
            'Twitter': {
                'url': f'https://twitter.com/search?q={encoded}',
                'check_method': 'always_link'
            },
            'LinkedIn': {
                'url': f'https://www.linkedin.com/search/results/people/?keywords={encoded}',
                'check_method': 'always_link'
            },
            'GitHub': {
                'url': f'https://github.com/search?q={encoded}',
                'check_method': 'always_link'
            },
            'TikTok': {
                'url': f'https://www.tiktok.com/search?q={encoded}',
                'check_method': 'always_link'
            }
        }
        
        for name, info in platforms.items():
            if info['check_method'] == 'status_code':
                try:
                    resp = requests.get(info['url'], timeout=5, allow_redirects=False)
                    exists = resp.status_code in info['status_ok']
                    result['social_media'][name] = {'exists': exists, 'url': info['url']}
                except:
                    result['social_media'][name] = {'exists': False, 'url': info['url'], 'error': 'Timeout'}
            elif info['check_method'] == 'text_contains':
                try:
                    resp = requests.get(info['url'], timeout=5)
                    exists = any(tag in resp.text for tag in info['text_ok'])
                    result['social_media'][name] = {'exists': exists, 'url': info['url']}
                except:
                    result['social_media'][name] = {'exists': False, 'url': info['url'], 'error': 'Timeout'}
            else:
                result['social_media'][name] = {'exists': None, 'url': info['url'], 'note': 'Link pencarian disediakan'}
                result['search_links'].append({'platform': name, 'url': info['url']})
        
        return result
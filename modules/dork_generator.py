import urllib.parse
from datetime import datetime

class DorkGenerator:
    def generate(self, phone):
        dorks = []
        clean = phone.replace('+', '').replace(' ', '').replace('-', '')
        queries = [clean, phone]
        
        templates = [
            ('"{}" site:facebook.com', 'Facebook'),
            ('"{}" site:twitter.com', 'Twitter/X'),
            ('"{}" site:instagram.com', 'Instagram'),
            ('"{}" site:linkedin.com', 'LinkedIn'),
            ('"{}" site:github.com', 'GitHub'),
            ('"{}" site:pastebin.com', 'Pastebin (Leak)'),
            ('"{}" site:docs.google.com', 'Google Docs'),
            ('"{}" site:youtube.com', 'YouTube'),
            ('"{}" site:tiktok.com', 'TikTok'),
            ('"{}" site:reddit.com', 'Reddit'),
            ('"{}" filetype:pdf', 'PDF Documents'),
            ('"{}" filetype:txt', 'Text Files'),
            ('"{}" filetype:csv', 'CSV/Spreadsheet'),
            ('"{}" "phone" "contact"', 'Contact Pages'),
            ('"{}" "alamat" OR "address"', 'Address Information'),
            ('"{}" "nama" OR "name"', 'Name References'),
        ]
        
        for q in queries:
            if not q: continue
            for template, cat in templates:
                dork = template.format(q)
                dorks.append({
                    'query': dork,
                    'category': cat,
                    'url': f"https://www.google.com/search?q={urllib.parse.quote_plus(dork)}",
                    'timestamp': datetime.now().isoformat()
                })
        return dorks
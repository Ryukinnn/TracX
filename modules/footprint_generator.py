#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.parse
from datetime import datetime

class FootprintGenerator:
    def generate_dorks(self, phone, number_info):
        dorks = []
        clean = phone.replace('+', '').replace(' ', '').replace('-', '')
        queries = [clean, phone, number_info.get('e164', phone)]
        
        templates = [
            ('"{}" site:facebook.com', 'Facebook'),
            ('"{}" site:twitter.com', 'Twitter'),
            ('"{}" site:instagram.com', 'Instagram'),
            ('"{}" site:linkedin.com', 'LinkedIn'),
            ('"{}" site:github.com', 'GitHub'),
            ('"{}" site:pastebin.com', 'Pastebin (Leak)'),
            ('"{}" site:docs.google.com', 'Google Docs'),
            ('"{}" filetype:pdf', 'PDF Docs'),
            ('"{}" "phone" "contact"', 'Contact Pages'),
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
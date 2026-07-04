#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from pathlib import Path

class Reporter:
    def __init__(self):
        self.report_dir = Path.home() / '.tracx' / 'reports'
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, data, phone, format_type='html'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_phone = phone.replace('+', '').replace(' ', '')
        filename = f"{safe_phone}_{timestamp}"
        
        if format_type == 'json':
            return self._generate_json(data, filename)
        elif format_type == 'html':
            return self._generate_html(data, phone, filename)
        else:
            return self._generate_txt(data, phone, filename)
    
    def _generate_json(self, data, filename):
        path = self.report_dir / f"{filename}.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
        return str(path)
    
    def _generate_txt(self, data, phone, filename):
        path = self.report_dir / f"{filename}.txt"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"TRACX REPORT - {phone}\n{'='*50}\n")
            f.write(f"Generated: {datetime.now()}\n\n")
            if data.get('number_info'):
                f.write("NUMBER INFO:\n")
                for k,v in data['number_info'].items():
                    if v: f.write(f"  {k}: {v}\n")
        return str(path)
    
    def _generate_html(self, data, phone, filename):
        path = self.report_dir / f"{filename}.html"
        html = f"""
<html><head><meta charset="UTF-8"><title>TracX Report</title>
<style>body{{background:#0d1117;color:#c9d1d9;font-family:Arial;padding:20px}}
.section{{background:#161b22;padding:15px;margin:15px 0;border-radius:8px}}
h2{{color:#58a6ff}} .field{{display:flex;padding:5px 0}}
.label{{width:150px;font-weight:bold;color:#8b949e}}
.warning{{background:#3b1f1f;border-left:4px solid #f85149;padding:10px}}
.success{{background:#1f3b1f;border-left:4px solid #3fb950;padding:10px}}
</style></head><body>
<h1>🔍 TracX Footprint Report</h1>
<p><strong>Target:</strong> {phone} | <strong>Date:</strong> {datetime.now()}</p>
<div class="warning">⚠️ For legal investigation only.</div>
"""
        if data.get('number_info'):
            html += "<div class='section'><h2>📱 Number Info</h2>"
            for k,v in data['number_info'].items():
                if v: html += f"<div class='field'><span class='label'>{k}</span><span>{v}</span></div>"
            html += "</div>"
        if data.get('breach') and data['breach'].get('found'):
            html += "<div class='section'><h2>💀 Breach Indication</h2><div class='warning'>"
            for b in data['breach'].get('breaches',[]): html += f"<p>• {b}</p>"
            html += "</div></div>"
        html += "</body></html>"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return str(path)
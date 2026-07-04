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
            f.write(f"TRACX ULTIMATE REPORT\n{'='*60}\n")
            f.write(f"Target: {phone}\nTanggal: {datetime.now()}\n\n")
            for section, content in data.items():
                f.write(f"\n--- {section.upper()} ---\n")
                if isinstance(content, dict):
                    for k, v in content.items():
                        if v: f.write(f"{k}: {v}\n")
                elif isinstance(content, list):
                    for item in content[:20]:
                        if isinstance(item, dict):
                            f.write(f"{item.get('query', item)}\n")
                        else:
                            f.write(f"{item}\n")
        return str(path)
    
    def _generate_html(self, data, phone, filename):
        path = self.report_dir / f"{filename}.html"
        html = f"""
<html><head><meta charset="UTF-8">
<title>TracX Ultimate Report</title>
<style>
body{{background:#0d1117;color:#c9d1d9;font-family:Arial;padding:30px}}
.container{{max-width:1100px;margin:auto}}
h1{{color:#58a6ff;border-bottom:2px solid #58a6ff;padding-bottom:10px}}
h2{{color:#58a6ff;margin-top:30px}}
.section{{background:#161b22;padding:20px;margin:15px 0;border-radius:8px;border:1px solid #30363d}}
.field{{display:flex;padding:8px 0;border-bottom:1px solid #21262d}}
.label{{font-weight:bold;width:200px;color:#8b949e}}
.value{{flex:1;word-break:break-word}}
.warning{{background:#3b1f1f;border-left:4px solid #f85149;padding:15px;margin:20px 0}}
.success{{background:#1f3b1f;border-left:4px solid #3fb950;padding:15px;margin:20px 0}}
.footer{{margin-top:40px;padding-top:20px;border-top:1px solid #30363d;text-align:center;color:#8b949e}}
a{{color:#58a6ff}}
</style></head><body>
<div class="container">
<h1>🔍 TracX Ultimate Digital Footprint Report</h1>
<p><strong>Target:</strong> {phone} | <strong>Generated:</strong> {datetime.now()}</p>
<div class="warning">⚠️ For authorized legal investigation only.</div>
"""
        # Iterasi semua sections
        for section, content in data.items():
            if not content: continue
            html += f"<div class='section'><h2>{section.upper()}</h2>"
            if isinstance(content, dict):
                for k, v in content.items():
                    if v and not k.startswith('_'):
                        html += f"<div class='field'><span class='label'>{k}</span><span class='value'>{v}</span></div>"
            elif isinstance(content, list):
                for item in content[:30]:
                    if isinstance(item, dict):
                        html += f"<div class='field'><span class='value'>• {item.get('query', item)}</span></div>"
                    else:
                        html += f"<div class='field'><span class='value'>• {item}</span></div>"
            html += "</div>"
        
        html += f"""
<div class="footer">
<p>Laporan dibuat oleh TracX v2.0 — {datetime.now()}</p>
<p>🔒 Untuk kepentingan investigasi keamanan yang sah.</p>
</div>
</div></body></html>
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return str(path)
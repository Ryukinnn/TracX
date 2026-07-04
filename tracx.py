#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TracX - Digital Footprint Investigator
Advanced OSINT tool for phone number intelligence gathering
Kali Linux Compatible | Python 3.8+
"""

import argparse
import json
import sys
import os
import webbrowser
from datetime import datetime

# Import modul internal (real, tanpa API Key)
from modules.number_analyzer import NumberAnalyzer
from modules.carrier_lookup import CarrierLookup
from modules.social_scraper import SocialScraper
from modules.breach_checker import BreachChecker
from modules.footprint_generator import FootprintGenerator
from modules.reporter import Reporter

# ANSI Colors
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

VERSION = "1.0.0"
BANNER = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   {Colors.BOLD}████████╗██████╗  █████╗  ██████╗██╗  ██╗{Colors.CYAN}                  ║
║   {Colors.BOLD}╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝{Colors.CYAN}                  ║
║   {Colors.BOLD}   ██║   ██████╔╝███████║██║      ╚███╔╝ {Colors.CYAN}                  ║
║   {Colors.BOLD}   ██║   ██╔══██╗██╔══██║██║      ██╔██╗ {Colors.CYAN}                  ║
║   {Colors.BOLD}   ██║   ██║  ██║██║  ██║╚██████╗██╔╝ ██╗{Colors.CYAN}                  ║
║   {Colors.BOLD}   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝{Colors.CYAN}                  ║
║                                                                          ║
║         {Colors.BOLD}Digital Footprint Investigator v{VERSION}{Colors.CYAN}                      ║
║         {Colors.DIM}OSINT - Phone Number Intelligence (Real){Colors.CYAN}                      ║
╚══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""

def print_banner():
    print(BANNER)

def print_disclaimer():
    disclaimer = f"""
{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                         ⚠️  PERINGATAN  ⚠️                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Alat ini dibuat untuk tujuan PENDIDIKAN dan PENELITIAN          ║
║  keamanan siber yang SAH DAN LEGAL.                             ║
║  DILARANG KERAS digunakan untuk doxing, pelecehan,              ║
║  atau aktivitas kriminal.                                       ║
║  PENGUNA BERTANGGUNG JAWAB PENUH atas konsekuensi hukum.        ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(disclaimer)

def interactive_mode():
    print(f"\n{Colors.YELLOW}[?] Masukkan nomor telepon target (dengan kode negara):{Colors.RESET}")
    print(f"{Colors.DIM}   Contoh: +6281234567890 (Indonesia){Colors.RESET}")
    print(f"{Colors.DIM}   Contoh: +14155552671 (US){Colors.RESET}")
    while True:
        phone = input(f"\n{Colors.CYAN}➜{Colors.RESET} Nomor: ").strip()
        if phone.lower() in ['exit', 'quit', 'q']:
            print(f"{Colors.YELLOW}[!] Keluar...{Colors.RESET}")
            sys.exit(0)
        if phone:
            return phone
        print(f"{Colors.RED}[-] Nomor tidak boleh kosong!{Colors.RESET}")

def run_investigation(phone, args):
    results = {}
    
    # 1. Analisis Nomor (REAL - offline)
    print(f"\n{Colors.CYAN}[*] Menganalisis nomor...{Colors.RESET}")
    analyzer = NumberAnalyzer()
    number_info = analyzer.analyze(phone)
    results['number_info'] = number_info
    
    if number_info.get('error'):
        print(f"{Colors.RED}[-] Error: {number_info['error']}{Colors.RESET}")
        return results
    
    print(f"{Colors.GREEN}[+] Nomor valid: {number_info.get('e164')}{Colors.RESET}")
    print(f"    📍 Negara: {number_info.get('country_name')} ({number_info.get('country_code')})")
    print(f"    📱 Tipe: {number_info.get('line_type')}")

    # 2. Deteksi Operator (REAL - offline)
    if not args.no_carrier:
        print(f"\n{Colors.CYAN}[*] Mendeteksi operator...{Colors.RESET}")
        carrier = CarrierLookup()
        carrier_info = carrier.lookup(phone)
        results['carrier_info'] = carrier_info
        if carrier_info and not carrier_info.get('error'):
            print(f"{Colors.GREEN}[+] Operator: {carrier_info.get('carrier', 'Tidak diketahui')}{Colors.RESET}")
            print(f"    🌐 Zona waktu: {carrier_info.get('timezone', 'N/A')}")

    # 3. Pencarian Jejak Digital (REAL - HTTP request + Google)
    if not args.no_footprint:
        print(f"\n{Colors.CYAN}[*] Mencari jejak digital (real-time)...{Colors.RESET}")
        scraper = SocialScraper()
        footprint = scraper.search(phone, number_info)
        results['footprint'] = footprint
        
        if footprint.get('social_media'):
            print(f"{Colors.GREEN}[+] Ditemukan jejak aktif:{Colors.RESET}")
            for platform, data in footprint['social_media'].items():
                if data:
                    status = "✅ Aktif" if data.get('exists') else "❌ Tidak ditemukan"
                    print(f"    🔗 {platform}: {status}")
        
        if footprint.get('search_links'):
            print(f"{Colors.DIM}    📌 {len(footprint['search_links'])} link pencarian disiapkan.{Colors.RESET}")

    # 4. Pengecekan Kebocoran Data (REAL - Google scraping)
    if not args.no_breach:
        print(f"\n{Colors.CYAN}[*] Memeriksa kebocoran data (real-time scraping)...{Colors.RESET}")
        checker = BreachChecker()
        breach_result = checker.check(phone)
        results['breach'] = breach_result
        
        if breach_result and breach_result.get('found'):
            print(f"{Colors.RED}[!] {breach_result.get('message')}{Colors.RESET}")
            for b in breach_result.get('breaches', [])[:3]:
                print(f"    🔴 {b}")
        else:
            print(f"{Colors.GREEN}[+] {breach_result.get('message', 'Tidak ditemukan indikasi bocor.')}{Colors.RESET}")

    # 5. Generate Google Dorks (REAL)
    if not args.no_dorks:
        print(f"\n{Colors.CYAN}[*] Menghasilkan Google Dorks...{Colors.RESET}")
        generator = FootprintGenerator()
        dorks = generator.generate_dorks(phone, number_info)
        results['dorks'] = dorks
        if dorks:
            print(f"{Colors.GREEN}[+] {len(dorks)} Google Dorks siap digunakan.{Colors.RESET}")

    # 6. Buat Laporan
    if args.report:
        print(f"\n{Colors.CYAN}[*] Membuat laporan...{Colors.RESET}")
        reporter = Reporter()
        report_file = reporter.generate(results, phone, args.report)
        if report_file:
            print(f"{Colors.GREEN}[+] Laporan tersimpan: {report_file}{Colors.RESET}")

    return results

def main():
    parser = argparse.ArgumentParser(description="TracX - Digital Footprint Investigator (Real OSINT)")
    parser.add_argument("-p", "--phone", help="Nomor telepon target (format E.164, contoh: +6281234567890)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Mode interaktif")
    parser.add_argument("--report", metavar="FORMAT", nargs='?', const="html", choices=['txt', 'json', 'html'], help="Buat laporan")
    parser.add_argument("--output", metavar="FILE", help="Simpan hasil ke file JSON")
    parser.add_argument("--map", action="store_true", help="Buka Google Maps dengan lokasi perkiraan")
    parser.add_argument("--no-carrier", action="store_true", help="Lewati deteksi operator")
    parser.add_argument("--no-footprint", action="store_true", help="Lewati pencarian jejak digital")
    parser.add_argument("--no-breach", action="store_true", help="Lewati pengecekan kebocoran data")
    parser.add_argument("--no-dorks", action="store_true", help="Lewati pembuatan Google Dorks")
    parser.add_argument("--disclaimer", action="store_true", help="Tampilkan peringatan penggunaan")
    
    args = parser.parse_args()
    print_banner()
    
    if args.disclaimer:
        print_disclaimer()
        sys.exit(0)
    
    if args.interactive or not args.phone:
        phone = interactive_mode()
    else:
        phone = args.phone
    
    if not phone.startswith('+'):
        print(f"{Colors.RED}[-] Nomor harus dimulai dengan '+' dan kode negara.{Colors.RESET}")
        sys.exit(1)
    
    print(f"\n{Colors.YELLOW}⚠️  PERINGATAN: Gunakan hanya untuk tujuan legal & etis.{Colors.RESET}")
    confirm = input(f"{Colors.YELLOW}Lanjutkan investigasi untuk {phone}? (y/n): {Colors.RESET}")
    if confirm.lower() != 'y':
        sys.exit(0)
    
    results = run_investigation(phone, args)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"{Colors.GREEN}[+] Hasil disimpan ke: {args.output}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}[+] Investigasi selesai.{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted{Colors.RESET}")
        sys.exit(0)
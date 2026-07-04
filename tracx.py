#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TracX - Ultimate Digital Footprint Investigator
Phone number OSINT with deep scraping
"""

import sys
import os
import json
import webbrowser
from datetime import datetime

# Modul internal
from modules.number_analyzer import NumberAnalyzer
from modules.carrier_lookup import CarrierLookup
from modules.truecaller_scraper import TruecallerScraper
from modules.social_scraper import SocialScraper
from modules.breach_checker import BreachChecker
from modules.dork_generator import DorkGenerator
from modules.geo_locator import GeoLocator
from modules.reporter import Reporter

# Warna
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

VERSION = "2.0.0"
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
║         {Colors.BOLD}Ultimate Digital Footprint Investigator v{VERSION}{Colors.CYAN}          ║
║         {Colors.DIM}Deep OSINT - Phone Number Intelligence{Colors.CYAN}                     ║
╚══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""

def print_banner():
    print(BANNER)

def print_disclaimer():
    print(f"""
{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                         ⚠️  PERINGATAN  ⚠️                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Alat ini hanya untuk tujuan PENDIDIKAN & PENELITIAN KEAMANAN.  ║
║  DILARANG KERAS untuk doxing, pelecehan, atau kejahatan.       ║
║  Pengguna bertanggung jawab penuh atas konsekuensi hukum.      ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_menu():
    print(f"""
{Colors.CYAN}{Colors.BOLD}📌 PILIH MODUL INVESTIGASI:{Colors.RESET}
{Colors.GREEN} 1. {Colors.RESET}Informasi Dasar Nomor (Negara, Operator, Zona Waktu)
{Colors.GREEN} 2. {Colors.RESET}Scrape Truecaller (Nama, Lokasi, Foto, dll.)
{Colors.GREEN} 3. {Colors.RESET}Cek Jejak Media Sosial (WA, Telegram, FB, IG, dll.)
{Colors.GREEN} 4. {Colors.RESET}Pengecekan Kebocoran Data (Google, Pastebin)
{Colors.GREEN} 5. {Colors.RESET}Google Dorks Generator + Auto Buka
{Colors.GREEN} 6. {Colors.RESET}Perkiraan Lokasi & Alamat (dari kode area)
{Colors.GREEN} 7. {Colors.RESET}Jalankan SEMUA MODUL (Full Investigation)
{Colors.GREEN} 8. {Colors.RESET}Buat Laporan dari Hasil Terakhir
{Colors.RED} 0. {Colors.RESET}Keluar
""")

def get_phone():
    phone = input(f"{Colors.YELLOW}📱 Masukkan nomor (format +628...): {Colors.RESET}").strip()
    if not phone.startswith('+'):
        print(f"{Colors.RED}Nomor harus diawali dengan '+' dan kode negara.{Colors.RESET}")
        return None
    return phone

def save_results(results, filename="tracx_results.json"):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"{Colors.GREEN}[+] Hasil disimpan ke {filename}{Colors.RESET}")

def main():
    clear_screen()
    print_banner()
    print_disclaimer()
    results = {}
    phone = None

    while True:
        show_menu()
        choice = input(f"{Colors.CYAN}➜ Pilihan Anda: {Colors.RESET}").strip()

        if choice == '0':
            print(f"{Colors.YELLOW}Keluar...{Colors.RESET}")
            sys.exit(0)

        # Minta nomor jika belum ada atau jika modul memerlukan nomor
        if choice not in ['7', '8'] and not phone:
            phone = get_phone()
            if not phone:
                continue

        if choice == '1':
            print(f"\n{Colors.CYAN}[*] Menganalisis nomor...{Colors.RESET}")
            analyzer = NumberAnalyzer()
            results['number_info'] = analyzer.analyze(phone)
            print_result(results['number_info'], "INFORMASI NOMOR")

            # Tambahkan carrier
            carrier = CarrierLookup()
            results['carrier_info'] = carrier.lookup(phone)
            print_result(results['carrier_info'], "OPERATOR & ZONA WAKTU")

        elif choice == '2':
            print(f"\n{Colors.CYAN}[*] Scraping Truecaller... (mungkin butuh beberapa detik){Colors.RESET}")
            scraper = TruecallerScraper()
            results['truecaller'] = scraper.scrape(phone)
            print_result(results['truecaller'], "TRUECALLER")

        elif choice == '3':
            print(f"\n{Colors.CYAN}[*] Mencari jejak di media sosial...{Colors.RESET}")
            social = SocialScraper()
            results['social'] = social.search(phone)
            print_result(results['social'], "JEJAK MEDIA SOSIAL")

        elif choice == '4':
            print(f"\n{Colors.CYAN}[*] Memeriksa kebocoran data...{Colors.RESET}")
            breach = BreachChecker()
            results['breach'] = breach.check(phone)
            print_result(results['breach'], "KEBOCORAN DATA")

        elif choice == '5':
            print(f"\n{Colors.CYAN}[*] Menghasilkan Google Dorks...{Colors.RESET}")
            dorkgen = DorkGenerator()
            results['dorks'] = dorkgen.generate(phone)
            print_result(results['dorks'], "GOOGLE DORKS")

        elif choice == '6':
            print(f"\n{Colors.CYAN}[*] Mencari lokasi dari kode area...{Colors.RESET}")
            geo = GeoLocator()
            results['geo'] = geo.locate(phone)
            print_result(results['geo'], "PERKIRAAN LOKASI")

        elif choice == '7':
            # Jalankan semua modul
            print(f"\n{Colors.CYAN}{Colors.BOLD}🚀 MENJALANKAN FULL INVESTIGASI...{Colors.RESET}")
            # 1. Nomor
            analyzer = NumberAnalyzer()
            results['number_info'] = analyzer.analyze(phone)
            print_result(results['number_info'], "INFORMASI NOMOR")

            carrier = CarrierLookup()
            results['carrier_info'] = carrier.lookup(phone)
            print_result(results['carrier_info'], "OPERATOR")

            # 2. Truecaller
            tc = TruecallerScraper()
            results['truecaller'] = tc.scrape(phone)
            print_result(results['truecaller'], "TRUECALLER")

            # 3. Sosmed
            social = SocialScraper()
            results['social'] = social.search(phone)
            print_result(results['social'], "MEDIA SOSIAL")

            # 4. Breach
            breach = BreachChecker()
            results['breach'] = breach.check(phone)
            print_result(results['breach'], "KEBOCORAN DATA")

            # 5. Dorks
            dorkgen = DorkGenerator()
            results['dorks'] = dorkgen.generate(phone)
            print_result(results['dorks'], "GOOGLE DORKS")

            # 6. Geo
            geo = GeoLocator()
            results['geo'] = geo.locate(phone)
            print_result(results['geo'], "LOKASI")

            print(f"\n{Colors.GREEN}[+] Full investigation selesai!{Colors.RESET}")
            save_results(results)

        elif choice == '8':
            if not results:
                print(f"{Colors.RED}Belum ada hasil. Jalankan investigasi dulu!{Colors.RESET}")
                continue
            fmt = input(f"{Colors.YELLOW}Format laporan (html/json/txt) [html]: {Colors.RESET}").strip() or 'html'
            rep = Reporter()
            filepath = rep.generate(results, phone, fmt)
            if filepath:
                print(f"{Colors.GREEN}[+] Laporan tersimpan: {filepath}{Colors.RESET}")

        else:
            print(f"{Colors.RED}Pilihan tidak valid!{Colors.RESET}")

        input(f"\n{Colors.DIM}Tekan Enter untuk melanjutkan...{Colors.RESET}")
        clear_screen()
        print_banner()

def print_result(data, title):
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔══ {title} ══{Colors.RESET}")
    if isinstance(data, dict):
        for k, v in data.items():
            if v and not str(v).startswith('http') and k != 'error':
                print(f"  {Colors.BOLD}{k}:{Colors.RESET} {v}")
    elif isinstance(data, list):
        for item in data[:10]:
            if isinstance(item, dict):
                print(f"  • {item.get('query', item)}")
            else:
                print(f"  • {item}")
    else:
        print(f"  {data}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted{Colors.RESET}")
        sys.exit(0)
# TracX — Ultimate Digital Footprint Investigator

**TracX** adalah alat OSINT super agresif untuk melacak **jejak digital lengkap** dari sebuah nomor telepon. Dapat menampilkan:
- Nama pemilik (dari Truecaller)
- Lokasi (negara, kota, perkiraan alamat)
- Semua akun media sosial (WhatsApp, Telegram, FB, IG, dll.)
- Kebocoran data (Pastebin, GitHub, Google)
- Google Dorks untuk pencarian lebih dalam
- Perkiraan koordinat geografis

> **PERINGATAN**: Alat ini **sangat ampuh** dan dapat memicu pemblokiran IP jika digunakan secara berlebihan. Hanya untuk **investigasi legal** dengan izin tertulis.

---

## Instalasi di Kali Linux

```bash
git clone https://github.com/yourusername/TracX.git
cd TracX
pip3 install -r requirements.txt
chmod +x tracx.py
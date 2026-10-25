JokoScan v2.0 🔍

Black Hat Elite Scanner — Author: Dwi Joko Purwanto (KARANGANYAR ELITE HACKER)

JokoScan adalah tools scanner keamanan jaringan dan web yang menggabungkan puluhan tool reconnaissance, vulnerability scanning, dan information gathering dalam satu antarmuka berwarna. Cukup berikan satu target domain, dan JokoScan akan menjalankan serangkaian pemindaian secara otomatis.

---

⚠️ DISCLAIMER

PERINGATAN KERAS: Tools ini dibuat untuk tujuan edukasi dan pengujian keamanan yang sah (penetration testing dengan izin tertulis).

· JANGAN gunakan tools ini pada sistem/domain yang bukan milik Anda atau tanpa izin eksplisit.
· Penggunaan tanpa izin dapat melanggar hukum pidana (mis. UU ITE di Indonesia, CFAA di AS) dan dapat berujung pada tuntutan hukum.
· Penulis tidak bertanggung jawab atas penyalahgunaan atau kerusakan yang ditimbulkan.

Gunakan dengan bijak dan bertanggung jawab. ✅

---

📋 Fitur

JokoScan menjalankan 70+ modul pemindaian yang dikelompokkan sebagai berikut:

🔎 Information Gathering & Recon

Modul Deskripsi
scan_host Informasi host via host
scan_whois Informasi Whois domain
scan_dns_recon DNS recon via dnsrecon
scan_dnsenum Enumerasi DNS via dnsenum
scan_dnswalk Zone transfer check via dnswalk
scan_dnsmap Brute force subdomain via dnsmap
scan_fierce Enumerasi subdomain via fierce
scan_amass Enumerasi subdomain via amass
scan_the_harvester Email & info via theHarvester
scan_dmitry Info gathering via DMitry
scan_lbd Deteksi load balancer
scan_whatweb Deteksi teknologi web

🛡️ Vulnerability Scanning

Modul Deskripsi
scan_nikto Scan kerentanan web via nikto
scan_nikto_* 15+ plugin Nikto (xss, shellshock, ssl, cgi, dll)
scan_wapiti Scan kerentanan via wapiti
scan_golismero Scan penuh via golismero
scan_uniscan_* 6 modul Uniscan (file/dir brute, RFI, XSS, dll)
scan_xsser Deteksi XSS via xsser
scan_dirb Brute force direktori via dirb

🔐 SSL/TLS & Crypto Checks

Modul Deskripsi
scan_ssl_heartbleed Cek Heartbleed via sslyze
scan_sslyze_hbleed Cek Heartbleed
scan_sslyze_ocsp Cek OCSP stapling
scan_sslyze_zlib Cek ZLib compression
scan_sslyze_reneg Cek renegosiasi
scan_sslyze_resum Cek session resumption
scan_nmap_hbleed Heartbleed via Nmap
scan_nmap_poodle POODLE via Nmap
scan_nmap_ccs CCS Injection via Nmap
scan_nmap_freak FREAK via Nmap
scan_nmap_logjam LOGJAM via Nmap
scan_nmap_sloris Slowloris via Nmap
scan_slowloris Slowloris DoS check

🖧 Port & Service Scanning

Modul Deskripsi
scan_nmap Fast scan port
scan_full_tcp Full TCP scan (1-65535)
scan_full_udp Full UDP scan (1-65535)
scan_ftp Cek FTP (port 21)
scan_telnets Cek Telnet (port 23)
scan_sqlserver Cek MS-SQL (port 1433)
scan_mysql Cek MySQL (port 3306)
scan_oracle Cek Oracle (port 1521)
scan_rdp_udp / scan_rdp_tcp Cek RDP (port 3389)
scan_snmp Cek SNMP (port 161)
scan_smb_tcp / scan_smb_udp Cek SMB
scan_stuxnet Deteksi Stuxnet (port 445)

🌐 CMS & Web App Detection

Modul Deskripsi
scan_wp_check Deteksi WordPress
scan_drp_check Deteksi Drupal
scan_joom_check Deteksi Joomla
scan_webdav Cek WebDAV
scan_iis_webdav Cek IIS WebDAV
scan_aspnet_elmah_axd Cek ASP.NET Elmah
scan_uniscan_robots Cek robots.txt & sitemap.xml

---

🧰 Prasyarat (Requirements)

JokoScan adalah wrapper yang memanggil banyak tools eksternal. Pastikan tools berikut terpasang dan tersedia di $PATH:

Wajib (inti)

```bash
sudo apt update
sudo apt install -y python3 nmap whois dnsutils wget
```

Tools Keamanan (install sesuai kebutuhan)

```bash
# Debian/Ubuntu (via apt)
sudo apt install -y nikto dirb dnsrecon dnsenum dnsmap fierce lbd whatweb wapiti sslyze

# Tools yang perlu diinstall manual / via pip / GitHub:
# - wafw00f      : pip install wafw00f
# - theHarvester : https://github.com/laramies/theHarvester
# - amass        : https://github.com/owasp-amass/amass
# - golismero    : https://github.com/golismero/golismero
# - xsser        : https://github.com/epsylon/xsser
# - uniscan      : https://github.com/ggrothendieck/uniscan
# - dmitry       : https://github.com/jaygreig86/dmitry
# - davtest      : https://github.com/cldrn/davtest
# - dnswalk      : https://github.com/drwetter/dnswalk
```

💡 Tips: Jika sebuah tool tidak terpasang, modul terkait akan gagal dan menampilkan pesan error, tetapi modul lain tetap berjalan.

Python

· Python 3.6+
· Tidak ada dependensi library eksternal (hanya standard library).

---

🚀 Instalasi

```bash
# 1. Clone / unduh file
git clone <repo-url> jokoscan
cd jokoscan

# 2. Beri izin eksekusi
chmod +x jokoscan.py

# 3. (Opsional) verifikasi
python3 jokoscan.py --help
```

---

🎯 Cara Penggunaan

Sintaks Dasar

```bash
python3 jokoscan.py <target> [--skip MODUL ...]
```

Contoh

1. Scan penuh sebuah domain

```bash
python3 jokoscan.py example.com
```

2. Scan dengan URL lengkap (protokol & www. akan dinormalisasi otomatis)

```bash
python3 jokoscan.py https://www.example.com
```

3. Scan IP address

```bash
python3 jokoscan.py 192.168.1.10
```

4. Melewati modul tertentu (berguna untuk mempercepat atau menghindari scan berat)

```bash
python3 jokoscan.py example.com --skip scan_full_tcp scan_full_udp scan_golismero
```

5. Melewati semua modul Nikto

```bash
python3 jokoscan.py example.com --skip \
  scan_nikto scan_nikto_xss scan_nikto_subrute scan_nikto_shellshock \
  scan_nikto_internalip scan_nikto_putdel scan_nikto_headers \
  scan_nikto_ms01070 scan_nikto_servermsgs scan_nikto_outdated \
  scan_nikto_httpoptions scan_nikto_cgi scan_nikto_ssl \
  scan_nikto_sitefiles scan_nikto_paths
```

Argumen

Argumen Wajib Deskripsi
target ✅ Domain, URL, atau IP target
--skip ❌ Satu atau lebih nama fungsi modul yang dilewati (dipisah spasi)

---

📊 Contoh Output

```
  ___  _       ___  ____  ____  ____ 
 / __)( )     / __)/_  _)(_  _)(  _ \
( (_-.| |    ( (__   ) (   ) |  )   /
 \___/\_)__   \___)  (__)  (__)  (_)\
                                      
BLACK HAT ELITE SCANNER v2.0
Author: Dwi Joko Purwanto (KARANGANYAR ELITE HACKER)
Target: example.com
Status: ONLINE
----------------------------------------
[!] Scanning Host Info for example.com
[+] Host Information Found:
...
[!] Running Nmap Fast Scan on example.com
[+] Open Ports Detected:
...
========================================
Scan Complete!
========================================
```

---

⚙️ Cara Kerja

1. Normalisasi target — URL di-parse, www. dihapus, diambil hostname-nya.
2. Cek koneksi internet — Status ditampilkan di banner.
3. Eksekusi modul berurutan — Setiap fungsi modul memanggil tool eksternal via subprocess dengan timeout (default 300 detik, 600 detik untuk full port scan).
4. Filter --skip — Modul yang namanya ada di daftar skip tidak akan dijalankan.
5. Error handling — Jika satu modul gagal (tool tidak ada, timeout, dll), modul lain tetap lanjut.

---

🧪 Rekomendasi Penggunaan Etis

Gunakan JokoScan hanya pada:

· ✅ Sistem milik sendiri (lab pribadi, VM, CTF).
· ✅ Target yang Anda punya izin tertulis untuk diuji (engagement kontrak).
· ✅ Platform latihan legal seperti HackTheBox, TryHackMe, VulnHub, dll.

Hindari:

· ❌ Memindai domain publik tanpa izin.
· ❌ Menggunakan modul DoS (Slowloris) pada sistem produksi.
· ❌ Menyalahgunakan temuan untuk tujuan ilegal.

---

🐛 Troubleshooting

Masalah Solusi
command not found untuk tool tertentu Install tool yang disebutkan di bagian Prasyarat
Modul berjalan lambat / timeout Gunakan --skip untuk melewati scan berat (scan_full_tcp, scan_full_udp, scan_golismero)
Output kosong / tidak terdeteksi Cek apakah target benar-benar online (ping <target>)
Warna tidak muncul Pastikan terminal mendukung ANSI color (bash/zsh modern)

---

📜 Lisensi

Belum ditentukan — hubungi penulis untuk informasi lebih lanjut.

---

👤 Author

Dwi Joko Purwanto
KARANGANYAR ELITE HACKER
🔹 Black Hat Elite Scanner v2.0

---

🙏 Kontribusi

Pull request, issue, dan saran modul baru sangat diterima. Pastikan setiap kontribusi mengikuti prinsip ethical hacking dan tidak menambahkan fitur yang bersifat destruktif tanpa peringatan jelas.

---

Ingat: With great power comes great responsibility. Gunakan JokoScan untuk membuat internet lebih aman, bukan merusaknya. 🛡️
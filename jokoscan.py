#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import argparse
import json
import time
import random
import threading
import re
from urllib.parse import urlsplit
from collections import defaultdict

# --- Constants & Colors ---
class Bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[45m'
    BG_MAGENTA = '\033[46m'
    BG_WHITE = '\033[47m'

# --- Utility Functions ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Bcolors.BOLD}
  ___  _       ___  ____  ____  ____ 
 / __)( )     / __)/_  _)(_  _)(  _ \
( (_-.| |    ( (__   ) (   ) |  )   /
 \___/\_)__   \___)  (__)  (__)  (_)\\
                                      
{Bcolors.ENDC}
{Bcolors.WARNING}BLACK HAT ELITE SCANNER v2.0{Bcolors.ENDC}
{Bcolors.CYAN}Author: Dwi Joko Purwanto (KARANGANYAR ELITE HACKER){Bcolors.ENDC}
{Bcolors.BLUE}Target: {target}{Bcolors.ENDC}
{Bcolors.GREEN}Status: {status}{Bcolors.ENDC}
{Bcolors.BOLD}----------------------------------------{Bcolors.ENDC}
"""
    print(banner)

def get_terminal_width():
    try:
        return subprocess.check_output(['stty', 'size']).split()[1]
    except:
        return 80

def spinner(message):
    spinners = ['|', '/', '-', '\\']
    for i in range(100):
        sys.stdout.write(f"\r{Bcolors.BOLD}[+] {message}: {spinners[i % len(spinners)]}{Bcolors.ENDC}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\r" + " " * (len(message) + 20) + "\r", end="")

def run_command(cmd, timeout=300):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

def check_internet():
    try:
        result = subprocess.run("ping -c 1 google.com > /dev/null 2>&1", shell=True)
        return result.returncode == 0
    except:
        return False

def get_target_domain(url):
    parsed = urlsplit(url)
    host = parsed.netloc
    if host.startswith('www.'):
        host = host[4:]
    return host

# --- Scanning Modules ---

def scan_host(domain):
    print(f"{Bcolors.BOLD}[!] Scanning Host Info for {domain}{Bcolors.ENDC}")
    stdout, stderr, rc = run_command(f"host {domain}")
    if "has address" in stdout or "mail is handled" in stdout:
        print(f"{Bcolors.GREEN}[+] Host Information Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.FAIL}[-] No Host Information Found.{Bcolors.ENDC}")

def scan_nmap(domain):
    print(f"{Bcolors.BOLD}[!] Running Nmap Fast Scan on {domain}{Bcolors.ENDC}")
    spinner("Nmap")
    stdout, stderr, rc = run_command(f"nmap -F --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.GREEN}[+] Open Ports Detected:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.FAIL}[-] No Open Ports Found.{Bcolors.ENDC}")

def scan_waf(domain):
    print(f"{Bcolors.BOLD}[!] Checking for WAF on {domain}{Bcolors.ENDC}")
    spinner("WAF Check")
    stdout, stderr, rc = run_command(f"wafw00f {domain}")
    if "WAF Detected" in stdout:
        print(f"{Bcolors.WARNING}[+] WAF Detected:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No WAF Detected.{Bcolors.ENDC}")

def scan_ssl_heartbleed(domain):
    print(f"{Bcolors.BOLD}[!] Checking Heartbleed Vulnerability on {domain}{Bcolors.ENDC}")
    spinner("Heartbleed Check")
    stdout, stderr, rc = run_command(f"sslyze --heartbleed {domain}")
    if "HEARTBLEED" in stdout:
        print(f"{Bcolors.FAIL}[+] Heartbleed Vulnerable!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Not Vulnerable to Heartbleed.{Bcolors.ENDC}")

def scan_xss(domain):
    print(f"{Bcolors.BOLD}[!] Checking XSS Protection on {domain}{Bcolors.ENDC}")
    spinner("XSS Check")
    stdout, stderr, rc = run_command(f"nmap -p 80 --script http-security-headers {domain}")
    if "X-XSS-Protection" in stdout:
        print(f"{Bcolors.GREEN}[+] XSS Protection Header Present.{Bcolors.ENDC}")
    else:
        print(f"{Bcolors.WARNING}[-] XSS Protection Header Missing.{Bcolors.ENDC}")

def scan_slowloris(domain):
    print(f"{Bcolors.BOLD}[!] Checking Slowloris DoS on {domain}{Bcolors.ENDC}")
    spinner("Slowloris Check")
    stdout, stderr, rc = run_command(f"nmap -p 80,443 --script http-slowloris --max-parallelism 500 {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.FAIL}[+] Vulnerable to Slowloris DoS!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Not Vulnerable to Slowloris.{Bcolors.ENDC}")

def scan_dns_recon(domain):
    print(f"{Bcolors.BOLD}[!] Running DNS Recon on {domain}{Bcolors.ENDC}")
    spinner("DNS Recon")
    stdout, stderr, rc = run_command(f"dnsrecon -d {domain}")
    if "Zone Transfer" in stdout:
        print(f"{Bcolors.WARNING}[+] Zone Transfer Successful!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Zone Transfer Issues.{Bcolors.ENDC}")

def scan_the_harvester(domain):
    print(f"{Bcolors.BOLD}[!] Running The Harvester on {domain}{Bcolors.ENDC}")
    spinner("The Harvester")
    stdout, stderr, rc = run_command(f"theHarvester -l 50 -b censys -d {domain}")
    if "Emails" in stdout:
        print(f"{Bcolors.GREEN}[+] Emails Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.FAIL}[-] No Emails Found.{Bcolors.ENDC}")

def scan_golismero(domain):
    print(f"{Bcolors.BOLD}[!] Running Golismero Full Scan on {domain}{Bcolors.ENDC}")
    spinner("Golismero")
    stdout, stderr, rc = run_command(f"golismero {domain} -e all")
    if "Vulnerabilities" in stdout:
        print(f"{Bcolors.FAIL}[+] Vulnerabilities Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Major Vulnerabilities Found.{Bcolors.ENDC}")

def scan_dirb(domain):
    print(f"{Bcolors.BOLD}[!] Running DirB Brute Force on {domain}{Bcolors.ENDC}")
    spinner("DirB")
    stdout, stderr, rc = run_command(f"dirb http://{domain} /usr/share/dirb/wordlists/common.txt -fi")
    if "FOUND:" in stdout:
        print(f"{Bcolors.WARNING}[+] Directories Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Directories Found.{Bcolors.ENDC}")

def scan_xsser(domain):
    print(f"{Bcolors.BOLD}[!] Running XSSer on {domain}{Bcolors.ENDC}")
    spinner("XSSer")
    stdout, stderr, rc = run_command(f"xsser --all=http://{domain}")
    if "Vulnerability" in stdout:
        print(f"{Bcolors.FAIL}[+] XSS Vulnerability Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No XSS Vulnerabilities Found.{Bcolors.ENDC}")

def scan_uniscan(domain):
    print(f"{Bcolors.BOLD}[!] Running Uniscan on {domain}{Bcolors.ENDC}")
    spinner("Uniscan")
    stdout, stderr, rc = run_command(f"uniscan -u http://{domain} -q -w -r -s -d")
    if "[+]" in stdout:
        print(f"{Bcolors.WARNING}[+] Findings from Uniscan:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Major Findings.{Bcolors.ENDC}")

def scan_nikto(domain):
    print(f"{Bcolors.BOLD}[!] Running Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto")
    stdout, stderr, rc = run_command(f"nikto -h http://{domain}")
    if "Vulnerabilities" in stdout:
        print(f"{Bcolors.FAIL}[+] Vulnerabilities Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Major Vulnerabilities Found.{Bcolors.ENDC}")

def scan_dmitry(domain):
    print(f"{Bcolors.BOLD}[!] Running DMitry on {domain}{Bcolors.ENDC}")
    spinner("DMitry")
    stdout, stderr, rc = run_command(f"dmitry -e -s -p -b {domain}")
    if "E-Mail" in stdout:
        print(f"{Bcolors.GREEN}[+] Emails and Subdomains Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.FAIL}[-] No Information Found.{Bcolors.ENDC}")

def scan_dnsenum(domain):
    print(f"{Bcolors.BOLD}[!] Running DNSEnum on {domain}{Bcolors.ENDC}")
    spinner("DNSEnum")
    stdout, stderr, rc = run_command(f"dnsenum {domain}")
    if "AXFR record query failed" not in stdout:
        print(f"{Bcolors.WARNING}[+] DNS Records Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No DNS Records Found.{Bcolors.ENDC}")

def scan_fierce(domain):
    print(f"{Bcolors.BOLD}[!] Running Fierce on {domain}{Bcolors.ENDC}")
    spinner("Fierce")
    stdout, stderr, rc = run_command(f"fierce --domain {domain}")
    if "Found" in stdout:
        print(f"{Bcolors.GREEN}[+] Subdomains Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.FAIL}[-] No Subdomains Found.{Bcolors.ENDC}")

def scan_wapiti(domain):
    print(f"{Bcolors.BOLD}[!] Running Wapiti on {domain}{Bcolors.ENDC}")
    spinner("Wapiti")
    stdout, stderr, rc = run_command(f"wapiti -u http://{domain} -f txt -o wapiti_report.txt")
    if "Host:" in stdout:
        print(f"{Bcolors.FAIL}[+] Vulnerabilities Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Major Vulnerabilities Found.{Bcolors.ENDC}")

def scan_amass(domain):
    print(f"{Bcolors.BOLD}[!] Running AMass on {domain}{Bcolors.ENDC}")
    spinner("AMass")
    stdout, stderr, rc = run_command(f"amass enum -d {domain}")
    if "names were discovered" not in stdout:
        print(f"{Bcolors.GREEN}[+] Subdomains Found:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.FAIL}[-] No Subdomains Found.{Bcolors.ENDC}")

def scan_webdav(domain):
    print(f"{Bcolors.BOLD}[!] Checking WebDAV on {domain}{Bcolors.ENDC}")
    spinner("WebDAV Check")
    stdout, stderr, rc = run_command(f"davtest -url http://{domain}")
    if "SUCCEED" in stdout:
        print(f"{Bcolors.WARNING}[+] WebDAV Enabled!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] WebDAV Not Enabled.{Bcolors.ENDC}")

def scan_whatweb(domain):
    print(f"{Bcolors.BOLD}[!] Running WhatWeb on {domain}{Bcolors.ENDC}")
    spinner("WhatWeb")
    stdout, stderr, rc = run_command(f"whatweb {domain} -a 1")
    if "HTTPServer" in stdout:
        print(f"{Bcolors.GREEN}[+] Technologies Detected:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.FAIL}[-] No Technologies Detected.{Bcolors.ENDC}")

def scan_telnets(domain):
    print(f"{Bcolors.BOLD}[!] Checking Telnet Service on {domain}{Bcolors.ENDC}")
    spinner("Telnet Check")
    stdout, stderr, rc = run_command(f"nmap -p 23 --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.FAIL}[+] Telnet Service Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Telnet Service Closed.{Bcolors.ENDC}")

def scan_ftp(domain):
    print(f"{Bcolors.BOLD}[!] Checking FTP Service on {domain}{Bcolors.ENDC}")
    spinner("FTP Check")
    stdout, stderr, rc = run_command(f"nmap -p 21 --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.FAIL}[+] FTP Service Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] FTP Service Closed.{Bcolors.ENDC}")

def scan_stuxnet(domain):
    print(f"{Bcolors.BOLD}[!] Checking Stuxnet Worm on {domain}{Bcolors.ENDC}")
    spinner("Stuxnet Check")
    stdout, stderr, rc = run_command(f"nmap --script stuxnet-detect -p 445 {domain}")
    if "open" in stdout:
        print(f"{Bcolors.FAIL}[+] Stuxnet Worm Detected!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Stuxnet Worm Not Detected.{Bcolors.ENDC}")

def scan_sqlserver(domain):
    print(f"{Bcolors.BOLD}[!] Checking MS-SQL Server on {domain}{Bcolors.ENDC}")
    spinner("MS-SQL Check")
    stdout, stderr, rc = run_command(f"nmap -p 1433 --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.WARNING}[+] MS-SQL Server Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] MS-SQL Server Closed.{Bcolors.ENDC}")

def scan_mysql(domain):
    print(f"{Bcolors.BOLD}[!] Checking MySQL DB on {domain}{Bcolors.ENDC}")
    spinner("MySQL Check")
    stdout, stderr, rc = run_command(f"nmap -p 3306 --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.WARNING}[+] MySQL DB Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] MySQL DB Closed.{Bcolors.ENDC}")

def scan_oracle(domain):
    print(f"{Bcolors.BOLD}[!] Checking Oracle DB on {domain}{Bcolors.ENDC}")
    spinner("Oracle Check")
    stdout, stderr, rc = run_command(f"nmap -p 1521 --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.WARNING}[+] Oracle DB Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Oracle DB Closed.{Bcolors.ENDC}")

def scan_rdp_udp(domain):
    print(f"{Bcolors.BOLD}[!] Checking RDP over UDP on {domain}{Bcolors.ENDC}")
    spinner("RDP UDP Check")
    stdout, stderr, rc = run_command(f"nmap -p 3389 --open -sU {domain}")
    if "open" in stdout:
        print(f"{Bcolors.FAIL}[+] RDP over UDP Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] RDP over UDP Closed.{Bcolors.ENDC}")

def scan_rdp_tcp(domain):
    print(f"{Bcolors.BOLD}[!] Checking RDP over TCP on {domain}{Bcolors.ENDC}")
    spinner("RDP TCP Check")
    stdout, stderr, rc = run_command(f"nmap -p 3389 --open -sT {domain}")
    if "open" in stdout:
        print(f"{Bcolors.FAIL}[+] RDP over TCP Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] RDP over TCP Closed.{Bcolors.ENDC}")

def scan_full_tcp(domain):
    print(f"{Bcolors.BOLD}[!] Performing Full TCP Port Scan on {domain}{Bcolors.ENDC}")
    spinner("Full TCP Scan")
    stdout, stderr, rc = run_command(f"nmap -p 1-65535 --open {domain}", timeout=600)
    if "open" in stdout:
        print(f"{Bcolors.WARNING}[+] TCP Ports Open:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No TCP Ports Open.{Bcolors.ENDC}")

def scan_full_udp(domain):
    print(f"{Bcolors.BOLD}[!] Performing Full UDP Port Scan on {domain}{Bcolors.ENDC}")
    spinner("Full UDP Scan")
    stdout, stderr, rc = run_command(f"nmap -p 1-65535 -sU --open {domain}", timeout=600)
    if "open" in stdout:
        print(f"{Bcolors.WARNING}[+] UDP Ports Open:{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No UDP Ports Open.{Bcolors.ENDC}")

def scan_snmp(domain):
    print(f"{Bcolors.BOLD}[!] Checking SNMP Service on {domain}{Bcolors.ENDC}")
    spinner("SNMP Check")
    stdout, stderr, rc = run_command(f"nmap -p 161 -sU --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.WARNING}[+] SNMP Service Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] SNMP Service Closed.{Bcolors.ENDC}")

def scan_aspnet_elmah_axd(domain):
    print(f"{Bcolors.BOLD}[+] Checking ASP.NET Elmah Logger on {domain}{Bcolors.ENDC}")
    spinner("Elmah Check")
    temp_file = "/tmp/rapidscan_temp_aspnet_elmah_axd"
    stdout, stderr, rc = run_command(f"wget -O {temp_file} --tries=1 http://{domain}/elmah.axd")
    try:
        if os.path.exists(temp_file):
            with open(temp_file, "r", errors="ignore") as f:
                content = f.read()
            if "Microsoft SQL Server Error Log" in content:
                print(f"{Bcolors.WARNING}[+] Elmah Logger Found!{Bcolors.ENDC}")
                print(content)
            else:
                print(f"{Bcolors.GREEN}[-] Elmah Logger Not Found.{Bcolors.ENDC}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def scan_smb_tcp(domain):
    print(f"{Bcolors.BOLD}[+] Checking SMB over TCP on {domain}{Bcolors.ENDC}")
    spinner("SMB TCP Check")
    stdout, stderr, rc = run_command(f"nmap -p 445,137-139 --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.WARNING}[+] SMB over TCP Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] SMB over TCP Closed.{Bcolors.ENDC}")

def scan_smb_udp(domain):
    print(f"{Bcolors.BOLD}[+] Checking SMB over UDP on {domain}{Bcolors.ENDC}")
    spinner("SMB UDP Check")
    stdout, stderr, rc = run_command(f"nmap -p 137,138 --open {domain}")
    if "open" in stdout:
        print(f"{Bcolors.WARNING}[+] SMB over UDP Open!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] SMB over UDP Closed.{Bcolors.ENDC}")

def scan_iis_webdav(domain):
    print(f"{Bcolors.BOLD}[+] Checking IIS WebDAV on {domain}{Bcolors.ENDC}")
    spinner("IIS WebDAV Check")
    stdout, stderr, rc = run_command(f"nmap -p 80 --script=http-iis-webdav-vuln {domain}")
    if "WebDAV is ENABLED" in stdout:
        print(f"{Bcolors.WARNING}[+] IIS WebDAV Enabled!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] IIS WebDAV Not Enabled.{Bcolors.ENDC}")

def scan_wp_check(domain):
    print(f"{Bcolors.BOLD}[+] Checking WordPress Installation on {domain}{Bcolors.ENDC}")
    spinner("WP Check")
    temp_file = "/tmp/rapidscan_temp_wp_check"
    stdout, stderr, rc = run_command(f"wget -O {temp_file} --tries=1 http://{domain}/wp-admin")
    try:
        if os.path.exists(temp_file):
            with open(temp_file, "r", errors="ignore") as f:
                content = f.read()
            if "WordPress" in content:
                print(f"{Bcolors.WARNING}[+] WordPress Installation Found!{Bcolors.ENDC}")
                print(content)
            else:
                print(f"{Bcolors.GREEN}[-] WordPress Not Found.{Bcolors.ENDC}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def scan_drp_check(domain):
    print(f"{Bcolors.BOLD}[+] Checking Drupal Installation on {domain}{Bcolors.ENDC}")
    spinner("Drupal Check")
    temp_file = "/tmp/rapidscan_temp_drp_check"
    stdout, stderr, rc = run_command(f"wget -O {temp_file} --tries=1 http://{domain}/user")
    try:
        if os.path.exists(temp_file):
            with open(temp_file, "r", errors="ignore") as f:
                content = f.read()
            if "Drupal" in content:
                print(f"{Bcolors.WARNING}[+] Drupal Installation Found!{Bcolors.ENDC}")
                print(content)
            else:
                print(f"{Bcolors.GREEN}[-] Drupal Not Found.{Bcolors.ENDC}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def scan_joom_check(domain):
    print(f"{Bcolors.BOLD}[+] Checking Joomla Installation on {domain}{Bcolors.ENDC}")
    spinner("Joomla Check")
    temp_file = "/tmp/rapidscan_temp_joom_check"
    stdout, stderr, rc = run_command(f"wget -O {temp_file} --tries=1 http://{domain}/administrator")
    try:
        if os.path.exists(temp_file):
            with open(temp_file, "r", errors="ignore") as f:
                content = f.read()
            if "Joomla" in content:
                print(f"{Bcolors.WARNING}[+] Joomla Installation Found!{Bcolors.ENDC}")
                print(content)
            else:
                print(f"{Bcolors.GREEN}[-] Joomla Not Found.{Bcolors.ENDC}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def scan_uniscan_robots(domain):
    print(f"{Bcolors.BOLD}[+] Checking Robots.txt & Sitemap.xml on {domain}{Bcolors.ENDC}")
    spinner("Robots Check")
    stdout, stderr, rc = run_command(f"uniscan -e -u http://{domain}")
    if "[+]" in stdout:
        print(f"{Bcolors.WARNING}[+] Robots/Sitemap Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Robots/Sitemap Not Found.{Bcolors.ENDC}")

def scan_lbd(domain):
    print(f"{Bcolors.BOLD}[+] Checking Load Balancers on {domain}{Bcolors.ENDC}")
    spinner("LBD Check")
    stdout, stderr, rc = run_command(f"lbd {domain}")
    if "Load-balancing" in stdout:
        print(f"{Bcolors.WARNING}[+] Load Balancer Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Load Balancer Found.{Bcolors.ENDC}")

def scan_dnswalk(domain):
    print(f"{Bcolors.BOLD}[+] Checking Zone Transfer with DNSEnum on {domain}{Bcolors.ENDC}")
    spinner("DNSEnum ZT Check")
    stdout, stderr, rc = run_command(f"dnswalk -d {domain}")
    if "0 errors" in stdout:
        print(f"{Bcolors.WARNING}[+] Zone Transfer Successful!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Zone Transfer Found.{Bcolors.ENDC}")

def scan_whois(domain):
    print(f"{Bcolors.BOLD}[+] Checking Whois Information on {domain}{Bcolors.ENDC}")
    spinner("Whois Check")
    stdout, stderr, rc = run_command(f"whois {domain}")
    if "Admin Email:" in stdout:
        print(f"{Bcolors.WARNING}[+] Whois Information Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Whois Information Found.{Bcolors.ENDC}")

def scan_nmap_header(domain):
    print(f"{Bcolors.BOLD}[+] Checking XSS Filter Header on {domain}{Bcolors.ENDC}")
    spinner("Nmap Header Check")
    stdout, stderr, rc = run_command(f"nmap -p 80 --script http-security-headers {domain}")
    if "XSS filter is disabled" in stdout:
        print(f"{Bcolors.WARNING}[+] XSS Filter Disabled!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] XSS Filter Enabled.{Bcolors.ENDC}")

def scan_nmap_sloris(domain):
    print(f"{Bcolors.BOLD}[+] Checking Slowloris with Nmap on {domain}{Bcolors.ENDC}")
    spinner("Nmap Sloris Check")
    stdout, stderr, rc = run_command(f"nmap -p 80,443 --script http-slowloris --max-parallelism 500 {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.FAIL}[+] Vulnerable to Slowloris!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Not Vulnerable to Slowloris.{Bcolors.ENDC}")

def scan_sslyze_hbleed(domain):
    print(f"{Bcolors.BOLD}[+] Checking Heartbleed with SSLyze on {domain}{Bcolors.ENDC}")
    spinner("SSLyze Heartbleed Check")
    stdout, stderr, rc = run_command(f"sslyze --heartbleed {domain}")
    if "HEARTBLEED" in stdout:
        print(f"{Bcolors.FAIL}[+] Heartbleed Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Heartbleed Found.{Bcolors.ENDC}")

def scan_nmap_hbleed(domain):
    print(f"{Bcolors.BOLD}[+] Checking Heartbleed with Nmap on {domain}{Bcolors.ENDC}")
    spinner("Nmap Heartbleed Check")
    stdout, stderr, rc = run_command(f"nmap -p 443 --script ssl-heartbleed {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.FAIL}[+] Heartbleed Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Heartbleed Found.{Bcolors.ENDC}")

def scan_nmap_poodle(domain):
    print(f"{Bcolors.BOLD}[+] Checking POODLE with Nmap on {domain}{Bcolors.ENDC}")
    spinner("Nmap POODLE Check")
    stdout, stderr, rc = run_command(f"nmap -p 443 --script ssl-poodle {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.FAIL}[+] POODLE Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No POODLE Found.{Bcolors.ENDC}")

def scan_nmap_ccs(domain):
    print(f"{Bcolors.BOLD}[+] Checking CCS Injection with Nmap on {domain}{Bcolors.ENDC}")
    spinner("Nmap CCS Check")
    stdout, stderr, rc = run_command(f"nmap -p 443 --script ssl-ccs-injection {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.FAIL}[+] CCS Injection Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No CCS Injection Found.{Bcolors.ENDC}")

def scan_nmap_freak(domain):
    print(f"{Bcolors.BOLD}[+] Checking FREAK with Nmap on {domain}{Bcolors.ENDC}")
    spinner("Nmap FREAK Check")
    stdout, stderr, rc = run_command(f"nmap -p 443 --script ssl-enum-ciphers {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.FAIL}[+] FREAK Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No FREAK Found.{Bcolors.ENDC}")

def scan_nmap_logjam(domain):
    print(f"{Bcolors.BOLD}[+] Checking LOGJAM with Nmap on {domain}{Bcolors.ENDC}")
    spinner("Nmap LOGJAM Check")
    stdout, stderr, rc = run_command(f"nmap -p 443 --script ssl-dh-params {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.FAIL}[+] LOGJAM Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No LOGJAM Found.{Bcolors.ENDC}")

def scan_sslyze_ocsp(domain):
    print(f"{Bcolors.BOLD}[+] Checking OCSP Stapling with SSLyze on {domain}{Bcolors.ENDC}")
    spinner("SSLyze OCSP Check")
    stdout, stderr, rc = run_command(f"sslyze --certinfo=basic {domain}")
    if "ERROR - OCSP response status is not successful" in stdout:
        print(f"{Bcolors.WARNING}[+] OCSP Stapling Failed!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] OCSP Stapling Successful.{Bcolors.ENDC}")

def scan_sslyze_zlib(domain):
    print(f"{Bcolors.BOLD}[+] Checking ZLib Compression with SSLyze on {domain}{Bcolors.ENDC}")
    spinner("SSLyze Zlib Check")
    stdout, stderr, rc = run_command(f"sslyze --compression {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.WARNING}[+] ZLib Compression Enabled!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] ZLib Compression Disabled.{Bcolors.ENDC}")

def scan_sslyze_reneg(domain):
    print(f"{Bcolors.BOLD}[+] Checking Renegotiation with SSLyze on {domain}{Bcolors.ENDC}")
    spinner("SSLyze Reneg Check")
    stdout, stderr, rc = run_command(f"sslyze --reneg {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.WARNING}[+] Renegotiation Enabled!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Renegotiation Disabled.{Bcolors.ENDC}")

def scan_sslyze_resum(domain):
    print(f"{Bcolors.BOLD}[+] Checking Session Resumption with SSLyze on {domain}{Bcolors.ENDC}")
    spinner("SSLyze Resum Check")
    stdout, stderr, rc = run_command(f"sslyze --resum {domain}")
    if "VULNERABLE" in stdout:
        print(f"{Bcolors.WARNING}[+] Session Resumption Enabled!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Session Resumption Disabled.{Bcolors.ENDC}")

def scan_uniscan_filebrute(domain):
    print(f"{Bcolors.BOLD}[+] Brute Forcing Files with Uniscan on {domain}{Bcolors.ENDC}")
    spinner("Uniscan File Brute")
    stdout, stderr, rc = run_command(f"uniscan -w -u http://{domain}")
    if "[+]" in stdout:
        print(f"{Bcolors.WARNING}[+] Open Files Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Open Files Found.{Bcolors.ENDC}")

def scan_uniscan_dirbrute(domain):
    print(f"{Bcolors.BOLD}[+] Brute Forcing Directories with Uniscan on {domain}{Bcolors.ENDC}")
    spinner("Uniscan Dir Brute")
    stdout, stderr, rc = run_command(f"uniscan -q -u http://{domain}")
    if "[+]" in stdout:
        print(f"{Bcolors.WARNING}[+] Open Directories Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Open Directories Found.{Bcolors.ENDC}")

def scan_uniscan_ministresser(domain):
    print(f"{Bcolors.BOLD}[+] Stress Testing Domain with Uniscan on {domain}{Bcolors.ENDC}")
    spinner("Uniscan Stress Test")
    stdout, stderr, rc = run_command(f"uniscan -r -u http://{domain}")
    if "[+]" in stdout:
        print(f"{Bcolors.WARNING}[+] Stress Test Passed!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Stress Test Failed.{Bcolors.ENDC}")

def scan_uniscan_rfi(domain):
    print(f"{Bcolors.BOLD}[+] Checking LFI/RFI/RCE with Uniscan on {domain}{Bcolors.ENDC}")
    spinner("Uniscan RFI Check")
    stdout, stderr, rc = run_command(f"uniscan -s -u http://{domain}")
    if "[+]" in stdout:
        print(f"{Bcolors.FAIL}[+] LFI/RFI/RCE Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No LFI/RFI/RCE Found.{Bcolors.ENDC}")

def scan_uniscan_xss(domain):
    print(f"{Bcolors.BOLD}[+] Checking XSS/SQLi with Uniscan on {domain}{Bcolors.ENDC}")
    spinner("Uniscan XSS Check")
    stdout, stderr, rc = run_command(f"uniscan -d -u http://{domain}")
    if "[+]" in stdout:
        print(f"{Bcolors.FAIL}[+] XSS/SQLi Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No XSS/SQLi Found.{Bcolors.ENDC}")

def scan_nikto_xss(domain):
    print(f"{Bcolors.BOLD}[+] Checking Apache Expect XSS with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto XSS Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'apache_expect_xss' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] Apache Expect XSS Header Missing!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Apache Expect XSS Header Present.{Bcolors.ENDC}")

def scan_nikto_subrute(domain):
    print(f"{Bcolors.BOLD}[+] Brute Forcing Subdomains with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto Sub Brute")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'subdomain' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] Subdomains Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Subdomains Found.{Bcolors.ENDC}")

def scan_nikto_shellshock(domain):
    print(f"{Bcolors.BOLD}[+] Checking Shellshock with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto Shellshock Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'shellshock' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.FAIL}[+] Shellshock Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Shellshock Found.{Bcolors.ENDC}")

def scan_nikto_internalip(domain):
    print(f"{Bcolors.BOLD}[+] Checking Internal IP Leak with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto IP Leak Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'cookies' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] Internal IP Leaked!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Internal IP Leak.{Bcolors.ENDC}")

def scan_nikto_putdel(domain):
    print(f"{Bcolors.BOLD}[+] Checking HTTP PUT DEL with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto PUT DEL Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'put_del_test' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] HTTP PUT DEL Enabled!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] HTTP PUT DEL Disabled.{Bcolors.ENDC}")

def scan_nikto_headers(domain):
    print(f"{Bcolors.BOLD}[+] Checking Headers with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto Headers Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'headers' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] Vulnerable Headers Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Vulnerable Headers Found.{Bcolors.ENDC}")

def scan_nikto_ms01070(domain):
    print(f"{Bcolors.BOLD}[+] Checking MS10-070 with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto MS10-070 Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'ms10-070' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] MS10-070 Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No MS10-070 Found.{Bcolors.ENDC}")

def scan_nikto_servermsgs(domain):
    print(f"{Bcolors.BOLD}[+] Checking Server Issues with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto Server Msgs Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'msgs' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] Server Issues Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Server Issues Found.{Bcolors.ENDC}")

def scan_nikto_outdated(domain):
    print(f"{Bcolors.BOLD}[+] Checking Outdated Server with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto Outdated Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'outdated' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] Server Outdated!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] Server Up to Date.{Bcolors.ENDC}")

def scan_nikto_httpoptions(domain):
    print(f"{Bcolors.BOLD}[+] Checking HTTP Options with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto HTTP Options Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'httpoptions' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] HTTP Options Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No HTTP Options Found.{Bcolors.ENDC}")

def scan_nikto_cgi(domain):
    print(f"{Bcolors.BOLD}[+] Enumerating CGI Directories with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto CGI Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'cgi' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] CGI Directories Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No CGI Directories Found.{Bcolors.ENDC}")

def scan_nikto_ssl(domain):
    print(f"{Bcolors.BOLD}[+] Checking SSL with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto SSL Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'ssl' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] SSL Vulnerabilities Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No SSL Vulnerabilities Found.{Bcolors.ENDC}")

def scan_nikto_sitefiles(domain):
    print(f"{Bcolors.BOLD}[+] Checking Interesting Files with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto Site Files Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'sitefiles' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] Interesting Files Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Interesting Files Found.{Bcolors.ENDC}")

def scan_nikto_paths(domain):
    print(f"{Bcolors.BOLD}[+] Checking Injectable Paths with Nikto on {domain}{Bcolors.ENDC}")
    spinner("Nikto Paths Check")
    stdout, stderr, rc = run_command(f"nikto -Plugins 'paths' -host http://{domain}")
    if "0 item(s) reported" not in stdout:
        print(f"{Bcolors.WARNING}[+] Injectable Paths Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Injectable Paths Found.{Bcolors.ENDC}")

def scan_dnsmap(domain):
    print(f"{Bcolors.BOLD}[+] Brute Forcing Subdomains with DNSMap on {domain}{Bcolors.ENDC}")
    spinner("DNSMap Brute")
    stdout, stderr, rc = run_command(f"dnsmap {domain}")
    if "#1" in stdout:
        print(f"{Bcolors.WARNING}[+] Subdomains Found!{Bcolors.ENDC}")
        print(stdout)
    else:
        print(f"{Bcolors.GREEN}[-] No Subdomains Found.{Bcolors.ENDC}")

def main():
    global target, status
    parser = argparse.ArgumentParser(description='RapidScan v2.0 - Black Hat Elite Edition')
    parser.add_argument('target', help='Target domain or IP')
    parser.add_argument('--skip', nargs='+', help='Skip specific scans')
    args = parser.parse_args()

    target = get_target_domain(args.target)
    status = "ONLINE" if check_internet() else "OFFLINE"

    clear_screen()
    print_banner()

    skip_modules = args.skip or []

    # List of all scan functions (duplikasi golismero dibersihkan, pertahankan scan_golismero utama)
    all_scans = [
        scan_host, scan_nmap, scan_waf, scan_ssl_heartbleed, scan_xss, scan_slowloris,
        scan_dns_recon, scan_the_harvester, scan_golismero, scan_dirb, scan_xsser,
        scan_uniscan, scan_nikto, scan_dmitry, scan_dnsenum, scan_fierce, scan_wapiti,
        scan_amass, scan_webdav, scan_whatweb, scan_telnets, scan_ftp, scan_stuxnet,
        scan_sqlserver, scan_mysql, scan_oracle, scan_rdp_udp, scan_rdp_tcp,
        scan_full_tcp, scan_full_udp, scan_snmp, scan_aspnet_elmah_axd, scan_smb_tcp,
        scan_smb_udp, scan_iis_webdav, scan_wp_check, scan_drp_check, scan_joom_check,
        scan_uniscan_robots, scan_lbd, scan_dnswalk, scan_whois,
        scan_nmap_header, scan_nmap_sloris, scan_sslyze_hbleed, scan_nmap_hbleed,
        scan_nmap_poodle, scan_nmap_ccs, scan_nmap_freak, scan_nmap_logjam,
        scan_sslyze_ocsp, scan_sslyze_zlib, scan_sslyze_reneg, scan_sslyze_resum,
        scan_uniscan_filebrute, scan_uniscan_dirbrute,
        scan_uniscan_ministresser, scan_uniscan_rfi, scan_uniscan_xss, scan_nikto_xss,
        scan_nikto_subrute, scan_nikto_shellshock, scan_nikto_internalip, scan_nikto_putdel,
        scan_nikto_headers, scan_nikto_ms01070, scan_nikto_servermsgs, scan_nikto_outdated,
        scan_nikto_httpoptions, scan_nikto_cgi, scan_nikto_ssl, scan_nikto_sitefiles,
        scan_nikto_paths, scan_dnsmap
    ]

    # Filter out skipped scans
    scans_to_run = [scan for scan in all_scans if scan.__name__ not in skip_modules]

    # Run scans sequentially
    for scan in scans_to_run:
        try:
            scan(target)
        except Exception as e:
            print(f"{Bcolors.FAIL}[-] Error running {scan.__name__}: {e}{Bcolors.ENDC}")

    print(f"{Bcolors.BOLD}========================================{Bcolors.ENDC}")
    print(f"{Bcolors.BOLD}Scan Complete!{Bcolors.ENDC}")
    print(f"{Bcolors.BOLD}========================================{Bcolors.ENDC}")

if __name__ == "__main__":
    main()

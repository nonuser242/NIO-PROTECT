
#!/usr/bin/env python3
import os
import sys
import ssl
import socket
import hashlib
import platform
import subprocess
import ipaddress
import urllib.request
from datetime import datetime
from getpass import getpass

VERSION = "1.0"
REPORT = "nio_report.txt"

def banner():
    os.system("clear")
    print("""
 _   _ ___ ___   ____  ____   ___ _____ _____ ____ _____
| \ | |_ _/ _ \ |  _ \|  _ \ / _ \_   _| ____/ ___|_   _|
|  \| || | | | || |_) | |_) | | | || | |  _| \___ \ | |
| |\  || | |_| ||  __/|  _ <| |_| || | | |___ ___) || |
|_| \_|___\___/ |_|   |_| \_\\___/ |_| |_____|____/ |_|

       N I O   P R O T E C T   v1.0
          ADVANCED SECURITY TOOLKIT
    """)

def report(message):
    with open(REPORT, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def system_info():
    print("\n--- SYSTEM INFORMATION ---")
    print("OS:", platform.system())
    print("Version:", platform.version())
    print("Architecture:", platform.machine())
    print("Python:", platform.python_version())
    print("Device:", platform.node())
    report("System information checked")
    input("\nEnter si aad u laabato...")

def network_info():
    print("\n--- NETWORK INFORMATION ---")
    for command in [["ip", "addr"], ["ip", "route"]]:
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=5
            )
            print(result.stdout or result.stderr)
        except Exception as e:
            print("Network command unavailable:", e)
    report("Network information checked")
    input("\nEnter si aad u laabato...")

def dns_lookup():
    host = input("\nGeli domain (tusaale google.com): ").strip()
    try:
        results = socket.getaddrinfo(host, None)
        addresses = sorted(set(x[4][0] for x in results))
        print("\nDNS RESULTS:")
        for address in addresses:
            print(" [+]", address)
        report(f"DNS lookup: {host}")
    except Exception as e:
        print("DNS error:", e)
    input("\nEnter si aad u laabato...")

def ping_test():
    host = input("\nGeli domain ama IP: ").strip()
    if not host or host.startswith("-"):
        print("Input khaldan.")
        return input("\nEnter...")
    option = "-n" if platform.system() == "Windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", option, "4", host],
            capture_output=True, text=True, timeout=15
        )
        print(result.stdout or result.stderr)
        report(f"Ping test: {host}")
    except Exception as e:
        print("Ping error:", e)
    input("\nEnter si aad u laabato...")

def port_scanner():
    print("\n--- AUTHORIZED LOCAL PORT SCANNER ---")
    target = input("Geli private IP ama localhost: ").strip()

    try:
        ip = ipaddress.ip_address(socket.gethostbyname(target))
        if not (ip.is_private or ip.is_loopback):
            print("Waxaa la oggol yahay private IP ama localhost oo keliya.")
            return input("\nEnter...")
    except Exception:
        print("IP khaldan.")
        return input("\nEnter...")

    print("\nIsticmaal oo keliya qalab aad leedahay ama fasax u haysato.")
    if input("Ma haysataa fasax? (yes/no): ").lower() != "yes":
        return

    ports = [21, 22, 25, 53, 80, 110, 143, 443, 445, 3306, 8080, 8443]
    print(f"\nScanning {ip} ...")

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.6)
                if s.connect_ex((str(ip), port)) == 0:
                    print(f"[OPEN] Port {port}")
        except OSError:
            pass

    report(f"Local authorized port scan: {ip}")
    input("\nScan complete. Enter...")

def website_checker():
    url = input("\nGeli website URL (https://example.com): ").strip()

    if not url.startswith(("https://", "http://")):
        print("URL waa inuu ku bilaabmaa http:// ama https://")
        return input("\nEnter...")

    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "NIO-PROTECT/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            print("\nHTTP STATUS:", response.status)
            print("\nSECURITY HEADERS:")
            headers = response.headers
            for h in [
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "X-Content-Type-Options",
                "X-Frame-Options",
                "Referrer-Policy"
            ]:
                print(f"{h}: {headers.get(h, 'Not detected')}")

        report(f"Website header check: {url}")

    except Exception as e:
        print("Website check error:", e)

    input("\nEnter si aad u laabato...")

def ssl_checker():
    host = input("\nGeli domain (tusaale google.com): ").strip()

    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=8) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure:
                cert = secure.getpeercert()
                print("\nSSL CERTIFICATE")
                print("Subject:", cert.get("subject"))
                print("Issuer:", cert.get("issuer"))
                print("Valid from:", cert.get("notBefore"))
                print("Valid until:", cert.get("notAfter"))
                print("TLS Version:", secure.version())
        report(f"SSL check: {host}")
    except Exception as e:
        print("SSL error:", e)

    input("\nEnter si aad u laabato...")

def password_checker():
    print("\n--- PASSWORD STRENGTH TEST ---")
    password = getpass("Geli password tijaabo ah: ")

    score = 0
    checks = [
        (len(password) >= 12, "12 characters ama ka badan"),
        (any(c.islower() for c in password), "Lowercase"),
        (any(c.isupper() for c in password), "Uppercase"),
        (any(c.isdigit() for c in password), "Numbers"),
        (any(not c.isalnum() for c in password), "Symbols")
    ]

    for passed, label in checks:
        print(("[OK] " if passed else "[NO] ") + label)
        score += passed

    levels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"]
    print("\nSTRENGTH:", levels[score])
    print("Xusuusnow: ha gelin password-kaaga dhabta ah.")
    report("Password strength test completed")
    input("\nEnter...")

def file_hash():
    path = input("\nGeli file path: ").strip()
    if not os.path.isfile(path):
        print("File lama helin.")
        return input("\nEnter...")

    digest = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                digest.update(chunk)
        print("\nSHA256:", digest.hexdigest())
        report(f"SHA256 calculated: {os.path.basename(path)}")
    except Exception as e:
        print("Hash error:", e)

    input("\nEnter...")

def show_report():
    print("\n--- SECURITY REPORT ---")
    if os.path.exists(REPORT):
        with open(REPORT, encoding="utf-8") as f:
            print(f.read() or "Report waa madhan.")
    else:
        print("Weli report lama samayn.")
    input("\nEnter si aad u laabato...")

def menu():
    while True:
        banner()
        print("""
 [1] System Information
 [2] Network Analyzer
 [3] DNS Lookup
 [4] Ping Tester
 [5] Local Port Scanner
 [6] Website Security Headers
 [7] SSL Certificate Checker
 [8] Password Strength Tester
 [9] SHA256 File Hash
 [10] Security Report
 [0] Exit
        """)

        choice = input("NIO-PROTECT >> ").strip()

        actions = {
            "1": system_info,
            "2": network_info,
            "3": dns_lookup,
            "4": ping_test,
            "5": port_scanner,
            "6": website_checker,
            "7": ssl_checker,
            "8": password_checker,
            "9": file_hash,
            "10": show_report
        }

        if choice == "0":
            print("\nNIO PROTECT CLOSED. Stay Safe!")
            break
        elif choice in actions:
            try:
                actions[choice]()
            except KeyboardInterrupt:
                print("\nOperation stopped.")
                input("Enter...")
        else:
            print("Doorasho khaldan!")
            input("Enter...")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nNIO PROTECT CLOSED.")


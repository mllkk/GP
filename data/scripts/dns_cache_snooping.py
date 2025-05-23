import subprocess
import re
from result_manager import save_result

def dns_cache_snooping_scan(target_ip):
    VULN_ID    = "DNS-001"
    VULN_TITLE = "DNS Cache Snooping"
    SCRIPT     = "dns_cache_snooping_scan.py"

    print(f"[+] Hedef DNS Sunucusu: {target_ip}")
    print("[+] Nmap ile DNS Cache Snooping testi yapılıyor...\n")

    try:
        command = [
            "nmap", "-sU",
            "--script=dns-cache-snoop",
            "--script-args=dns-cache-snoop.mode=nonrecursive",
            "-p", "53",
            target_ip
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout
        print(output)

        # Varsayılan değerler
        status  = "closed"
        details = "No cached domains detected."

        if "dns-cache-snoop" in output.lower():
            found_domains = re.findall(
                r'Host appears to be snooping on the following domains:\s*(.+)',
                output
            )
            if found_domains:
                status  = "open"
                details = "; ".join(found_domains)

        else:
            details = "Nmap script did not run or returned an error."

        # Sonucu kaydet
        save_result(
            vuln_id     = VULN_ID,
            vuln_title  = VULN_TITLE,
            target_ip   = target_ip,
            status      = status,
            script_name = SCRIPT,
            details     = details
        )

        # Ekrana özet ver
        if status == "open":
            print(f"\n[+] Zafiyet **AÇIK** – Bulunan alan adları: {details}")
        else:
            print("\n[-] Zafiyet kapalı görünüyor.")

    except Exception as e:
        print(f"[!] Hata oluştu: {e}")
        save_result(
            vuln_id     = VULN_ID,
            vuln_title  = VULN_TITLE,
            target_ip   = target_ip,
            status      = "error",
            script_name = SCRIPT,
            details     = str(e)
        )

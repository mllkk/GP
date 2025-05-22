# data/scripts/syn_scan.py
"""
Nmap SYN (-sS) taraması yapar ve sonucu /temp/scan_results.json dosyasına yazar.

Kullanım:
    from data.scripts.syn_scan import syn_scan
    syn_scan("192.168.1.20")
"""

import subprocess
import re
from service.result_manager import save_result


def syn_scan(target_ip: str) -> None:
    """
    target_ip      : Tarama yapılacak hedef IP
    """
    VULN_ID    = "PORT-001"             # vulnerabilities2.json’daki ilgili kayıt
    VULN_TITLE = "Open TCP Ports"
    SCRIPT     = "syn_scan.py"

    print(f"[+] Hedef IP: {target_ip}")
    print("[+] Nmap ile SYN taraması yapılıyor...\n")

    try:
        # Nmap SYN taraması (-sS)
        command = ["nmap", "-sS", "-p-", "--open", target_ip]
        result  = subprocess.run(command, capture_output=True, text=True, check=False)

        output = result.stdout
        print(output)  # Ham çıktıyı göster

        # 80/tcp open http benzeri satırları yakala
        open_ports = re.findall(r"(\d+)/tcp\s+open\s+(\S+)", output)

        if open_ports:
            status  = "open"
            details = ", ".join([f"{port}/{service}" for port, service in open_ports])
            print("\n[+] Açık TCP Portlar Tespit Edildi:")
            for port, service in open_ports:
                print(f"    - Port {port}/TCP ({service})")
        else:
            status  = "closed"
            details = "No open TCP ports detected."
            print("\n[-] Açık port bulunamadı veya hedef erişilemez.")

        # Sonucu JSON’a kaydet
        save_result(
            vuln_id     = VULN_ID,
            vuln_title  = VULN_TITLE,
            target_ip   = target_ip,
            status      = status,
            script_name = SCRIPT,
            details     = details
        )

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


# Bu dosya artık doğrudan çalıştırılmak için tasarlanmıyor.
# Tüm çağrılar start.py üzerinden yapılacak.

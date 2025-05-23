import subprocess
import re
import os

def run(ip):
    print(f"[+] {ip} için SSL güvenlik taraması başlatılıyor...")

    try:
        # Tarama komutu - port 443 ve çeşitli SSL script'leri
        command = [
            "nmap",
            "-p", "443",
            "--script", "ssl-cert,ssl-enum-ciphers,ssl-heartbleed",
            ip
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout
        
        # Kayıt klasörü
        os.makedirs(".results", exist_ok=True)
        output_file = f".results/ssl_scan_{ip.replace('.', '_')}.txt"

        findings = []

        # Ham çıktıyı yaz
        findings.append(">>> Nmap Çıktısı:\n")
        findings.append(output)

        # Expired sertifikalar
        expired_certs = re.findall(r"Not valid after: (.*?)\n", output)
        if expired_certs:
            findings.append("\n[!] Süresi Dolmuş Sertifikalar:")
            for cert in expired_certs:
                findings.append(f"    - Geçerlilik Bitiş: {cert}")
        else:
            findings.append("\n[+] Süresi dolmuş sertifika bulunamadı.")

        # Güvenilir olmayan sertifikalar
        if "self-signed" in output or "signed by an unknown" in output:
            findings.append("\n[!] Güvenilmeyen bir sertifika tespit edildi!")
        else:
            findings.append("\n[+] Sertifika güvenilir görünüyor.")

        # Heartbleed kontrolü
        if "VULNERABLE" in output and "Heartbleed" in output:
            findings.append("\n[!] Heartbleed açığı tespit edildi!")
        else:
            findings.append("\n[+] Heartbleed açığı tespit edilmedi.")

        # Güçsüz şifreleme kontrolü
        if "weak cipher" in output or "EXP-" in output or "NULL" in output:
            findings.append("\n[!] Zayıf şifreleme algoritmaları tespit edildi!")
        else:
            findings.append("\n[+] Şifreleme algoritmaları güvenli görünüyor.")

        # Dosyaya yaz
        with open(output_file, "w") as f:
            f.write("\n".join(findings))

        print(f"[✓] Sonuçlar kaydedildi: {output_file}")

    except Exception as e:
        print(f"[!] Hata oluştu: {e}")

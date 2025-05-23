import subprocess
import os

def scan_samba_badlock(ip):
    print(f"Nmap kullanarak {ip} adresinde Samba Badlock (CVE-2016-2118) zafiyetini tarıyor...")

    # Nmap ile Samba Badlock zafiyet taraması yapma
    command = f"nmap -p 445 --script smb-vuln-cve-2016-2118 {ip}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    output = result.stdout
    print("\nNmap Çıktısı:")
    print(output)

    findings = []
    findings.append(f">>> Samba Badlock Scan Sonuçları for {ip}:\n")
    findings.append(output)

    # Zafiyet kontrolü
    if "VULNERABLE" in output.upper() or "CVE-2016-2118" in output:
        alert = (
            "\n⚠️ Hedef sistem Samba Badlock (CVE-2016-2118) zafiyetine karşı savunmasız! ⚠️\n"
            "Bu açıklık MITM saldırılarıyla kimlik doğrulama seviyesini düşürerek hassas bilgilerin açığa çıkmasına neden olabilir.\n"
            "🔧 Çözüm: Samba'yı 4.2.11 / 4.3.8 / 4.4.2 veya daha yeni bir sürüme güncelleyin."
        )
        print(alert)
        findings.append(alert)
    else:
        ok_msg = "\n✅ Hedef sistem Samba Badlock zafiyetine karşı savunmasız görünmüyor."
        print(ok_msg)
        findings.append(ok_msg)

    # .results klasörünü oluştur (varsa)
    os.makedirs(".results", exist_ok=True)
    output_file = f".results/samba_badlock_{ip.replace('.', '_')}.txt"

    # Sonuçları dosyaya yaz
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(findings))

    print(f"\n[✓] Sonuçlar kaydedildi: {output_file}")

if __name__ == "__main__":
    target_ip = input("Hedef IP adresini girin: ")
    scan_samba_badlock(target_ip)

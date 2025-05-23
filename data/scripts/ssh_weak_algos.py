import subprocess
import os

def run(ip):
    print(f"[+] {ip} için SSH zayıf şifreleme algoritmaları taraması başlatılıyor...")

    try:
        command = [
            "nmap",
            "-p", "22",
            "--script", "ssh2-enum-algos",
            ip
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout

        os.makedirs(".results", exist_ok=True)
        output_file = f".results/ssh_weak_algos_{ip.replace('.', '_')}.txt"

        findings = []
        findings.append(">>> Nmap Çıktısı:\n")
        findings.append(output)

        weak_algos = ["arcfour", "arcfour128", "arcfour256"]
        found_weak_algos = [algo for algo in weak_algos if algo in output]

        if found_weak_algos:
            findings.append("\n[!] Zayıf SSH şifreleme algoritmaları tespit edildi:")
            findings.append(f"    - {', '.join(found_weak_algos)}")
            print(f"\n[!] Zayıf SSH algoritmaları bulundu: {', '.join(found_weak_algos)}")
        else:
            findings.append("\n[+] Zayıf SSH şifreleme algoritmaları bulunamadı.")
            print("\n[+] Zayıf SSH şifreleme algoritmaları bulunamadı.")

        with open(output_file, "w") as f:
            f.write("\n".join(findings))

        print(f"[✓] Sonuçlar kaydedildi: {output_file}")

    except Exception as e:
        print(f"[!] Hata oluştu: {e}")

if __name__ == "__main__":
    target_ip = input("Hedef IP adresini girin: ")
    run(target_ip)

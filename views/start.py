import os 
import re
import subprocess
import shutil
import time
from pathlib import Path
from PyPDF2 import PdfReader
from service.pdf_to_txt import pdf_to_text
from service.extract import extract_vulnerabilities
from data.match_scripts import match_scripts_with_vulnerabilities,run_matched_python_scripts

quick_ascii = r"""
 $$$$$$\            $$\           $$\       
$$  __$$\           \__|          $$ |      
$$ /  $$ |$$\   $$\ $$\  $$$$$$$\ $$ |  $$\ 
$$ |  $$ |$$ |  $$ |$$ |$$  _____|$$ | $$  |
$$ |  $$ |$$ |  $$ |$$ |$$ /      $$$$$$  / 
$$ $$\$$ |$$ |  $$ |$$ |$$ |      $$  _$$<  
\$$$$$$ / \$$$$$$  |$$ |\$$$$$$$\ $$ | \$$\ 
 \___$$$\  \______/ \__| \_______|\__|  \__|
     \___|                                  
                                            
                                            
"""


# Uygulamanın başlangıcında gösterilecek bilgiler
def show_intro():
    print(quick_ascii)
    print("----------------------------------------------------")
    print("Q U I C K : verification test tool")
    print("Example:")
    print("1. /path/to/your/file.pdf 2. 192.168.1.1")
    print("----------------------------------------------------")

# Kullanıcıdan dosya yolunu ve IP adresini almak
def get_user_input():
    print("\nPlease enter the following information:")
    file_path = input("Enter the full path of the PDF file: ").strip()
    ip_address = input("Enter the target IP address: ").strip()

    # Dosya yolunun geçerli olup olmadığını kontrol et
    if not os.path.isfile(file_path):
        print(f"Hata: Dosya bulunamadı: {file_path}")
        return None, None

    # IP adresinin geçerli formatta olup olmadığını kontrol et
    if not validate_ip(ip_address):
        print(f"Hata: Geçersiz IP adresi: {ip_address}")
        return None, None

    return file_path, ip_address

# IP adresi doğrulama fonksiyonu (0-255 kontrolü ile)
def validate_ip(ip):
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    if not re.match(pattern, ip):
        return False
    parts = ip.split('.')
    for part in parts:
        if int(part) < 0 or int(part) > 255:
            return False
    return True

def main():
    show_intro()  
    file_path, ip_address = get_user_input()
    
    if file_path is None or ip_address is None:
        print("Lütfen hataları giderip tekrar deneyin.")
        return

    print(f"PDF file: {file_path}")
    print(f"IP addres: {ip_address}")
    
    # PDF dosyasını TXT formatına dönüştür ve temp klasörüne kaydet
    output_path = pdf_to_text(file_path)
    json = extract_vulnerabilities(output_path)

    script_path = Path("scripts.json")
    vuln_path = Path(json)
    output_path = Path("matched_results.json")

    results = match_scripts_with_vulnerabilities(script_path, vuln_path)

    # Terminale yaz
    for res in results:
        print(f"Vulnerability '{res['vulnerability_title']}' matched with script '{res['script_name']}' (Similarity: {res['similarity_score']})")

    # JSON dosyasına kaydet
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("\n✅ Eşleştirme sonuçları 'matched_results.json' dosyasına kaydedildi.")

    target_ip = input("Lütfen hedef IP adresini girin: ")
    run_matched_python_scripts(output_path, script_path, target_ip)
    
    # Burada PDF işleme veya IP doğrulama sonrası diğer işlemler eklenebilir.

if __name__ == "__main__":
    main()

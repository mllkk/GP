import os 
import re
import subprocess
import shutil
import time
from PyPDF2 import PdfReader
from service.pdf_to_txt import pdf_to_text
from service.extract import extract_vulnerabilities

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
        print("Please fix errors and try again.")
        return

    print(f"PDF file: {file_path}")
    print(f"IP address: {ip_address}")

    # Convert PDF → TXT in temp/
    pdf_to_text(file_path)

    # Now pick up the first .txt in temp/ and run extractor
    temp_dir = "temp"
    txt_files = [f for f in os.listdir(temp_dir) if f.lower().endswith(".txt")]
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in {temp_dir}")
    input_txt = os.path.join(temp_dir, txt_files[0])

    extract_vulnerabilities(input_txt)


if __name__ == "__main__":
    main()
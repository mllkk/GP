import os
import re
import subprocess
import shutil
import time

# Renk kodları (ANSI escape codes)
mavi = '\033[94m'
mor = '\033[35m'
reset = '\033[0m'

# ASCII sanatını oluşturma
quick_ascii = """

________/\\\________/\\\________/\\\__/\\\\\\\\\\\________/\\\\\\\\\__/\\\________/\\\_        
 _____/\\\\/\\\\____\/\\\_______\/\\\_\/////\\\///______/\\\////////__\/\\\_____/\\\//__       
  ___/\\\//\////\\\__\/\\\_______\/\\\_____\/\\\_______/\\\/___________\/\\\__/\\\//_____      
   __/\\\______\//\\\_\/\\\_______\/\\\_____\/\\\______/\\\_____________\/\\\\\\//\\\_____     
    _\//\\\______/\\\__\/\\\_______\/\\\_____\/\\\_____\/\\\_____________\/\\\//_\//\\\____    
     __\///\\\\/\\\\/___\/\\\_______\/\\\_____\/\\\_____\//\\\____________\/\\\____\//\\\___   
      ____\////\\\//_____\//\\\______/\\\______\/\\\______\///\\\__________\/\\\_____\//\\\__  
       _______\///\\\\\\___\///\\\\\\\\\/____/\\\\\\\\\\\____\////\\\\\\\\\_\/\\\______\//\\\_ 
        _________\//////______\/////////_____\///////////________\/////////__\///________\///__
 
"""

# Uygulamanın başlangıcında gösterilecek bilgiler
def show_intro():
    print(f"{mavi}{quick_ascii[:24]}{reset}")  # Mavi renkli ilk kısmı
    time.sleep(0.5)
    print(f"{mor}{quick_ascii[24:]}{reset}")  # Mor renkli geri kalan kısmı
    print("----------------------------------------------------")
    print("Uygulama Adı: PDF Yükleme ve IP Doğrulama Servisi")
    print("Örnek kullanım:")
    print("1. pdf_dosyasi_yolu /path/to/your/file.pdf - ip_adresi 192.168.1.1")
    print("----------------------------------------------------")

# Kullanıcıdan dosya yolunu ve IP adresini almak
def get_user_input():
    print("\nLütfen aşağıdaki bilgileri girin:")
    file_path = input("PDF dosyasının tam yolunu girin: ")
    ip_address = input("IP adresini girin: ")

    # Dosya yolunun geçerli olup olmadığını kontrol et
    if not os.path.isfile(file_path):
        print(f"Hata: Dosya bulunamadı: {file_path}")
        return None, None

    # IP adresinin geçerli formatta olup olmadığını kontrol et
    if not validate_ip(ip_address):
        print(f"Hata: Geçersiz IP adresi: {ip_address}")
        return None, None

    return file_path, ip_address

# IP adresi doğrulama fonksiyonu
def validate_ip(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return bool(re.match(pattern, ip))

# Dosyayı temp klasörüne kaydetme
def save_to_temp(file_path):
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)  # Temp klasörünü oluştur
    temp_file_path = os.path.join(temp_dir, os.path.basename(file_path))  # Dosyanın yeni yolu
    shutil.copy(file_path, temp_file_path)  # Dosyayı temp klasörüne kopyala
    return temp_file_path


def main():
    show_intro()  # Başlangıç yazılarını göster
    file_path, ip_address = get_user_input()

    if file_path and ip_address:
        send_curl_request(file_path, ip_address)

if __name__ == "__main__":
    main()

import os
import importlib

def main():
    ip_address = input("Tarama yapmak istediğiniz IP adresini girin: ")

    scripts_dir = "scripts"
    # scripts klasöründeki tüm .py dosyalarını listele
    for filename in os.listdir(scripts_dir):
        # Sadece .py dosyalarını ve __init__.py hariç tut
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]  # '.py' kısmını çıkar
            try:
                # Dinamik olarak modülü import et
                module = importlib.import_module(f"{scripts_dir}.{module_name}")
                
                # Eğer modülde run fonksiyonu varsa çağır
                if hasattr(module, "run"):
                    print(f"\n[+] {module_name} modülü çalıştırılıyor...")
                    module.run(ip_address)
                else:
                    print(f"[!] {module_name} modülünde 'run' fonksiyonu bulunamadı!")
            
            except Exception as e:
                print(f"[!] {module_name} modülünde hata oluştu: {e}")

if __name__ == "__main__":
    main()

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from datetime import datetime

def create_remediation_report(ip_address):
    file_name = f"remediation_report_{ip_address.replace('.', '_')}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    # Sayfa boyutu
    width, height = A4

    # Arka plan rengi (lacivert)
    c.setFillColor(HexColor("#202d48"))
    c.rect(0, 0, width, height, fill=True, stroke=False)

    # Yazı rengi beyaz
    c.setFillColor(white)

    # Sol üst: QUICK
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 50, "QUICK")

    # Sağ üst: Ocak 2026
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(width - 50, height - 50, "JANUARY 2026")

    # Orta başlık
    c.setFont("Helvetica-Bold", 26)
    c.drawString(50, height - 200, "REMEDIATION")

    c.drawString(50, height - 235, "TEST REPORT")

    # IP bilgisi
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 270, ip_address)

    # PDF oluştur
    c.save()
    print(f"[+] PDF oluşturuldu: {file_name}")

if __name__ == "__main__":
    ip = input("IP adresini girin (örnek: 192.168.10.44): ")
    create_remediation_report(ip)

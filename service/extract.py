import re
import json

with open(r"C:\Users\mlkon\OneDrive\Masaüstü\proje 2\temp\metasploitable_kmyuqm.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Her zafiyet bloğunu ayır: Plugin Information ile biten bloklar
blocks = re.findall(r'(\d{5}) - (.+?)\nSynopsis\n(.*?)\nSee Also\n(.*?)\n(.*?)Plugin Information', content, re.DOTALL)

vulns = []

for block in blocks:
    vuln_id = block[0]
    title = block[1].strip()
    description = block[2].strip().replace("\n", " ")
    vulns.append({
        "id": vuln_id,
        "title": title,
        "description": description
    })

# JSON'a yaz
with open("vulnerabilities.json", "w", encoding="utf-8") as f:
    json.dump(vulns, f, indent=4, ensure_ascii=False)

print(f"✅ Toplam {len(vulns)} zafiyet JSON olarak kaydedildi.")

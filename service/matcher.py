#!/usr/bin/env python3
import json
import difflib

# 1. Dosyaları yükle
vulns   = json.load(open("temp/vulnerabilities.json", "r"))
scripts = json.load(open("scripts/scripts.json",       "r"))

def find_best_script(desc, scripts, threshold=0.4):
    best, best_score = None, 0.0
    for s in scripts:
        score = difflib.SequenceMatcher(None,
                                        desc.lower(),
                                        s["description"].lower()).ratio()
        if score > best_score:
            best_score, best = score, s
    return best if best_score >= threshold else None

# 2. Eşleştirmeleri oluştur
matches = []
for v in vulns:
    script = find_best_script(v["description"], scripts)
    if script:
        matches.append({"vuln_id": v["id"], "script": script["name"]})
    else:
        print(f"[!] Eşleşme yok: id={v['id']} desc=\"{v['description']}\"")

# 3. matches.json olarak kaydet
with open("matches.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"[+] Toplam {len(matches)} eşleşme bulundu ve matches.json’a yazıldı.")

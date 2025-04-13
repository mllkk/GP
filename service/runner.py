#!/usr/bin/env python3
import json
import subprocess

# 1. matches.json’u yükle
matches = json.load(open("matches.json", "r"))

open_vulns = []

# 2. Her eşleşmeyi çalıştır
for m in matches:
    vid = m["vuln_id"]
    script = m["script"]
    print(f"[+] Running {script} for vuln {vid}...")
    res = subprocess.run(["python", script])
    if res.returncode == 1:
        print(f"    -> OPEN (exit code 1)")
        open_vulns.append(vid)
    else:
        print(f"    -> CLOSED (exit code {res.returncode})")

# 3. Sonuçları kaydet
with open("open_vulns.json", "w") as f:
    json.dump(open_vulns, f, indent=2)

print(f"[+] {len(open_vulns)} açık zafiyet bulundu. open_vulns.json’a yazıldı.")

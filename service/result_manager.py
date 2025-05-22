import json
from datetime import datetime
from pathlib import Path

def save_result(vuln_id: str,
                vuln_title: str,
                target_ip: str,
                status: str,
                script_name: str,
                details: str = "") -> None:
    """
    Tarama sonucunu /temp/scan_results.json dosyasına ekler
    (daha önce varsa günceller).
    """
    # proje kökünün temp klasörüne giden yolu oluştur
    results_path = Path(__file__).resolve().parent.parent / "temp" / "scan_results.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)      # temp klasörü yoksa oluştur

    # Dosya varsa oku, yoksa boş liste…
    if results_path.exists():
        try:
            with open(results_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    # Mevcut kaydı güncelle / yeni kayıt ekle
    entry = {
        "vuln_id": vuln_id,
        "vuln_title": vuln_title,
        "target_ip": target_ip,
        "status": status,                  # "open" | "closed"
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "script_name": script_name,
        "details": details
    }

    updated = False
    for item in data:
        if item["vuln_id"] == vuln_id and item["target_ip"] == target_ip:
            item.update(entry)
            updated = True
            break

    if not updated:
        data.append(entry)

    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

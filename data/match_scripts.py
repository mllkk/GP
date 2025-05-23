from pathlib import Path
import json
from sentence_transformers import SentenceTransformer, util

def match_scripts_with_vulnerabilities(scripts_file, vulnerabilities_file):
    # Sentence-BERT modelini yükle
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Dosyaları oku
    with open(scripts_file, "r", encoding="utf-8") as f:
        scripts = json.load(f)

    with open(vulnerabilities_file, "r", encoding="utf-8") as f:
        vulnerabilities = json.load(f)

    # Script açıklamalarının embedding'lerini önceden al
    script_descriptions = [script.get("description", "") for script in scripts]
    script_embeddings = model.encode(script_descriptions, convert_to_tensor=True)

    matched_results = []

    for vuln in vulnerabilities:
        vuln_desc = vuln.get("description", "")
        vuln_embedding = model.encode(vuln_desc, convert_to_tensor=True)

        # Cosine benzerliğini hesapla
        cosine_scores = util.cos_sim(vuln_embedding, script_embeddings)[0]
        best_score_idx = cosine_scores.argmax().item()
        best_score = cosine_scores[best_score_idx].item()

        if best_score > 0.5:  # eşik değeri
            best_match = scripts[best_score_idx]
            matched_results.append({
                "vulnerability_id": vuln.get("id"),
                "vulnerability_title": vuln.get("title"),
                "script_id": best_match.get("id"),
                "script_name": best_match.get("name"),
                "similarity_score": round(best_score, 2)
            })
        else:
            matched_results.append({
                "vulnerability_id": vuln.get("id"),
                "vulnerability_title": vuln.get("title"),
                "script_id": None,
                "script_name": None,
                "similarity_score": round(best_score, 2)
            })

    return matched_results
import importlib.util

def run_matched_python_scripts(matched_file, scripts_file, target_ip):
    with open(matched_file, "r", encoding="utf-8") as f:
        matched_results = json.load(f)

    with open(scripts_file, "r", encoding="utf-8") as f:
        all_scripts = json.load(f)

    script_dict = {script["id"]: script for script in all_scripts}

    for match in matched_results:
        script_id = match.get("script_id")
        if script_id and script_id in script_dict:
            script_info = script_dict[script_id]
            script_path = script_info.get("filepath")

            if script_path and Path(script_path).exists():
                print(f"\n🚀 Çalıştırılıyor: {script_info['name']}")

                try:
                    # Dinamik olarak Python script dosyasını yükle
                    spec = importlib.util.spec_from_file_location("script_module", script_path)
                    script_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(script_module)

                    # Script dosyasındaki run(ip) fonksiyonunu çağır
                    if hasattr(script_module, "run"):
                        script_module.run(target_ip)
                    else:
                        print(f"⚠️ Hata: {script_path} içinde 'run' fonksiyonu bulunamadı.")
                except Exception as e:
                    print(f"❌ Script çalıştırma hatası: {e}")
            else:
                print(f"❌ Script yolu bulunamadı: {script_path}")
                
if __name__ == "__main__":
    script_path = Path("scripts.json")
    vuln_path = Path("vulnerabilities2.json")
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



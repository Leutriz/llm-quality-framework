import json
import os
import csv
import argparse
from adapters.ollama import OllamaAdapter
from engine.scoring import score_response

def load_dataset(file_path):
    """Lädt das JSON-Dataset aus dem angegebenen Pfad."""
    if not os.path.exists(file_path):
        print(f"Fehler: Datei {file_path} nicht gefunden.")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Fehler: Die Datei {file_path} enthält kein gültiges JSON.")
            return []

def main():
    # 1. Initialisierung + CLI Setup
    parser = argparse.ArgumentParser(description="LLM Quality Framework Runner")
    parser.add_argument("--model", type=str, default="llama3", help="Name des Ollama Modells")
    parser.add_argument("--dataset", type=str, default="datasets/core.json", help="Pfad zum Dataset")
    parser.add_argument("--output", type=str, default="reports/report.csv", help="Pfad für den CSV-Export")
    
    args = parser.parse_args()

    # Verzeichnisse sicherstellen
    os.makedirs("reports", exist_ok=True)

    print(f"\n--- LLM Quality Framework ---")
    print(f"Modell: {args.model} | Dataset: {args.dataset}")
    
    dataset = load_dataset(args.dataset)
    adapter = OllamaAdapter(args.model)
    
    results = []

    if not dataset:
        return
    
    # 2. Loop über alle Testfälle (Response Collection)
    print(f"\nStarte Testlauf...")
    for item in dataset:
        prompt_id = item.get("id", "unknown")
        prompt_text = item.get("prompt", "")
        keywords = item.get("expected_keywords", [])
        
        print(f"[{prompt_id}] Running...", end=" ", flush=True)
        response = adapter.send(prompt_text)
        eval_result = score_response(response, keywords)
        
        # Daten für CSV sammeln
        results.append({
            "id": prompt_id,
            "score": eval_result["final_score"],
            "matched_keywords": ", ".join(eval_result["matched_keywords"]),
            "prompt": prompt_text,
            "response": response.replace("\n", " ")
        })
        print(f"DONE (Score: {eval_result['final_score']}/100)")

        # Feedback-Details anzeigen
        if eval_result["final_score"] < 100:
            print(f"   └─ Grund für Abzug:")
            if len(eval_result["matched_keywords"]) < len(keywords):
                missing = set(keywords) - set(eval_result["matched_keywords"])
                print(f"      - Fehlende Keywords: {list(missing)}")
            if eval_result["length"] < 20:
                print(f"      - Warnung: Antwort ist extrem kurz ({eval_result['length']} Zeichen)")
        else:
            print(f"   └─ Perfekter Match! Alle Keywords gefunden.")
        print("-" * 30)

    # 3. CSV Export
    keys = results[0].keys()
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    print(f"\n✅ Report gespeichert unter: {args.output}")

if __name__ == "__main__":
    main()
import json
import os
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
    dataset_path = 'datasets/core.json'
    model_name = "llama3" # Später machen wir das über CLI-Parameter
    
    print(f"--- LLM Quality Framework ---")
    print(f"Modell: {model_name} | Dataset: {dataset_path}")
    
    # 1. Initialisierung
    dataset = load_dataset(dataset_path)
    adapter = OllamaAdapter(model_name)
    
    results = []

    if not dataset:
        print("Abbruch: Kein Dataset geladen.")
        return

    # 2. Loop über alle Testfälle (Response Collection)
    print(f"\nStarte Testlauf für {len(dataset)} Fälle...\n")
    
    for item in dataset:
        prompt_text = item.get("prompt", "")
        keywords = item.get("expected_keywords", [])
        
        print(f"Running [{item.get('id')}]...", end=" ", flush=True)
        response = adapter.send(prompt_text)
        
        # Scoring aufrufen
        evaluation = score_response(response, keywords)
        
        results.append({
            "id": item.get("id"),
            "score": evaluation["final_score"],
            "matches": evaluation["matched_keywords"],
            "response": response
        })
        print(f"DONE (Score: {evaluation['final_score']}/100)")

        # Feedback-Details anzeigen
        if evaluation["final_score"] < 100:
            print(f"   └─ Grund für Abzug:")
            if len(evaluation["matched_keywords"]) < len(keywords):
                missing = set(keywords) - set(evaluation["matched_keywords"])
                print(f"      - Fehlende Keywords: {list(missing)}")
            if evaluation["length"] < 20:
                print(f"      - Warnung: Antwort ist extrem kurz ({evaluation['length']} Zeichen)")
        else:
            print(f"   └─ Perfekter Match! Alle Keywords gefunden.")
        print("-" * 30)

    # 3. Zusammenfassung (vorläufig)
    print(f"\n--- Testlauf beendet ---")
    for res in results:
        print(f"\nID: {res['id']}")
        print(f"Antwort: {res['response'][:100]}...") # Zeige nur die ersten 100 Zeichen

if __name__ == "__main__":
    main()
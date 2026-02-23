import json
import os

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
    # Pfad zum Dataset (wird später über CLI steuerbar)
    dataset_path = 'datasets/core.json'
    
    print(f"--- LLM Quality Framework ---")
    print(f"Lade Dataset: {dataset_path}...")
    
    dataset = load_dataset(dataset_path)
    
    if dataset:
        print(f"Erfolgreich geladen: {len(dataset)} Testfälle gefunden.")
        for item in dataset:
            print(f" - [{item['id']}] Prompt: {item['prompt'][:50]}...")
    else:
        print("Dataset konnte nicht geladen werden.")

if __name__ == "__main__":
    main()
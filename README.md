# LLM Quality Framework

Model-agnostic testing framework for evaluating chatbot / LLM output quality, stability, and hallucination risk.

## Key Features

- **Dataset-driven:** Teste systematisch mit vordefinierten Testfällen.
- **Model-agnostic:** Wechsel zwischen OpenAI und lokalen Modellen (Ollama) ohne Code-Änderung.
- **Scoring Engine:** Automatische Bewertung (0-100) basierend auf Keywords und Sanity-Checks.
- **Quality Gate:** Blockiert Releases (Exit Code 1), wenn die Modell-Qualität sinkt.
- **Hallucination Detection:** Spezielles Adversarial Dataset zum Entlarven von KI-Lügen.

## Architecture

```text
Dataset (JSON) → Model Adapter (Ollama/API) → Scoring Engine → CSV Report → Quality Gate (Pass/Fail)
```

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Start local model: `ollama run llama3`
3. Run tests: `python runner.py --model llama3 --dataset datasets/core.json --output reports/test_run_1.csv`
4. Report generated in output folder

## CLI Parameters

| Parameter | Beschreibung                     | Default            |
| :-------- | :------------------------------- | :----------------- |
| model     | "Name des Modells (z.B. llama3)" | llama3             |
| dataset   | Pfad zur JSON-Testdatei          | datasets/core.json |
| output    | Zielpfad für den CSV-Report      | reports/report.csv |

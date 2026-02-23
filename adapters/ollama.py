import requests
from .base import BaseAdapter

class OllamaAdapter(BaseAdapter):
    """
    Adapter für lokale Modelle via Ollama API.
    Dokumentation: https://github.com/ollama/ollama/blob/main/docs/api.md
    """

    def __init__(self, model_name: str, host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.url = f"{host}/api/generate"

    def send(self, prompt: str) -> str:
        """
        Sendet den Prompt an die lokale Ollama Instanz.
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload, timeout=30)

            if response.status_code == 404:
                return f"Error 404: Modell '{self.model_name}' nicht gefunden. Hast du 'ollama pull {self.model_name}' ausgeführt?"

            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            return f"Error: Verbindung zu Ollama fehlgeschlagen. {e}"
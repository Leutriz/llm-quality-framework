from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    Abstrakte Basisklasse für alle Modell-Adapter.
    Garantiert, dass jeder Adapter eine 'send'-Methode besitzt.
    """

    @abstractmethod
    def send(self, prompt: str) -> str:
        """
        Sendet einen Prompt an das Modell und gibt die Antwort als String zurück.
        """
        pass
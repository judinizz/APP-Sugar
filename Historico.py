from abc import ABC, abstractmethod

class Historico(ABC):
    @abstractmethod
    def salvaAlimento(self):
        pass

    @abstractmethod
    def mostraHistorico(self):
        pass 
    
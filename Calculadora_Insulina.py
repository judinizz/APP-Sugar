from Interface_Insulina import InterfaceInsulina
from typing import Type

class Calculadora_Insulina:
    """
    Classe responsável por realizar o cálculo da dosagem de insulina e verificar alertas
    relacionados ao uso de insulina com base na dosagem calculada.
    """

    def fazCalculoDosagem(self, insulina: Type[InterfaceInsulina]) -> float:
        dosagem = insulina.calculaDosagem()
        return dosagem

    def fazVerificacaoAlarme(self, insulina: Type[InterfaceInsulina], dosagem_calculada) -> str:
        alarme = insulina.verificaAlarme(dosagem_calculada)
        return alarme



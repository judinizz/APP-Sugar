from Alimento import Alimento

class Nutrientes:
    def __init__(self):
        self.total_energia = 0
        self.total_proteina = 0
        self.total_lipideos = 0
        self.total_carboidratos = 0
        self.total_fibra = 0

    def adicionaNutrientes(self, alimento: str) -> None:
        """
        Adiciona os nutrientes de um alimento aos totais acumulados.
        """

        if alimento.nutrientes is None:
            raise ValueError("O alimento não possui dados de nutrientes.")
        
        self.total_energia += alimento.nutrientes[0]
        self.total_proteina += alimento.nutrientes[1]
        self.total_lipideos += alimento.nutrientes[2]
        self.total_carboidratos += alimento.nutrientes[3]
        self.total_fibra += alimento.nutrientes[4]

    def obter_totais(self) -> str:
        """
        Retorna os totais acumulados de cada nutriente em forma de dicionário.
        """
        return {
            "energia": self.total_energia,
            "proteina": self.total_proteina,
            "lipideos": self.total_lipideos,
            "carboidratos": self.total_carboidratos,
            "fibra": self.total_fibra,
        }
    
    def obterLista(self) -> list:
        """
        Retorna os totais acumulados de cada nutriente em forma de lista.
        """
        lista = [self.total_energia, self.total_proteina, self.total_lipideos, self.total_carboidratos, self.total_fibra]
        return lista 


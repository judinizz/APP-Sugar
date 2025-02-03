class Verificadora:
    @staticmethod
    def verificar_inteiro(valor: str, tipo: str = "float") -> bool:
        """
        Verifica se um valor pode ser convertido para um tipo específico (float ou int)
        e se é maior que zero.
        """
        try:
            if tipo == "float":
                return float(valor) > 0  # Converte para float e verifica se é maior que 0
            elif tipo == "int":
                return int(valor) > 0  # Converte para int e verifica se é maior que 0
            else:
                return False  # Tipo inválido
        except ValueError:
            return False  # Retorna False se a conversão falhar






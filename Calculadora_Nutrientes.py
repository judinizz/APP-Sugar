class Calculadora_Nutrientes:
    def __init__(self, peso: float, altura: float, idade: int, sexo: int, atividade_fisica: int, tipo_diabetes: str, nutrientes: list) -> None:
        """
        Inicializa a calculadora com os dados do usuário.
        """
        self.peso = peso
        self.altura = altura
        self.idade = idade
        self.sexo = sexo
        self.atividade_fisica = atividade_fisica
        self.tipo_diabetes = tipo_diabetes
        self.nutrientes = nutrientes

    def calcula_tmb(self) -> float:
        """
        Calcula a Taxa Metabólica Basal (TMB) usando a fórmula de Harris-Benedict,
        levando em consideração o sexo e a idade do usuário.
        """
        if self.sexo == 2:  # Masculino
            return (10 * self.peso) + (6.25 * self.altura) - (5 * self.idade) + 5
        elif self.sexo == 1:  # Feminino
            return (10 * self.peso) + (6.25 * self.altura) - (5 * self.idade) - 161
        else:
            raise ValueError("Sexo inválido.")

    def calcula_gcd(self) -> float:
        """
        Calcula o Gasto Calórico Diário (GCD) com base na TMB e no nível de atividade física.
        """
        tmb = self.calcula_tmb()
        if tmb <= 0:
            print(tmb)
            raise ValueError("TMB calculado inválido. Verifique os dados do perfil médico.")
        
        fator_atividade = {
            1: 1.05,
            2: 1.25,
            3: 1.65,
            4: 1.9,
        }.get(self.atividade_fisica, 0)
        if fator_atividade == 0:
            raise ValueError("Nível de atividade física inválido.")

        return tmb * fator_atividade

    def calcula_macros(self) -> list:
        """
        Calcula a distribuição ideal de macronutrientes (carboidratos, proteínas, lipídios e fibras)
        com base no GCD e no tipo de diabetes do usuário.
        """
        gcd = self.calcula_gcd()
        if gcd <= 0:
            raise ValueError("GCD calculado inválido. Verifique os dados de entrada.")
        
        # Percentuais de macronutrientes (ajustado para diabetes)
        if self.tipo_diabetes in ["Tipo 1", "Tipo 2", "Gestacional"]:
            carb_percent = 0.45 
            prot_percent = 0.25
            lip_percent = 0.30
        elif self.tipo_diabetes == "Pré-diabetes":
            carb_percent = 0.50  
            prot_percent = 0.20
            lip_percent = 0.30
        else:
            raise ValueError("Tipo de diabetes inválido.")
        
        # Cálculo dos macronutrientes
        carb_gramas = (gcd * carb_percent) / 4  # 1 g de carboidrato = 4 kcal
        prot_gramas = (gcd * prot_percent) / 4  # 1 g de proteína = 4 kcal
        lip_gramas = (gcd * lip_percent) / 9  # 1 g de lipídio = 9 kcal

        # Fibras (recomendação: 14 g por 1000 kcal consumidas)
        fibras_gramas = (gcd / 1000) * 14

        carboidratos = round(carb_gramas, 2)
        proteinas = round(prot_gramas, 2)
        lipideos = round(lip_gramas, 2)
        fibras = round(fibras_gramas, 2)

        return [proteinas, lipideos, carboidratos, fibras]

    def alarmeNutrientes(self) -> str:
        """
        Verifica se os macros inseridos estão dentro do limite calculado.
        """
        macros = self.calcula_macros()

        proteinas_msg = (
            f"\nQuantidade de Proteínas acima do recomendado!\nQuantidade Recomendada: {macros[0]}g\nQuantidade ingerida: {self.nutrientes[0]}g\n"
            if self.nutrientes[0] > macros[0] else "Quantidade de Proteínas dentro do recomendado!\n"
        )
        lipideos_msg = (
            f"\nQuantidade de Lipídios acima do recomendado!\nQuantidade Recomendada: {macros[1]}g\nQuantidade ingerida: {self.nutrientes[1]}g\n"
            if self.nutrientes[1] > macros[1] else "Quantidade de Lipídeos dentro do recomendado!\n"
        )
        carboidratos_msg = (
            f"\nQuantidade de Carboidratos acima do recomendado!\nQuantidade Recomendada: {macros[2]}g\nQuantidade ingerida: {self.nutrientes[2]}g\n"
            if self.nutrientes[2] > macros[2] else "Quantidade de arboidratos dentro do recomendado!\n"
        )
        fibras_msg = (
            f"\nQuantidade de Fibras acima do recomendado!\nQuantidade Recomendada: {macros[3]}g\nQuantidade ingerida: {self.nutrientes[3]}g\n"
            if self.nutrientes[3] > macros[3] else "Quantidade de fibras dentro do recomendado!"
        )
        

        return f"{proteinas_msg} {lipideos_msg} {carboidratos_msg} {fibras_msg}".strip()


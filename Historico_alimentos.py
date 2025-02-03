from supabase import create_client, Client
from Chaves_banco import SUPABASE_KEY, SUPABASE_URL
from datetime import datetime

# Inicializa o cliente Supabase para comunicação com o banco de dados
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class HistoricoAlimentos:
    """
    Classe responsável por gerenciar o histórico de alimentos consumidos pelos usuários.
    """
    
    def salvaAlimento(self, usuario: str, refeicao: str, descricao: str, nutrientes: list) -> bool: # tem q receber Alimento.descricao e Alimento.nutrientes
        """
        Salva os dados de um alimento consumido no banco de dados, associando-os a um usuário e refeição.
        """
        # Recupera os IDs correspondente
        resposta_refeicao = supabase.table('Refeicao').select('id').eq('refeicao', refeicao).execute()

        if resposta_refeicao.data and len(resposta_refeicao.data) > 0:
            id_refeicao = resposta_refeicao.data[0]['id']

        resposta_alimento = supabase.table('Alimentos').select('id').eq('descricao', descricao).execute()

        if resposta_alimento.data and len(resposta_refeicao.data) > 0:
            id_alimento = resposta_alimento.data[0]['id']

        resposta_usuario = supabase.table('Usuarios').select('id').eq('email', usuario).execute()

        if resposta_usuario.data and len(resposta_usuario.data) > 0:
            id_usuario = resposta_usuario.data[0]['id']
        
        # Define a data da refeição como a data atual
        dia_refeicao = datetime.today().strftime('%Y-%m-%d')

        # Insere os dados no banco
        response = supabase.table('Historico_Alimentos').insert({
            'dia': dia_refeicao,
            'id_refeicao': id_refeicao,
            'id_alimento': id_alimento,
            'energia' : nutrientes[0],
            'proteina': nutrientes[1],
            'lipideo': nutrientes[2],
            'carboidrato': nutrientes[3],
            'fibra': nutrientes[4],
            'id_usuario': id_usuario
        }).execute()


        if not response.data:  
            print("Nenhum dado encontrado para o alimento selecionado.")
            return False

        if 'error' in response:  
            print("Erro ao buscar dados:", response['error'])
            return False

    def mostraHistorico(self, data: str, refeicao: str, usuario: str) -> str:
        """
        Recupera e formata os dados do histórico de alimentos consumidos em uma data específica e refeição.

        Args:
            data (str): Data no formato 'YYYY-MM-DD'.
            refeicao (str): Nome da refeição.
            usuario (str): E-mail do usuário.

        Returns:
            str: Histórico formatado dos alimentos consumidos.
        """
        # Recupera os IDs correspondentes
        resposta_refeicao = supabase.table('Refeicao').select('id').eq('refeicao', refeicao).execute()

        if resposta_refeicao.data and len(resposta_refeicao.data) > 0:
            id_refeicao = resposta_refeicao.data[0]['id']


        resposta_usuario = supabase.table('Usuarios').select('id').eq('email', usuario).execute()

        if resposta_usuario.data and len(resposta_usuario.data) > 0:
            id_usuario = resposta_usuario.data[0]['id']

        # Consulta o histórico de alimentos para a data e refeição fornecidas
        response = supabase.table("Historico_Alimentos").select("dia, Refeicao(refeicao),Alimentos(descricao), proteina, carboidrato, fibra, lipideo, energia").match({"dia": data, "id_refeicao": id_refeicao, "id_usuario":id_usuario}).execute()
        dados = response.data

        # Formata os dados para exibição
        linhas_formatadas = []

        for i, item in enumerate(dados, 1):
            linhas_formatadas.append(f"Alimento {i}:")
            linhas_formatadas.append(f"  Descrição: {item['Alimentos']['descricao']}")
            linhas_formatadas.append(f"  Proteína: {item['proteina']} g")
            linhas_formatadas.append(f"  Carboidrato: {item['carboidrato']} g")
            linhas_formatadas.append(f"  Fibra: {item['fibra']} g")
            linhas_formatadas.append(f"  Lipídeo: {item['lipideo']} g")
            linhas_formatadas.append(f"  Energia: {item['energia']} kcal")
            linhas_formatadas.append("-" * 40)
        

        if not response.data:  
            print("Nenhum dado encontrado no histórico")
            return False

        if 'error' in response:  
            print("Erro ao buscar dados:", response['error'])
            return False

        return "\n".join(linhas_formatadas)




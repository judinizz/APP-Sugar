import csv
import sys
import tkinter as tk
from datetime import datetime
import re

from tkinter import messagebox, StringVar, OptionMenu, Frame, Button
from supabase import create_client, Client
from Chaves_banco import SUPABASE_URL, SUPABASE_KEY
from Alimento import Alimento
from Usuario import Usuario
from Historico_refeicao import HistoricoRefeicao
from Historico_alimentos import HistoricoAlimentos
from Perfil_Medico import PerfilMedico

from tkcalendar import DateEntry
from Nutrientes import Nutrientes
from Insulina import Asparge, Humalog, NPH, Glargina
from PIL import Image, ImageTk
from Verificadora import Verificadora
from Calculadora_Insulina import Calculadora_Insulina
from Calculadora_Nutrientes import Calculadora_Nutrientes
import os


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

caminho_imagem1 = os.path.join(os.path.dirname(__file__), "Telas", "1.png")
caminho_imagem2 = os.path.join(os.path.dirname(__file__), "Telas", "2.png")
caminho_imagem3 = os.path.join(os.path.dirname(__file__), "Telas", "3.png")
caminho_imagem4 = os.path.join(os.path.dirname(__file__), "Telas", "4.png")
caminho_imagem5 = os.path.join(os.path.dirname(__file__), "Telas", "5.png")
caminho_imagem6 = os.path.join(os.path.dirname(__file__), "Telas","6.png")
caminho_TACO = os.path.join(os.path.dirname(__file__), "TACO.csv")

def configurar_tela_inicial(frame: tk.Frame) -> None:
    """
    Configura o fundo da tela inicial com uma imagem.
    """
    imagem = Image.open(caminho_imagem1)
    imagem = imagem.resize((360, 640), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(imagem)

    canvas = tk.Canvas(frame, width=360, height=640)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg)
    canvas.image = bg
    canvas.place(relwidth=1, relheight=1)

def configurar_fundo_login(frame: tk.Frame) -> None:
    """
    Configura o fundo da tela de login com uma imagem.
    """
    imagem = Image.open(caminho_imagem3)
    imagem = imagem.resize((360, 640), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(imagem)

    canvas = tk.Canvas(frame, width=360, height=640)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg)
    canvas.image = bg
    canvas.place(relwidth=1, relheight=1)
    
def configurar_fundo_cadastro(frame: tk.Frame) -> None:
    """
    Configura o fundo da tela de cadastro com uma imagem.
    """
    imagem = Image.open(caminho_imagem2)
    imagem = imagem.resize((360, 640), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(imagem)

    canvas = tk.Canvas(frame, width=360, height=640)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg)
    canvas.image = bg
    canvas.place(relwidth=1, relheight=1)

def configurar_fundo_liso(frame: tk.Frame) -> None:
    """
    Configura um fundo liso com uma imagem.
    """
    imagem = Image.open(caminho_imagem4)
    imagem = imagem.resize((360, 640), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(imagem)

    canvas = tk.Canvas(frame, width=360, height=640)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg)
    canvas.image = bg
    canvas.place(relwidth=1, relheight=1)

def configurar_fundo_perfil_medico(frame: tk.Frame) -> None:
    """
    Configura um fundo do perfil médico com uma imagem.
    """
    imagem = Image.open(caminho_imagem6)
    imagem = imagem.resize((360, 640), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(imagem)

    canvas = tk.Canvas(frame, width=360, height=640)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg)
    canvas.image = bg
    canvas.place(relwidth=1, relheight=1)

def mudar_tela(nova_tela, root: tk.Tk, *args) -> None:
    """
    Troca a tela atual por uma nova tela.
    """
    for widget in root.winfo_children():
        widget.destroy()
    nova_tela(root, *args)

def obter_dimensoes_tela() -> tuple: 
    largura_tela = 360 
    altura_tela = 640 
    centro_x = largura_tela / 2 
    return largura_tela, altura_tela, centro_x

def Tela_Inicial(root: tk.Tk) -> None: 
    """
    Cria a tela inicial com opções de login e cadastro.
    """
    frame = tk.Frame(root) 
    frame.place(relwidth=1, relheight=1) 
    configurar_tela_inicial(frame) 
    largura_tela, altura_tela, centro_x = obter_dimensoes_tela() 
    botao1 = tk.Button(frame, text="Entrar", width=20, command=lambda: mudar_tela(Tela_Login, root)) 
    botao2 = tk.Button(frame, text="Cadastrar", width=20, command=lambda: mudar_tela(Tela_Cadastro, root)) 
    botao1.place(x=centro_x, y=6.5 * (altura_tela / 12), anchor="center") 
    botao2.place(x=centro_x, y=7.5 * (altura_tela / 12), anchor="center")

def Tela_Login(root: tk.Tk) -> None:
    """
    Cria a tela de login com campos para inserir usuário e senha.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    configurar_fundo_login(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    tk.Label(frame, text="Usuário:").place(x=centro_x, y=250, anchor="center")
    entry_usuario = tk.Entry(frame)
    entry_usuario.place(x=centro_x, y=280, anchor="center")

    tk.Label(frame, text="Senha:").place(x=centro_x, y=320, anchor="center")
    entry_senha = tk.Entry(frame, show="*")
    entry_senha.place(x=centro_x, y=350, anchor="center")

    error_label = tk.Label(frame, text="", fg="red")
    error_label.place(x=centro_x, y=420, anchor="center")


    def autenticar() -> None:
        """
        Autentica o usuário com base no email e senha inseridos.
        """
        email = entry_usuario.get()
        senha = entry_senha.get()
        usuario = Usuario(email)

        if usuario.autenticacao_usuario(senha):
            error_label.config(text="Login realizado com sucesso!", fg="green")
            root.after(200, lambda: mudar_tela(Tela_Consumo1, root, email))
        else:
            error_label.config(text="Usuário ou senha inválidos.", fg="red")

    tk.Button(frame, text="Login", width=20, command=autenticar).place(x=centro_x, y=490, anchor="center")
    tk.Button(frame, text="Voltar", width=20, command=lambda: mudar_tela(Tela_Inicial, root)).place(x=centro_x, y=540, anchor="center")



def Tela_Cadastro(root: tk.Tk) -> None:
    """
    Cria a tela de cadastro com campos para inserir email e senha.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    configurar_fundo_cadastro(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    tk.Label(frame, text="Email:").place(x=centro_x, y=200, anchor="center")
    entry_email = tk.Entry(frame)
    entry_email.place(x=centro_x, y=230, anchor="center")

    tk.Label(frame, text="Senha:").place(x=centro_x, y=260, anchor="center")
    entry_senha = tk.Entry(frame, show="*")
    entry_senha.place(x=centro_x, y=290, anchor="center")

    tk.Label(frame, text="Confirmar Senha:").place(x=centro_x, y=310, anchor="center")
    entry_conf_senha = tk.Entry(frame, show="*")
    entry_conf_senha.place(x=centro_x, y=340, anchor="center")

    error_label = tk.Label(frame, text="", fg="red")
    error_label.place(x=centro_x, y=390, anchor="center")

    def cadastrar() -> None:
        """
        Valida os dados de entrada e cadastra o usuário se as condições forem atendidas.
        """
        email = entry_email.get()
        senha = entry_senha.get()
        conf_senha = entry_conf_senha.get()

        # Validações de senha
        if len(senha) < 5:
            error_label.config(text="A senha deve ter no mínimo 7 caracteres", fg="red")
            return

        if not re.search(r'[a-zA-Z]', senha):
            error_label.config(text="A senha deve conter pelo menos uma letra.", fg="red")
            return

        if re.search(r'(\d)\1{2,}', senha):
            error_label.config(text="A senha não pode conter números repetidos em sequência.", fg="red")
            return
        
        if not senha or not conf_senha:
            error_label.config(text="Insira a senha", fg="red")
            return
        
        if senha != conf_senha:
            error_label.config(text="As senhas não coincidem.", fg="red")
            return
        
        # Validação de email
        if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
            error_label.config(text="Formato de e-mail inválido.", fg="red")
            return

        usuario = Usuario(email)
        response = usuario.insere_usuario(senha)
        print(response)

        if response is True:
            error_label.config(text="Usuário cadastrado com sucesso!", fg="green")
            root.after(2000, lambda: mudar_tela(Tela_PerfilMedico_Insulina, root, email))
        else:
            error_label.config(text="Email já cadastrado!", fg="red")

    tk.Button(frame, text="Avançar", width=20, command=cadastrar).place(x=centro_x, y=440, anchor="center")
    tk.Button(frame, text="Voltar", width=20, command=lambda: mudar_tela(Tela_Inicial, root)).place(x=centro_x, y=480, anchor="center")


def Tela_PerfilMedico_Insulina(root: tk.Tk, email:str) -> None: 
    """
    Cria a tela para verificar se o usuário toma insulina e determinar quais telas de Perfil Médico irão aparecer.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    configurar_fundo_perfil_medico(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    tk.Label(frame, text="Toma Insulina (Sim/Não):").place(x=centro_x, y=190, anchor="center")
    insulina_var = tk.StringVar()
    tk.OptionMenu(frame, insulina_var, "Sim", "Não").place(x=centro_x, y=220, anchor="center")

    error_label = tk.Label(frame, text="", fg="red")
    error_label.place(x=centro_x, y=360, anchor="center")

    def avancar():
        toma_insulina = insulina_var.get()

        if not toma_insulina:
            error_label.config(text="Selecione se toma insulina!", fg="red")
            return

        if toma_insulina == "Sim":
            mudar_tela(Tela_PerfilMedico2, root, email, toma_insulina)
        else:
            mudar_tela(Tela_PerfilMedico1, root, email, None, None, toma_insulina)

    tk.Button(frame, text="Avançar", width=20, command=avancar).place(x=centro_x, y=300, anchor="center")
    tk.Button(frame, text="Voltar", width=20, command=lambda: mudar_tela(Tela_Cadastro, root)).place(x=centro_x, y=350, anchor="center")

def Tela_PerfilMedico2(root, email, toma_insulina):
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    configurar_fundo_perfil_medico(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    tk.Label(frame, text="Tipo de Insulina:").place(x=centro_x, y=160, anchor="center")
    tipo_insulina_var = tk.StringVar()
    tk.OptionMenu(frame, tipo_insulina_var, "Asparge", "Humalog", "NPH", "Glargina").place(x=centro_x, y=190, anchor="center")

    tk.Label(frame, text="Dosagem Máxima de Insulina (unidades):").place(x=centro_x, y=230, anchor="center")
    entry_dosagem_max = tk.Entry(frame)
    entry_dosagem_max.place(x=centro_x, y=260, anchor="center")

    error_label = tk.Label(frame, text="", fg="red")
    error_label.place(x=centro_x, y=510, anchor="center")

    def avancar() -> None:
        """
        Valida os dados de entrada e avança para a segunda tela do perfil médico se as condições forem atendidas.
        """
        tipo_insulina = tipo_insulina_var.get()
        dosagem_max = entry_dosagem_max.get()

        if not tipo_insulina:
            error_label.config(text="Tipo de Insulina não selecionado!", fg="red")
            return
        if not Verificadora.verificar_inteiro(dosagem_max, tipo="float"):
            error_label.config(text="Dosagem inválida!", fg="red")
            return

        mudar_tela(Tela_PerfilMedico1, root, email, tipo_insulina, dosagem_max, toma_insulina)

    tk.Button(frame, text="Avançar", width=20, command=avancar).place(x=centro_x, y=350, anchor="center")
    tk.Button(frame, text="Voltar", width=20, command=lambda: mudar_tela(Tela_PerfilMedico_Insulina, root, email)).place(x=centro_x, y=400, anchor="center")

def Tela_PerfilMedico1(root, email:str, tipo_insulina:str, dosagem_max:int, toma_insulina:str) -> None:
    """
    Cria a primeira ou segunda tela do perfil médico (dependendo de toma_insulina) com campos para inserir sexo, altura, peso, idade, atividade física e tipo de diabetes.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    configurar_fundo_perfil_medico(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    tk.Label(frame, text=f"Email: {email}", font=("Helvetica", 12), bg="#FFFFFF").place(x=centro_x, y=25, anchor="center")

    tk.Label(frame, text="Sexo:").place(x=centro_x, y=70, anchor="center")
    sexo_var = tk.StringVar()
    tk.OptionMenu(frame, sexo_var, "Masculino", "Feminino").place(x=centro_x, y=100, anchor="center")

    tk.Label(frame, text="Altura (cm):").place(x=centro_x, y=130, anchor="center")
    entry_altura = tk.Entry(frame)
    entry_altura.place(x=centro_x, y=160, anchor="center")

    tk.Label(frame, text="Peso (kg):").place(x=centro_x, y=190, anchor="center")
    entry_peso = tk.Entry(frame)
    entry_peso.place(x=centro_x, y=220, anchor="center")

    tk.Label(frame, text="Idade:").place(x=centro_x, y=250, anchor="center")
    entry_idade = tk.Entry(frame)
    entry_idade.place(x=centro_x, y=280, anchor="center")

    tk.Label(frame, text="Atividade Física:").place(x=centro_x, y=310, anchor="center")
    atividade_var = tk.StringVar()
    tk.OptionMenu(frame, atividade_var, "Sedentário", "Leve", "Moderado", "Intenso").place(x=centro_x, y=340, anchor="center")

    tk.Label(frame, text="Tipo de Diabetes:").place(x=centro_x, y=380, anchor="center")
    diabetes_var = tk.StringVar()
    tk.OptionMenu(frame, diabetes_var, "Tipo 1", "Tipo 2", "Pré-diabetes", "Gestacional").place(x=centro_x, y=410, anchor="center")

    error_label = tk.Label(frame, text="", fg="red")
    error_label.place(x=centro_x, y=460, anchor="center")

    def salvar() -> None:
        """
        Valida os dados de entrada e salva o perfil médico se as condições forem atendidas.
        """
        sexo = sexo_var.get()
        altura = entry_altura.get()
        peso = entry_peso.get()
        idade = entry_idade.get()
        atividade = atividade_var.get()
        tipo_diabetes = diabetes_var.get()

        if not sexo:
            error_label.config(text="Sexo não selecionado!")
            return
        if not Verificadora.verificar_inteiro(altura, tipo="float"):
            error_label.config(text="Altura inválida!")
            return
        if not Verificadora.verificar_inteiro(peso, tipo="float"):
            error_label.config(text="Peso inválido!")
            return
        if not Verificadora.verificar_inteiro(idade, tipo="int"):
            error_label.config(text="Idade inválida!")
            return
        if not atividade:
            error_label.config(text="Atividade Física não selecionada!")
            return
        if not tipo_diabetes:
            error_label.config(text="Tipo de diabetes não selecionado!", fg="red")
            return

        perfil_medico = PerfilMedico(email, sexo, altura, peso, idade, atividade, toma_insulina, tipo_diabetes, tipo_insulina, dosagem_max)

        if perfil_medico.cria_perfil_medico():
            error_label.config(text="Perfil médico cadastrado com sucesso!", fg="green")
            root.after(2000, lambda: mudar_tela(Tela_Alerta, root, email))
        else:
            error_label.config(text="Reveja as informações inseridas!", fg="red")

    tk.Button(frame, text="Salvar", width=20, command=salvar).place(x=centro_x, y=500, anchor="center")
    tk.Button(frame, text="Voltar", width=20, command=lambda: mudar_tela(Tela_Alerta, root)).place(x=centro_x, y=550, anchor="center")

def Tela_Alerta(root: tk.Tk, email: str) -> None:
    """
    Cria a tela de alerta final após o cadastro do perfil médico.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    # Configura o fundo da tela de alerta com uma imagem
    imagem = Image.open(caminho_imagem5)
    imagem = imagem.resize((360, 640), Image.Resampling.LANCZOS)
    bg = ImageTk.PhotoImage(imagem)

    canvas = tk.Canvas(frame, width=360, height=640)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg)
    canvas.image = bg
    canvas.place(relwidth=1, relheight=1)
    
    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    def avancar() -> None:
        """
        Avança para a tela de consumo após o alerta.
        """
        mudar_tela(Tela_Consumo1, root, email)
    
    tk.Button(frame, text="Avançar", width=10, command=avancar).place(x=300, y=15, anchor="center")


def Tela_Consumo1(root: tk.Tk, email: str) -> None:
    """
    Cria a tela de consumo inicial com opções para adicionar alimento, histórico de nutrientes, dosagem de insulina e sair.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    # Configura o fundo liso da tela
    configurar_fundo_liso(frame)
    
    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    # Boas-vindas ao usuário
    tk.Label(frame, text=f"Bem-vindo(a), {email}", font=("Helvetica", 14), bg="#0493b3").place(x=centro_x, y=50, anchor="center")
    
    # Botão para adicionar alimento
    tk.Button(frame, text="Adicionar Alimento", width=25, command=lambda: mudar_tela(Tela_CadastroRefeicao, root, email)).place(x=centro_x, y=250, anchor="center")
    
    # Botão para visualizar o histórico de alimentos
    tk.Button(frame, text="Histórico Alimentos", width=25, command=lambda: mudar_tela(Tela_Historico_Nutrientes, root, email)).place(x=centro_x, y=320, anchor="center")
    
    # Botão para visualizar a dosagem de insulina/macros das refeições
    tk.Button(frame, text="Dosagem Insulina/Macros", width=25, command=lambda: mudar_tela(Tela_Historico_Insulina, root, email)).place(x=centro_x, y=390, anchor="center")
    
    # Botão para sair do sistema
    tk.Button(frame, text="Sair", width=25, command=sys.exit).place(x=centro_x, y=460, anchor="center")


def Tela_CadastroRefeicao(root: tk.Tk, email: str) -> None:
    """
    Cria a tela de cadastro de refeição com opções para selecionar o tipo de refeição.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    # Configura o fundo liso da tela
    configurar_fundo_liso(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    # Campo de seleção de refeição
    tk.Label(frame, text="Selecione a refeição:").place(x=centro_x, y=250, anchor="center")
    refeicao_var = tk.StringVar(value="Café da manhã")
    tk.OptionMenu(frame, refeicao_var, "Café da manhã", "Almoço", "Jantar", "Lanche").place(x=centro_x, y=280, anchor="center")

    def avancar() -> None:
        """
        Avança para a tela de cadastro de alimentos após selecionar a refeição.
        """
        refeicao = refeicao_var.get()
        mudar_tela(Tela_CadastroAlimento, root, email, refeicao)
    # Botão para avançar para a próxima tela
    tk.Button(frame, text="Avançar", width=20, command=avancar).place(x=centro_x, y=420, anchor="center")
    
    # Botão para voltar para a tela de consumo inicial
    tk.Button(frame, text="Voltar", width=20, command=lambda: mudar_tela(Tela_Consumo1, root, email)).place(x=centro_x, y=470, anchor="center")

###########################################################################################

historico_alimentos = HistoricoAlimentos()

def Tela_CadastroAlimento(root: tk.Tk, email: str, refeicao:str) -> None:
    """
    Tela para adicionar alimentos e salvar a refeição com cálculo de insulina usando polimorfismo.
    """
    historico_refeicao = HistoricoRefeicao()
    alimentos_adicionados = []
    nutrientes = Nutrientes()
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    configurar_fundo_liso(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    tk.Label(frame, text=f"Refeição selecionada: {refeicao}", font=("Helvetica", 14), bg="#0493b3").place(x=centro_x, y=50, anchor="center")
    tk.Label(frame, text="Selecione o alimento:").place(x=centro_x, y=140, anchor="center")

    # Lê o arquivo CSV e extrai os alimentos
    def ler_csv(caminho_csv) -> None:
        try:
            with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
                leitor = csv.DictReader(csvfile, delimiter=';')
                return [linha['descricao'] for linha in leitor]
        except (FileNotFoundError, KeyError):
            return ["Erro ao carregar alimentos"]

    lista_alimentos = ler_csv(caminho_TACO)

    # Configuração do campo de seleção de alimentos
    alimento_var = tk.StringVar(value="Selecione um alimento")
    option_menu = tk.OptionMenu(frame, alimento_var, *lista_alimentos)
    option_menu.place(x=centro_x, y=170, anchor="center")

    tk.Label(frame, text="Buscar alimento:").place(x=centro_x, y=210, anchor="center")
    entry_busca = tk.Entry(frame)
    entry_busca.place(x=centro_x, y=240, anchor="center")

    def buscar_alimentos(event=None) -> None:
        termo_busca = entry_busca.get().lower()
        resultado = [alimento for alimento in lista_alimentos if termo_busca in alimento.lower()]
        menu = option_menu["menu"]
        menu.delete(0, "end")
        for alimento in resultado or ["Alimento não encontrado"]:
            menu.add_command(label=alimento, command=lambda value=alimento: alimento_var.set(value))

    entry_busca.bind("<KeyRelease>", buscar_alimentos)

    tk.Label(frame, text="Informe a quantidade (gramas):").place(x=centro_x, y=270, anchor="center")
    entry_quantidade = tk.Entry(frame)
    entry_quantidade.place(x=centro_x, y=300, anchor="center")

    error_label = tk.Label(frame, text="", fg="red")
    error_label.place(x=centro_x, y=370, anchor="center")

    def adicionar_alimento() -> None:
        try:
            descricao_alimento = alimento_var.get()
            quantidade_valida = entry_quantidade.get()

            if not descricao_alimento or descricao_alimento == "Selecione um alimento":
                error_label.config(text="Por favor, selecione um alimento válido.", fg="red")
                return

            if not Verificadora.verificar_inteiro(quantidade_valida, tipo="float"):
                error_label.config(text="Insira um valor válido para a quantidade!", fg="red")
                return
            
            resposta_usuario = supabase.table('Usuarios').select('id').eq('email', email).execute()
            if not resposta_usuario.data:
                error_label.config(text="Usuário não encontrado.", fg="red")
                return
            
            
            quantidade = float(quantidade_valida)
            alimento = Alimento()
            alimento.adicionaAlimento(quantidade, descricao_alimento)
            historico_alimentos.salvaAlimento(email, refeicao, alimento.descricao, alimento.nutrientes)
            

            # Adiciona o alimento à lista de alimentos adicionados
            alimentos_adicionados.append(alimento)

            # Adiciona os nutrientes do alimento aos nutrientes totais
            nutrientes.adicionaNutrientes(alimento)


            error_label.config(text="Alimento adicionado com sucesso!", fg="green")
            alimento_var.set("Selecione um alimento")
            entry_quantidade.delete(0, tk.END)

        except Exception as e:
            print(f"Erro inesperado ao adicionar alimento: {e}")
            error_label.config(text="Erro inesperado ao adicionar alimento.", fg="red")


    def salvar_refeicao() -> None:
        try:
            if not alimentos_adicionados:
                error_label.config(text="Nenhum alimento foi adicionado à refeição.", fg="red")
                return

            # Calcula os nutrientes totais
            nutrientes_totais = nutrientes.obterLista()

            # Recupera o id_usuario a partir do email
            resposta_usuario = supabase.table('Usuarios').select('id').eq('email', email).execute()

            if not resposta_usuario.data:
                error_label.config(text="Usuário não encontrado.", fg="red")
                return
            
            id_usuario = resposta_usuario.data[0]['id']
            
            # Recupera o perfil médico do usuário
            resposta_perfil_medico = supabase.table('Perfil_medico').select('*').eq('id_usuario', id_usuario).execute()
            
            if not resposta_perfil_medico.data:
                error_label.config(text="Perfil médico não encontrado", fg="red")
                return
            
            # Garante que estamos lidando com um único registro do perfil médico
            perfil_medico = resposta_perfil_medico.data[0] if isinstance(resposta_perfil_medico.data, list) and resposta_perfil_medico.data else None
            
            if not perfil_medico:
                error_label.config(text="Dados do perfil médico inválidos", fg="red")
                return
            

            peso = perfil_medico.get('peso')
            idade = perfil_medico.get('idade')
            altura = perfil_medico.get('altura')
            id_sexo = perfil_medico.get('id_sexo')
            id_atividade = perfil_medico.get('id_atividade')
            toma_insulina = perfil_medico.get('toma_insulina')

            #verifica se o usuário toma insulina para fazer o cálculo
            if toma_insulina == True:
                id_tipo_insulina = perfil_medico.get('id_tipo_insulina')
                id_tipo_diabetes = perfil_medico.get('id_tipo_diabetes')
                dosagem_max = perfil_medico.get('dosagem_max')

                resposta_tipo_insulina = supabase.table('Tipos_insulina').select('tipo').eq('id', id_tipo_insulina).execute()

                if resposta_tipo_insulina.data and len(resposta_tipo_insulina.data) > 0:
                    tipo_insulina = resposta_tipo_insulina.data[0]['tipo']

                resposta_tipo_diabetes = supabase.table('Tipos_diabetes').select('tipo').eq('id', id_tipo_diabetes).execute()

                if resposta_tipo_diabetes.data and len(resposta_tipo_diabetes.data) > 0:
                    tipo_diabetes = resposta_tipo_diabetes.data[0]['tipo']

                # Verifica se todos os dados necessários estão presentes
                if not all([tipo_diabetes, peso, dosagem_max]):
                    error_label.config(text="Dados do perfil médico incompletos", fg="red")
                    return

                # Define a insulina como "Humalog" sempre
                if tipo_insulina == "Humalog":
                    insulina = Humalog(peso, tipo_diabetes, nutrientes.total_carboidratos, nutrientes.total_proteina, dosagem_max)
                elif tipo_insulina == "Asparge":
                    insulina = Asparge(peso, tipo_diabetes, nutrientes.total_carboidratos, nutrientes.total_proteina, dosagem_max)
                elif tipo_insulina == "NPH":
                    insulina = NPH(peso, tipo_diabetes, nutrientes.total_carboidratos, nutrientes.total_proteina, dosagem_max)
                elif tipo_insulina == "Glargina":
                    insulina = Glargina(peso, tipo_diabetes, nutrientes.total_carboidratos, nutrientes.total_proteina, dosagem_max)

                # Salva a refeição no banco de dados

                calculadora_insulina = Calculadora_Insulina()
                insulina_calculada = calculadora_insulina.fazCalculoDosagem(insulina)
                sucesso = historico_refeicao.salvaRefeicao(email, refeicao, nutrientes_totais, insulina_calculada)
                alarme = calculadora_insulina.fazVerificacaoAlarme(insulina, insulina_calculada)
                if sucesso:
                    error_label.config(text=f"A refeição foi salva com sucesso!\nA dosagem de insulina calculada é de: {insulina_calculada} UI", fg="green")
                    messagebox.showinfo("Verificação de Dose", alarme)     
                else:
                    error_label.config(text="Erro ao salvar a refeição. Verifique os dados.", fg="GREEN")
            
            elif toma_insulina == False: 
                id_tipo_diabetes = perfil_medico.get('id_tipo_diabetes')

                resposta_tipo_diabetes = supabase.table('Tipos_diabetes').select('tipo').eq('id', id_tipo_diabetes).execute()
                if resposta_tipo_diabetes.data and len(resposta_tipo_diabetes.data) > 0:
                    tipo_diabetes = resposta_tipo_diabetes.data[0]['tipo']

                calculadora_nutrientes = Calculadora_Nutrientes(peso, altura, idade, id_sexo, id_atividade, tipo_diabetes, nutrientes_totais)
                print(calculadora_nutrientes.sexo, calculadora_nutrientes.peso, calculadora_nutrientes.altura, calculadora_nutrientes.idade)
                alarme = calculadora_nutrientes.alarmeNutrientes()
                sucesso = historico_refeicao.salvaRefeicao(email, refeicao, nutrientes_totais)

                if sucesso:
                    error_label.config(text=f"A refeição foi salva com sucesso!", fg="green")
                    messagebox.showinfo("Verificação de Dose", alarme)     
                else:
                    error_label.config(text="Erro ao salvar a refeição. Verifique os dados.", fg="GREEN")
            
        except Exception as e:
            print(f"Erro ao salvar a refeição: {e}")
            error_label.config(text="Erro ao salvar a refeição.", fg="red")

    def voltar() -> None:
        """
        Volta para a tela de cadastro de refeição
        """
        mudar_tela(Tela_CadastroRefeicao, root, email)

    def avançar():
        mudar_tela(Tela_Consumo1, root, email)

    # Botões de ação
    tk.Button(frame, text="Adicionar Alimento", width=20, command=adicionar_alimento).place(x=centro_x, y=480, anchor="center")
    tk.Button(frame, text="Salvar Refeição", width=20, command=salvar_refeicao).place(x=centro_x, y=520, anchor="center")
    tk.Button(frame, text="Voltar", width=20, command=voltar).place(x=centro_x, y=560, anchor="center")
    tk.Button(frame, text="Finalizar", width=20, command=avançar).place(x=centro_x, y=600, anchor="center")


#########################################################################################

def Tela_Historico_Insulina(root: tk.Tk, email_usuario: str) -> None:
    """
    Cria a tela de histórico de insulina com opções para selecionar a data e a refeição.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)
    configurar_fundo_liso(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    # Título da tela
    tk.Label(frame, text="Histórico de Insulina/Macros",font=("Helvetica", 12), bg="#0493b3").place(x=centro_x, y=50, anchor="center")
    tk.Label(frame, text="Selecione a data:").place(x=centro_x, y=100, anchor="center")

    # Entrada de data
    data_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    data_entry.place(x=centro_x, y=140, anchor="center")

    # Campo de seleção de refeição
    tk.Label(frame, text="Selecione a refeição:").place(x=centro_x, y=180, anchor="center")
    refeicao_var = tk.StringVar(value="Selecione uma refeição")
    refeicoes_disponiveis = ["Café da manhã", "Almoço", "Jantar", "Lanche"]
    tk.OptionMenu(frame, refeicao_var, *refeicoes_disponiveis).place(x=centro_x, y=220, anchor="center")

    # Canvas com barra de rolagem
    canvas_frame = tk.Frame(frame)
    canvas_frame.place(x=0, y=260, width=largura_tela, height=250)
    
    canvas = tk.Canvas(canvas_frame)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Label para mensagens de erro
    error_label = tk.Label(frame, text="", fg="red")
    error_label.place(x=centro_x, y=430, anchor="center")
    
    def limpar_frame() -> None:
        """
        Limpa todos os widgets do frame rolável.
        """
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        error_label.config(text="")

    def exibir_historico() -> None:
        """
        Exibe o histórico de insulina e nutrientes para a data e refeição selecionadas.
        """
        limpar_frame()
        data_selecionada = data_entry.get_date().strftime('%Y-%m-%d')
        refeicao_selecionada = refeicao_var.get()

        data_obj = datetime.strptime(data_selecionada, "%Y-%m-%d")
        data_formatada = data_obj.strftime("%d/%m/%Y")

        # Validação das entradas
        if refeicao_selecionada == "Selecione uma refeição":
            error_label.config(text="Por favor, selecione uma refeição.", fg="red")
            return

        # Calcula e exibe o histórico de insulina
        try:
            # Instância das classes necessárias
            historico = HistoricoRefeicao()

            resposta_usuario = supabase.table('Usuarios').select('id').eq('email', email_usuario).execute()

            if resposta_usuario.data and len(resposta_usuario.data) > 0:
                id_usuario = resposta_usuario.data[0]['id']

            resposta_perfilmedico = supabase.table('Perfil_medico').select('toma_insulina').eq('id_usuario', id_usuario).execute()

            if resposta_perfilmedico.data and len(resposta_perfilmedico.data) > 0:
                toma_insulina = resposta_perfilmedico.data[0]['toma_insulina']
            
            # Obtém os dados do banco
            resultado_historico = historico.mostraHistorico(data=data_selecionada, refeicao=refeicao_selecionada, usuario=email_usuario, toma_insulina= toma_insulina)
            
            if not resultado_historico:
                tk.Label(scrollable_frame, text="Nenhum dado encontrado para a data e refeição selecionadas.", font=("Helvetica", 8)).pack(pady=5)
                return

            tk.Label(scrollable_frame, text=f"Histórico de Insulina e/ou\n Nutrientes em {data_formatada}:", font=("Helvetica", 8)).pack(pady=5)
            
            for linha in resultado_historico.splitlines():
                tk.Label(scrollable_frame, text=linha.strip(), anchor="w", justify="left").pack(fill="x", pady=2)

        except Exception as e:
            print(f"Erro ao exibir histórico: {e}")
            tk.Label(scrollable_frame, text="Erro ao carregar o histórico. Verifique os dados.", fg="red").pack(pady=5)

    def voltar() -> None:
        """
        Retorna para a tela de consumo inicial.
        """
        mudar_tela(Tela_Consumo1, root, email_usuario)

    # Botões
    tk.Button(frame, text="Exibir Histórico", width=20, command=exibir_historico).place(x=centro_x, y=540, anchor="center")
    tk.Button(frame, text="Limpar", width=20, command=limpar_frame).place(x=centro_x, y=580, anchor="center")
    tk.Button(frame, text="Voltar", width=20, command=voltar).place(x=centro_x, y=620, anchor="center")

def Tela_Historico_Nutrientes(root: tk.Tk, email_usuario: str) -> None:
    """
    Cria a tela de histórico de nutrientes com opções para selecionar a data e a refeição.
    """
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)
    configurar_fundo_liso(frame)

    largura_tela, altura_tela, centro_x = obter_dimensoes_tela()

    # Título da tela
    tk.Label(frame, text="Histórico de Alimentos", font=("Helvetica", 10), bg="#0493b3").place(x=centro_x, y=50, anchor="center")

    # Entrada de data
    tk.Label(frame, text="Selecione a data:").place(x=centro_x, y=125, anchor="center")
    data_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    data_entry.place(x=centro_x, y=155, anchor="center")

    # Campo de seleção de refeição
    tk.Label(frame, text="Selecione a refeição:").place(x=centro_x, y=195, anchor="center")
    refeicao_var = tk.StringVar(value="Selecione uma refeição")
    refeicoes_disponiveis = ["Café da manhã", "Almoço", "Jantar", "Lanche"]
    tk.OptionMenu(frame, refeicao_var, *refeicoes_disponiveis).place(x=centro_x, y=225, anchor="center")

    # Label para mensagens de erro
    error_label = tk.Label(frame, text="", fg="red")
    error_label.place(x=centro_x, y=260, anchor="center")

    # Canvas com barra de rolagem
    canvas_frame = tk.Frame(frame)
    canvas_frame.place(x=0, y=270, width=largura_tela, height=250)

    canvas = tk.Canvas(canvas_frame)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Vincular o evento de rolagem com a roda do mouse
    def _on_mouse_wheel(event) -> None:
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

    def limpar_frame() -> None:
        """
        Limpa todos os widgets do frame rolável.
        """
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        error_label.config(text="")

    def exibir_historico() -> None:
        """
        Exibe o histórico de alimentos e nutrientes para a data e refeição selecionadas.
        """
        limpar_frame()
        data_selecionada = data_entry.get_date().strftime('%Y-%m-%d')
        refeicao_selecionada = refeicao_var.get()

        # Validação das entradas
        if refeicao_selecionada == "Selecione uma refeição":
            error_label.config(text="Por favor, selecione uma refeição.", fg="red")
            return

        # Obtém o histórico de alimentos do banco
        historico = historico_alimentos.mostraHistorico(
            data=data_selecionada,
            refeicao=refeicao_selecionada,
            usuario=email_usuario
        )

        data_obj = datetime.strptime(data_selecionada, "%Y-%m-%d")

        data_formatada = data_obj.strftime("%d/%m/%Y")

        if not historico:
            tk.Label(scrollable_frame, text="Nenhum dado encontrado para a data selecionada.", font=("Helvetica", 8)).pack(pady=5)
        else:
            tk.Label(scrollable_frame, text=f"Histórico de Alimentos em {data_formatada}:", font=("Helvetica", 8)).pack(pady=5)
            tk.Label(scrollable_frame, text=f"{historico}", anchor="w", justify="left", font=("Helvetica", 8)).pack(fill="x", pady=2)
                
    def voltar() -> None:
        """
        Retorna para a tela de consumo inicial.
        """
        mudar_tela(Tela_Consumo1, root, email_usuario)

    tk.Button(frame, text="Exibir Histórico", width=20, command=exibir_historico).place(x=centro_x, y=540, anchor="center")
    tk.Button(frame, text="Limpar", width=20, command=limpar_frame).place(x=centro_x, y=580, anchor="center")
    tk.Button(frame, text="Voltar", width=20, command=voltar).place(x=centro_x, y=620, anchor="center")

###############################################################################

root = tk.Tk()
root.title("Contagem de Carboidratos")
root.geometry("360x640")
mudar_tela(Tela_Inicial, root)
root.mainloop()
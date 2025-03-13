import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import json

# Variáveis globais
arquivo_usuarios = 'usuarios.json'
dados_usuarios = {}
janela = None
fonte_padrao = None
fonte_titulo = None
"""Quando as variáveis são definidas no início do código (ou seja, como variáveis globais), isso garante que elas
possam ser acessadas e modificadas por diversas funções ao longo do programa sem a necessidade de passá-las como
parâmetros ou criar uma estrutura de objeto para gerenciá-las."""


def iniciar_janela():
    global janela, fonte_padrao, fonte_titulo
    # Cria a janela de login
    janela = ctk.CTk()
    # Define o título da janela
    janela.title("Gerenciamento de Estoque")

    # Obtém o tamanho da tela do monitor
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Define o tamanho da janela
    largura_janela = 600  # Largura da janela
    altura_janela = 600  # Altura da janela

    # Calcula a posição para centralizar a janela
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2

    # Posiciona a janela no centro da tela
    janela.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')

    # Define a paleta de cores da janela
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Define as fontes que vão ser usadas
    fonte_padrao = ctk.CTkFont("Arial", 14)
    fonte_titulo = ctk.CTkFont("Arial", 24, "bold")


def carregar_dados():
    # Função para carregar dados do arquivo
    global dados_usuarios, arquivo_usuarios
    if os.path.exists(arquivo_usuarios):
        # Verifica se o arquivo já existe
        with open(arquivo_usuarios, 'r') as arquivo:
            """Se o arquivo exitir ele é aberto no modo 'r' (modo de leitura - "read"). O arquivo é aberto com o 
            gerenciador de contexto 'with', que garante que o arquivo vai ser fechado depois que for usado. É aberto 
            com o nome 'arquivo' para facilitar"""
            dados_usuarios = json.load(arquivo)
            # Os dados são atribuidos a essa variável para serem usados em outras partes do programa
    else:
        # Se o arquivo não existir, o else é executado
        dados_usuarios = {}
        # Um dicionário vazio é atribuido a variável de dados para inicializar com um valor padrão


def salvar_dados():
    """Função para salvar os dados dos usuários cadastrados. Abre o arquivo no modo write (escrita). Se ele não
    existir é criado, e se exixtir seu conteúdo é sobrescrito"""
    with open(arquivo_usuarios, 'w') as arquivo:
        json.dump(dados_usuarios, arquivo)
        # Aqui converte os dados para serem armazenados no arquivo


def tela_login():
    """
    Exibe a tela de login com os campos de entrada e botões.
    """
    global entry_nome, entry_senha

    for widget in janela.winfo_children():
        widget.destroy()

    texto = ctk.CTkLabel(janela, text='Login', font=fonte_titulo)
    texto.pack(padx=10, pady=(30, 20))

    entry_nome = ctk.CTkEntry(janela, placeholder_text='Usuário', width=300, font=fonte_padrao)
    entry_nome.pack(padx=10, pady=10)

    entry_senha = ctk.CTkEntry(janela, placeholder_text='Senha', show='*', width=300, font=fonte_padrao)
    entry_senha.pack(padx=10, pady=10)

    botao_logar = ctk.CTkButton(janela, text='Login', command=autenticar, width=200, font=fonte_padrao)
    botao_logar.pack(padx=10, pady=20)

    botao_esqueci_senha = ctk.CTkButton(janela, text='Esqueci minha senha', command=tela_esqueci_senha, width=200, font=fonte_padrao, fg_color="transparent")
    botao_esqueci_senha.pack(padx=10, pady=5)

    botao_cadastro = ctk.CTkButton(janela, text='Cadastrar-se', command=tela_cadastro, width=200, font=fonte_padrao, fg_color="transparent")
    botao_cadastro.pack(padx=10, pady=5)

    entry_nome.configure(border_width=0, placeholder_text_color="white")
    entry_senha.configure(border_width=0, placeholder_text_color="white")

    janela.bind('<Return>', autenticar)

def autenticar():
    """
    Verifica os dados do usuário e, se corretos, tenta abrir a janela principal.
    """
    nome = entry_nome.get()
    senha = entry_senha.get()

    if not nome or not senha:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    if nome in dados_usuarios and dados_usuarios[nome]['senha'] == senha:
        messagebox.showinfo("Login", "Login realizado com sucesso.")
        janela.destroy()
        try:
            from main import janela_principal
            janela_principal()
        except ImportError as e:
            messagebox.showerror("Erro", f"Erro ao importar o módulo principal: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
            sys.exit(1)
    else:
        messagebox.showerror("Erro de Login", "Login ou senha incorretos.")

def tela_cadastro():
    """
    Exibe a tela de cadastro com campos para login, senha e e-mail.
    """
    global entry_nome_cad, entry_senha_cad, entry_email_cad

    for widget in janela.winfo_children():
        widget.destroy()

    texto = ctk.CTkLabel(janela, text='Cadastrar-se', font=fonte_titulo)
    texto.pack(padx=10, pady=(30, 20))

    entry_nome_cad = ctk.CTkEntry(janela, placeholder_text='Escolha um login', width=300, font=fonte_padrao)
    entry_nome_cad.pack(padx=10, pady=10)

    entry_senha_cad = ctk.CTkEntry(janela, placeholder_text='Crie uma senha', show='*', width=300, font=fonte_padrao)
    entry_senha_cad.pack(padx=10, pady=10)

    entry_email_cad = ctk.CTkEntry(janela, placeholder_text='Seu e-mail', width=300, font=fonte_padrao)
    entry_email_cad.pack(padx=10, pady=10)

    botao_cadastrar = ctk.CTkButton(janela, text='Cadastrar', command=cadastrar_usuario, width=200, font=fonte_padrao)
    botao_cadastrar.pack(padx=10, pady=20)

    botao_voltar = ctk.CTkButton(janela, text='Voltar', command=tela_login, width=200, font=fonte_padrao, fg_color="transparent")
    botao_voltar.pack(padx=10, pady=10)

    entry_nome_cad.configure(border_width=0, placeholder_text_color="white")
    entry_senha_cad.configure(border_width=0, placeholder_text_color="white")
    entry_email_cad.configure(border_width=0, placeholder_text_color="white")

def cadastrar_usuario():
    """
    Efetua o cadastro do usuário, armazenando os dados com senha criptografada.
    """
    nome = entry_nome_cad.get()
    senha = entry_senha_cad.get()
    email = entry_email_cad.get()

    if not nome or not senha or not email:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    if nome in dados_usuarios:
        messagebox.showerror("Erro", "Nome de usuário já existe.")
        return

    dados_usuarios[nome] = {'senha': senha, 'email': email}
    salvar_dados()
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
    tela_login()

def tela_esqueci_senha():
    """
    Exibe a tela de recuperação de senha:
      - Limpa a janela atual.
      - Cria o campo para que o usuário informe o login.
      - Exibe os botões de recuperar senha e voltar.
    """
    global entry_nome_rec

    for widget in janela.winfo_children():
        widget.destroy()

    texto = ctk.CTkLabel(janela, text='Recuperar Senha', font=fonte_titulo)
    texto.pack(padx=10, pady=(30, 20))

    entry_nome_rec = ctk.CTkEntry(janela, placeholder_text='Seu login', width=300, font=fonte_padrao)
    entry_nome_rec.pack(padx=10, pady=10)

    botao_recuperar = ctk.CTkButton(janela, text='Recuperar Senha', command=recuperar_senha, width=200, font=fonte_padrao)
    botao_recuperar.pack(padx=10, pady=20)

    botao_voltar = ctk.CTkButton(janela, text='Voltar', command=tela_login, width=200, font=fonte_padrao, fg_color="transparent")
    botao_voltar.pack(padx=10, pady=10)

    entry_nome_rec.configure(border_width=0, placeholder_text_color="white")

def recuperar_senha():
    """
    Realiza a "recuperação" de senha:
      - Obtém o login informado pelo usuário.
      - Se o usuário existir, simula o envio de uma instrução para o e-mail cadastrado.
      - Caso contrário, exibe uma mensagem de erro.
    """
    nome = entry_nome_rec.get()

    if nome in dados_usuarios:
        email = dados_usuarios[nome]['email']
        messagebox.showinfo("Recuperação de Senha", f"Uma instrução de recuperação foi enviada para o e-mail: {email}")
        tela_login()
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

def principal():
    iniciar_janela()
    carregar_dados()
    tela_login()
    janela.mainloop()

if __name__ == "__main__":
    principal()

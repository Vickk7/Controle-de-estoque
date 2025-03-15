import customtkinter as ctk
from tkinter import messagebox
import hashlib
from app.user import autenticar_usuario, cadastrar_usuario, carregar_dados
from app.visual import configurar_tema, criar_entrada, criar_botao
from app.janela_principal import janela_principal


# Variáveis globais
janela = None
entry_nome = None
entry_senha = None
entry_nome_cad = None
entry_senha_cad = None
entry_email_cad = None
entry_nome_rec = None


def iniciar_janela():
    """Configura a janela principal do login."""
    global janela
    janela = ctk.CTk()
    janela.title("Gerenciamento de Estoque")

    # Define tamanho e posição da janela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    largura_janela = 600
    altura_janela = 600
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    configurar_tema()


def tela_login():
    """Cria a tela de login."""
    global entry_nome, entry_senha
    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Login", font=("Arial", 24, "bold")).pack(pady=20)

    entry_nome = criar_entrada(janela, "Usuário")
    entry_nome.pack(pady=10)

    entry_senha = criar_entrada(janela, "Senha")
    entry_senha.configure(show="*")
    entry_senha.pack(pady=10)

    criar_botao(janela, "Login", autenticar).pack(pady=10)
    criar_botao(janela, "Cadastrar-se", tela_cadastro, "transparent").pack(pady=5)
    criar_botao(janela, "Esqueci minha senha", tela_esqueci_senha, "transparent").pack(pady=5)


def autenticar():
    """Processa a autenticação do usuário."""
    nome = entry_nome.get()
    senha = entry_senha.get()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    if not nome or not senha:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    if autenticar_usuario(nome, senha_hash):
        messagebox.showinfo("Login", "Login realizado com sucesso.")
        janela.destroy()
        janela_principal()
    else:
        messagebox.showerror("Erro de Login", "Login ou senha incorretos.")


def tela_cadastro():
    """Cria a tela de cadastro."""
    global entry_nome_cad, entry_senha_cad, entry_email_cad
    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Cadastrar-se", font=("Arial", 24, "bold")).pack(pady=20)

    entry_nome_cad = criar_entrada(janela, "Crie um usuário")
    entry_nome_cad.pack(pady=10)

    entry_senha_cad = criar_entrada(janela, "Crie uma senha")
    entry_senha_cad.configure(show="*")
    entry_senha_cad.pack(pady=10)

    entry_email_cad = criar_entrada(janela, "Seu e-mail")
    entry_email_cad.pack(pady=10)

    criar_botao(janela, "Cadastrar", cadastrar).pack(pady=20)
    criar_botao(janela, "Voltar", tela_login, "transparent").pack(pady=5)


def cadastrar():
    """Processa o cadastro do usuário."""
    nome = entry_nome_cad.get()
    senha = entry_senha_cad.get()
    email = entry_email_cad.get()

    if not nome or not senha or not email:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    if cadastrar_usuario(nome, senha_hash, email):
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        tela_login()
    else:
        messagebox.showerror("Erro", "Nome de usuário já existe.")


def tela_esqueci_senha():
    global entry_nome_rec

    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Recuperar Senha", font=("Arial", 24, "bold")).pack(pady=20)

    entry_nome_rec = criar_entrada(janela, "Seu login")
    entry_nome_rec.pack(pady=10)

    criar_botao(janela, "Recuperar senha", recuperar_senha).pack(pady=20)
    criar_botao(janela, "Voltar", tela_login, "transparent").pack(pady=5)


def recuperar_senha():
    nome = entry_nome_rec.get()
    dados_usuarios = carregar_dados()
    if nome in dados_usuarios:
        email = dados_usuarios[nome]['email']
        messagebox.showinfo("Recuperação de Senha", f"Uma instrução de recuperação foi enviada para o e-mail: {email}")
        tela_login()
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")


def iniciar_login():
    """Inicia a tela de login."""
    iniciar_janela()
    tela_login()
    janela.mainloop()

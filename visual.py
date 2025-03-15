import customtkinter as ctk


def configurar_tema():
    """Configura o tema padrão da aplicação."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


def criar_entrada(janela, placeholder):
    """Cria um campo de entrada estilizado."""
    return ctk.CTkEntry(janela, placeholder_text=placeholder, width=300)


def criar_botao(janela, texto, comando, fundo="dark blue"):
    """Cria um botão estilizado."""
    return ctk.CTkButton(janela, text=texto, command=comando, width=200, fg_color=fundo)

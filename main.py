import tkinter as tk
import os
import platform
from controle import *
from relatorio import *


def abrir_pdf(caminho_pdf):
    if platform.system() == "Windows":
        os.startfile(caminho_pdf)


def janela_principal():
    # Janela Principal
    root_main = ctk.CTk()
    root_main.title("Gerenciamento de Estoque")

    # Obtém o tamanho da tela do monitor
    largura_tela = root_main.winfo_screenwidth()
    altura_tela = root_main.winfo_screenheight()

    # Obtém o tamanho da janela
    largura_janela = 800  # Largura da janela
    altura_janela = 600  # Altura da janela

    # Calcula a posição para centralizar a janela
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2

    # Posiciona a janela no centro da tela
    root_main.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')

    def confirmar_saida():
        # Pergunta de confirmação
        resposta = messagebox.askyesno("Confirmar", "Você realmente deseja sair?")
        if resposta:  # Se o usuário clicar em "Sim"
            root_main.destroy()  # Fecha a aplicação

    # Funções para os menus
    def menu_cadastrar_produto():
        messagebox.showinfo("Cadastrar produto", "Abrindo tela de cadastro")
        cadastrar_produto()

    def menu_registrar_saida():
        messagebox.showinfo("Registrar as saídas", "Abrindo tela de saída de produto")
        registrar_saida()

    def menu_registrar_entrada():
        messagebox.showinfo("Registrar as entradas", "Abrindo tela de entrada de produto")
        registrar_entrada()

    def menu_remover_produto():
        messagebox.showinfo("Remover produto", "Abrindo tela de remoção de produto")
        remover_produto()

    def menu_relatorio_estoque():
        relatorio_estoque()

    def menu_relatorio_venda():
        messagebox.showinfo("Emitir as saídas e entradas", "Abrindo tela de emissão relatorio de saídas e entradas.")
        relatorio_entrada_saida()

    def menu_sobre_sistema():
        texto_sobre = """Este sistema foi desenvolvido para gerenciar o estoque, vendas e entradas de produtos de uma empresa.
A interface foi criada com o framework CustomTkinter para proporcionar uma experiência de usuário moderna e fluída."""

        messagebox.showinfo("IFBA - Turma 1.18.1M", texto_sobre)

    menubar = tk.Menu(root_main)

    # Menu CADASTRAR
    menu_cadastrar = tk.Menu(menubar, tearoff=0)
    menu_cadastrar.add_command(label="Cadastrar", command=menu_cadastrar_produto)
    menu_cadastrar.add_command(label="Saída", command=menu_registrar_saida)
    menu_cadastrar.add_command(label="Entrada", command=menu_registrar_entrada)
    menu_cadastrar.add_command(label="Remover", command=menu_remover_produto)
    menubar.add_cascade(label="Produtos", menu=menu_cadastrar)

    # Menu RELATORIO
    menu_relatorio = tk.Menu(menubar, tearoff=0)
    menu_relatorio.add_command(label="Estoque", command=menu_relatorio_estoque)
    menu_relatorio.add_command(label="Saídas e entradas", command=menu_relatorio_venda)
    menubar.add_cascade(label="Relatórios", menu=menu_relatorio)

    # Menu SOBRE
    menu_sobre = tk.Menu(menubar, tearoff=0)
    menubar.add_command(label="Sobre", command=menu_sobre_sistema)

    # Menu SAIR
    menu_sair = tk.Menu(menubar, tearoff=0)
    menubar.add_command(label="Sair", command=confirmar_saida)

    root_main.config(menu=menubar)

    root_main.mainloop()


if __name__ == "__main__":
    abre_janela_principal()

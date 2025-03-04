import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from estoque import *


def janela_principal():
    # Cria a janela principal
    janela = ctk.CTk()
    # Define o título da janela
    janela.title("Gerenciamento de estoque")

    # Obtém o tamanho da tela do monitor
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Define o tamanho da janela
    largura_janela = 600  # Largura da janela
    altura_janela = 400  # Altura da janela

    # Calcula a posição para centralizar a janela
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2

    # Posiciona a janela no centro da tela
    janela.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')

    # Define a paleta de cores da janela e o estilo padrão das fontes
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    fonte_padrao = ("Arial", 14)

    # Função para exibir informações sobre o programa
    def mostrar_sobre():
        messagebox.showinfo("Sobre", "Este programa é um sistema de gerenciamento de estoque desenvolvido "
                                     "em Python. A interface foi criada com o framework CustomTkinter para "
                                     "proporcionar uma experiência de usuário moderna e fluída.")

    # Função para lidar com a seleção das opções do estoque
    def selecionar_opcao(opcao):
        if opcao == 1:
            messagebox.showinfo("Opção Selecionada", "Você selecionou: Cadastrar produto")
            cadastrar_produto()
        elif opcao == 2:
            messagebox.showinfo("Opção Selecionada", "Você selecionou: Registrar entrada de produto")
            registrar_entrada()
        elif opcao == 3:
            messagebox.showinfo("Opção Selecionada", "Você selecionou: Registrar saída de produto")
            registrar_saida()
        elif opcao == 4:
            messagebox.showinfo("Opção Selecionada", "Você selecionou: Remover produto")
            remover_produto()
        elif opcao == 5:
            messagebox.showinfo("Opção Selecionada", "Você selecionou: Exibir estoque atual")
            calcular_estoque()
        elif opcao == 6:
            messagebox.showinfo("Opção Selecionada", "Você selecionou: Ver histórico de entradas e saídas")
            ver_historico()
        elif opcao == 7:
            messagebox.showinfo("Opção Selecionada", "Você selecionou: Gerar relatório")
            gerar_relatorio()

    def confirmar_saida():
        resposta = messagebox.askyesno("Confirmar Saída", "Você realmente deseja sair?")
        if resposta:
            janela.destroy()

    # Cria a barra de menu usando tkinter
    menu_bar = tk.Menu(janela)

    # Cria o menu "Estoque"
    menu_estoque = tk.Menu(menu_bar, tearoff=0)
    menu_estoque.add_command(label="Cadastrar produto", command=lambda: selecionar_opcao(1))
    menu_estoque.add_command(label="Registrar entrada de produto", command=lambda: selecionar_opcao(2))
    menu_estoque.add_command(label="Registrar saída de produto", command=lambda: selecionar_opcao(3))
    menu_estoque.add_command(label="Remover produto", command=lambda: selecionar_opcao(4))
    menu_estoque.add_command(label="Exibir estoque atual", command=lambda: selecionar_opcao(5))
    menu_estoque.add_command(label="Ver histórico de entradas e saídas", command=lambda: selecionar_opcao(6))
    menu_estoque.add_command(label="Gerar relatório", command=lambda: selecionar_opcao(7))
    menu_bar.add_cascade(label="Menu", menu=menu_estoque)

    # Cria o menu "Sobre"
    menu_sobre = tk.Menu(menu_bar, tearoff=0)
    menu_sobre.add_command(label="Informações do sistema", command=mostrar_sobre)
    menu_bar.add_cascade(label="Sobre", menu=menu_sobre)

    # Cria o menu "Sair"
    menu_sair = tk.Menu(menu_bar, tearoff=0)
    menu_sair.add_command(label="Sair", command=confirmar_saida)
    menu_bar.add_cascade(label="Sair", menu=menu_sair)

    # Adiciona a barra de menu à janela
    janela.configure(menu=menu_bar)

    # Cria um rótulo de boas-vindas
    texto = ctk.CTkLabel(janela, text="Bem-vindo ao Sistema de Gerenciamento de Estoque", font=("Arial", 20, "bold"))
    texto.pack(pady=(40, 20))

    # Inicia o loop da interface, mantendo a janela aberta
    janela.mainloop()

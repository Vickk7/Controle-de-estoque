import customtkinter as ctk
from visual import criar_entrada, criar_botao
from controle import *
from janela_principal import janela_principal
import json


# Variáveis globais
janela = None


def tela_cadastrar_produto():
    # Exibe a tela para cadastrar um novo produto

    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Cadastrar Produto", font=("Arial", 24, "bold")).pack(pady=20)

    entry_nome = criar_entrada(janela, "Nome do produto")
    entry_nome.pack(pady=10)

    entry_quantidade = criar_entrada(janela, "Quantidade inicial")
    entry_quantidade.pack(pady=10)

    entry_preco = criar_entrada(janela, "Preço")
    entry_preco.pack(pady=10)

    criar_botao(janela, "Cadastrar produto", cadastrar_produto(entry_nome, entry_quantidade, entry_preco)).pack(pady=10)
    criar_botao(janela, "Voltar", janela_principal, "transparent").pack(pady=5)


def tela_registrar_entrada():
    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Entrada de produto", font=("Arial", 24, "bold")).pack(pady=20)

    entry_nome = criar_entrada(janela, "Nome do produto")
    entry_nome.pack(pady=10)

    entry_quantidade = criar_entrada(janela, "Quantidade a adicionar")
    entry_quantidade.pack(pady=10)

    criar_botao(janela, "Registrar entrada", registrar_entrada(entry_nome, entry_quantidade)).pack(pady=10)
    criar_botao(janela, "Voltar", janela_principal, "transparent").pack(pady=5)


def tela_registrar_saida():
    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Saída de produto", font=("Arial", 24, "bold")).pack(pady=20)

    entry_nome = criar_entrada(janela, "Nome do produto")
    entry_nome.pack(pady=10)

    entry_quantidade = criar_entrada(janela, "Quantidade a remover")
    entry_quantidade.pack(pady=10)

    criar_botao(janela, "Registrar saída", registrar_entrada(entry_nome, entry_quantidade)).pack(pady=10)
    criar_botao(janela, "Voltar", janela_principal, "transparent").pack(pady=5)


def tela_remover_produto():
    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Remover Produto", font=("Arial", 24, "bold")).pack(pady=20)

    entry_nome = criar_entrada(janela, "Nome do produto")
    entry_nome.pack(pady=10)

    criar_botao(janela, "Remover", remover_produto(entry_nome)).pack(pady=10)
    criar_botao(janela, "Voltar", janela_principal, "transparent").pack(pady=5)


def tela_relatorio_estoque():
    """Exibe um relatório com os produtos cadastrados no estoque."""
    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Relatório de Estoque", font=("Arial", 24, "bold")).pack(pady=20)

    estoque = carregar_estoque()
    relatorio = ""
    if not estoque:
        relatorio = "Nenhum produto cadastrado."
    else:
        for produto in estoque.values():
            relatorio += (f"Produto: {produto['nome']}\n"
                          f"Quantidade: {produto['quantidade']}\n"
                          f"Preço: {produto['preco']:.2f}\n"
                          "-----------------\n")
    ctk.CTkLabel(janela, text=relatorio, font=("Arial", 14), justify="left").pack(pady=10)
    criar_botao(janela, "Voltar", janela_principal, "transparent").pack(pady=5)


def tela_relatorio_movimentacoes():
    """Exibe um relatório com as movimentações (entradas e saídas) registradas."""
    for widget in janela.winfo_children():
        widget.destroy()

    ctk.CTkLabel(janela, text="Relatório de Movimentações", font=("Arial", 24, "bold")).pack(pady=20)

    try:
        with open(ARQUIVO_MOVIMENTACOES, "r") as f:
            movimentacoes = json.load(f)
    except FileNotFoundError:
        movimentacoes = []

    relatorio = ""
    if not movimentacoes:
        relatorio = "Nenhuma movimentação registrada."
    else:
        for mov in movimentacoes:
            relatorio += (f"Produto: {mov['produto']}\n"
                          f"Tipo: {mov['tipo']}\n"
                          f"Quantidade: {mov['quantidade']}\n"
                          f"Data: {mov['data']}\n"
                          "-----------------\n")
    ctk.CTkLabel(janela, text=relatorio, font=("Arial", 14), justify="left").pack(pady=10)
    criar_botao(janela, "Voltar", janela_principal, "transparent").pack(pady=5)

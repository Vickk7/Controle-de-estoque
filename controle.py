import datetime
import json
from tkinter import messagebox
from janela_principal import janela_principal

# Define a rota do arquivo (onde vai estar localizado)
ARQUIVO_ESTOQUE = "estoque.json"
ARQUIVO_MOVIMENTACOES = "movimentacoes.json"


def carregar_estoque():
    """Carrega o estoque do arquivo JSON ou retorna um dicionário vazio caso o arquivo não exista."""
    try:
        with open(ARQUIVO_ESTOQUE, "r") as f:
            estoque = json.load(f)
    except FileNotFoundError:
        estoque = {}
    return estoque


def salvar_estoque(estoque):
    """Salva o dicionário de estoque no arquivo JSON."""
    with open(ARQUIVO_ESTOQUE, "w") as f:
        json.dump(estoque, f, indent=4)


def cadastrar_produto(entry_nome, entry_quantidade, entry_preco):
    nome = entry_nome.get().strip()
    if not nome:
        messagebox.showerror("Erro", "O nome do produto é obrigatório.")
        return
    try:
        quantidade = int(entry_quantidade.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
        return
    try:
        preco = float(entry_preco.get())
    except ValueError:
        messagebox.showerror("Erro", "Preço deve ser um número!")
        return

    estoque = carregar_estoque()
    if nome in estoque:
        messagebox.showerror("Erro", "Produto já existe!")
        return

    estoque[nome] = {"nome": nome, "quantidade": quantidade, "preco": preco}
    salvar_estoque(estoque)
    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
    janela_principal()


def registrar_entrada(entry_nome, entry_quantidade):
    nome = entry_nome.get().strip()
    if not nome:
        messagebox.showerror("Erro", "Informe o nome do produto!")
        return
    try:
        quantidade = int(entry_quantidade.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade inválida!")
        return

    estoque = carregar_estoque()
    if nome not in estoque:
        messagebox.showerror("Erro", "Produto não encontrado!")
        return

    estoque[nome]["quantidade"] += quantidade
    salvar_estoque(estoque)
    registrar_movimentacao("entrada", nome, quantidade)
    messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")
    janela_principal()


def registrar_saida(entry_nome, entry_quantidade):
    nome = entry_nome.get().strip()
    if not nome:
        messagebox.showerror("Erro", "Informe o nome do produto!")
        return
    try:
        quantidade = int(entry_quantidade.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade inválida!")
        return

    estoque = carregar_estoque()
    if nome not in estoque:
        messagebox.showerror("Erro", "Produto não encontrado!")
        return

    if estoque[nome]["quantidade"] < quantidade:
        messagebox.showerror("Erro", "Estoque insuficiente!")
        return

    estoque[nome]["quantidade"] -= quantidade
    salvar_estoque(estoque)
    registrar_movimentacao("saída", nome, quantidade)
    messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")
    janela_principal()


def remover_produto(entry_nome):
    nome = entry_nome.get().strip()
    if not nome:
        messagebox.showerror("Erro", "Informe o nome do produto!")
        return
    estoque = carregar_estoque()
    if nome not in estoque:
        messagebox.showerror("Erro", "Produto não encontrado!")
        return

    if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o produto {nome}?"):
        del estoque[nome]
        salvar_estoque(estoque)
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
    janela_principal()


def registrar_movimentacao(tipo, produto, quantidade):
    """Registra uma movimentação (entrada ou saída) com data/hora."""
    try:
        with open(ARQUIVO_MOVIMENTACOES, "r") as f:
            movimentacoes = json.load(f)
    except FileNotFoundError:
        movimentacoes = []

    movimentacoes.append({
        "produto": produto,
        "tipo": tipo,
        "quantidade": quantidade,
        "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(ARQUIVO_MOVIMENTACOES, "w") as f:
        json.dump(movimentacoes, f, indent=4)

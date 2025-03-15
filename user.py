# Biblioteca que converte o formato dos dados
import json
# Interaje com o sistema operacional
import os

# Define a rota do arquivo (onde vai estar localizado)
ARQUIVO_USUARIOS = "./usuarios.json"


def carregar_dados():
    """Carrega os dados de usuários do arquivo JSON."""
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {}
    with open(ARQUIVO_USUARIOS, "r") as f:
        # Retorna o json em formato de dicionario
        # Load carrega os dados que já existem
        return json.load(f)


def salvar_dados(dados):
    """Salva os dados dos usuários no arquivo JSON."""
    with open(ARQUIVO_USUARIOS, "w") as f:
        # Insere os dados novos usando o dump
        json.dump(dados, f, indent=4)


def autenticar_usuario(nome, senha):
    """Verifica se o usuário e senha são válidos."""
    # Carrega os dados em uma variavel em forma de dicionario
    dados_usuarios = carregar_dados()
    return nome in dados_usuarios and dados_usuarios[nome]['senha'] == senha


def cadastrar_usuario(nome, senha, email):
    """Cadastra um novo usuário, se ele ainda não existir."""
    dados_usuarios = carregar_dados()
    if nome in dados_usuarios:
        return False  # Usuário já existe
    dados_usuarios[nome] = {"senha": senha, "email": email}
    salvar_dados(dados_usuarios)
    return True

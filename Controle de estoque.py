import sqlite3

# Função para conectar ou criar o banco de dados
def conectar_banco():
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None

# Função para criar a tabela de produtos se já não existir
def criar_tabela(cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL)''')
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")

# Função para cadastrar um novo produto no estoque
def cadastrar_produto(cursor):
    nome = input("Nome do produto: ")
    try:
        quantidade = int(input("Quantidade em estoque: "))
        preco = float(input("Preço unitário: R$"))
        if not nome or quantidade < 0 or preco < 0:
            print("Dados inválidos. Certifique-se de que o nome não está vazio e de que a quantidade e o preço são números válidos.")
            return
        cursor.execute('''
            INSERT INTO produtos (nome, quantidade, preco)
            VALUES (?, ?, ?)
        ''', (nome, quantidade, preco))
        print(f"{nome} cadastrado(a) com sucesso.")
    except ValueError:
        print("Quantidade e preço devem ser números válidos. Tente novamente.")
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar {e}. Tente novamente.")

# Função para egistrar a entrada de produtos no estoque
def registrar_entrada(cursor):
    nome = input("Nome do produto: ")
    try:
        quantidade = int(input("Quantidade a adicionar: "))
        if quantidade < 0:
            print("Quantidade inválida. Deve ser um número inteiro positivo.")
            return
        cursor.execute('''
            SELECT quantidade FROM produtos WHERE nome = ?
        ''', (nome,))
        resultado = cursor.fetchone()
        if resultado:
            nova_quantidade = resultado[0] + quantidade
            cursor.execute('''
                UPDATE produtos SET quantidade = ? WHERE nome = ?
            ''', (nova_quantidade, nome))
            print(f"Entrada de {quantidade} unidades do produto '{nome}' registrada.")
        else:
            print(f"Produto '{nome}' não encontrado no estoque.")
    except ValueError:
        print("Quantidade deve ser um número válido.")
    except sqlite3.Error as e:
        print(f"Erro ao registrar entrada: {e}")

# Função para registrar a saída de produtos do estoque
def registrar_saida(cursor):
    nome = input("Nome do produto: ")
    try:
        quantidade = int(input("Quantidade a remover: "))
        if quantidade < 0:
            print("Quantidade inválida. Deve ser um número inteiro positivo.")
            return
        cursor.execute('''
            SELECT quantidade FROM produtos WHERE nome = ?
        ''', (nome,))
        resultado = cursor.fetchone()
        if resultado:
            if resultado[0] >= quantidade:
                nova_quantidade = resultado[0] - quantidade
                cursor.execute('''
                    UPDATE produtos SET quantidade = ? WHERE nome = ?
                ''', (nova_quantidade, nome))
                print(f"Saída de {quantidade} unidades do produto '{nome}' registrada.")
            else:
                print(f"Quantidade insuficiente em estoque. Apenas {resultado[0]} unidades disponíveis.")
        else:
            print(f"Produto '{nome}' não encontrado no estoque.")
    except ValueError:
        print("Quantidade deve ser um número válido.")
    except sqlite3.Error as e:
        print(f"Erro ao registrar saída: {e}")

# Função para remover um produto do estoque
def remover_produto(cursor):
    nome = input("Nome do produto a remover: ")
    try:
        cursor.execute('''
            DELETE FROM produtos WHERE nome = ?
        ''', (nome,))
        if cursor.rowcount > 0:
            print(f"Produto '{nome}' removido com sucesso.")
        else:
            print(f"Produto '{nome}' não encontrado no estoque.")
    except sqlite3.Error as e:
        print(f"Erro ao remover o produto: {e}")

# Função para calcular o estoque atual
def calcular_estoque(cursor):
    try:
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
        print("\nEstoque Atual:")
        print("{:<5} {:<20} {:<15} {:<10}".format('ID', 'Nome', 'Quantidade', 'Preço'))
        for produto in produtos:
            print("{:<5} {:<20} {:<15} R${:<10.2f}".format(produto[0], produto[1], produto[2], produto[3] if produto[3] else 0.00))
    except sqlite3.Error as e:
        print(f"Erro ao calcular o estoque: {e}")

# Função para gerar um relatório do estoque
def gerar_relatorio(cursor):
    try:
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
        with open('relatorio_estoque.txt', 'w') as arquivo:
            arquivo.write("Relatório de Estoque\n")
            arquivo.write("{:<5} {:<20} {:<15} {:<10}\n".format('ID', 'Nome', 'Quantidade', 'Preço'))
            for produto in produtos:
                arquivo.write("{:<5} {:<20} {:<15} R${:<10.2f}\n".format(produto[0], produto[1], produto[2], produto[3] if produto[3] else 0.00))
        print("Relatório 'relatorio_estoque.txt' gerado com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao gerar relatório: {e}")

# Função para fechar a conexão com o banco de dados
def fechar_conexao(conn):
    try:
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro ao fechar a conexão: {e}")

# Menu interativo
def menu_interativo():
    conn, cursor = conectar_banco()
    if conn and cursor:
        criar_tabela(cursor)

        while True:
            print("\n===== Controle de Estoque =====")
            print("1. Cadastrar produto")
            print("2. Registrar entrada de produto")
            print("3. Registrar saída de produto")
            print("4. Remover produto")
            print("5. Exibir estoque atual")
            print("6. Gerar relatório")
            print("7. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                cadastrar_produto(cursor)
            elif opcao == '2':
                registrar_entrada(cursor)
            elif opcao == '3':
                registrar_saida(cursor)
            elif opcao == '4':
                remover_produto(cursor)
            elif opcao == '5':
                calcular_estoque(cursor)
            elif opcao == '6':
                gerar_relatorio(cursor)
            elif opcao == '7':
                print("Saindo do sistema...")
                fechar_conexao(conn)
                break
            else:
                print("Opção inválida. Tente novamente.")

# Execução do programa
if __name__ == "__main__":
    menu_interativo()

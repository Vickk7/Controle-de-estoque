import sqlite3
import datetime

# Função para conectar ou criar o banco de dados
def conectar_banco():
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None

# Função para criar as tabelas de produtos e histórico se já não existirem
def criar_tabelas(cursor):
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                data_hora TEXT NOT NULL
            )
        ''')
    except sqlite3.Error as e:
        print(f"Erro ao criar as tabelas: {e}")

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
        print(f"Erro ao cadastrar produto: {e}")

# Função para registrar a entrada de produtos no estoque
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
            # Registrar no histórico
            data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO historico (produto_nome, quantidade, tipo, data_hora)
                VALUES (?, ?, 'Entrada', ?)
            ''', (nome, quantidade, data_hora))
            print(f"Entrada de {quantidade} unidades do produto '{nome}' registrada em {data_hora}.")
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
                # Registrar no histórico
                data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('''
                    INSERT INTO historico (produto_nome, quantidade, tipo, data_hora)
                    VALUES (?, ?, 'Saída', ?)
                ''', (nome, quantidade, data_hora))
                print(f"Saída de {quantidade} unidades do produto '{nome}' registrada em {data_hora}.")
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


# Função para ver o histórico de entradas e saídas
def ver_historico(cursor):
    try:
        cursor.execute('SELECT * FROM historico ORDER BY data_hora DESC')
        registros = cursor.fetchall()
        print("\nHistórico de Entradas e Saídas:")
        print("{:<5} {:<20} {:<10} {:<8} {:<20}".format('ID', 'Produto', 'Quantidade', 'Tipo', 'Data/Hora'))
        for registro in registros:
            print("{:<5} {:<20} {:<10} {:<8} {:<20}".format(registro[0], registro[1], registro[2], registro[3], registro[4]))
    except sqlite3.Error as e:
        print(f"Erro ao obter o histórico: {e}")


def gerar_relatorio(cursor):
    try:
        with open('relatorio_estoque.txt', 'w') as arquivo:
            # Relatório do estoque atual
            arquivo.write("=== Relatório de Estoque ===\n")
            arquivo.write("{:<5} {:<20} {:<15} {:<10}\n".format('ID', 'Nome', 'Quantidade', 'Preço'))
            cursor.execute('SELECT * FROM produtos')
            produtos = cursor.fetchall()
            for produto in produtos:
                arquivo.write("{:<5} {:<20} {:<15} R${:<10.2f}\n".format(
                    produto[0], produto[1], produto[2], produto[3] if produto[3] else 0.00))

            arquivo.write("\n")  # Linha em branco para separar as seções

            # Relatório do histórico de entradas e saídas
            arquivo.write("=== Histórico de Entradas e Saídas ===\n")
            arquivo.write("{:<5} {:<20} {:<10} {:<8} {:<20}\n".format(
                'ID', 'Produto', 'Quantidade', 'Tipo', 'Data/Hora'))
            cursor.execute('SELECT * FROM historico ORDER BY data_hora DESC')
            registros = cursor.fetchall()
            for registro in registros:
                arquivo.write("{:<5} {:<20} {:<10} {:<8} {:<20}\n".format(
                    registro[0], registro[1], registro[2], registro[3], registro[4]))
            print("Relatório 'relatorio_estoque.txt' gerado com sucesso, incluindo o histórico de entradas e saídas.")
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
        criar_tabelas(cursor)

        while True:
            print("\n===== Controle de Estoque =====")
            print("1. Cadastrar produto")
            print("2. Registrar entrada de produto")
            print("3. Registrar saída de produto")
            print("4. Remover produto")
            print("5. Exibir estoque atual")
            print("6. Ver histórico de entradas e saídas")
            print("7. Gerar relatório")
            print("8. Sair")
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
                ver_historico(cursor)
            elif opcao == '7':
                gerar_relatorio(cursor)
            elif opcao == '8':
                print("Saindo do sistema...")
                fechar_conexao(conn)
                break
            else:
                print("Opção inválida. Tente novamente.")

# Execução do programa
if __name__ == "__main__":
    menu_interativo()

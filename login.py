# Versão personalizada do tkinter, ideal pra fazer interfaces (nomeada de ctk para facilitar o uso):
import customtkinter as ctk
# Funçaõ do tkinter para exibir caixas de mensagem na tela:
from tkinter import messagebox
# Função para abrir a janela principal
from main import janela_principal


def login():
    # Cria a janela de login
    janela = ctk.CTk()
    # Define o título da janela
    janela.title("Gerenciamento de estoque")

    # Obtém o tamanho da tela do monitor
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Define o tamanho da janela
    largura_janela = 400  # Largura da janela
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

    # Cria um rótulo (texto estático) na janela
    texto = ctk.CTkLabel(janela, text="Faça seu login", font=("Arial", 20, "bold"))
    # Define o posicionamento do rótulo na janela. Adiciona 40 pixels acima e 20 abaixo do rótulo
    texto.pack(pady=(40, 20))

    # Cria uma entrada (campo de texto) na interface, nesse caso para colocar o login
    entry_login = ctk.CTkEntry(janela, placeholder_text='Login', width=300, height=35, font=fonte_padrao)
    # Define o posicionamento do texto na janela. Adiciona 10 pixels acima e 10 abaixo do texto
    entry_login.pack(pady=10)

    # Cria uma entrada (campo de texto) na interface, nesse caso para colocar a senha
    entry_senha = ctk.CTkEntry(janela, placeholder_text='Senha', show='*', width=300, height=35, font=fonte_padrao)
    # Define o posicionamento do texto na janela. Adiciona 10 pixels acima e 10 abaixo do texto
    entry_senha.pack(pady=10)

    def autenticar():
        # Obtém os valores inseridos nos campos de entrada
        nome = entry_login.get()
        senha = entry_senha.get()

        # Verifica se retorna True ou False
        if nome == 'admin' and senha == '1234':
            # Se a autenticação for bem-sucedida, uma mensagem de confirmação é exibida
            messagebox.showinfo("Login", "Login realizado com sucesso")
            # O formulário de login é destruido/fechado
            janela.destroy()
            # Se as credencias estiverem certas, a função que abre a janela principal é chamada
            janela_principal()
        else:
            # Se a autenticação falhar, uma mensagem de erro é exibida informando que as credenciais estão incorretas
            messagebox.showerror("Erro de Login", "Credencias Incorretas")

    # Cria um botão que, ao ser acionado, chama a função login
    botao = ctk.CTkButton(janela, text="Login", command=autenticar, width=150, height=35, font=fonte_padrao)
    # Define o posicionamento do botão na janela. Preenche com 11 pixels de margem horizontal e 11 de margem vertical
    botao.pack(pady=(20, 10))

    # Inicia o loop da interface, mantendo a janela aberta
    janela.mainloop()


# Se a condição for verdadeira (ou seja, o script está sendo executado diretamente), a função login() será chamada
if __name__ == "__main__":
    login()

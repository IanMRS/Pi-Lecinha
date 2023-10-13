from tkinter import *
from tkinter import ttk
import sqlite3

# Função para criar a tabela no banco de dados
def criar_tabela():
    comando = '''
    CREATE TABLE IF NOT EXISTS clientes (
        codigo INTEGER PRIMARY KEY,
        nome TEXT,
        telefone TEXT
    )
    '''
    cursor.execute(comando)
    conexao.commit()

# Função para inserir um novo cliente no banco de dados
def inserir_cliente():
    nome = nome_entry.get()
    telefone = telefone_entry.get()
    comando = "INSERT INTO clientes (nome, telefone) VALUES (?, ?)"
    dados = (nome, telefone)
    cursor.execute(comando, dados)
    conexao.commit()
    listar_clientes()

# Função para listar os clientes na Treeview
def listar_clientes():
    comando = "SELECT * FROM clientes"
    cursor.execute(comando)
    resultados = cursor.fetchall()
    # Limpa a Treeview antes de adicionar os novos dados
    for item in lista_cliente.get_children():
        lista_cliente.delete(item)
    for linha in resultados:
        lista_cliente.insert('', 'end', values=linha)

root = Tk()  # Cria uma instância da classe Tk(), que representa a janela principal da interface gráfica

# Conecta ao banco de dados SQLite
conexao = sqlite3.connect('banco_de_dados.db')
cursor = conexao.cursor()

criar_tabela()

class Funcs():
    def limpa_tela():
        codigo_entry.delete(0, END)
        nome_entry.delete(0, END)
        telefone_entry.delete(0, END)

class Application(Funcs):
    def __init__(self):  # função para abrir a janela
        self.root = root
        self.tela()  # função tela,
        self.frames_da_tela()  # chamar a função frame da tela
        self.widgets_frame1()  # chamar os botões
        self.tabela()
        root.mainloop()  # criar um loop para abrir a janela

    def tela(self):  # função para configurar a tela
        self.root.title("Cadastro de Clientes")  # Texto da barra superior
        self.root.configure(background='#444444')
        self.root.geometry("800x600")  # dimensões do começo da janela
        self.root.resizable(True, True)  # Tela responsiva
        self.root.maxsize(width=1920, height=1800)  # definir a largura e altura máxima
        self.root.minsize(width=600, height=500)  # tamanho mínimo

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#045D32', highlightbackground='#ffffff', highlightthickness=1)
        # 3 formas de interação, os widgets. place, pack e grid
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#045D32', highlightbackground='#ffffff', highlightthickness=1)
        self.frame_2.place(relx=0.02, rely=0.49, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        ###Botão Limpar
        bt_limpar = Button(self.frame_1, text="Limpar", command=Funcs.limpa_tela)
        bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        ###Botão buscar
        bt_buscar = Button(self.frame_1, text="Buscar")
        bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        ###Botão Novo
        bt_novo = Button(self.frame_1, text="Novo", command=inserir_cliente)
        bt_novo.place(relx=0.65, rely=0.1, relwidth=0.1, relheight=0.15)

        ###Botão Alterar
        bt_alterar = Button(self.frame_1, text="Alterar")
        bt_alterar.place(relx=0.75, rely=0.1, relwidth=0.1, relheight=0.15)

        ###Botão Apagar
        bt_apagar = Button(self.frame_1, text="Apagar")
        bt_apagar.place(relx=0.85, rely=0.1, relwidth=0.1, relheight=0.15)

        ###Label e entrada dos códigos
        lb_codigo = Label(self.frame_1, text="Código")  # Código de busca
        lb_codigo.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.1)

        global codigo_entry
        codigo_entry = Entry(self.frame_1)
        codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.1, relheight=0.1)

        ###Label e entrada de nome
        lb_nome = Label(self.frame_1, text="Nome")
        lb_nome.place(relx=0.05, rely=0.35, relwidth=0.1, relheight=0.1)

        global nome_entry
        nome_entry = Entry(self.frame_1)
        nome_entry.place(relx=0.05, rely=0.45, relwidth=0.90, relheight=0.1)

        ###Label e entrada de Ia
        lb_telefone = Label(self.frame_1, text="Telefone")
        lb_telefone.place(relx=0.05, rely=0.6, relwidth=0.1, relheight=0.1)

        global telefone_entry
        telefone_entry = Entry(self.frame_1)
        telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4, relheight=0.1)

    def tabela(self):
        global lista_cliente
        lista_cliente = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3"))
        lista_cliente.heading("#0", text="")
        lista_cliente.heading("#1", text="Código")
        lista_cliente.heading("#2", text="Nome")
        lista_cliente.heading("#3", text="Telefone")

        lista_cliente.column("#0", width=1)
        lista_cliente.column("#1", width=50)
        lista_cliente.column("#2", width=200)
        lista_cliente.column("#3", width=125)

        lista_cliente.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        scroll_lista = Scrollbar(self.frame_2, orient='vertical')  # Barra de rolagem da lista
        lista_cliente.configure(yscroll=scroll_lista.set)  # A barra pertence à lista
        scroll_lista.place(relx=0.95, rely=0.1, relwidth=0.04, relheight=0.85)

        listar_clientes()

if __name__ == '__main__':
    app = Application()
    app.root.mainloop()

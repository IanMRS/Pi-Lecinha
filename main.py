from tkinter import *
from tkinter import ttk

import db_action as dba
import db_connection as dbc

#from reportlab.pdfgen import canvas 
#from reportlab.lib.pagesizes import letter. A4#Gerar relatorios em PDF, dps eu vejo isso

root = Tk()  # Cria uma instância da classe Tk(), que representa a janela principal da interface gráfica

class Application(dba.Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgtes_frame1()
        self.tabela()
        self.select_lista()
        self.Menus()
        root.mainloop()


    def select_lista(self):
        # Atualiza a lista de clientes na interface
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        lista = dba.Funcs.cursor.execute("""SELECT cod, nome_cliente, telefone FROM clientes ORDER BY nome_cliente ASC;""")
        for i in lista:
            self.lista_cliente.insert("", END, values=i)
        dbc.disconnect_db(self.connection)


    def double_click(self, event):
        # Manipula o evento de duplo clique em uma linha da lista
        self.limpa_tela()
        self.lista_cliente.selection()
        for n in self.lista_cliente.selection():
            col1, col2, col3 = self.lista_cliente.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)


    def tela(self):
        # Configuração da janela principal
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='#444444')
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.maxsize(width=1920, height=1800)
        self.root.minsize(width=600, height=500)


    def frames_da_tela(self):
        # Criação dos frames para organizar os elementos
        self.frame_1 = Frame(self.root, bd=4, bg='#045D32', highlightbackground='#ffffff', highlightthickness=1)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#045D32', highlightbackground='#ffffff', highlightthickness=1)
        self.frame_2.place(relx=0.02, rely=0.49, relwidth=0.96, relheight=0.46)


    def widgtes_frame1(self):
        # Elementos no frame 1
        self.bt_limpar = Button(self.frame_1, text="Limpar", command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_buscar = Button(self.frame_1, text="Buscar", command=self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_novo = Button(self.frame_1, text="Novo", command=self.add_cliente)
        self.bt_novo.place(relx=0.65, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_alterar = Button(self.frame_1, text="Alterar", command=self.alterar_cliente)
        self.bt_alterar.place(relx=0.75, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_apagar = Button(self.frame_1, text="Apagar", command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.85, rely=0.1, relwidth=0.1, relheight=0.15)

        self.lb_codigo = Label(self.frame_1, text="Código")
        self.lb_codigo.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.1)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.1, relheight=0.1)

        self.lb_nome = Label(self.frame_1, text="Nome")
        self.lb_nome.place(relx=0.05, rely=0.35, relwidth=0.1, relheight=0.1)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05,rely=0.45, relwidth=0.90, relheight=0.1)
        self.lb_telefone = Label(self.frame_1, text="Telefone")
        self.lb_telefone.place(relx=0.05, rely=0.6, relwidth=0.1, relheight=0.1)

        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4, relheight=0.1)


    def tabela(self):
        # Criação da tabela no frame 2
        self.lista_cliente = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3"))
        self.lista_cliente.heading("#0", text="")
        self.lista_cliente.heading("#1", text="Código")
        self.lista_cliente.heading("#2", text="Nome")
        self.lista_cliente.heading("#3", text="Telefone")

        self.lista_cliente.column("#0", width=1)
        self.lista_cliente.column("#1", width=50)
        self.lista_cliente.column("#2", width=200)
        self.lista_cliente.column("#3", width=125)

        self.lista_cliente.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroll_lista = Scrollbar(self.frame_2, orient='vertical')  # Barra de rolagem da lista
        self.lista_cliente.configure(yscroll=self.scroll_lista.set)  # A barra pertence à lista
        self.scroll_lista.place(relx=0.95, rely=0.1, relwidth=0.04, relheight=0.85)
        self.lista_cliente.bind("<Double-1>", self.double_click)

    def Menus(self): #opções, a barrinha q aparece encima, calma q mexo
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit():
            self.root.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Sobre", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu2.add_command(label="Limpa Cliente", command=self.limpa_tela)

Application()  # Cria uma instância da classe Application, o que inicia a aplicação TKINTER
from tkinter import *
from tkinter import ttk

import db_action as dba

#from reportlab.pdfgen import canvas 
#from reportlab.lib.pagesizes import letter. A4#Gerar relatorios em PDF, dps eu vejo isso

class Application():
    def __init__(self, crud):
        self.crud = crud
        self.root = Tk() # Cria uma instância da classe Tk(), que representa a janela principal da interface gráfica
        self.tela()
        self.frames_da_tela()
        self.widgtes_frame1()
        self.tabela()
        self.update_lista()
        self.Menus()


    def stop(self):
        self.root.destroy()


    def start(self):
        self.root.mainloop()


    def double_click(self, event):
        # Manipula o evento de duplo clique em uma linha da lista
        self.limpa_tela()
        self.lista_cliente.selection()
        for n in self.lista_cliente.selection():
            col1, col2, col3, col4 = self.lista_cliente.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.obs_entry.insert(END, col4)


    def tela(self):
        # Configuração da janela principal
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='#444444')
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        self.root.maxsize(width=1920, height=1080)
        self.root.minsize(width=600, height=500)


    def limpa_tela(self):
        # Limpa os campos de entrada (Entry)
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.obs_entry.delete(0, END)


    def update_lista(self):
        # Atualiza a lista de clientes na interface
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        for i in self.crud.read():
            self.lista_cliente.insert("", END, values=i)


    def press_button(self, action):
        #É recomendável que ponha isso toda vez q um botão for apertado e altere as listas
        action
        self.update_lista()
        self.limpa_tela()


    def frames_da_tela(self):
        # Criação dos frames para organizar os elementos
        self.frame_1 = Frame(self.root, bd=4, bg='#045D32', highlightbackground='#ffffff', highlightthickness=1)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.6)

        self.frame_2 = Frame(self.root, bd=4, bg='#045D32', highlightbackground='#ffffff', highlightthickness=1)
        self.frame_2.place(relx=0.02, rely=.6, relwidth=0.96, relheight=0.40)


    def widgtes_frame1(self):
        # Elementos no frame 1
        self.lb_codigo = Label(self.frame_1, text="Código")
        self.lb_codigo.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.1)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.1, relheight=0.1)


        self.lb_nome = Label(self.frame_1, text="Nome")
        self.lb_nome.place(relx=0.05, rely=0.26, relwidth=0.1, relheight=0.1)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05,rely=0.36, relwidth=0.90, relheight=0.1)


        self.lb_telefone = Label(self.frame_1, text="Telefone")
        self.lb_telefone.place(relx=0.05, rely=0.47, relwidth=0.1, relheight=0.1)

        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.57, relwidth=0.4, relheight=0.1)


        self.lb_obs = Label(self.frame_1, text="Observações")
        self.lb_obs.place(relx=0.05, rely=0.68, relwidth=0.1, relheight=0.1)

        self.obs_entry = Entry(self.frame_1)
        self.obs_entry.place(relx=0.05, rely=.78, relwidth=0.4, relheight=0.1)


        self.bt_limpar = Button(self.frame_1, text="Limpar", command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_buscar = Button(self.frame_1, text="Buscar", command=lambda: self.crud.search([self.nome_entry.get(),self.telefone_entry.get(), self.obs_entry.get()]))
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_novo = Button(self.frame_1, text="Novo", command=lambda: self.press_button(self.crud.insert([self.nome_entry.get(),self.telefone_entry.get(),self.obs_entry.get()])))
        self.bt_novo.place(relx=0.65, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_alterar = Button(self.frame_1, text="Alterar", command=lambda: self.press_button(self.crud.update([self.nome_entry.get(),self.telefone_entry.get()], f"id = {self.codigo_entry.get()}")))
        self.bt_alterar.place(relx=0.75, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_apagar = Button(self.frame_1, text="Apagar", command=lambda: self.press_button(self.crud.delete(f"id = {self.codigo_entry.get()}")))
        self.bt_apagar.place(relx=0.85, rely=0.1, relwidth=0.1, relheight=0.15)


    def tabela(self):
        # Criação da tabela no frame 2
        self.lista_cliente = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.lista_cliente.heading("#0", text="")
        self.lista_cliente.heading("#1", text="Código")
        self.lista_cliente.heading("#2", text="Nome")
        self.lista_cliente.heading("#3", text="Telefone")
        self.lista_cliente.heading("#4", text="Observação")

        self.lista_cliente.column("#0", width=1)
        self.lista_cliente.column("#1", width=50)
        self.lista_cliente.column("#2", width=200)
        self.lista_cliente.column("#3", width=125)
        self.lista_cliente.column("#4", width=125)

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

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Sobre", menu=filemenu2)

        filemenu.add_command(label="Sair", command=self.stop)
        filemenu2.add_command(label="Limpa Cliente", command=self.limpa_tela)

maneja_clientes = Application(dba.crud_clientes)
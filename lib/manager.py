from tkinter import *
from tkinter import ttk

#from reportlab.pdfgen import canvas 
#from reportlab.lib.pagesizes import letter. A4#Gerar relatorios em PDF, dps eu vejo isso

class GenericManager(Frame):
    def __init__(self, crud, frame):
        super().__init__(frame)
        self.crud = crud
        self.nome_dado = self.crud.table_name.capitalize()
        #self.root = Frame(frame)

        self.inicializar()

    def double_click(self, event):
        # Manipula o evento de duplo clique em uma linha da lista
        self.limpa_tela()
        selected_item = self.lista_itens.selection()
        if selected_item:
            for n in selected_item:
                col = self.lista_itens.item(n, 'values')
                self.id_entrie.insert(END, col[0])
                [entrie.insert(END, col[i+1]) for i, entrie in enumerate(self.entries)]

    def inicializar(self):
        self.configure(background='#444444')

        self.frames()
        self.widgets()
        self.table()
        self.update_lista()
        

    def limpa_tela(self):
        # Limpa os campos de entrada (Entry)
        self.id_entrie.delete(0, END)
        [entrie.delete(0, END) for entrie in self.entries]

    def update_lista(self, lista = None):
        # Atualiza a lista de clientes na interface
        self.lista_itens.delete(*self.lista_itens.get_children())
        if lista is None:
            lista = self.crud.read()
        for i in lista:
            self.lista_itens.insert("", END, values=i)

    def press_button(self, action):
        #É recomendável que ponha isso toda vez q um botão for apertado e altere as listas
        action
        self.update_lista()
        self.limpa_tela()

    def frames(self):
        self.top_row = Frame(self)
        self.top_row.pack(fill='both', expand=True, padx=10, pady=10)

        self.inputs = Frame(self)
        self.inputs.pack(fill='both', expand=True, padx=10, pady=10)

        self.bottom_row = Frame(self)
        self.bottom_row.pack(fill='both', expand=True, padx=10, pady=10)

    def widgets(self):
        self.entries = []
        self.labels = []

        self.id_label = Label(self.inputs, text="Código")
        self.id_entrie = Entry(self.inputs)
        self.id_label.grid(row=0,column=0)
        self.id_entrie.grid(row=0,column=1)

        for i,column in enumerate(self.crud.columns):
            label = Label(self.inputs, text=column.capitalize())
            entrie = Entry(self.inputs)
            label.grid(row=i+1,column=0)
            entrie.grid(row=i+1,column=1)
            self.entries.append(entrie)
            self.labels.append(label)

        def entries_content(): return [entrie_text.get() for entrie_text in self.entries]

        self.botoes = [Button(self.top_row, text="Limpar", command=self.limpa_tela),
                       Button(self.top_row, text="Buscar", command=lambda: self.update_lista(self.crud.search(entries_content()))),
                       Button(self.top_row, text="Novo", command=lambda: self.press_button(self.crud.insert(entries_content()))),
                       Button(self.top_row, text="Alterar", command=lambda: self.press_button(self.crud.update(entries_content(), f"id = {self.id_entrie.get()}"))),
                       Button(self.top_row, text="Apagar", command=lambda: self.press_button(self.crud.delete(f"id = {self.id_entrie.get()}")))]

        for i,botao in enumerate(self.botoes):
            botao.grid(row=0,column=i)

    def table(self):
        table_columns=[]
        table_columns.append("Código")
        for column in self.crud.columns:
            table_columns.append(column)

        # Criação da tabela no frame 2
        self.lista_itens = ttk.Treeview(self.bottom_row, columns=table_columns, show='headings')
        for column in table_columns:
            self.lista_itens.heading(column, text=column.capitalize())
            self.lista_itens.column(column, width=125)

        self.lista_itens.grid(row=0,column=0)

        self.scroll_lista = Scrollbar(self.bottom_row, orient='vertical')  # Barra de rolagem da lista
        self.lista_itens.configure(yscroll=self.scroll_lista.set)  # A barra pertence à lista
        self.scroll_lista.grid(row=0,column=1)
        self.lista_itens.bind("<Double-1>", self.double_click)
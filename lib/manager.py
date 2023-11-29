from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

PADDING_X = 10
PADDING_Y = 10
BACKGROUND_COLOR = '#444444'
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1
BUTTON_RELIEF = "raised"

class GenericManager(Frame):
    def __init__(self, crud, frame):
        super().__init__(frame)
        self.crud = crud
        self.nome_dado = self.crud.table_name.capitalize()

        self.configure(background=BACKGROUND_COLOR)

        self.frames()
        self.widgets()
        self.table()
        self.update_lista()

    def frames(self):
        frame_names = ['top_row', 'inputs', 'bottom_row']
        for name in frame_names:
            frame = Frame(self)
            if name == 'bottom_row':
                frame.pack(fill='both', expand=True, padx=PADDING_X, pady=PADDING_Y)
                frame.grid_columnconfigure(0, weight=1)
                frame.grid_rowconfigure(0, weight=1)
            else:
                frame.pack(padx=PADDING_X, pady=PADDING_Y)

            setattr(self, name, frame)

    def widgets(self):
        self.entries = []
        for i, column in enumerate(self.crud.columns):
            label = Label(self.inputs, text=column.capitalize())
            entry = DateEntry(self.inputs) if "data" in column else Entry(self.inputs)
            label.grid(row=0, column=i)
            entry.grid(row=1, column=i)
            self.entries.append(entry)

        self.botoes = [
            ("Novo", self.insert_button_pressed),
            ("Alterar", self.update_button_pressed),
            ("Buscar", self.search_button_pressed),
            ("Limpar", self.limpa_tela),
            ("Apagar", self.delete_button_pressed)
        ]

        for i, (text, command) in enumerate(self.botoes):
            Button(self.top_row, text=text, command=command, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, relief=BUTTON_RELIEF).grid(row=0, column=i)

    def table(self):
        table_columns = self.crud.columns

        self.lista_itens = ttk.Treeview(self.bottom_row, columns=table_columns, show='headings')
        for column in table_columns:
            self.lista_itens.heading(column, text=column.capitalize())
            self.lista_itens.column(column, anchor='center')

        for i in range(len(table_columns)):
            self.lista_itens.column(i, stretch=YES)

        self.lista_itens.grid(row=0, column=0, sticky="nsew")

        scroll_lista = Scrollbar(self.bottom_row, orient=VERTICAL, command=self.lista_itens.yview)
        self.lista_itens.configure(yscroll=scroll_lista.set)
        scroll_lista.grid(row=0, column=1, sticky="ns")
        self.lista_itens.bind("<Double-1>", self.double_click)

    def insert_button_pressed(self):
        self.crud.insert(self.get_entries_content())
        self.update_lista()
        self.limpa_tela()

    def update_button_pressed(self):
        self.crud.update(self.get_entries_content(), f"id = {self.get_entries_content()[0]}")
        self.update_lista()
        self.limpa_tela()

    def search_button_pressed(self):
        self.crud.search(self.get_entries_content())
        self.update_lista()

    def delete_button_pressed(self):
        self.crud.delete(f"id = {self.get_entries_content()[0]}")
        self.update_lista()
        self.limpa_tela()

    def limpa_tela(self):
        for entry in self.entries:
            entry.delete(0, END)

    def update_lista(self, lista=None):
        self.lista_itens.delete(*self.lista_itens.get_children())
        if lista is None:
            lista = self.crud.read()
        for item in lista:
            temp_lista = [GenericManager.unformat_date(element) if "data" in self.crud.columns[index] else element for index, element in enumerate(item)]
            self.lista_itens.insert("", END, values=temp_lista)

    def double_click(self, event):
        selected_row = self.lista_itens.selection()
        if selected_row:
            self.limpa_tela()
            for row_id in selected_row:
                columns = self.lista_itens.item(row_id, 'values')
                [entry.insert(END, col) for col, entry in zip(columns, self.entries)]

    @staticmethod
    def format_date(selected_date):
        return datetime.strftime(str(selected_date), "%Y%m%d")

    @staticmethod
    def unformat_date(selected_date):
        parsed_date = datetime.strptime(str(selected_date), '%Y%m%d')
        return parsed_date.strftime('%d/%m/%y')

    def get_entries_content(self):
        return [entry.get() if not isinstance(entry, DateEntry) else self.format_date(entry.get_date()) for entry in self.entries]
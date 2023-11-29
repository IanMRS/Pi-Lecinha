from tkinter import Frame, Label, Entry, Button, Scrollbar
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class GenericManager(Frame):
    def __init__(self, crud, frame):
        super().__init__(frame)
        self.crud = crud
        self.nome_dado = self.crud.table_name.capitalize()

        self.configure(background='#444444')

        self.frames()
        self.widgets()
        self.table()
        self.update_lista()

    def double_click(self, event):
        selected_row = self.lista_itens.selection()
        if selected_row:
            self.limpa_tela()
            for row_id in selected_row:
                columns = self.lista_itens.item(row_id, 'values')
                [entry.insert(END, col) for col, entry in zip(columns, self.entries)]

    def limpa_tela(self):
        [entry.delete(0, END) for entry in self.entries]

    def update_lista(self, lista=None):
        self.lista_itens.delete(*self.lista_itens.get_children())
        if lista is None:
            lista = self.crud.read()
        for item in lista:
            temp_lista = []
            for index,element in enumerate(item):
                if "data" in self.crud.columns[index]:
                    temp_lista.append(GenericManager.unformat_date(element))
                else:
                    temp_lista.append(element)

            self.lista_itens.insert("", END, values=temp_lista)

    def press_button(self, action):
        action
        self.update_lista()
        self.limpa_tela()

    def frames(self):
        self.top_row = Frame(self)
        self.top_row.pack(padx=10, pady=10)

        self.inputs = Frame(self)
        self.inputs.pack(padx=10, pady=10)

        self.bottom_row = Frame(self)
        self.bottom_row.pack(fill='both', expand=True, padx=10, pady=10)
        self.bottom_row.grid_columnconfigure(0, weight=1)
        self.bottom_row.grid_rowconfigure(0, weight=1)

    def widgets(self):
        self.entries = []
        for i, column in enumerate(self.crud.columns):
            label = Label(self.inputs, text=column.capitalize())
            if "data" in column:
                entry = DateEntry(self.inputs)
            else:
                entry = Entry(self.inputs)
            label.grid(row=0, column=i)
            entry.grid(row=1, column=i)
            self.entries.append(entry)

        def entries_content(): return [entrie_text.get() if not isinstance(entrie_text, DateEntry) else GenericManager.format_date(entrie_text.get_date()) for entrie_text in self.entries]

        self.botoes = [Button(self.top_row, text="Novo",    command=lambda: self.press_button(self.crud.insert(entries_content()))),
                       Button(self.top_row, text="Alterar", command=lambda: self.press_button(self.crud.update(entries_content(), f"id = {entries_content()[0]}"))),
                       Button(self.top_row, text="Buscar",  command=lambda: self.update_lista(self.crud.search(entries_content()))),
                       Button(self.top_row, text="Limpar",  command=self.limpa_tela),
                       Button(self.top_row, text="Apagar",  command=lambda: self.press_button(self.crud.delete(f"id = {entries_content()[0]}")))]

        for i, button in enumerate(self.botoes):
            button.grid(row=0, column=i)

    def table(self):
        table_columns = self.crud.columns

        self.lista_itens = ttk.Treeview(self.bottom_row, columns=table_columns, show='headings')
        for column in table_columns:
            self.lista_itens.heading(column, text=column.capitalize())
            self.lista_itens.column(column, anchor='center')

        for i in range(len(table_columns)):
            self.lista_itens.column(i, stretch=YES)

        self.lista_itens.grid(row=0, column=0, sticky="nsew")

        self.scroll_lista = Scrollbar(self.bottom_row, orient=VERTICAL, command=self.lista_itens.yview)
        self.lista_itens.configure(yscroll=self.scroll_lista.set)
        self.scroll_lista.grid(row=0, column=1, sticky="ns")
        self.lista_itens.bind("<Double-1>", self.double_click)

    @staticmethod
    def format_date(selected_date):
        formatted_date = datetime.strftime(str(selected_date), "%Y%m%d")
        return formatted_date

    @staticmethod
    def unformat_date(selected_date):
        parsed_date = datetime.strptime(str(selected_date), '%Y%m%d')

        formatted_date = parsed_date.strftime('%d/%m/%y')
        return formatted_date
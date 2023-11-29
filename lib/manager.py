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
        self.data_name = self.crud.table_name.capitalize()

        self.configure(background=BACKGROUND_COLOR)

        self.frames()
        self.widgets()
        self.table()

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

        self.buttons = [
            ("Novo", self.insert_button_pressed),
            ("Alterar", self.update_button_pressed),
            ("Buscar", self.search_button_pressed),
            ("Limpar", self.clear_inputs),
            ("Apagar", self.delete_button_pressed)
        ]

        for i, (text, command) in enumerate(self.buttons):
            Button(self.top_row, text=text, command=command, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, relief=BUTTON_RELIEF).grid(row=0, column=i)

    def table(self):
        table_columns = self.crud.columns

        self.item_table = ttk.Treeview(self.bottom_row, columns=table_columns, show='headings')
        for column in table_columns:
            self.item_table.heading(column, text=column.capitalize())
            self.item_table.column(column, anchor='center')

        for i in range(len(table_columns)):
            self.item_table.column(i, stretch=YES)

        self.item_table.grid(row=0, column=0, sticky="nsew")

        scroll_list = Scrollbar(self.bottom_row, orient=VERTICAL, command=self.item_table.yview)
        self.item_table.configure(yscroll=scroll_list.set)
        scroll_list.grid(row=0, column=1, sticky="ns")
        self.item_table.bind("<Double-1>", self.double_click)

        self.refresh_table()

    def insert_button_pressed(self):
        self.crud.insert(self.get_inputs_content())
        self.refresh_table()
        self.clear_inputs()

    def update_button_pressed(self):
        self.crud.update(self.get_inputs_content(), f"id = {self.get_inputs_content()[0]}")
        self.refresh_table()
        self.clear_inputs()

    def search_button_pressed(self):
        self.crud.search(self.get_inputs_content())
        self.refresh_table()

    def delete_button_pressed(self):
        self.crud.delete(f"id = {self.get_inputs_content()[0]}")
        self.refresh_table()
        self.clear_inputs()

    def clear_inputs(self):
        for entry in self.entries:
            entry.delete(0, END)

    def refresh_table(self, selected_list=None):
        self.item_table.delete(*self.item_table.get_children())
        if selected_list is None:
            selected_list = self.crud.read()
        for item in selected_list:
            temp_list = [GenericManager.unformat_date(element) if "data" in self.crud.columns[index] else element for index, element in enumerate(item)]
            self.item_table.insert("", END, values=temp_list)

    def double_click(self, event):
        selected_row = self.item_table.selection()
        if selected_row:
            self.clear_inputs()
            for row_id in selected_row:
                columns = self.item_table.item(row_id, 'values')
                for col, entry in zip(columns, self.entries):
                    entry.insert(END, col)

    @staticmethod
    def format_date(selected_date):
        return datetime.strftime(str(selected_date), "%Y%m%d")

    @staticmethod
    def unformat_date(selected_date):
        parsed_date = datetime.strptime(str(selected_date), '%Y%m%d')
        return parsed_date.strftime('%d/%m/%y')

    def get_inputs_content(self):
        return [entry.get() if not isinstance(entry, DateEntry) else self.format_date(entry.get_date()) for entry in self.entries]
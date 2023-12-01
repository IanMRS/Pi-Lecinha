from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from lib import crud as c
from lib import date_formatting as df
from lib.manager_table import ManagerTable

PADDING_X = 10
PADDING_Y = 10
BACKGROUND_COLOR = "#444444"
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1

class GenericManager(Frame):
    def __init__(self, crud, frame):
        super().__init__(frame)
        self.crud = crud
        self.data_name = self.crud.table_name.capitalize()
        self.columns_display_names = [column[3:].capitalize().replace("_", " ") if "id_" in column[:3] else "Código" if "id" in column[:2] else column.capitalize().replace("_", " ") for column in self.crud.columns]

        self.configure(background=BACKGROUND_COLOR)

        self.init_frames()
        self.init_inputs()
        self.init_widgets()

        self.data_table = ManagerTable(self,self.crud, self.columns_display_names)
        self.data_table.grid_columnconfigure(0, weight=1)
        self.data_table.grid_rowconfigure(0, weight=1)
        self.data_table.pack(fill="both", expand=True, padx=PADDING_X, pady=PADDING_Y)

        self.bind("<FocusIn>", self.init_keybinds)
        self.bind("<FocusOut>", self.stop_keybinds)

    def init_keybinds(self, event=None):
        shortcut_mapping = {
            "<Control-Return>": self.on_control_enter,
            "<Return>": self.on_enter,
            "<Control-BackSpace>": self.clear_button_pressed,
            "<Delete>": self.delete_button_pressed,
            "<Shift-BackSpace>": self.delete_button_pressed,
            "<Escape>": self.unselect_inputs,
            "<Double-1>": self.on_double_click
        }

        for key, command in shortcut_mapping.items():
            self.winfo_toplevel().bind(key, command)

        self.unselect_inputs()
        self.refresh_inputs()

    def stop_keybinds(self, event=None):
        for key in ["<Return>", "<Control-Return>", "<Control-BackSpace>", "<Shift-BackSpace>", "<Delete>", "<Escape>","<Double-1>"]:
            self.winfo_toplevel().unbind(key)

    def init_frames(self):
        frame_names = ["top_row", "inputs"]
        for name in frame_names:
            frame = Frame(self)
            frame.pack(padx=PADDING_X, pady=PADDING_Y)

            setattr(self, name, frame)

    def init_inputs(self):
        self.entries = []
        for column in self.crud.columns:
            if "data" in column:
                self.entries.append(DateEntry(self.inputs, date_pattern="dd/mm/yyyy"))
            elif "id_" in column[:3]:
                self.entries.append(self.create_id_dropdown(column))
            else:
                self.entries.append(Entry(self.inputs))

        for index, entry in enumerate(self.entries):
            self.create_label_and_entry(index, entry)

    def init_widgets(self):
        buttons = [
            ("Novo", self.insert_button_pressed),
            ("Alterar", self.update_button_pressed),
            ("Buscar", self.search_button_pressed),
            ("Limpar", self.clear_button_pressed),
            ("Apagar", self.delete_button_pressed)
        ]

        for i, (text, command) in enumerate(buttons):
            Button(self.top_row, text=text, command=command, width=BUTTON_WIDTH, height=BUTTON_HEIGHT).grid(row=0, column=i)

    def create_id_dropdown(self, column):
        temp_banco = column[3:]
        temp_search = c.BANCOS[temp_banco].read()

        while "id_" in c.BANCOS[temp_banco].columns[1]:
            temp_banco = c.BANCOS[temp_banco].columns[1][3:]
            temp_search = c.BANCOS[temp_banco].read()

        options = [element[1] for element in temp_search]
        return ttk.Combobox(self.inputs, values=options)

    def create_label_and_entry(self, column_index, entry):
        label_text = self.columns_display_names[column_index]
        label = Label(self.inputs, text=label_text)
        label.grid(row=0, column=column_index)
        entry.grid(row=1, column=column_index)

    def on_enter(self, event=None):
        (self.update_button_pressed if "" not in self.get_inputs_content() else self.search_button_pressed)()

    def on_control_enter(self, event=None):
        (self.insert_button_pressed if self.get_inputs_content()[0] == ""else self.update_button_pressed)()

    def on_double_click(self, event=None):
        selected_row = self.item_table.selection()
        if selected_row:
            self.clear_inputs()
            for row_id in selected_row:
                columns = self.item_table.item(row_id, "values")
                self.insert_values_in_inputs(columns)

    def insert_button_pressed(self, event=None):
        self.crud.insert(self.get_inputs_content())
        self.clear_button_pressed()

    def update_button_pressed(self, event=None):
        condition = f"id = {self.get_inputs_content()[0]}"
        self.crud.update(self.get_inputs_content(), condition)
        self.clear_button_pressed()

    def search_button_pressed(self, event=None):
        search_result = self.crud.search(self.get_inputs_content())
        self.refresh_table(search_result)
        self.clear_inputs()

        if len(search_result) == 1:
            self.insert_values_in_inputs(search_result[0])

    def delete_button_pressed(self, event=None):
        self.popup = Toplevel()
        self.popup.title("Confirmação")

        label = Label(self.popup, text=f"Você tem certeza?")
        label.pack(padx=PADDING_X, pady=PADDING_Y)

        yes_button = Button(self.popup, text="Sim", command=self.delete_confirmed)
        yes_button.pack(side="left", padx=PADDING_X)

        no_button = Button(self.popup, text="Não", command=self.popup.destroy)
        no_button.pack(side="right", padx=PADDING_X)

        self.popup.wait_window()

    def delete_confirmed(self):
        self.crud.delete(f"id = {self.get_inputs_content()[0]}")
        self.clear_button_pressed()
        self.popup.destroy()

    def clear_button_pressed(self, event=None):
        self.refresh_table()
        self.clear_inputs()
        self.unselect_inputs()

    def clear_inputs(self, event=None):
        for entry in self.entries:
            entry.delete(0, END)

    def insert_values_in_inputs(self, values):
        for col, entry in zip(values, self.entries):
            entry.insert(END, col)

    def unselect_inputs(self, event=None):
        self.focus_set()

    def refresh_inputs(self):
        for index, entry in enumerate(self.entries):
            if isinstance(entry, ttk.Combobox):
                self.refresh_dropdowns(entry, index)

    def refresh_dropdowns(self, entry, index):
        banco_anterior = self.crud.table_name
        temp_banco = self.crud.columns[index][3:]
        temp_search = c.BANCOS[temp_banco].read()

        while "id_" in c.BANCOS[temp_banco].columns[1]:
            banco_anterior = temp_banco
            temp_banco = c.BANCOS[temp_banco].columns[1][3:]
            temp_search = c.BANCOS[temp_banco].db_input(f"SELECT c.* FROM {temp_banco} c JOIN {banco_anterior} a ON c.id = a.id_{temp_banco};").fetchall()

        options = [element[1] for element in temp_search]
        entry["values"] = options

    def get_inputs_content(self):
        inputs = []
        for entry in self.entries:
            if isinstance(entry, DateEntry):
                inputs.append(df.format_date(entry.get_date()))
            elif isinstance(entry, ttk.Combobox):
                inputs.append(entry.current() + 1)
            else:
                inputs.append(entry.get())

        return inputs
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from lib import crud as c 

PADDING_X = 10
PADDING_Y = 10
BACKGROUND_COLOR = "#444444"
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1
BUTTON_RELIEF = "raised"

class GenericManager(Frame):
    def __init__(self, crud, frame):
        super().__init__(frame)
        self.crud = crud
        self.data_name = self.crud.table_name.capitalize()

        self.configure(background=BACKGROUND_COLOR)

        self.init_frames()
        self.init_inputs()
        self.init_widgets()
        self.init_table()

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
        }

        for key, command in shortcut_mapping.items():
            self.winfo_toplevel().bind(key, command)

        self.unselect_inputs()
        self.refresh_inputs()

    def stop_keybinds(self, event=None):
        self.winfo_toplevel().unbind("<Return>")
        self.winfo_toplevel().unbind("<Control-Return>")
        self.winfo_toplevel().unbind("<Control-BackSpace>")
        self.winfo_toplevel().unbind("<Shift-BackSpace>")
        self.winfo_toplevel().unbind("<Delete>")
        self.winfo_toplevel().unbind("<Escape>")

    def init_frames(self):
        frame_names = ["top_row", "inputs", "bottom_row"]
        for name in frame_names:
            frame = Frame(self)
            if name == "bottom_row":
                frame.pack(fill="both", expand=True, padx=PADDING_X, pady=PADDING_Y)
                frame.grid_columnconfigure(0, weight=1)
                frame.grid_rowconfigure(0, weight=1)
            else:
                frame.pack(padx=PADDING_X, pady=PADDING_Y)

            setattr(self, name, frame)

    def init_inputs(self):
        self.entries = []
        for column in self.crud.columns:
            if "data" in column:
                self.entries.append(DateEntry(self.inputs, date_pattern="dd/mm/yyyy"))
            elif "id_" in column[:3]:
                temp_banco = column[3:]
                temp_search = c.BANCOS[temp_banco].read()

                while "id_" in c.BANCOS[temp_banco].columns[1]:
                    temp_banco = c.BANCOS[temp_banco].columns[1][3:]
                    temp_search = c.BANCOS[temp_banco].read()

                options = [element[1] for element in temp_search]
                dropdown = ttk.Combobox(self.inputs, values=options)
                self.entries.append(dropdown)
            else:
                self.entries.append(Entry(self.inputs))

        for i, (column, entry) in enumerate(zip(self.crud.columns, self.entries)):
            column_text = column 
            if "id_" in column[:3]:
                label = Label(self.inputs, text=column[3:].capitalize())
            else:
                label = Label(self.inputs, text=column.capitalize())
            label.grid(row=0, column=i)
            entry.grid(row=1, column=i)

    def refresh_inputs(self):
        for index, entry in enumerate(self.entries):
            if isinstance(entry, ttk.Combobox):
                banco_anterior = self.crud.table_name
                temp_banco = self.crud.columns[index][3:]
                temp_search = c.BANCOS[temp_banco].read()

                while "id_" in c.BANCOS[temp_banco].columns[1]:
                    banco_anterior = temp_banco
                    temp_banco = c.BANCOS[temp_banco].columns[1][3:]
                    temp_search = c.BANCOS[temp_banco].db_input(f"SELECT c.* FROM {temp_banco} c JOIN {banco_anterior} a ON c.id = a.id_{temp_banco};").fetchall()

                options = [element[1] for element in temp_search]
                entry["values"] = options     

    def init_widgets(self):
        self.buttons = [
            ("Novo", self.insert_button_pressed),
            ("Alterar", self.update_button_pressed),
            ("Buscar", self.search_button_pressed),
            ("Limpar", self.clear_button_pressed),
            ("Apagar", self.delete_button_pressed)
        ]

        for i, (text, command) in enumerate(self.buttons):
            Button(self.top_row, text=text, command=command, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, relief=BUTTON_RELIEF).grid(row=0, column=i)

    def init_table(self):
        table_columns = self.crud.columns

        self.item_table = ttk.Treeview(self.bottom_row, columns=table_columns, show="headings")
        for column in table_columns:
            column_text = column 
            if "id_" in column[:3]:
                self.item_table.heading(column, text=column[3:].capitalize())
            else:
                self.item_table.heading(column, text=column.capitalize())
            self.item_table.column(column, anchor="center")

        for i in range(len(table_columns)):
            self.item_table.column(i, stretch=YES)

        self.item_table.grid(row=0, column=0, sticky="nsew")

        scroll_list = Scrollbar(self.bottom_row, orient=VERTICAL, command=self.item_table.yview)
        self.item_table.configure(yscroll=scroll_list.set)
        scroll_list.grid(row=0, column=1, sticky="ns")
        self.item_table.bind("<Double-1>", self.double_click)

        self.refresh_table()

    def insert_button_pressed(self, event=None):
        self.crud.insert(self.get_inputs_content())
        self.clear_button_pressed()

    def update_button_pressed(self, event=None):
        condition = f"id = {self.get_inputs_content()[0]}"
        self.crud.update(self.get_inputs_content(), condition)
        self.clear_button_pressed()

    def on_enter(self, event=None):
        (self.update_button_pressed if "" not in self.get_inputs_content()  else self.search_button_pressed)()

    def on_control_enter(self, event=None):
        (self.insert_button_pressed if self.get_inputs_content()[0] == "" else self.update_button_pressed)()

    def search_button_pressed(self, event=None):
        search_result = self.crud.search(self.get_inputs_content())
        self.refresh_table(search_result)
        self.clear_inputs()

        if len(search_result) == 1:
            for col, entry in zip(search_result[0], self.entries):
                entry.insert(END, col)

    def delete_button_pressed(self, event=None):
        def delete_confirmed():
            self.crud.delete(f"id = {self.get_inputs_content()[0]}")
            self.clear_button_pressed()
            popup.destroy()

        popup = Toplevel()
        popup.title("Confirmação")

        label = Label(popup, text=f"Você tem certeza?")
        label.pack(padx=PADDING_X, pady=PADDING_Y)

        yes_button = Button(popup, text="Sim", command=lambda: delete_confirmed())
        yes_button.pack(side="left", padx=PADDING_X)

        no_button = Button(popup, text="Não", command=lambda: popup.destroy())
        no_button.pack(side="right", padx=PADDING_X)

        popup.wait_window()

    def clear_button_pressed(self, event=None):
        self.refresh_table()
        self.clear_inputs()
        self.unselect_inputs()

    def clear_inputs(self, event=None):
        for entry in self.entries:
            entry.delete(0, END)

    def unselect_inputs(self, event=None):
        self.focus_set()

    def refresh_table(self, table_values = None):
        table_values = self.crud.read() if table_values is None else table_values
        self.item_table.delete(*self.item_table.get_children())
        for item in table_values:
            temp_list = []
            for index, element in enumerate(item):
                if "data" in self.crud.columns[index]:
                    temp_list.append(GenericManager.unformat_date(element))
                elif "id_" in self.crud.columns[index][:3]:
                    temp_banco = self.crud.columns[index][3:]
                    temp_search = c.BANCOS[temp_banco].read()

                    temp_element = temp_search[element-1][1]
                    current_index = temp_search[element-1][0]
                    extracted_index = temp_search[index-1][1]

                    temp_element1 = None
                    while "id_" in c.BANCOS[temp_banco].columns[1]:
                        temp_banco = c.BANCOS[temp_banco].columns[1][3:]
                        temp_search = c.BANCOS[temp_banco].read()

                        temp_element1 = temp_search[temp_element-1][1]

                    temp_list.append(temp_element1 if temp_element1 is not None else temp_element)
                else:
                    temp_list.append(element)
            self.item_table.insert("", END, values=temp_list)

    def double_click(self, event=None):
        selected_row = self.item_table.selection()
        if selected_row:
            self.clear_inputs()
            for row_id in selected_row:
                columns = self.item_table.item(row_id, "values")
                for col, entry in zip(columns, self.entries):
                    entry.insert(END, col)

    @staticmethod
    def format_date(selected_date):
        if isinstance(selected_date, str):
            return selected_date
        return datetime.strftime(selected_date, "%Y%m%d")

    @staticmethod
    def unformat_date(selected_date):
        parsed_date = datetime.strptime(str(selected_date), "%Y%m%d")
        return parsed_date.strftime("%d/%m/%y")

    def get_inputs_content(self):
        inputs = []
        for entry in self.entries:
            if isinstance(entry, DateEntry):
                inputs.append(self.format_date(entry.get_date()))
            elif isinstance(entry, ttk.Combobox):
                inputs.append(entry.current()+1)
            else:
                inputs.append(entry.get())
                
        return inputs
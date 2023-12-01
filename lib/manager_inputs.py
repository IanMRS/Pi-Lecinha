from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from lib import crud as c
from lib import date_formatting as df

class ManagerInputs(Frame):
    def __init__(self,frame,crud):
        super().__init__(frame)
        self.crud = crud
        self.entries = []
        for column in self.crud.columns:
            if "data" in column:
                self.entries.append(DateEntry(self, date_pattern="dd/mm/yyyy"))
            elif "id_" in column[:3]:
                self.entries.append(self.create_id_dropdown(column))
            else:
                self.entries.append(Entry(self))

        for index, entry in enumerate(self.entries):
            self.create_label_and_entry(index, entry)

    def create_id_dropdown(self, column):
        temp_banco = column[3:]
        temp_search = c.BANCOS[temp_banco].read()

        while "id_" in c.BANCOS[temp_banco].columns[1]:
            temp_banco = c.BANCOS[temp_banco].columns[1][3:]
            temp_search = c.BANCOS[temp_banco].read()

        options = [element[1] for element in temp_search]
        return ttk.Combobox(self, values=options)

    def create_label_and_entry(self, column_index, entry):
        label_text = self.crud.columns_display_names[column_index]
        label = Label(self, text=label_text)
        label.grid(row=0, column=column_index)
        entry.grid(row=1, column=column_index)

    def clear(self, event=None):
        for entry in self.entries:
            entry.delete(0, END)

    def insert(self, values):
        for col, entry in zip(values, self.entries):
            entry.insert(END, col)

    def unselect(self, event=None):
        self.focus_set()

    def refresh(self):
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

    def get(self):
        inputs = []
        for entry in self.entries:
            if isinstance(entry, DateEntry):
                inputs.append(df.format_date(entry.get_date()))
            elif isinstance(entry, ttk.Combobox):
                inputs.append(entry.current() + 1)
            else:
                inputs.append(entry.get())

        return inputs
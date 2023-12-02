from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from lib import crud as c
from lib import date_formatting as df

class ManagerInputs(Frame):
    """A class representing input fields for CRUD operations in a Tkinter interface."""

    def __init__(self, frame, crud):
        """
        Initialize the ManagerInputs instance.

        Parameters:
        - frame: The Tkinter frame to which the ManagerInputs belongs.
        - crud: An instance of CRUD operations for managing data.
        """
        super().__init__(frame)
        self.crud = crud
        self.entries = []

        # Create input fields for each column in the CRUD operation
        for column in self.crud.columns:
            if "data" in column:
                self.entries.append(DateEntry(self, date_pattern="dd/mm/yyyy"))
            elif "id_" in column[:3]:
                self.entries.append(self.create_id_dropdown(column))
            else:
                self.entries.append(Entry(self))

        # Grid labels and entries for each column
        for index, entry in enumerate(self.entries):
            self.create_label_and_entry(index, entry)

    def create_id_dropdown(self, column):
        """
        Create a dropdown (Combobox) for ID columns.

        Parameters:
        - column: The ID column name.

        Returns:
        A ttk.Combobox representing the ID dropdown.
        """
        nome_banco = column[3:]
        temp_search = c.BANCOS[nome_banco].read()

        while "id_" in c.BANCOS[nome_banco].columns[1]:
            nome_banco = c.BANCOS[nome_banco].columns[1][3:]
            temp_search = c.BANCOS[nome_banco].read()

        options = [element[1] for element in temp_search]
        return ttk.Combobox(self, values=options)

    def create_label_and_entry(self, column_index, entry):
        """
        Create a label and entry field for a column.

        Parameters:
        - column_index: The index of the column.
        - entry: The input field for the column.
        """
        label_text = self.crud.columns_display_names[column_index]
        label = Label(self, text=label_text)
        label.grid(row=0, column=column_index)
        entry.grid(row=1, column=column_index)

    def clear(self, event=None):
        """Clear all input fields."""
        for entry in self.entries:
            entry.delete(0, END)

    def insert(self, values):
        """
        Insert values into the input fields.

        Parameters:
        - values: The values to be inserted into the input fields.
        """
        for col, entry in zip(values, self.entries):
            entry.insert(END, col)

    def unselect(self, event=None):
        """Unselect the input fields."""
        self.focus_set()

    def refresh(self):
        """Refresh the input fields."""
        for index, entry in enumerate(self.entries):
            if isinstance(entry, ttk.Combobox):
                self.refresh_dropdowns(entry, index)

    def refresh_dropdowns(self, entry, index):
        """
        Refresh the options for a dropdown (Combobox).

        Parameters:
        - entry: The Combobox to be refreshed.
        - index: The index of the column associated with the Combobox.
        """
        banco_anterior = self.crud.table_name
        nome_banco = self.crud.columns[index][3:]
        temp_search = c.BANCOS[nome_banco].read()

        while "id_" in c.BANCOS[nome_banco].columns[1]:
            banco_anterior = nome_banco
            nome_banco = c.BANCOS[nome_banco].columns[1][3:]
            temp_search = c.BANCOS[nome_banco].db_input(f"SELECT c.* FROM {nome_banco} c JOIN {banco_anterior} a ON c.id = a.id_{nome_banco};").fetchall()

        options = [element[1] for element in temp_search]
        entry["values"] = options

    def get(self):
        """
        Get the values from the input fields.

        Returns:
        A list of values from the input fields.
        """
        inputs = []
        for entry in self.entries:
            if isinstance(entry, DateEntry):
                inputs.append(df.format_date(entry.get_date()))
            elif isinstance(entry, ttk.Combobox):
                inputs.append(entry.current() + 1)
            else:
                inputs.append(entry.get())

        return inputs
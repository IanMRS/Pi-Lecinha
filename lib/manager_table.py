from tkinter import *
from tkinter import ttk
from lib import date_formatting as df
from lib import crud as c

class ManagerTable(Frame):
    """A class representing a table manager using Tkinter."""

    def __init__(self, frame, crud):
        """
        Initialize the ManagerTable instance.

        Parameters:
        - frame: The Tkinter frame to which the ManagerTable belongs.
        - crud: An instance of CRUD operations for managing data.
        """
        super().__init__(frame)

        self.crud = crud
        self.table_columns = self.crud.columns
        self.display_names = self.crud.columns_display_names

        self.item_table = ttk.Treeview(self, columns=self.table_columns, show="headings")

        for index, column in enumerate(self.table_columns):
            self.create_table_heading(index, column)
            self.configure_table_column(column)

        self.create_table_and_scroll_list()

        self.refresh()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def refresh(self, table_values=None):
        """
        Refresh the table with updated data.

        Parameters:
        - table_values: Optional parameter to specify the data for the table.
        """
        table_values = self.crud.read() if table_values is None else table_values
        self.item_table.delete(*self.item_table.get_children())
        for item in table_values:
            temp_list = self.process_table_values(item)
            self.item_table.insert("", END, values=temp_list)

    def process_table_values(self, item):
        """
        Process table values before inserting into the table.

        Parameters:
        - item: A list representing a row of data from the CRUD operations.

        Returns:
        A processed list of values for displaying in the table.
        """
        processed_values = []
        for col, element in zip(self.table_columns, item):
            if "data" in col:
                processed_values.append(df.unformat_date(element))
            elif "id_" in col[:3]:
                processed_values.append(self.process_id_column(col, element))
            else:
                processed_values.append(element)
        return processed_values

    def process_id_column(self, column, element):
        """
        Process ID columns to fetch corresponding values from related tables.

        Parameters:
        - column: The ID column name.
        - element: The ID element to be processed.

        Returns:
        The processed value corresponding to the ID.
        """
        temp_banco = column[3:]
        temp_search = c.BANCOS[temp_banco].read()
        temp_element = temp_search[element - 1][1]
        
        current_index = temp_search[element - 1][0]

        while "id_" in c.BANCOS[temp_banco].columns[1]:
            temp_banco = c.BANCOS[temp_banco].columns[1][3:]
            temp_search = c.BANCOS[temp_banco].read()
            temp_element = temp_search[temp_element - 1][1]
        return temp_element

    def create_table_heading(self, column_index, column):
        """
        Set table heading text.

        Parameters:
        - column_index: The index of the column.
        - column: The name of the column.
        """
        column_text = self.display_names[column_index]
        self.item_table.heading(column, text=column_text)

    def create_table_and_scroll_list(self):
        """Configure grid layout for the table and scrollbar."""
        self.item_table.grid(row=0, column=0, sticky="nsew")

        scroll_list = Scrollbar(self, orient=VERTICAL, command=self.item_table.yview)
        self.item_table.configure(yscroll=scroll_list.set)
        scroll_list.grid(row=0, column=1, sticky="ns")

    def configure_table_column(self, column):
        """
        Configure table column alignment.

        Parameters:
        - column: The name of the column.
        """
        self.item_table.column(column, anchor="center")
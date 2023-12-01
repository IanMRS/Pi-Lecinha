from tkinter import *
from tkinter import ttk
from lib import date_formatting as df
from lib import crud as c

class ManagerTable(Frame):
    def __init__(self,frame,crud):
        super().__init__(frame)

        self.crud = crud
        self.table_columns = self.crud.columns
        self.display_names = self.crud.columns_display_names

        self.item_table = ttk.Treeview(self, columns=self.table_columns, show="headings")
        for index, column in enumerate(self.table_columns):
            self.create_table_heading(index, column)
            self.configure_table_column(column)

        self.create_table_and_scroll_list()

        self.refresh_table()

    def refresh_table(self, table_values=None):
        table_values = self.crud.read() if table_values is None else table_values
        self.item_table.delete(*self.item_table.get_children())
        for item in table_values:
            temp_list = self.process_table_values(item)
            self.item_table.insert("", END, values=temp_list)

    def process_table_values(self, item):
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
        temp_banco = column[3:]
        temp_search = c.BANCOS[temp_banco].read()
        temp_element = temp_search[element-1][1]
        
        current_index = temp_search[element-1][0]

        while "id_" in c.BANCOS[temp_banco].columns[1]:
            temp_banco = c.BANCOS[temp_banco].columns[1][3:]
            temp_search = c.BANCOS[temp_banco].read()

            temp_element = temp_search[temp_element-1][1]
        return temp_element

    def create_table_heading(self, column_index, column):
        column_text = self.display_names[column_index]
        self.item_table.heading(column, text=column_text)

    def create_table_and_scroll_list(self):
        self.item_table.grid(row=0, column=0, sticky="nsew")

        scroll_list = Scrollbar(self, orient=VERTICAL, command=self.item_table.yview)
        self.item_table.configure(yscroll=scroll_list.set)
        scroll_list.grid(row=0, column=1, sticky="ns")

    def configure_table_column(self, column):
        self.item_table.column(column, anchor="center")
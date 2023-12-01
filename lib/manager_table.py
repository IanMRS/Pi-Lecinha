from tkinter import *
from tkinter import ttk, messagebox
from lib import date_formatting as df
from lib import crud as c

class ManagerTable(Frame):
    def __init__(self,frame,crud,columns_display_names):
        super().__init__(frame)

        self.crud = crud
        self.table_columns = self.crud.columns
        self.display_names = columns_display_names

        self.item_table = ttk.Treeview(self, columns=self.table_columns, show="headings")
        for index, column in enumerate(self.table_columns):
            self.create_table_heading(index, column)
            self.configure_table_column(column)

        self.create_table_and_scroll_list()

        self.refresh_table()

    def refresh_table(self, table_values = None):
        table_values = self.crud.read() if table_values is None else table_values
        self.item_table.delete(*self.item_table.get_children())
        for item in table_values:
            temp_list = []
            for index, element in enumerate(item):
                if "data" in self.table_columns[index]:
                    temp_list.append(df.unformat_date(element))
                elif "id_" in self.table_columns[index][:3]:
                    temp_banco = self.table_columns[index][3:]
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
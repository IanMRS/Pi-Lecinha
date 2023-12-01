from tkinter import *
from tkinter import ttk, messagebox

class ManagerButtons(Frame):
    BUTTON_WIDTH = 10
    BUTTON_HEIGHT = 1
    PADDING_X = 10
    PADDING_Y = 10

    def __init__(self,frame,crud,inputs,table):
        super().__init__(frame)
        self.crud = crud
        self.inputs = inputs
        self.table = table
        buttons = [
            ("Novo", self.insert_button_pressed),
            ("Alterar", self.update_button_pressed),
            ("Buscar", self.search_button_pressed),
            ("Limpar", self.clear_button_pressed),
            ("Apagar", self.delete_button_pressed)
        ]

        for i, (text, command) in enumerate(buttons):
            Button(self, text=text, command=command, width=BUTTON_WIDTH, height=BUTTON_HEIGHT).grid(row=0, column=i)

    def insert_button_pressed(self, event=None):
        self.crud.insert(self.inputs.get())
        self.clear_button_pressed()

    def update_button_pressed(self, event=None):
        condition = f"id = {self.inputs.get()[0]}"
        self.crud.update(self.inputs.get(), condition)
        self.clear_button_pressed()

    def search_button_pressed(self, event=None):
        search_result = self.crud.search(self.inputs.get())
        self.table.refresh(search_result)
        self.inputs.clear()

        if len(search_result) == 1:
            self.inputs.insert(search_result[0])

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
        self.crud.delete(f"id = {self.inputs.get()[0]}")
        self.clear_button_pressed()
        self.popup.destroy()

    def clear_button_pressed(self, event=None):
        self.table.refresh()
        self.inputs.clear()
        self.inputs.unselect()

    def init_keybinds(self, event=None):
        shortcut_mapping = {
            "<Control-Return>": self.on_control_enter,
            "<Return>": self.on_enter,
            "<Control-BackSpace>": self.clear_button_pressed,
            "<Delete>": self.delete_button_pressed,
            "<Shift-BackSpace>": self.delete_button_pressed,
            "<Escape>": self.inputs.unselect,
            "<Double-1>": self.on_double_click
        }

        for key, command in shortcut_mapping.items():
            self.winfo_toplevel().bind(key, command)

        self.inputs.unselect()
        self.inputs.refresh()

    def stop_keybinds(self, event=None):
        for key in ["<Return>", "<Control-Return>", "<Control-BackSpace>", "<Shift-BackSpace>", "<Delete>", "<Escape>", "<Double-1>"]:
            self.winfo_toplevel().unbind(key)

    def on_enter(self, event=None):
        (self.update_button_pressed if "" not in self.inputs.get() else self.search_button_pressed)()

    def on_control_enter(self, event=None):
        (self.insert_button_pressed if self.inputs.get()[0] == ""else self.update_button_pressed)()

    def on_double_click(self, event=None):
        selected_row = self.table.item_table.selection()
        if selected_row:
            self.inputs.clear()
            for row_id in selected_row:
                columns = self.table.item_table.item(row_id, "values")
                self.inputs.insert(columns)
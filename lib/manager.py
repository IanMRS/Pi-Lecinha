from tkinter import Frame
from lib.manager_table import ManagerTable
from lib.manager_inputs import ManagerInputs
from lib.manager_buttons import ManagerButtons

class GenericManager(Frame):
    PADDING_X = 10
    PADDING_Y = 10
    BACKGROUND_COLOR = "#444444"
    
    def __init__(self, crud, frame = None):
        self.crud = crud
        self.data_name = self.crud.table_name.capitalize()
        print(f"\nAdmin. {self.data_name}: Inicializando")

        super().__init__(frame)
        self.configure_widgets()
        self.pack_widgets()

        self.bind("<FocusIn>", self.buttons.init_keybinds)
        self.bind("<FocusOut>", self.buttons.stop_keybinds)

    def configure_widgets(self):
        print(f"Admin. {self.data_name}: Configurando Widgets")
        self.configure(background=BACKGROUND_COLOR)

        self.inputs = ManagerInputs(self, self.crud)
        self.table = ManagerTable(self, self.crud)
        self.buttons = ManagerButtons(self, self.crud, self.inputs, self.table)

    def pack_widgets(self):
        print(f"Admin. {self.data_name}: Empacotando Widgets")
        self.buttons.pack(padx=PADDING_X, pady=PADDING_Y)
        self.inputs.pack(padx=PADDING_X, pady=PADDING_Y)
        self.table.pack(fill="both", expand=True, padx=PADDING_X, pady=PADDING_Y)

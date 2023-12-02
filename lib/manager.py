from tkinter import Frame
from lib.manager_table import ManagerTable
from lib.manager_inputs import ManagerInputs
from lib.manager_buttons import ManagerButtons

class GenericManager(Frame):
    """A generic manager for handling CRUD operations with a Tkinter interface."""

    # Class constants
    PADDING_X = 10
    PADDING_Y = 10
    BACKGROUND_COLOR = "#444444"
    
    def __init__(self, crud, frame=None):
        """
        Initialize the GenericManager instance.

        Parameters:
        - crud: An instance of CRUD operations for managing data.
        - frame: The Tkinter frame to which the GenericManager belongs.
        """
        self.crud = crud
        self.data_name = self.crud.table_name.capitalize()
        print(f"\nAdmin. {self.data_name}: Inicializando")

        super().__init__(frame)
        self.configure_widgets()
        self.pack_widgets()

        # Bind key events for focus in and out
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self,event=None):
        self.crud.start_connection()
        self.buttons.init_keybinds()

    def on_focus_out(self,event=None):
        self.buttons.stop_keybinds()
        self.crud.stop_connection()


    def configure_widgets(self):
        """
        Configure widgets for the GenericManager.

        This method initializes and configures the necessary widgets for the manager.
        """
        print(f"Admin. {self.data_name}: Configurando Widgets")
        self.configure(background=self.BACKGROUND_COLOR)

        self.inputs = ManagerInputs(self, self.crud)
        self.table = ManagerTable(self, self.crud)
        self.buttons = ManagerButtons(self, self.crud, self.inputs, self.table)

    def pack_widgets(self):
        """
        Pack widgets into the GenericManager.

        This method packs the configured widgets into the manager's frame.
        """
        print(f"Admin. {self.data_name}: Empacotando Widgets")
        self.buttons.pack(padx=self.PADDING_X, pady=self.PADDING_Y)
        self.inputs.pack(padx=self.PADDING_X, pady=self.PADDING_Y)
        self.table.pack(fill="both", expand=True, padx=self.PADDING_X, pady=self.PADDING_Y)
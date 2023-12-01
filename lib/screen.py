from tkinter import ttk

from lib.window import FullScreenWindow
from lib.notebook import MainNotebook

class MainScreen(FullScreenWindow):
    def __init__(self):
        super().__init__("Administrar aluguel de temporada")
        self.root.configure(background="#444444")
        self.main_notebook = MainNotebook(self.root)
        self.main_notebook.pack(fill="both", expand=True)
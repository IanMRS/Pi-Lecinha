from tkinter import ttk

from lib.window import FullScreenWindow
from lib.notebook import MainNotebook

class MainScreen(FullScreenWindow):
    """A class representing the main screen for managing vacation rentals."""

    def __init__(self):
        """Initialize the MainScreen instance."""
        super().__init__("Administrar aluguel de temporada")
        self.root.configure(background="#444444")
        self.main_notebook = MainNotebook(self.root)
        self.main_notebook.pack(fill="both", expand=True)
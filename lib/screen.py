from tkinter import ttk

from lib.window import FullScreenWindow
from lib.manager import GenericManager
from lib import crud
from lib.calendario import GUICalendar
from lib.dashboard import FinanceiroApp

class MainScreen(FullScreenWindow):
    def __init__(self):
        super().__init__("Administrar aluguel de temporada")

        self.create_widgets()
        self.configure_layout()

        self.root.configure(background="#444444")
        self.start()
        
    
    def create_widgets(self):
        self.main_notebook = ttk.Notebook(self.root)

        abas = [
            ("Dashboard Financeiro",FinanceiroApp(self.main_notebook)),
            ("Clientes",            GenericManager(crud.BANCOS["cliente"],self.main_notebook)),
            ("Casas",               GenericManager(crud.BANCOS["casa"],self.main_notebook)),
            ("Sites",               GenericManager(crud.BANCOS["origem"],self.main_notebook)),
            ("Alugueis",            GenericManager(crud.BANCOS["aluguel"],self.main_notebook)),
            ("Aluguel-Casa",        GenericManager(crud.BANCOS["aluguel_has_casa"],self.main_notebook)),
            ("Calendário",          GUICalendar(self.main_notebook))]
            
        for titulo, aba in abas:
            self.main_notebook.add(aba, text = titulo)       


    def configure_layout(self):
        self.main_notebook.pack(fill="both", expand=True)
from tkinter import *
from tkinter import ttk

from lib.window import Window
from lib.manager import GenericManager
from lib import crud
from lib.calendario import Calendario
from lib.dashboard import FinanceiroApp

class MainScreen(Window):
    def __init__(self):
        super().__init__()

        self.frames_da_tela()

        self.root.title(f"Administrar aluguel de temporada")
        self.root.configure(background='#444444')
        
    
    def frames_da_tela(self):
        self.notebook = ttk.Notebook(self.root)  # Criar o Notebook

        abas = [('Dashboard Financeiro',    FinanceiroApp(self.notebook)),
                ('Clientes',                GenericManager(crud.bancos["cliente"],self.notebook)),
                ('Casas',                   GenericManager(crud.bancos["casa"],self.notebook)),
                ('Sites',                   GenericManager(crud.bancos["origem"],self.notebook)),
                ('Alugueis',                GenericManager(crud.bancos["aluguel"],self.notebook)),
                ('Aluguel-Casa',            GenericManager(crud.bancos["aluguel_has_casa"],self.notebook)),
                ('Calendário',              Calendario(self.notebook))]
            
        for titulo, aba in abas:                        # Adicionar as abas
            self.notebook.add(aba, text = titulo)       

        self.notebook.pack(fill='both', expand=True)    # Empacotar o Notebook para exibição

tela = MainScreen()
tela.start()
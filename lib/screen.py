from tkinter import *
from tkinter import ttk

from lib.window import Window
from lib.manager import GenericManager
from lib import crud
from lib.calendario import Calendario
from lib.dashboard import FinanceiroApp

class MainScreen(w.Window):
    def __init__(self):
        self.main_window=Tk()
        self.frames_da_tela()
        self.menus()

        self.main_window.title(f"Administrar aluguel de temporada")
        self.main_window.configure(background='#444444')
        self.main_window.resizable(False, False)
        
    
    def frames_da_tela(self):
        self.notebook = ttk.Notebook(self.main_window)  # Criar o Notebook

        abas = [('Dashboard Financeiro',    d.FinanceiroApp(self.notebook)),
                ('Clientes',                man.GenericManager(crud.bancos["cliente"],self.notebook)),
                ('Casas',                   man.GenericManager(crud.bancos["casa"],self.notebook)),
                ('Sites',                   man.GenericManager(crud.bancos["origem"],self.notebook)),
                ('Alugueis',                man.GenericManager(crud.bancos["aluguel"],self.notebook)),
                ('Aluguel-Casa',            man.GenericManager(crud.bancos["aluguel_has_casa"],self.notebook)),
                ('Calendário',              car.Calendario(self.notebook))]
            
        for titulo, aba in abas:
            self.notebook.add(aba, text = titulo)

        self.notebook.pack(fill='both', expand=True)  # Empacotar o Notebook para exibição

tela = MainScreen()
tela.start()
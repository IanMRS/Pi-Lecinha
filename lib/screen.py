from tkinter import *
from tkinter import ttk
from lib import window as w
from lib import manager as man
from lib import crud as c
from lib import calendario as car
from lib import dashboard as d

class MainScreen(w.Window):
    def __init__(self):
        self.root=Tk()
        self.frames_da_tela()
        self.menus()

        self.root.title(f"Administrar aluguel de temporada")
        self.root.configure(background='#444444')
        self.root.resizable(False, False)
        
    
    def frames_da_tela(self):
        self.notebook = ttk.Notebook(self.root)  # Criar o Notebook

        abas = [('Dashboard Financeiro',    d.FinanceiroApp(self.notebook)),
                ('Clientes',                man.GenericManager(c.bancos["cliente"],self.notebook)),
                ('Casas',                   man.GenericManager(c.bancos["casa"],self.notebook)),
                ('Sites',                   man.GenericManager(c.bancos["origem"],self.notebook)),
                ('Alugueis',                man.GenericManager(c.bancos["aluguel"],self.notebook)),
                ('Aluguel-Casa',            man.GenericManager(c.bancos["aluguel_has_casa"],self.notebook)),
                ('Calendário',              car.Calendario(self.notebook))]
            
        for titulo, aba in abas:
            self.notebook.add(aba, text = titulo)

        self.notebook.pack(fill='both', expand=True)  # Empacotar o Notebook para exibição
        # Criação dos frames para organizar os elementos

    def menus(self): #opções, a barrinha q aparece encima, calma q mexo
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Sobre", menu=filemenu2)

        filemenu.add_command(label="Sair", command=self.stop)

tela = MainScreen()
tela.start()
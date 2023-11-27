from tkinter import *
from tkinter import ttk
from lib import window as w
from lib import manager as man
from lib import crud as c
from lib import calendario as car

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

            # Aba 1
            self.aba1 = man.GenericManager(c.crud_cliente,self.notebook)
            #self.aba1 = Frame(self.notebook)

            self.notebook.add(self.aba1, text='Clientes')

            # Aba 2
            self.aba2 = man.GenericManager(c.crud_casa,self.notebook)
            self.notebook.add(self.aba2, text='Casas')

            # Aba 3
            self.aba3 = man.GenericManager(c.crud_origem,self.notebook)
            self.notebook.add(self.aba3, text='Sites')

            # Aba 4
            self.aba4 = man.GenericManager(c.crud_aluguel,self.notebook)
            self.notebook.add(self.aba4, text='Alugueis')

            # Aba 5
            self.aba7 = man.GenericManager(c.crud_aluguel_casa,self.notebook)
            self.notebook.add(self.aba7, text='Aluguel-Casa')

            # Aba 5
            self.aba5 = car.Calendario(self.notebook)
            self.notebook.add(self.aba5, text='Calendário')
            
            # Aba 5
            #self.aba6 = d.FinanceiroApp(self.notebook)
            #self.notebook.add(self.aba6, text='Calendário')

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
from tkinter import *

def menus(self): #opções, a barrinha q aparece encima, calma q mexo
    menubar = Menu(self.main_window)
    self.main_window.config(menu=menubar)
    filemenu = Menu(menubar)
    filemenu2 = Menu(menubar)

    menubar.add_cascade(label="Opções", menu=filemenu)
    menubar.add_cascade(label="Sobre", menu=filemenu2)

    filemenu.add_command(label="Sair", command=self.stop)

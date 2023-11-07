from tkinter import *

class Window(Frame):
    def __init__(self,title=None):
        self.root = Tk()
        self.root.title(title)
        pass

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()

janela = Window("TESTE")

janela.start()
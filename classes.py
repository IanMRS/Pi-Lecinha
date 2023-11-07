from tkinter import *

class Window(Frame):
    def __init__(self):
        self.root = Tk()
        pass

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()

janela = Window()
janela.root.wm_title("TESTE")

janela.start()
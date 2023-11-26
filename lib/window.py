from tkinter import *

class Window(Frame):
    def __init__(self,title=None):
        self.root = Tk()
        self.root.title(title)

        #atalhos
        #self.root.bind('<F11>', lambda event: self.toggle_full_screen())
        #self.root.bind('<Escape>', lambda event: self.exit_full_screen())
        pass

    def start(self):
        self.full_screen()
        self.root.mainloop()

    def stop(self):
        self.root.destroy()

    def full_screen(self):
        self.root.attributes('-fullscreen', True)

    def exit_full_screen(self):
        self.root.attributes('-fullscreen', False)

    def toggle_full_screen(self):
        if self.root.attributes('-fullscreen'):
            self.exit_full_screen()
        else:
            self.full_screen()
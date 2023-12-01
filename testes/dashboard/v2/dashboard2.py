import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, date

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyBudget")

        # Seção PERFIL
        self.create_profile_section()

        # Seção + NOVO
        self.create_new_section()

        # Seção NAV
        self.create_nav_section()

    def create_profile_section(self):
        profile_frame = ttk.LabelFrame(self.root, text="PERFIL")
        profile_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Adicione widgets da seção de perfil aqui

    def create_new_section(self):
        new_frame = ttk.LabelFrame(self.root, text="+ NOVO")
        new_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Adicione widgets da seção + NOVO aqui

    def create_nav_section(self):
        nav_frame = ttk.LabelFrame(self.root, text="NAV")
        nav_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Adicione widgets da seção NAV aqui


def main():
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
from tkinter.ttk import Notebook
from tkinter import Frame

from lib import crud
from lib.manager import GenericManager
from lib.doubledgraph import DoubleGraph

class MainNotebook(Notebook):
    """A class representing a main notebook with multiple tabs for managing different entities."""

    def __init__(self, frame):
        """
        Initialize the MainNotebook instance.

        Parameters:
        - frame: The Tkinter frame to which the MainNotebook belongs.
        """
        print("\nNotebook: Criando")
        super().__init__(frame)
        self.criar_abas()
    
    def criar_abas(self):
        """Create tabs (notebook pages) and add them to the MainNotebook."""
        self.abas = [
            ("Clientes", GenericManager(crud.BANCOS["cliente"], self)),
            ("Casas", GenericManager(crud.BANCOS["casa"], self)),
            ("Sites", GenericManager(crud.BANCOS["origem"], self)),
            ("Alugueis", GenericManager(crud.BANCOS["aluguel"], self)),
            ("Aluguel-Casa", GenericManager(crud.BANCOS["aluguel_has_casa"], self)),
            ("Dashboard", DoubleGraph(self))]
            
        for index, (titulo, aba) in enumerate(self.abas):
            print(f"Notebook: Criando aba {titulo} ({index+1}/{len(self.abas)})")
            self.add(aba, text=titulo)
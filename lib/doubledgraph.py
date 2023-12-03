from lib.dashboard import FinanceiroApp
from lib.calendario import GUICalendar
from tkinter import *
from lib import crud

class DoubleGraph(Frame):
    """A class representing a frame with two components: FinanceiroApp and GUICalendar."""

    def __init__(self, frame):
        """
        Initialize the DoubleGraph instance.

        Parameters:
        - frame: The Tkinter frame to which the DoubleGraph belongs.
        """
        super().__init__(frame)
        self.dashboard = FinanceiroApp(self,crud.BANCOS["origem"],crud.BANCOS["aluguel"])
        self.calendario = GUICalendar(self,crud.BANCOS["aluguel"],crud.BANCOS["casa"],crud.BANCOS["aluguel_has_casa"])
        self.dashboard.grid(row=0, column=0)
        self.calendario.grid(row=0, column=1)
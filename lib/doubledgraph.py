from lib.dashboard import FinanceiroApp
from lib.calendario import GUICalendar
from tkinter import *

class DoubleGraph(Frame):
    """A class representing a frame with two components: FinanceiroApp and GUICalendar."""

    def __init__(self, frame):
        """
        Initialize the DoubleGraph instance.

        Parameters:
        - frame: The Tkinter frame to which the DoubleGraph belongs.
        """
        super().__init__(frame)
        self.dashboard = FinanceiroApp(self)
        self.calendario = GUICalendar(self)
        self.dashboard.grid(row=0, column=0)
        self.calendario.grid(row=0, column=1)
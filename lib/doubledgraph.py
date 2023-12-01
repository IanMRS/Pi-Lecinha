from lib.dashboard import FinanceiroApp
from lib.calendario import GUICalendar
from tkinter import *

class DoubleGraph(Frame):
          def __init__(self,frame):
                    super().__init__(frame)
                    self.dashboard = FinanceiroApp(self)
                    self.calendario = GUICalendar(self)
                    self.dashboard.grid(row=0, column=0)
                    self.calendario.grid(row=0, column=1)
                    
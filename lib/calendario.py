from tkinter import Frame
from lib.calendario_day_grid import GUIDayGrid
from lib.calendario_header import GUICalendarHeader

class GUICalendar(Frame):
    """TODO: ATUALIZAR COMENTÁRIOS
    GUI Calendar for rental management.

    Attributes:
    - PADDING_X: Horizontal padding value.
    - PADDING_Y: Vertical padding value.
    """

    PADDING_X = 10
    PADDING_Y = 10

    def __init__(self, frame, crud_alugueis, crud_casa, crud_aluguel_casa):
        """
        Initialize the GUICalendar.

        Parameters:
        - frame: The parent frame.
        """
        super().__init__(frame)
        self.calendar_frame = GUIDayGrid(self, crud_alugueis, crud_casa, crud_aluguel_casa)
        self.header_frame = GUICalendarHeader(self,self.calendar_frame)

        self.place_widgets()

        self.header_frame.refresh_calendar()

        self.bind("<FocusIn>", self.on_focus)

    def on_focus(self, event=None):
        """Handle the focus event by updating and showing the current month."""
        self.header_frame.refresh_calendar()
        self.winfo_toplevel().focus_set()

    def place_widgets(self):        
        self.header_frame.grid(row=0, column=0, padx=self.PADDING_X)
        self.calendar_frame.grid(row=1, column=0, padx=self.PADDING_X)

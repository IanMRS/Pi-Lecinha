from tkinter import *
from lib.calendario_day_grid import GUIDayGrid
from lib.calendario_header import GUICalendarHeader

class GUICalendar(Frame):
    """
    GUI Calendar for rental management.

    Attributes:
    - MONTHS: Dictionary mapping month numbers to month names.
    - DAYS: List of weekday abbreviations.
    - COLOR_RED: Red color code.
    - COLOR_WHITE: White color code.
    - COLOR_DARK_GREEN: Dark green color code.
    - PADDING_X: Horizontal padding value.
    - PADDING_Y: Vertical padding value.
    - CALENDAR_DAY_WIDTH: Width of each calendar day element.
    - CALENDAR_DAY_HEIGHT: Height of each calendar day element.
    """

    PADDING_X = 10
    PADDING_Y = 10

    def __init__(self, frame):
        """
        Initialize the GUICalendar.

        Parameters:
        - frame: The parent frame.
        """
        super().__init__(frame)

        self.init_frames()

        self.header_frame.show_month()
        self.bind("<FocusIn>", self.on_focus)

    def on_focus(self, event=None):
        """
        Handle the focus event by updating and showing the current month.
        """
        self.header_frame.show_month()
        self.winfo_toplevel().focus_set()

    def init_frames(self):
        """
        Initialize frame elements for the calendar.
        """
        self.calendar_frame = GUIDayGrid(self)
        self.header_frame = GUICalendarHeader(self,self.calendar_frame)

        self.header_frame.grid(row=0, column=0, padx=self.PADDING_X)
        self.calendar_frame.grid(row=1, column=0, padx=self.PADDING_X)
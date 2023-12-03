from tkinter import *
import calendar
from lib import crud as c
from lib import date_formatting as df
from datetime import datetime, timedelta
from lib.calendario_day_grid import GUIDayGrid

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

    MONTHS = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

    PADDING_X = 10
    PADDING_Y = 10

    def __init__(self, frame):
        """
        Initialize the GUICalendar.

        Parameters:
        - frame: The parent frame.
        """
        super().__init__(frame)
        self.current_date = datetime.now()

        self.init_frames()
        self.init_header_frame()

        self.show_month()
        self.bind("<FocusIn>", self.on_focus)

    def on_focus(self, event=None):
        """
        Handle the focus event by updating and showing the current month.
        """
        self.show_month()
        self.winfo_toplevel().focus_set()

    def init_frames(self):
        """
        Initialize frame elements for the calendar.
        """
        self.header_frame = Frame(self)
        self.header_frame.grid(row=0, column=0, padx=self.PADDING_X)

        self.calendar_frame = GUIDayGrid(self)
        self.calendar_frame.grid(row=1, column=0, padx=self.PADDING_X)

    def init_header_frame(self):
        """
        Initialize header elements including buttons and labels.
        """
        self.prev_month_button = Button(self.header_frame, text="Previous Month", command=self.show_previous_month)
        self.prev_month_button.grid(row=0, column=0, padx=self.PADDING_X, pady=self.PADDING_Y)

        self.current_month = Label(self.header_frame, text=self.format_current_month())
        self.current_month.grid(row=0, column=1, padx=self.PADDING_X, pady=self.PADDING_Y)

        self.next_month_button = Button(self.header_frame, text="Next Month", command=self.show_next_month)
        self.next_month_button.grid(row=0, column=2, pady=self.PADDING_Y)

    def format_current_month(self):
        """
        Format the current month for display.

        Returns:
        A formatted string of the current month and year.
        """
        return f"{self.MONTHS[self.current_date.month]}, {self.current_date.year}"

    def show_month(self):
        """
        Show the current month on the calendar.
        """
        year, month = self.current_date.year, self.current_date.month
        self.calendar_frame.update_rental_info()
        self.calendar_frame.create_day_buttons(year, month)
        self.current_month.config(text=self.format_current_month())

    def show_previous_month(self):
        """
        Show the previous month on the calendar.
        """
        self.update_current_date(-1)
        self.show_month()

    def show_next_month(self):
        """
        Show the next month on the calendar.
        """
        self.update_current_date(1)
        self.show_month()

    def update_current_date(self, increment):
        """
        Update the current date based on the provided increment.

        Parameters:
        - increment: An integer value to increment or decrement the current date.
        """
        self.current_date = self.current_date + timedelta(days=calendar.monthrange(self.current_date.year, self.current_date.month)[1] * increment)
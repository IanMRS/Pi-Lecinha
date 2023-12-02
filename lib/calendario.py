from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import calendar
import holidays
from lib import crud as c
from lib import date_formatting as df
from datetime import datetime, timedelta, date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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
    DAYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

    COLOR_RED = "red"
    COLOR_WHITE = "#FFFFFF"
    COLOR_DARK_GREEN = "#00BE2F"
    PADDING_X = 10
    PADDING_Y = 10
    CALENDAR_DAY_WIDTH = 8
    CALENDAR_DAY_HEIGHT = 3

    def __init__(self, frame):
        """
        Initialize the GUICalendar.

        Parameters:
        - frame: The parent frame.
        """
        super().__init__(frame)
        self.day_buttons = []
        self.current_date = datetime.now()

        self.init_frames()
        self.init_header_frame()
        self.init_calendar_weekdays()

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

        self.calendar_frame = Frame(self)
        self.calendar_frame.grid(row=1, column=0, padx=self.PADDING_X)

    def init_calendar_weekdays(self):
        """
        Initialize labels for calendar weekdays.
        """
        for index, day in enumerate(self.DAYS):
            day_label = Label(self.calendar_frame, text=day, height=self.CALENDAR_DAY_HEIGHT)
            day_label.grid(row=0, column=index + 1)

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
        self.update_rental_info()
        self.create_day_buttons(year, month)
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

    def create_day_buttons(self, year, month):
        """
        Create day buttons for the current month.

        Parameters:
        - year: The year of the current month.
        - month: The month of the current month.
        """
        for button in self.day_buttons:
            button.grid_forget()

        _, last_day = calendar.monthrange(year, month)
        first_weekday, _ = calendar.monthrange(year, month)

        holidays_list = self.get_holidays(month, year)

        for i in range(1, last_day + 1):
            day_element = Label(self.calendar_frame, text=str(i), width=self.CALENDAR_DAY_WIDTH, height=self.CALENDAR_DAY_HEIGHT, borderwidth=2, relief="ridge")

            if i in holidays_list:
                day_element.configure(background=self.COLOR_RED)

            self.paint_day_button_based_on_rent_status(day_element, i)
            self.grid_element(day_element, i, first_weekday)

    def paint_day_button_based_on_rent_status(self, day_element, day):
        """
        Paint the day button based on the rental status.

        Parameters:
        - day_element: The day button element.
        - day: The day of the month.
        """
        formatted_day = f"{self.current_date.year}{self.current_date.month:02d}{day:02d}"

        if formatted_day in self.rented_days:
            for key, value in self.houses_rented_per_day.items():
                if formatted_day in value:
                    day_color = self.blend_colors(self.COLOR_WHITE, self.COLOR_DARK_GREEN, key / self.houses_in_total)
                    day_element.configure(bg=day_color)
                    break

    def grid_element(self, day_element, day, first_weekday):
        """
        Grid the day button element on the calendar.

        Parameters:
        - day_element: The day button element.
        - day: The day of the month.
        - first_weekday: The first weekday of the month.
        """
        row = 2 + (day + first_weekday - 2) // 7
        col = (day + first_weekday - 2) % 7 + 1
        day_element.grid(row=row, column=col)
        self.day_buttons.append(day_element)

    def update_rental_info(self):
        """
        Update rental information including rental data, house data, rental-has-house data, and dictionaries for rentals and rented days.
        """
        self.rental_data = c.BANCOS["aluguel"].read()
        self.house_data = c.BANCOS["casa"].read()
        self.houses_in_total = len(self.house_data)
        self.rental_has_house = c.BANCOS["aluguel_has_casa"].read()
        self.rental_dictionary = {}
        self.rented_days = set()

        for relation in self.rental_has_house:
            rent_id, house_id = relation[1], relation[2]

            rent_data = self.rental_data[rent_id - 1]
            start_rental_date, end_rental_date = str(rent_data[3]), str(rent_data[4])
            rental_dates = df.get_days_between_dates(start_rental_date, end_rental_date)

            self.rental_dictionary.setdefault(house_id, set()).update(rental_dates)
            self.rented_days.update(rental_dates)

        self.houses_rented_per_day = self.count_date_occurrences(self.rental_dictionary)

    @staticmethod
    def blend_colors(color1, color2, percentage):
        """
        Blend two colors based on a given percentage.

        Parameters:
        - color1: The first color code.
        - color2: The second color code.
        - percentage: The blending percentage.

        Returns:
        The blended color code.
        """
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        r = int(r1 + (r2 - r1) * percentage)
        g = int(g1 + (g2 - g1) * percentage)
        b = int(b1 + (b2 - b1) * percentage)

        blended_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        return blended_color

    @staticmethod
    def count_date_occurrences(input_dict):
        """
        Count the occurrences of dates in a dictionary.

        Parameters:
        - input_dict: The input dictionary with dates.

        Returns:
        A dictionary containing counts of occurrences for each date.
        """
        date_count = {}

        for key, date_list in input_dict.items():
            for dates in date_list:
                if dates in date_count:
                    date_count[dates] += 1
                else:
                    date_count[dates] = 1

        result_dict = {}
        for date, count in date_count.items():
            if count in result_dict:
                result_dict[count].append(date)
            else:
                result_dict[count] = [date]

        return result_dict

    @staticmethod
    def get_holidays(month, year):
        """
        Get a list of holidays for a given month and year.

        Parameters:
        - month: The month.
        - year: The year.

        Returns:
        A list of day numbers representing holidays.
        """
        brazilian_holidays = holidays.country_holidays("BR")
        holidays_list = []

        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            if date(year, month, day) in brazilian_holidays:
                holidays_list.append(day)

        return holidays_list
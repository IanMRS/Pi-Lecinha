from tkinter import *
import calendar
import holidays
from datetime import date
from lib import crud as c
from lib import date_formatting as df

class GUIDayGrid(Frame):
    DAYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

    CALENDAR_DAY_WIDTH = 8
    CALENDAR_DAY_HEIGHT = 3
    COLOR_RED = "red"
    COLOR_WHITE = "#FFFFFF"
    COLOR_DARK_GREEN = "#00BE2F"

    def __init__(self,frame):
        """TODO: ATUALIZAR COMENTÁRIOS"""
        super().__init__(frame)
        self.day_buttons = []
        self.init_calendar_weekdays()

    def init_calendar_weekdays(self):
        """
        Initialize labels for calendar weekdays.
        """
        for index, day in enumerate(self.DAYS):
            day_label = Label(self, text=day, height=self.CALENDAR_DAY_HEIGHT)
            day_label.grid(row=0, column=index + 1)

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

        for day in range(1, last_day + 1):
            day_element = Label(self, text=str(day), width=self.CALENDAR_DAY_WIDTH, height=self.CALENDAR_DAY_HEIGHT, borderwidth=2, relief="ridge")

            if day in holidays_list:
                day_element.configure(background=self.COLOR_RED)

            formated_date = f"{year}{month:02d}{day:02d}"

            self.paint_day_button_based_on_rent_status(day_element, formated_date)
            self.grid_element(day_element, day, first_weekday)

    def paint_day_button_based_on_rent_status(self, day_element, rent_day):
        """
        Paint the day button based on the rental status.

        Parameters:
        - day_element: The day button element.
        - day: The day of the month.
        """
        if rent_day in self.rented_days:
            for key, value in self.houses_rented_per_day.items():
                if rent_day in value:
                    day_color = self.blend_colors(self.COLOR_WHITE, self.COLOR_DARK_GREEN, key / self.houses_in_total)
                    day_element.configure(bg=day_color)
                    break


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
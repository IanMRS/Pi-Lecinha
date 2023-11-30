from tkinter import *
from tkinter import ttk
import calendar
import holidays
from lib import crud as c
from datetime import datetime, timedelta, date

COLOR_RED = "red"
COLOR_LIGHT_GREEN = "#00FF3F"
COLOR_DARK_GREEN = "#00BE2F"

class GUICalendar(Frame):
    MONTHS = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(self, frame):
        super().__init__(frame)
        self.day_buttons = []
        self.current_date = calendar.datetime.datetime.now()

        self.init_frames()
        self.init_header_frame()

        self.show_month()
        self.winfo_toplevel().focus_set()        

    def init_frames(self):
        self.header_frame = Frame(self)
        self.header_frame.grid(row=0, column=0,padx=10, pady=10)

        self.calendar_frame = Frame(self)
        self.calendar_frame.grid(row=1, column=0,padx=10, pady=10)

    def init_header_frame(self):
        self.prev_month_button = Button(self.header_frame, text="Previous Month", command=self.show_previous_month)
        self.prev_month_button.grid(row=0, column=0,padx=10, pady=10)

        self.current_month = Label(self.header_frame, text=self.get_current_month_text())
        self.current_month.grid(row=0, column=1, padx=10, pady=10)

        self.next_month_button = Button(self.header_frame, text="Next Month", command=self.show_next_month)
        self.next_month_button.grid(row=0, column=2, pady=10)

    def get_current_month_text(self):
        return f"{GUICalendar.MONTHS[self.current_date.month]}, {self.current_date.year}"

    def show_month(self):
        year, month = self.current_date.year, self.current_date.month
        self.update_rented_dates()
        self.create_day_buttons(year, month)
        self.current_month.config(text=self.get_current_month_text())

    def show_previous_month(self):
        self.update_current_date(-1)
        self.show_month()

    def show_next_month(self):
        self.update_current_date(1)
        self.show_month()

    def update_current_date(self, increment):
        self.current_date = self.current_date + timedelta(days=calendar.monthrange(self.current_date.year, self.current_date.month)[1] * increment)

    def create_day_buttons(self, year, month):
        for button in self.day_buttons:
            button.grid_forget()

        _, last_day = calendar.monthrange(year, month)
        first_weekday, _ = calendar.monthrange(year, month)

        holidays_list = GUICalendar.get_holidays(month, year)

        for i in range(1, last_day + 1):
            day_element = self.create_day_button(i)

            if i in holidays_list:
                day_element.configure(background=COLOR_RED)

            self.paint_day_button_based_on_rent_status(day_element, i)
            self.grid_element(day_element, i, first_weekday)

    def create_day_button(self, i):
        return Label(
            self.calendar_frame,
            text=str(i),
            width=8,
            height=3,
            borderwidth=2,
            relief="ridge"
        )

    def paint_day_button_based_on_rent_status(self, day_element, day):
        formatted_day = f"{self.current_date.year}{self.current_date.month:02d}{day:02d}"

        for data in self.rental_data:
            dates_between = GUICalendar.get_days_between_dates(str(data[3]), str(data[4]))
            if formatted_day in dates_between:
                day_element.configure(bg=COLOR_LIGHT_GREEN)
                break

    def grid_element(self, day_element, day, first_weekday):
        row = 2 + (day + first_weekday - 2) // 7
        col = (day + first_weekday - 2) % 7 + 1
        day_element.grid(row=row, column=col)
        self.day_buttons.append(day_element)

    def update_rented_dates(self):
        self.rental_data = c.BANCOS["aluguel"].read()
        self.house_data = c.BANCOS["casa"].read()
        self.rental_has_house = c.BANCOS["aluguel_has_casa"].read()
        self.rental_dictionary = {}

        for relation in self.rental_has_house:
            rent_id, house_id = relation[1], relation[2]

            if 0 <= int(rent_id if rent_id!="" else 0) - 1 < len(self.rental_data):
                rent_data = self.rental_data[rent_id - 1]
                self.rental_dictionary.setdefault(house_id, []).append(rent_data)
            else:
                print(f"Invalid rent_id: {rent_id}")

        print(self.rental_dictionary)

    @staticmethod
    def get_holidays(month, year):
        brazilian_holidays = holidays.country_holidays("BR")
        holidays_list = []

        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            if date(year, month, day) in brazilian_holidays:
                holidays_list.append(day)

        return holidays_list

    @staticmethod
    def get_days_between_dates(start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")
        delta = end_date - start_date
        days_in_between = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
        result = [day.strftime("%Y%m%d") for day in days_in_between]
        return result
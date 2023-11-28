from tkinter import *
from tkinter import ttk
import calendar
import holidays
from lib import crud as c
from datetime import datetime, timedelta, date

COLOR_RED = 'red'
COLOR_LIGHT_GREEN = 'green'

class Calendario(Frame):
    MONTHS = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(self, frame):
        super().__init__(frame)

        self.header_frame = Frame(self)
        self.header_frame.grid(row=0, column=0)

        self.calendar_frame = Frame(self)
        self.calendar_frame.grid(row=1, column=0)

        self.current_date = calendar.datetime.datetime.now()

        self.prev_month_button = Button(self.header_frame, text="Previous Month", command=self.show_previous_month)
        self.prev_month_button.grid(row=0, column=0)

        self.current_month = Label(self.header_frame, text=self.get_current_month_text())
        self.current_month.grid(row=0, column=1, padx=10)

        self.next_month_button = Button(self.header_frame, text="Next Month", command=self.show_next_month)
        self.next_month_button.grid(row=0, column=2)

        self.cal_display = Label(self.calendar_frame, text="", justify='left')
        self.cal_display.grid(row=1, column=0, columnspan=8)

        self.day_buttons = []

        self.show_month()

    def get_current_month_text(self):
        return f"{Calendario.MONTHS[self.current_date.month]}, {self.current_date.year}"

    def show_month(self):
        year, month = self.current_date.year, self.current_date.month
        self.ler_alugueis()
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

    def show_day(self, day):
        self.cal_display.config(text=f"{self.current_date.year}{self.current_date.month:02d}{day:02d}")

    def create_day_buttons(self, year, month):
        for button in self.day_buttons:
            button.grid_forget()

        _, last_day = calendar.monthrange(year, month)
        first_weekday, _ = calendar.monthrange(year, month)

        feriados = Calendario.get_holidays(month, year)

        for i in range(1, last_day + 1):
            day_element = self.create_day_button(i)

            if i in feriados:
                day_element.configure(background=COLOR_RED)

            self.paint_day_button_based_on_rent_status(day_element, i)
            self.grid_element(day_element, i, first_weekday)

    def create_day_button(self, i):
        return Button(
            self.calendar_frame,
            text=str(i),
            command=lambda i=i: self.show_day(i),
            width=5,
            height=2,
            borderwidth=2,
            relief="ridge"
        )

    def paint_day_button_based_on_rent_status(self, day_element, day):
        formatted_day = f"{self.current_date.year}{self.current_date.month:02d}{day:02d}"

        for data in self.dados_aluguel:
            dates_between = Calendario.get_days_between_dates(str(data[3]), str(data[4]))
            if formatted_day in dates_between:
                day_element.configure(bg=COLOR_LIGHT_GREEN)
                break

    def grid_element(self, day_element, day, first_weekday):
        row = 2 + (day + first_weekday - 2) // 7
        col = (day + first_weekday - 2) % 7 + 1
        day_element.grid(row=row, column=col)
        self.day_buttons.append(day_element)

    def ler_alugueis(self):
        self.dados_aluguel = c.BANCOS["aluguel"].read()
        self.dados_casa = c.BANCOS["casa"].read()

    @staticmethod
    def get_holidays(month, year):
        brazilian_holidays = holidays.country_holidays('BR')
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
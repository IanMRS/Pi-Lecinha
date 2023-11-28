from tkinter import *
from tkinter import ttk
import calendar
import holidays
from lib import crud as c
from datetime import datetime, timedelta, date

COLOR_RED = 'red'
COLOR_LIGHT_GREEN = 'green'

class Calendario(Frame):
    def __init__(self, frame):
        super().__init__(frame)

        self.header_frame = Frame(self)
        self.header_frame.grid(row=0, column=0)

        self.calendar_frame = Frame(self)
        self.calendar_frame.grid(row=1, column=0)

        self.current_date = calendar.datetime.datetime.now()

        self.prev_month_button = Button(self.header_frame, text="Previous Month", command=self.show_previous_month)
        self.prev_month_button.grid(row=0, column=0)

        self.current_month = Label(self.header_frame, text=f"{Calendario.num_to_month(self.current_date.month)}, {self.current_date.year}")
        self.current_month.grid(row=0, column=1, padx=10)  # Adjusted column and added padx for spacing

        self.next_month_button = Button(self.header_frame, text="Next Month", command=self.show_next_month)
        self.next_month_button.grid(row=0, column=2)  # Adjusted column

        self.days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(self.days):
            day_label = Label(self.calendar_frame, text=day)
            day_label.grid(row=0, column=i+1)

        self.cal_display = Label(self.calendar_frame, text="", justify='left')  # Changed variable name to cal_display
        self.cal_display.grid(row=1, column=0, columnspan=8)  # Adjusted row and columnspan

        self.day_buttons = []  # Store day buttons

        self.show_month()

    def ler_alugueis(self):
        self.dados_aluguel = c.BANCOS["aluguel"].read()
        self.dados_casa = c.BANCOS["casa"].read()


    def show_month(self):
        year, month = self.current_date.year, self.current_date.month

        self.ler_alugueis()
        self.create_day_buttons(year, month)
        
        self.current_month.config(text=f"{Calendario.num_to_month(self.current_date.month)}, {self.current_date.year}")

    def show_previous_month(self):
        year, month = self.current_date.year, self.current_date.month
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        self.current_date = self.current_date.replace(year=year, month=month)
        self.show_month()

    def show_next_month(self):
        year, month = self.current_date.year, self.current_date.month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        self.current_date = self.current_date.replace(year=year, month=month)
        self.show_month()

    def show_day(self, day):#função quando vc clica em botão
        self.cal_display.config(text=f"{self.current_date.year}{self.current_date.month:02d}{day:02d}")

    def create_day_buttons(self, year, month):
        dates_in_month = []

        for button in self.day_buttons:
            button.grid_forget()  # Clear existing buttons

        _, last_day = calendar.monthrange(year, month)
        first_weekday, _ = calendar.monthrange(year, month)

        feriados = Calendario.get_holidays(month,year)

        for i in range(1, last_day + 1):
            day_button = self.create_day_button(i)

            if i in feriados:
                day_button.configure(background=COLOR_RED)            

            self.paint_day_button_based_on_rent_status(day_button, i)
            self.grid_button(day_button, i, first_weekday)


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

    def paint_day_button_based_on_rent_status(self, day_button, day):
        formatted_day = f"{self.current_date.year}{self.current_date.month:02d}{day:02d}"

        for data in self.dados_aluguel:
            dates_between = Calendario.get_days_between_dates(str(data[3]), str(data[4]))
            if formatted_day in dates_between:
                day_button.configure(bg=COLOR_LIGHT_GREEN)
                break

    def grid_button(self, day_button, day, first_weekday):
        row = 2 + (day + first_weekday - 2) // 7
        col = (day + first_weekday - 2) % 7 + 1
        day_button.grid(row=row, column=col)
        self.day_buttons.append(day_button)

    def get_holidays(month, year):
        brazilian_holidays = holidays.country_holidays('BR')
        holidays_list = []

        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            if date(year, month, day) in brazilian_holidays:
                holidays_list.append(day)

        return holidays_list

    def num_to_month(num):
        months = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        return months[num]

    def get_days_between_dates(start_date_str, end_date_str):
        # Convert input date strings to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")

        # Calculate the number of days between the two dates
        delta = end_date - start_date

        # Generate a list of all days in between, including start and end dates
        days_in_between = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

        # Format the result as strings in the YYYYMMDD format
        result = [day.strftime("%Y%m%d") for day in days_in_between]

        return result
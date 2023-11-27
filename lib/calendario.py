from tkinter import *
from tkinter import ttk
import calendar
from lib import crud as c

COLOR_RED = 'red'
COLOR_BLUE = 'blue'
COLOR_GREEN = 'green'
COLOR_MAGENTA = 'magenta'

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

        self.current_month = Label(self.header_frame, text=f"{self.num_to_month(self.current_date.month)}, {self.current_date.year}")
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
        self.dados_aluguel = c.crud_aluguel.read()
        self.dados_casa = c.crud_casa.read()


    def formatted_date(self):
        return f"{self.current_date.year}{self.current_date.month}"


    def show_month(self):
        year, month = self.current_date.year, self.current_date.month

        self.ler_alugueis()
        self.create_day_buttons(year, month)
        
        self.current_month.config(text=f"{self.num_to_month(self.current_date.month)}, {self.current_date.year}")


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
        self.cal_display.config(text=f"{self.current_date.year}{self.current_date.month}{day}")

    def create_day_buttons(self, year, month):
        # Configure uniform button size
        button_width = 5
        button_height = 2

        dates_in_month = []

        for button in self.day_buttons:
            button.grid_forget()  # Clear existing buttons

        _, last_day = calendar.monthrange(year, month)
        first_weekday, _ = calendar.monthrange(year, month)

        for i in range(1, last_day + 1):
            day_button = self.create_day_button(i)
            self.apply_color_to_button(day_button, i)
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

    def apply_color_to_button(self, day_button, day):
        for data in self.dados_aluguel:
            date_start_year = int(str(data[3])[:4])
            date_end_year = int(str(data[4])[:4])

            date_start_month = int(str(data[3])[4:6])
            date_end_month = int(str(data[4])[4:6])
            
            date_start_day = int(str(data[3])[6:])
            date_end_day = int(str(data[4])[6:])

            starts_in_this_month = date_start_month == self.current_date.month
            ends_in_this_month = date_end_month == self.current_date.month

            day_is_bigger_than_start = date_start_day <= day
            day_is_smaller_than_end = date_end_day >= day

            within_same_year = self.current_date.year == date_start_year and self.current_date.year == date_end_year

            between_months = date_start_month < self.current_date.month < date_end_month and within_same_year

            if starts_in_this_month and day_is_bigger_than_start and ends_in_this_month and day_is_smaller_than_end and within_same_year:
                day_button.configure(bg=COLOR_RED)
            elif not starts_in_this_month and ends_in_this_month and day_is_smaller_than_end and within_same_year:
                day_button.configure(bg=COLOR_RED)
            elif starts_in_this_month and day_is_bigger_than_start and not ends_in_this_month and within_same_year:
                day_button.configure(bg=COLOR_RED)
            elif between_months and not starts_in_this_month and not ends_in_this_month and within_same_year:
                day_button.configure(bg=COLOR_RED)

    def grid_button(self, day_button, day, first_weekday):
        row = 2 + (day + first_weekday - 2) // 7
        col = (day + first_weekday - 2) % 7 + 1
        day_button.grid(row=row, column=col)
        self.day_buttons.append(day_button)

    def num_to_month(self, num):
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
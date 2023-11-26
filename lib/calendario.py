from tkinter import *
from tkinter import ttk
import calendar
from lib import crud as c

class Calendario(Frame):
    def __init__(self,frame):
        super().__init__(frame)

        self.top_row = Frame(self)
        self.top_row.pack(padx=10, pady=10)

        self.frame = Frame(self)
        self.frame.pack(padx=10, pady=10)

        self.current_date = calendar.datetime.datetime.now()

        self.prev_month_button = Button(self.top_row, text="Previous Month", command=self.show_previous_month)
        self.prev_month_button.grid(row=0, column=0)


        self.current_month = Label(self.top_row, text=self.num_to_month(self.current_date.month))
        self.current_month.grid(row=0, column=4)


        self.next_month_button = Button(self.top_row, text="Next Month", command=self.show_next_month)
        self.next_month_button.grid(row=0, column=8)

        self.days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(self.days):
            day_label = Label(frame, text=day)
            day_label.grid(row=1, column=i+1)

        cal_display = Label(frame, text="", justify='left')
        cal_display.grid(row=3, columnspan=8)

        self.day_buttons = []  # Store day buttons

        self.show_month()


    def show_month(self):
        year, month = self.current_date.year, self.current_date.month
        self.create_day_buttons(year, month)
        
        self.current_month.config(text=self.num_to_month(month))


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
        self.cal_display.config(text=f"You clicked on day {day}")


    def create_day_buttons(self, year, month):
        # Configure uniform button size
        button_width = 5
        button_height = 2

        for button in self.day_buttons:
            button.grid_forget()  # Clear existing buttons

        _, last_day = calendar.monthrange(year, month)
        first_weekday, _ = calendar.monthrange(year, month)

        for i in range(1, last_day + 1):
            day_button = Button(self, text=str(i), command=lambda i=i: self.show_day(i), width=button_width, height=button_height,borderwidth=2, relief="ridge")
            row = 4 + (i + first_weekday - 2) // 7
            col = 1+ (i + first_weekday - 2) % 7

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
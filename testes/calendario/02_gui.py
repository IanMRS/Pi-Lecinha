import tkinter as tk
import calendar

def show_month():
    global current_date
    year, month = current_date.year, current_date.month
    create_day_buttons(year, month)
    
    current_month.config(text=num_to_month(month))

def show_previous_month():
    global current_date
    year, month = current_date.year, current_date.month
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    current_date = current_date.replace(year=year, month=month)
    show_month()

def show_next_month():
    global current_date
    year, month = current_date.year, current_date.month
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    current_date = current_date.replace(year=year, month=month)
    show_month()

def show_day(day):#função quando vc clica em botão
    cal_display.config(text=f"You clicked on day {day}")

def create_day_buttons(year, month):
    # Configure uniform button size
    button_width = 5
    button_height = 2

    for button in day_buttons:
        button.grid_forget()  # Clear existing buttons

    _, last_day = calendar.monthrange(year, month)
    first_weekday, _ = calendar.monthrange(year, month)

    for i in range(1, last_day + 1):
        day_button = tk.Button(frame, text=str(i), command=lambda i=i: show_day(i), width=button_width, height=button_height,borderwidth=2, relief="ridge")
        row = 4 + (i + first_weekday - 2) // 7
        col = 1+ (i + first_weekday - 2) % 7

        day_button.grid(row=row, column=col)
        day_buttons.append(day_button)

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


def main():
    global root, frame, current_date, day_buttons, cal_display, current_month

    root = tk.Tk()
    root.title("Python Calendar")

    top_row = tk.Frame(root)
    top_row.pack(padx=10, pady=10)

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    current_date = calendar.datetime.datetime.now()

    prev_month_button = tk.Button(top_row, text="Previous Month", command=show_previous_month)
    prev_month_button.grid(row=0, column=0)


    current_month = tk.Label(top_row, text=num_to_month(current_date.month))
    current_month.grid(row=0, column=4)


    next_month_button = tk.Button(top_row, text="Next Month", command=show_next_month)
    next_month_button.grid(row=0, column=8)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        day_label = tk.Label(frame, text=day)
        day_label.grid(row=1, column=i+1)

    cal_display = tk.Label(frame, text="", justify="left")
    cal_display.grid(row=3, columnspan=8)

    day_buttons = []  # Store day buttons

    show_month()
    root.mainloop()

main()

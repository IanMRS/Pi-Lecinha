import tkinter as tk
import calendar

def show_current_month():
    global current_date
    year, month = current_date.year, current_date.month
    create_day_buttons(year, month)

def show_previous_month():
    global current_date
    year, month = current_date.year, current_date.month
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    current_date = current_date.replace(year=year, month=month)
    show_current_month()

def show_next_month():
    global current_date
    year, month = current_date.year, current_date.month
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    current_date = current_date.replace(year=year, month=month)
    show_current_month()

def show_day(day):#função quando vc clica em botão
    cal_display.config(text=f"You clicked on day {day}")

def create_day_buttons(year, month):
    for button in day_buttons:
        button.grid_forget()  # Clear existing buttons

    _, last_day = calendar.monthrange(year, month)
    for i in range(1, last_day + 1):
        day_button = tk.Button(frame, text=str(i), command=lambda i=i: show_day(i), width=button_width, height=button_height)
        row = 4 + (i - 1) // 7
        col = (i - 1) % 7
        day_button.grid(row=row, column=col)
        day_buttons.append(day_button)

def main():
    global root, frame, current_date, day_buttons, cal_display, button_width, button_height

    root = tk.Tk()
    root.title("Python Calendar")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    current_date = calendar.datetime.datetime.now()

    prev_month_button = tk.Button(frame, text="Previous Month", command=show_previous_month)
    prev_month_button.grid(row=1, column=0)
    next_month_button = tk.Button(frame, text="Next Month", command=show_next_month)
    next_month_button.grid(row=1, column=2)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        day_label = tk.Label(frame, text=day)
        day_label.grid(row=2, column=i)

    cal_display = tk.Label(frame, text="", justify='left')
    cal_display.grid(row=3, columnspan=7)

    # Configure uniform button size
    button_width = 5
    button_height = 2

    day_buttons = []  # Store day buttons

    show_current_month()
    root.mainloop()

if __name__ == "__main__":
    main()

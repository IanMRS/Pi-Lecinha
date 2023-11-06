import tkinter as tk
import calendar

def show_calendar(year, month):
    cal_text = calendar.month(year, month)
    cal_display.config(text=cal_text)

root = tk.Tk()
root.title("Python Calendar")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

year_label = tk.Label(frame, text="Year:")
year_label.grid(row=0, column=0)
year_entry = tk.Entry(frame)
year_entry.grid(row=0, column=1)

month_label = tk.Label(frame, text="Month:")
month_label.grid(row=1, column=0)
month_entry = tk.Entry(frame)
month_entry.grid(row=1, column=1)

show_button = tk.Button(frame, text="Show Calendar", command=lambda: show_calendar(int(year_entry.get()), int(month_entry.get())))
show_button.grid(row=2, columnspan=2)

cal_display = tk.Label(frame, text="", justify='left')
cal_display.grid(row=3, columnspan=2)

root.mainloop()

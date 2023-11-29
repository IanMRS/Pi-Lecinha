import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Make sure to install the tkcalendar library

def get_date():
    selected_date = cal.get_date()
    formatted_date = selected_date.strftime("%Y%m%d")
    result_label.config(text=f"Selected Date: {formatted_date}")

# Create the main window
root = tk.Tk()
root.title("Date Input Widget")

# Create a DateEntry widget
cal = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2)
cal.grid(row=0, column=0, padx=10, pady=10)

# Create a button to get the selected date
get_date_button = ttk.Button(root, text="Get Date", command=get_date)
get_date_button.grid(row=1, column=0, pady=10)

# Label to display the selected date
result_label = ttk.Label(root, text="Selected Date: ")
result_label.grid(row=2, column=0, pady=10)

# Start the Tkinter event loop
root.mainloop()

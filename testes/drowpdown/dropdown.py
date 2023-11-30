import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_index = dropdown.current()  # Get the index of the selected option
    print(f"Selected Index: {selected_index}")

# Create the main window
root = tk.Tk()
root.title("Tkinter Dropdown Example with Index")

# Create a Label
label = tk.Label(root, text="Select an option:")
label.pack(pady=10)

# Create a Dropdown
options = ["Option 1", "Option 2", "Option 3"]
dropdown = ttk.Combobox(root, values=options)
dropdown.pack(pady=10)

# Set a default value
dropdown.set(options[0])

# Bind the event handler to the dropdown
dropdown.bind("<<ComboboxSelected>>", on_select)

# Run the Tkinter event loop
root.mainloop()

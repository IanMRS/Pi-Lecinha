import tkinter as tk

def on_backspace(event):
    print("Backspace key pressed")

def on_delete(event):
    print("Delete key pressed")

def on_enter(event):
    print("Enter key pressed")

def on_ctrl_enter(event):
    print("Ctrl+Enter key pressed")

# Create the main Tkinter window
root = tk.Tk()

# Bind the functions to the corresponding keys
root.bind('<BackSpace>', on_backspace)
root.bind('<Delete>', on_delete)
root.bind('<Return>', on_enter)
root.bind('<Control-Return>', on_ctrl_enter)

# Run the Tkinter event loop
root.mainloop()

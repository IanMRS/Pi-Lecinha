import tkinter as tk

class ResponsiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Responsive Tkinter App")

        # Create a Label widget
        self.label = tk.Label(self.root, text="Resize the window to see the changes!", font=("Helvetica", 14))
        self.label.grid(row=0, column=0, sticky="nsew")

        # Create an Entry widget
        self.entry = tk.Entry(self.root, width=20, font=("Helvetica", 14))
        self.entry.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        # Set column and row weights to make elements expand with the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Bind the event handler to the window resize event
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Update the label text with the current window size
        size_str = f"Window Size: {event.width} x {event.height}"
        self.label.config(text=size_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResponsiveApp(root)
    root.mainloop()

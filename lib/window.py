import tkinter as tk

class FullScreenWindow:
    def __init__(self, title=None):
        self.root = tk.Tk()
        self.root.title(title)

        self.setup_key_bindings()

    def setup_key_bindings(self):
        self.root.bind("<F11>", self.toggle_full_screen)

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()

    def toggle_full_screen(self, event=None):
        """Toggle between fullscreen and normal mode."""
        try:
            self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        except tk.TclError as e:
            print(f"Error toggling fullscreen: {e}")

    def exit_full_screen(self, event=None):
        """Exit fullscreen mode."""
        try:
            self.root.attributes("-fullscreen", False)
        except tk.TclError as e:
            print(f"Error exiting fullscreen: {e}")

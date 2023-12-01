import tkinter as tk

class FullScreenWindow:
    """A class representing a full-screen window with toggleable fullscreen mode."""

    def __init__(self, title=None):
        """
        Initialize the FullScreenWindow instance.

        Parameters:
        - title: The title of the window.
        """
        self.root = tk.Tk()
        self.root.title(title)

        self.setup_key_bindings()
        self.toggle_full_screen()

    def setup_key_bindings(self):
        """Set up key bindings for fullscreen toggle."""
        self.root.bind("<F11>", self.toggle_full_screen)

    def start(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()

    def stop(self):
        """Stop the Tkinter main event loop and destroy the window."""
        self.root.destroy()

    def toggle_full_screen(self, event=None):
        """
        Toggle between fullscreen and normal mode.

        Parameters:
        - event: The event that triggered the fullscreen toggle.
        """
        try:
            self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        except tk.TclError as e:
            print(f"Error toggling fullscreen: {e}")

    def exit_full_screen(self, event=None):
        """
        Exit fullscreen mode.

        Parameters:
        - event: The event that triggered exiting fullscreen.
        """
        try:
            self.root.attributes("-fullscreen", False)
        except tk.TclError as e:
            print(f"Error exiting fullscreen: {e}")
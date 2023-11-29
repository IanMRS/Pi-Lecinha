import tkinter as tk

def full_screen(window):
    window.attributes("-fullscreen", True)

def exit_full_screen(window):
    window.attributes("-fullscreen", False)

def toggle_full_screen(window):
    if window.attributes("-fullscreen"):
        exit_full_screen(window)
    else:
        full_screen(window)

def create_full_screen_window():
    root = tk.Tk()
    root.title("Full Screen Window")

    # Bind the F11 key to toggle full screen
    root.bind("<F11>", lambda event: toggle_full_screen(root))

    # Bind the Escape key to exit full screen
    root.bind("<Escape>", lambda event: exit_full_screen(root))

    full_screen(root)

    # Add your widgets or content here

    root.mainloop()

# Create and run the full-screen window
create_full_screen_window()

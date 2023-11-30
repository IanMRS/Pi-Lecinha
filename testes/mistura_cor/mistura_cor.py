import tkinter as tk

def blend_colors(color1, color2, percentage):
    # Convert hexadecimal color codes to RGB
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    # Calculate the blended color
    r = int(r1 + (r2 - r1) * (percentage / 100))
    g = int(g1 + (g2 - g1) * (percentage / 100))
    b = int(b1 + (b2 - b1) * (percentage / 100))

    # Format the RGB values as hexadecimal
    blended_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return blended_color

def update_color():
    color1 = entry_color1.get()
    color2 = entry_color2.get()
    percentage = float(entry_percentage.get())

    blended_color = blend_colors(color1, color2, percentage)

    canvas.config(bg=blended_color)
    label_result.config(text=f"Blended Color: {blended_color}")

# Create the main window
root = tk.Tk()
root.title("Color Blender")

# Create and place widgets
label_color1 = tk.Label(root, text="Color 1:")
label_color1.grid(row=0, column=0, padx=10, pady=5)

entry_color1 = tk.Entry(root)
entry_color1.grid(row=0, column=1, padx=10, pady=5)

label_color2 = tk.Label(root, text="Color 2:")
label_color2.grid(row=1, column=0, padx=10, pady=5)

entry_color2 = tk.Entry(root)
entry_color2.grid(row=1, column=1, padx=10, pady=5)

label_percentage = tk.Label(root, text="Percentage:")
label_percentage.grid(row=2, column=0, padx=10, pady=5)

entry_percentage = tk.Entry(root)
entry_percentage.grid(row=2, column=1, padx=10, pady=5)

button_blend = tk.Button(root, text="Blend Colors", command=update_color)
button_blend.grid(row=3, column=0, columnspan=2, pady=10)

canvas = tk.Canvas(root, width=200, height=50)
canvas.grid(row=4, column=0, columnspan=2, pady=10)

label_result = tk.Label(root, text="")
label_result.grid(row=5, column=0, columnspan=2, pady=5)

# Run the Tkinter event loop
root.mainloop()

import tkinter as tk
from math import pi, cos, sin

def draw_doughnut_chart(canvas, data, inner_radius):
    total = sum(data)
    start_angle = 0
    
    # Calculate the center and radius for the doughnut
    center_x, center_y = (150, 150)
    outer_radius = 100
    
    # Draw the outer circle for the doughnut
    canvas.create_oval(center_x - outer_radius, center_y - outer_radius, center_x + outer_radius, center_y + outer_radius, outline="black")

    for value in data:
        # Calculate the percentage and corresponding angle
        percentage = value / total
        angle = 360 * percentage
        
        # Calculate the coordinates for the outer arc of the slice
        outer_x = center_x + outer_radius * cos(pi * start_angle / 180)
        outer_y = center_y - outer_radius * sin(pi * start_angle / 180)
        
        # Draw the outer arc of the slice
        canvas.create_arc(center_x - outer_radius, center_y - outer_radius, center_x + outer_radius, center_y + outer_radius, start=start_angle, extent=angle, fill="blue", outline="black")
        
        # Calculate the coordinates for the inner arc of the slice
        inner_x = center_x + inner_radius * cos(pi * start_angle / 180)
        inner_y = center_y - inner_radius * sin(pi * start_angle / 180)
        
        # Draw the line connecting the outer and inner arcs
        canvas.create_line(outer_x, outer_y, inner_x, inner_y, fill="white", width=2)
        
        # Draw the inner arc of the slice
        canvas.create_arc(center_x - inner_radius, center_y - inner_radius, center_x + inner_radius, center_y + inner_radius, start=start_angle, extent=angle, outline="black")

        # Update the start angle for the next slice
        start_angle += angle

# Example data for the doughnut chart
data = [30, 50, 20]
inner_radius = 50

# Create the main window
root = tk.Tk()
root.title("Doughnut Chart")

# Create a Canvas widget
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Draw the doughnut chart on the canvas
draw_doughnut_chart(canvas, data, inner_radius)

# Start the Tkinter event loop
root.mainloop()

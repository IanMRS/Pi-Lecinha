import tkinter as tk
from tkinter import ttk

def on_treeview_select(event):
    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item, 'values')
    additional_data = data_dict[selected_item]
    print("Values:", item_values)
    print("Additional Data:", additional_data)

root = tk.Tk()
root.title("Treeview with Hidden Additional Data")

tree = ttk.Treeview(root, columns=('Display Column',), show='headings')

tree.heading('Display Column', text='Display Column')

tree.pack()

# Add sample data
data = [("Item 1", "Additional Info 1"),
        ("Item 2", "Additional Info 2"),
        ("Item 3", "Additional Info 3")]

# Create a dictionary to store additional data for each item
data_dict = {}

for item in data:
    item_id = tree.insert("", tk.END, values=(item[0],))
    data_dict[item_id] = item[1]

tree.bind('<ButtonRelease-1>', on_treeview_select)

root.mainloop()

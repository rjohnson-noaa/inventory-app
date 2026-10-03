import tkinter as tk

# Set up GUI Window
root = tk.Tk()
root.title("IWCPS Inventory")

root.geometry("700x500")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Heading
title_heading = (tk.Label(root, text="IWCPS Inventory", font=("Calibri", 40, "bold")))
title_heading.grid(row=0, column=0, columnspan=2, padx= 15, pady=15)


# Functions for buttons


"""
# Input Form
tk.Label(root, text="Item name").grid(row=1, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Quantity").grid(row=2, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Price").grid(row=3, column=0, padx=5, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
#add_btn = tk.Button(root, text="Add Item", command=add_item)
#add_btn.grid(row=4, column=0, columnspan=2, pady=10)

#delete_btn = tk.Button(root, text="Delete Selected", command=delete_item)
#delete_btn.grid(row=5, column=0, columnspan=2, pady=5)
"""


root.mainloop()
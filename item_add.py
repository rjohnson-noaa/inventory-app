import tkinter as tk
from tkinter import messagebox, ttk

# Import functions from your separate python file
from inventory_db import *

def add_item():
    name = name_entry.get().strip()
    quantity = quantity_entry.get().strip()
    price = price_entry.get().strip()

    if name and quantity and price:
        try:
            qty_val = int(quantity)
            price_val = float(price)

            # Call function from inventory_db.py
            add_item_db(name, qty_val, price_val)

            update_inventory()
            clear_entries()
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Quantity must be an integer and price must be a number",
            )
    else:
        messagebox.showerror("Missing fields", "All fields are required")


def update_inventory():
    for row in tree.get_children():
        tree.delete(row)

    # Call function from inventory_db.py
    rows = fetch_all_items()

    for item_id, name, quantity, price in rows:
        tree.insert(
            "",
            "end",
            iid=item_id,
            values=(name, quantity, f"${price:.2f}"),
        )


def delete_item():
    selected = tree.selection()
    if selected:
        item_id = int(selected[0])

        # Call function from inventory_db.py
        delete_item_db(item_id)

        update_inventory()
    else:
        messagebox.showerror("No selection", "Please select an item to delete")


def clear_entries():
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)


# Set up GUI Window
root = tk.Tk()
root.title("IWCPS Inventory")

# Heading
tk.Label(
    root, text="IWCPS Inventory", font=("Helvetica", 16, "bold")
).grid(row=0, column=0, columnspan=2, pady=(10, 15))

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
add_btn = tk.Button(root, text="Add Item", command=add_item)
add_btn.grid(row=4, column=0, columnspan=2, pady=10)

delete_btn = tk.Button(root, text="Delete Selected", command=delete_item)
delete_btn.grid(row=5, column=0, columnspan=2, pady=5)

# Treeview
columns = ("Name", "Quantity", "Price")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=6, column=0, columnspan=2, pady=10)

# Initialize DB & launch app
init_db()
update_inventory()

root.mainloop()
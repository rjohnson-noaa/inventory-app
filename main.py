import tkinter as tk

from tkinter import messagebox, ttk

# Inventory list to store item data

inventory = []

# function to add item

def add_item():

    name = name_entry.get()

    quantity = quantity_entry.get()

    price = price_entry.get()

    if name and quantity and price:

        try:
            inventory.append({

                "name": name,

                "quantity": int(quantity),

                "price": float(price)

            })

            update_inventory()

            clear_entries()

        except ValueError:

            messagebox.showerror("Invalid input", "Quantity must be an integer and price must be number")

    else:

        messagebox.showerror("Missing fields", "All fields are required")

# function to update treeview with inventory items

def update_inventory():
    for row in tree.get_children():

        tree.delete(row)

    for idx, item in enumerate(inventory):

        tree.insert("", "end", iid=idx, values=(item["name"], item["quantity"], item["price"]))

#function to clear entry fields

def clear_entries():

    name_entry.delete(0, tk .END)

    quantity_entry.delete(0, tk .END)

    price_entry.delete(0, tk .END)

#function to delete selected item

def delete_item():

    selected = tree.selection()

    if selected:

        index = int(selected[0])

        del inventory[index]

        update_inventory()

    else:

        messagebox.showerror("No selection", "Please select an item to delete")


# set up main window/application

root = tk.Tk()
root.title("IWCPS Inventory") #title of application

tk.Label(root, text="Item name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Quantity").grid(row=1, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Price").grid(row=2, column=0, padx=5, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=2, column=1, padx=5, pady=5)

# buttons

add_btn = tk.Button(root, text="Add Item", command=add_item)

add_btn.grid(row=3, column=0, columnspan=2, pady=10)

delete_btn = tk.Button(root, text="Delete Selected", command=delete_item)

delete_btn.grid(row=4, column=0, columnspan=2, pady=5)

#Treeview to display inventory

columns = ("Name", "Quantity", "Price")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:

    tree.heading(col, text=col)

tree.grid(row=5, column=0, columnspan=2, pady=10)

#Start the GUI event loop

root.mainloop()
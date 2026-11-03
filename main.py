import flet as ft
import flet_datatable2 as fdt
import sqlite3



# database creation -------------------------------------------------------------------------------------------------------
conn = sqlite3.connect('inventory.db', check_same_thread=False)
cursor = conn.cursor()

def int_db():

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS inventory
                   (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity TEXT,
                    category TEXT,
                    location TEXT,
                    serial TEXT,
                    expiration TEXT,
                    notes TEXT
                   )
                   """)
    conn.commit()



# function that runs the entire app ------------------------------------------------------------------------------------
def main(page: ft.Page):
    int_db() #call the database in the main function
    #setting up the window to fit the tablet
    page.window.height = 960
    page.window.width = 600
    page.window.resizable = True
    page.padding = 0
    page.spacing = 0
    page.window.center()

    category = ['', 'Sampling/Biology', 'Stationary', 'Hardware & Tools', 'Tech/Equipment', 'Chemicals', 'Rain Gear',
                'Safety', 'Deck', 'Miscellaneous']  # list of item categories
    category_dd = [ft.DropdownOption(item) for item in category]  # turns the list items into dropdown options

    location = ['', 'Newport', 'Ship', 'OTHER']  # list of item main locations
    location_dd = [ft.DropdownOption(item) for item in location]  # turns the list items into dropdown options


#Defined NOAA Colors --------------------------------------------------------------------------------------------------
    dark_blue = '#003087'
    light_blue = '#0085CA'
    white = 'white'
    gray = '#F0F0F0'
    dark_gray = '#686868'

# MAIN PAGE functions and items -------------------------------------------------------------------
    add_item_btn = ft.Button(    #add item button
        on_click=lambda _: navigate_to('/add_page'),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.ADD,
                    size=30,
                    color=light_blue
                ),
                ft.Text('Add Item', size=25, color=dark_blue),
            ],
        ),
        width=300,
        height=150,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    search_item_btn = ft.Button(    # search item button on main page
        on_click=lambda _: navigate_to('/search_page'),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.SEARCH,
                    size=30,
                    color=light_blue
                ),
                ft.Text('Item Search', size=25, color=dark_blue)
            ],
        ),
        width=300,
        height=150,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    pack_unpack_btn = ft.Button(   # pack/unpack button on main page
        on_click=lambda _: navigate_to('/pack_unpack'),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.INVENTORY_2_OUTLINED,
                    size=30,
                    color=light_blue
                ),
                ft.Text('Pack/Unpack', size=25, color=dark_blue),
            ],
        ),
        width=300,
        height=150,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    main_page = ft.Container(
        expand=True,
        bgcolor=gray,
        content=ft.Column(
            expand=True,
            controls=[
                ft.AppBar(
                    leading=ft.Container(
                        padding=15,
                        content=ft.Image(src='../inventory-app/noaalogo.png')
                    ),
                    leading_width=90,
                    title=ft.Text('IWCPS Inventory',
                                  size=40,
                                  style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=white)),
                                  center_title=True,
                                  bgcolor=dark_gray,
                                  toolbar_height=100
                              ),
                ft.Container(height=130),
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[add_item_btn]
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[search_item_btn]
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[pack_unpack_btn]
                        )
                    ]
                ),
            ]
        )
    )

#DATA TABLE aspects ---------------------------------------------------------------------------------------------------
    def cell_text(val, size=13):    # Makes the overflow text into an ellipsis in the data table
        if isinstance(val, ft.Control):
            if isinstance(val, ft.Text):
                val.size = size
                val.overflow = ft.TextOverflow.ELLIPSIS
                val.max_lines = 1
                val.no_wrap = True
            return val
        return ft.Text(
            str(val or ""),
            size=size,
            overflow=ft.TextOverflow.ELLIPSIS,
            max_lines=1,
            no_wrap=True
        )

    def submit_item(e):     #function that adds an item into the database and table
        if not item_name.value or not item_name.value.strip():
            item_name.error_text = "Item Name is required!"
            item_name.update()

            page.overlay.append(
                ft.SnackBar(
                    content=ft.Text("Item name is required!"),
                    open=True,
                    bgcolor=ft.Colors.RED_600,
                )
            )
            page.update()
            return

        if item_quantity.disabled:
            qty_display = "Var"
        else:
            qty_display = item_quantity.value.strip() if item_quantity.value else "0"

        item_name.error_text = None

        sub_loc = (
            land_location.value if item_location.value == "Newport"
            else ship_location.value if item_location.value == "Ship"
            else other_location.value.strip() if item_location.value == "OTHER"
            else ""
        )

        location_display = f"{item_location.value or ''}{f' / {sub_loc}' if sub_loc else ''}"


        new_entry = ft.DataRow(on_select_change=handle_row_selection_change,

            cells = [
                ft.DataCell(ft.Text(item_name.value)),
                ft.DataCell(ft.Text(qty_display)),
                ft.DataCell(ft.Text(item_category.value)),
                ft.DataCell(ft.Text(location_display)),
                ft.DataCell(ft.Text(item_serial.value)),
                ft.DataCell(ft.Text(item_expire.value)),
                ft.DataCell(cell_text(ft.Text(notes.value)))

            ]
        )

        inventory_table.rows.append(new_entry)

        cursor.execute("""
                       INSERT INTO inventory (name, quantity, category, location, serial, expiration, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       """, (
                           item_name.value,
                           qty_display,
                           item_category.value,
                           location_display,
                           item_serial.value,
                           item_expire.value,
                           notes.value
                       ))
        conn.commit()

        # Clear input fields
        item_name.value = ""
        item_quantity.value = ""
        item_number_various.value = False
        item_quantity.disabled = False
        item_location.value = None
        land_location.value = None
        land_location.visible = False
        ship_location.visible = False
        ship_location.value = None
        other_location.value = ''
        other_location.visible = False
        serial_toggle.value = False
        item_serial.disabled = True
        item_expire.disabled = True
        expire_toggle.value = False
        item_category.value = None
        item_expire.value = ''
        item_serial.value = ''
        notes.value = ''

        load_item()
        page.update()

    def clear_all_cancel (e):    #clears all fields when navigating off the page
        item_name.value = ""
        item_quantity.value = ""
        item_number_various.value = False
        item_category.value = ''
        item_location.value = ''
        land_location.value = ''
        land_location.visible = False
        ship_location.visible = False
        ship_location.value = ''
        other_location.value = ''
        other_location.visible = False
        serial_toggle.value = False
        item_serial.disabled = True
        item_expire.disabled = True
        expire_toggle.value = False
        item_expire.value = ''
        item_serial.value = ''
        notes.value = ''

        for row in inventory_table.rows:
            row.selected = False

        navigate_to('/')

        page.update()

    def handle_row_selection_change(e: ft.Event[fdt.DataRow2]):   #row selection in the datatable
        e.control.selected = not e.control.selected
        e.control.update()

    def load_item():    #loads items from the DB into the app so they are saved upon opening and closing

        inventory_table.rows.clear()

        cursor.execute(
            "SELECT id, name, quantity, category, location, serial, expiration, notes FROM inventory"
        )
        for row in cursor.fetchall():
            data_row = ft.DataRow(
                on_select_change=handle_row_selection_change,
                cells=[
                    ft.DataCell(ft.Text(str(row[1]))),  # name
                    ft.DataCell(ft.Text(row[2] or "")),  # quantity
                    ft.DataCell(ft.Text(row[3] or "")),  # category
                    ft.DataCell(ft.Text(row[4] or "")),  # location
                    ft.DataCell(ft.Text(row[5] or "")),  # serial
                    ft.DataCell(ft.Text(row[6] or "")),  # expiration
                    ft.DataCell(cell_text(ft.Text(row[7] or ""))),  # notes
                ]
            )
            data_row.data = row[0]  # Store the 'id' value on the DataRow object
            inventory_table.rows.append(data_row)

        inventory_table.update()

    def delete_selected(e):      # deletes the selected item in the table
        selected_rows = [row for row in inventory_table.rows if row.selected]

        if not selected_rows:
            return

        for row in selected_rows:
            item_id = row.data  # Gets the primary key 'id'
            cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))

        conn.commit()
        load_item()

    def edit_item(e):
        selected_rows = [row for row in inventory_table.rows if row.selected]
        if len(selected_rows) != 1:
            page.overlay.append(
                ft.SnackBar(
                    content=ft.Text("Please select exactly one item to edit!"),
                    open=True,
                    bgcolor=ft.Colors.RED_600
                )
            )
            page.update()
            return
        target_row = selected_rows[0]
        item_id = target_row.data

        cursor.execute(
            "SELECT id, name, quantity, category, location, serial, expiration, notes FROM inventory WHERE id = ?",
            (item_id,)
        )
        record = cursor.fetchone()

        if record:
            edit_id.value = str(record[0])
            edit_name.value = record[1] or ""
            edit_qty.value = record[2] or ""
            edit_category.value = record[3] if record[3] in category else None
            edit_location.value = record[4] or ""
            edit_serial.value = record[5] or ""
            edit_expire.value = record[6] or ""
            edit_notes.value = record[7] or ""

        edit_name.error_text = None
        edit_dialog.open = True
        page.update()

    edit_id = ft.Text(visible=False)
    edit_name = ft.TextField(label="Item Name", width=250)
    edit_qty = ft.TextField(label="Quantity", width=250)
    edit_category = ft.Dropdown(label="Category", width=250, options=category_dd)
    edit_location = ft.Dropdown(label="Location", width=250, options = location_dd)
    edit_serial = ft.TextField(label="Serial #", width=250)
    edit_expire = ft.TextField(label="Expiration", width=250)
    edit_notes = ft.TextField(label="Notes", width=250, multiline=True)

    def close_popup(e):
        edit_dialog.open = False
        page.update()

    def save_edited_item(e):
        if not edit_name.value or not edit_name.value.strip():
            edit_name.error_text = "Item Name required"
            edit_name.update()
            return
        cursor.execute("""
                       UPDATE inventory
                       SET name       = ?,
                           quantity   = ?,
                           category   = ?,
                           location   = ?,
                           serial     = ?,
                           expiration = ?,
                           notes      = ?
                       WHERE id = ?
                       """, (
                           edit_name.value.strip(),
                           edit_qty.value.strip(),
                           edit_category.value,
                           edit_location.value,
                           edit_serial.value,
                           edit_expire.value,
                           edit_notes.value,
                           edit_id.value
                       ))
        conn.commit()

        edit_dialog.open = False
        load_item()
        page.update()

    edit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Item", weight=ft.FontWeight.BOLD, color=dark_blue),
        content=ft.Container(
            width=300,
            content=ft.Column(
                tight=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    edit_name,
                    edit_qty,
                    edit_category,
                    edit_location,
                    edit_serial,
                    edit_expire,
                    edit_notes,
                ]
            )
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_popup),
            ft.Button("Save", on_click=save_edited_item, bgcolor=dark_blue, color=white),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(edit_dialog)

    inventory_table = fdt.DataTable2(   #Displayed datatable
        fixed_top_rows=1,
        heading_row_color=dark_blue,
        data_text_style=ft.TextStyle(size=11, color=dark_blue),
        heading_text_style=ft.TextStyle(color=white, weight=ft.FontWeight.BOLD, size=11),
        show_checkbox_column=False,
        min_width=600,
        column_spacing=5,
        empty=ft.Text("There's no way we have nothing!"),
        columns=[
            fdt.DataColumn2(label=ft.Text("Name"), size=fdt.DataColumnSize.L),
            fdt.DataColumn2(label=ft.Text("Qty"), size=fdt.DataColumnSize.S),
            fdt.DataColumn2(label=ft.Text("Category"), size=fdt.DataColumnSize.M),
            fdt.DataColumn2(label=ft.Text("Location"), size=fdt.DataColumnSize.S),
            fdt.DataColumn2(label=ft.Text("Serial #"), size=fdt.DataColumnSize.S),
            fdt.DataColumn2(label=ft.Text("Expiration"), size=fdt.DataColumnSize.M),
            fdt.DataColumn2(label=ft.Text("Notes"), size=fdt.DataColumnSize.L),
        ],
        rows=[],
        data_row_height=60,
        expand=True
    )

    add_btn = ft.Button(
        on_click=submit_item,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.ADD,
                    size=25,
                    color=ft.Colors.GREEN
                ),
                ft.Text('Add', size=15, color=dark_blue)
            ],
        ),
        width=125,
        height=62.5,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    cancel_btn = ft.Button(    #cancel button that naviates back to home page and clears all entry fields
        on_click=clear_all_cancel,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.CANCEL,
                    size=25,
                    color=dark_gray
                ),
                ft.Text('Cancel', size=15, color=dark_blue),
            ],
        ),
        width=125,
        height=62.5,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    delete_btn = ft.Button(      # deletes the selected rows in the datatable when selected
        on_click=delete_selected,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.DELETE,
                    size=25,
                    color=ft.Colors.RED
                ),
                ft.Text('Delete', size=15, color=dark_blue),
            ],
        ),
        width=125,
        height=62.5,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    edit_btn = ft.Button(     #edits selected items in the data table and brings up a popup of the editable items
        on_click=edit_item,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.EDIT,
                    size=25,
                    color=light_blue
                ),
                ft.Text('Edit', size=15, color=dark_blue),
            ],
        ),
        width=125,
        height=62.5,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

# ADD PAGE functions and items ----------------------------------------------------------------------------------------
    item_name = ft.TextField(  #item name textfield
        label='Item Name',
        width=210,
        hint_text='Enter item name',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK
    )

    def quantity_change(e): #disables the item quantity textfield
        item_quantity.disabled = e.control.value
        item_quantity.value = ''
        item_quantity.update()

    item_quantity = ft.TextField(  #item quantity textfield
        label='Quantity',
        width=210,
        hint_text='# or click various',
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        disabled=False,
        input_filter=ft.NumbersOnlyInputFilter()
    )

    item_number_various = ft.Checkbox(  #checkbox that marks the item quantity as various and disables item quantity textfield
        label='Various',
        on_change=quantity_change
    )

    def location_visible(e): #makes sublocations visible depending on main location selection
        selected_value = e.control.value

        land_location.visible = (selected_value == 'Newport')
        ship_location.visible = (selected_value == 'Ship')
        other_location.visible = (selected_value == 'OTHER')

        #land_location.value = ''
        #ship_location.value = ''
        #other_location.value = ''

        land_location.update()
        ship_location.update()
        other_location.update()

    location = ['', 'Newport', 'Ship', 'OTHER']  #list of item main locations
    location_dd = [ft.DropdownOption(item) for item in location] #turns the list items into dropdown options

    item_location = ft.Dropdown(   #main item location dropdown (Newport, ship, other)
        label='Item Location',
        on_select=location_visible,
        width=210,
        options=location_dd
    )

    land_home = ['', 'NAL', 'BFB', 'Chemical Shed'] #list of item land locations
    land_home_dd = [ft.DropdownOption(item) for item in land_home] #turns the list items into dropdown options

    land_location = ft.Dropdown(  #Newport location dropdown (BFB, NAL, chem shed)
        label='Newport Location',
        visible=False,
        width=210,
        options=land_home_dd
    )

    ship_home = ['', 'Wet Lab', 'Acoustics', 'Chem Lab'] #list of item ship locations
    ship_home_dd = [ft.DropdownOption(item) for item in ship_home]#turns the list items into dropdown options

    ship_location = ft.Dropdown(   #ship location dropdown (wet lab, acoustics, chemlab)
        label='Ship Location',
        width=210,
        visible=False,
        options=ship_home_dd
    )

    other_location = ft.TextField(   #other location textfield
        label='Other location',
        visible=False,
        width=210
    )

    category = ['', 'Sampling/Biology', 'Stationary', 'Hardware & Tools', 'Tech/Equipment', 'Chemicals', 'Rain Gear',
                'Safety', 'Deck', 'Miscellaneous'] #list of item categories
    category_dd = [ft.DropdownOption(item) for item in category] #turns the list items into dropdown options

    item_category = ft.Dropdown(  #item category dropdown
        label='Item Category',
        width=210,
        options=category_dd
    )

    notes = ft.TextField(    #item notes textfield
        label='Notes (optional)',
        width=210,
        hint_text='Optional',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK,
        multiline=True
    )

    def serial_change(e): #enables the serial number textfield
        item_serial.disabled = not e.control.value
        item_serial.value = ''
        item_serial.update()

    item_serial = ft.TextField(   #item serial number textfield
        label='Item Serial #',
        width=210,
        keyboard_type=ft.KeyboardType.NUMBER,
        disabled=True
    )

    serial_toggle = ft.Checkbox(   #checkbox that enables the serial number textfield
        label='Serial Number',
        on_change=serial_change
    )

    def expire_change(e): #enables the item expiration date textfield
        item_expire.disabled = not e.control.value
        item_expire.value = ''
        item_expire.update()

    item_expire = ft.TextField(    #item expiration date textfield
        label='Item Expiration Date',
        width=210,
        hint_text='(MM/YY)',
        keyboard_type=ft.KeyboardType.DATETIME,
        disabled=True
    )

    expire_toggle = ft.Checkbox(   #checkbox to enable the expiration date textfield
        label='Expiration Date',
        on_change=expire_change
    )

    add_page = ft.Container(        #ADD PAGE
                expand=True,
                bgcolor=gray,
                content=ft.Column(
                    expand=True,
                    controls=[
                          ft.AppBar(
                              leading=ft.Container(
                                  padding=ft.Padding(left=15),
                                  content=ft.Row(
                                      controls=[
                                          ft.Text('Add Item', size=20, style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=white))
                                      ],
                                  )
                              ),
                              bgcolor=dark_gray,
                              center_title=False,
                          ),
                          ft.Row(
                              spacing=100,
                              alignment=ft.MainAxisAlignment.CENTER,
                              vertical_alignment=ft.CrossAxisAlignment.START,
                              controls=[
                                     ft.Column(
                                         spacing=15,
                                         controls=[
                                            item_name, ft.Column(
                                             controls=[item_quantity, item_number_various]),
                                                item_category,
                                                item_location,
                                                land_location,
                                                ship_location,
                                                other_location
                                        ]
                                     ),
                                     ft.Column(
                                         spacing=15,
                                         controls=[
                                           ft.Column(
                                               controls=[serial_toggle, item_serial]),
                                           ft.Column(
                                               controls=[expire_toggle, item_expire]),
                                                    notes
                                         ]
                                     )
                              ]
                          ),
                          ft.Container(
                              height=330,
                              content=ft.Column(controls=[inventory_table])),
                          ft.Column(
                              controls=
                              ft.Row(
                                  spacing=20,
                                  alignment=ft.MainAxisAlignment.CENTER,
                                  controls=[cancel_btn, delete_btn, edit_btn, add_btn]
                              )
                          )
                    ],
                ),
    )

#SEARCH PAGE functions and items ---------------------------------------------------------------------------------------------------------
    keyword_search = ft.TextField(    # keyword textfield for searching
        label='Search items',
        hint_text="Name, location, category...",
        width=450
    )



    search_page = ft.Container(
        content=ft.Column(
            controls=[
                ft.AppBar(
                    leading=ft.Container(
                        padding=ft.Padding.only(left=15),
                        content=ft.Row(
                            controls=[ft.Text('Item Search', size=20,
                                              style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=white))],
                        )
                    ),
                    bgcolor=dark_gray,
                    center_title=False,
                    toolbar_height=40

                ),
                ft.Row(
                    spacing=100,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(spacing=15, controls=[
                            keyword_search
                        ])
                    ]
                ),
                ft.Container(height=420, content=ft.Column(controls=[inventory_table])),
                ft.Column(controls=
                          ft.Row(spacing=20, alignment=ft.MainAxisAlignment.CENTER,
                                 controls=[cancel_btn, delete_btn, edit_btn]
                                 )
                          ),
            ]
        )
    )

# PACKING PAGE functions and items --------------------------------------------------------------------------------------------------------
    pack_unpack_page = ft.Container(inventory_table)

    packing_bin = []  # append when bins are entered


# Routing definition -------------------------------------------------------------------------------------------------
    def navigate_to(route_path):
        page.route = route_path
        route_change(None)

    def route_change(e):
        page.views.clear()

        # HOME / MAIN ROUTE
        if page.route == "/" or page.route == "":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[main_page],
                    padding=0,
                    spacing=0,
                )
            )
        # ADD ITEM ROUTE
        elif page.route == "/add_page":
            page.views.append(
                ft.View(
                    route="/add_page",
                    controls=[add_page],
                    padding=0,
                    spacing=0,
                )
            )
            page.update()
            load_item()  # Load AFTER rendering page
            return
        #ITEM SEARCH ROUTE
        elif page.route == '/search_page':
            page.views.append(
                ft.View(
                    route='/search_page',
                    controls = [search_page],
                    padding=0,
                    spacing=0,
                )
            )
            page.update()
            load_item()  # Load AFTER rendering page
            return
        #PACK/UNPACK ROUTE
        elif page.route == '/pack_unpack':
            load_item()
            page.views.append(
                ft.View(
                    route='/pack_unpack',
                    controls=[pack_unpack_page],
                    padding=0,
                    spacing=0,
                )
            )
    page.update()

    # Attach route listener & trigger initial view
    page.on_route_change = route_change
    page.route = "/"
    route_change(None)


if __name__ == '__main__':
    ft.run(main) #runs the entire application
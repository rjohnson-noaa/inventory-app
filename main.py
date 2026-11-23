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
    int_db()  # call the database in the main function
    # setting up the window to fit the tablet
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

    land_home = ['', 'NAL', 'BFB', 'Chemical Shed']  # list of item land locations
    land_home_dd = [ft.DropdownOption(item) for item in land_home]  # turns the list items into dropdown options

    ship_home = ['', 'Wet Lab', 'Acoustics', 'Chem Lab']  # list of item ship locations
    ship_home_dd = [ft.DropdownOption(item) for item in ship_home]  # turns the list items into dropdown options

    # Defined NOAA Colors --------------------------------------------------------------------------------------------------
    dark_blue = '#003087'
    light_blue = '#0085CA'
    white = 'white'
    gray = '#F0F0F0'
    dark_gray = '#686868'

    # MAIN PAGE functions and items -------------------------------------------------------------------
    add_item_btn = ft.Button(  # add item button
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

    search_item_btn = ft.Button(  # search item button on main page
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

    pack_unpack_btn = ft.Button(  # pack/unpack button on main page
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

    # DATA TABLE aspects ---------------------------------------------------------------------------------------------------
    def cell_text(val, size=13):  # Makes the overflow text into an ellipsis in the data table
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

    def submit_item(e):  # function that adds an item into the database and table
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

    def clear_all_cancel(e):  # clears all fields when navigating off the page
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

        keyword_search.value = '' #on search page

        selected_item_ids.clear()
        for row in inventory_table.rows:
            row.selected = False

        navigate_to('/')
        page.update()

    selected_item_ids = set()

    def handle_row_selection_change(e: ft.Event[fdt.DataRow2]):  # row selection in the datatable
        e.control.selected = not e.control.selected
        if e.control.selected:
            selected_item_ids.add(e.control.data)
        else:
            selected_item_ids.discard(e.control.data)
        e.control.update()

    def load_item(
            search_query: str = ""):  # loads items from the DB into the app so they are saved upon opening and closing
        inventory_table.rows.clear()

        query_str = (search_query or "").strip()

        if query_str:
            sql = """
                  SELECT id, \
                         name, \
                         quantity, \
                         category, \
                         location, \
                         serial, \
                         expiration, \
                         notes
                  FROM inventory
                  WHERE name LIKE ?
                     OR quantity LIKE ?
                     OR category LIKE ?
                     OR location LIKE ?
                     OR serial LIKE ?
                     OR expiration LIKE ?
                     OR notes LIKE ? \
                  """
            wildcard = f"%{query_str}%"
            cursor.execute(sql, (wildcard, wildcard, wildcard, wildcard, wildcard, wildcard, wildcard))
        else:
            cursor.execute(
                "SELECT id, name, quantity, category, location, serial, expiration, notes FROM inventory"
            )

        for row in cursor.fetchall():
            data_row = ft.DataRow(
                selected=(row[0] in selected_item_ids),
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

    def delete_selected(e):  # deletes the selected item in the table
        selected_rows = [row for row in inventory_table.rows if row.selected]

        if not selected_rows:
            return

        for row in selected_rows:
            item_id = row.data  # Gets the primary key 'id'
            cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            selected_item_ids.discard(item_id)

        conn.commit()
        load_item()

    # MULTI-ITEM EDIT DIALOG STATE & FUNCTIONS -------------------------------------------------------------
    active_edit_fields = []  # List of dictionaries holding each item's input controls

    def close_popup(e):
        edit_dialog_popup.open = False
        page.update()

    def save_edited_items(e):
        # Validate that all items have a name
        has_error = False
        for fields in active_edit_fields:
            if not fields["name"].value or not fields["name"].value.strip():
                fields["name"].error_text = "Name required"
                fields["name"].update()
                has_error = True
            else:
                fields["name"].error_text = None
                fields["name"].update()

        if has_error:
            return

        for fields in active_edit_fields:
            sub_loc = (
                fields["land"].value if fields["location"].value == "Newport"
                else fields["ship"].value if fields["location"].value == "Ship"
                else fields["other"].value.strip() if fields["location"].value == "OTHER"
                else ""
            )

            edit_location_display = f"{fields['location'].value or ''}{f' / {sub_loc}' if sub_loc else ''}"

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
                               fields["name"].value.strip(),
                               fields["qty"].value.strip(),
                               fields["category"].value,
                               edit_location_display,
                               fields["serial"].value,
                               fields["expire"].value,
                               fields["notes"].value,
                               fields["id"]
                           ))
        conn.commit()

        edit_dialog_popup.open = False
        load_item(keyword_search.value if page.route == '/search_page' else "")
        page.update()

    def edit_item(e):
        selected_rows = [row for row in inventory_table.rows if row.selected]
        if not selected_rows:
            page.overlay.append(
                ft.SnackBar(
                    content=ft.Text("Please select at least one item to edit!"),
                    open=True,
                    bgcolor=ft.Colors.RED_600
                )
            )
            page.update()
            return

        active_edit_fields.clear()
        edit_items_column.controls.clear()

        for idx, row in enumerate(selected_rows):
            item_id = row.data
            cursor.execute(
                "SELECT id, name, quantity, category, location, serial, expiration, notes FROM inventory WHERE id = ?",
                (item_id,)
            )
            record = cursor.fetchone()
            if not record:
                continue

            raw_loc = record[4] or ""
            if " / " in raw_loc:
                primary_loc, sub_loc = raw_loc.split(" / ", 1)
            else:
                primary_loc, sub_loc = raw_loc, ""

            # Create controls for this specific item
            e_name = ft.TextField(label="Item Name", width=250, value=record[1] or "")
            e_qty = ft.TextField(label="Quantity", width=250, value=record[2] or "")
            e_category = ft.Dropdown(
                label="Category",
                width=250,
                options=[ft.DropdownOption(item) for item in category],
                value=record[3] if record[3] in category else None
            )

            e_land = ft.Dropdown(
                label='Newport Location',
                visible=(primary_loc == 'Newport'),
                width=250,
                options=[ft.DropdownOption(item) for item in land_home],
                value=sub_loc if primary_loc == "Newport" and sub_loc in land_home else None
            )
            e_ship = ft.Dropdown(
                label='Ship Location',
                width=250,
                visible=(primary_loc == 'Ship'),
                options=[ft.DropdownOption(item) for item in ship_home],
                value=sub_loc if primary_loc == "Ship" and sub_loc in ship_home else None
            )
            e_other = ft.TextField(
                label='Other location',
                visible=(primary_loc == 'OTHER'),
                width=250,
                value=sub_loc if primary_loc == "OTHER" else ""
            )

            # Handler scoped to this specific item's location controls
            def make_location_handler(land_ctrl, ship_ctrl, other_ctrl):
                def on_loc_change(evt):
                    val = evt.control.value
                    land_ctrl.visible = (val == 'Newport')
                    ship_ctrl.visible = (val == 'Ship')
                    other_ctrl.visible = (val == 'OTHER')
                    land_ctrl.update()
                    ship_ctrl.update()
                    other_ctrl.update()
                return on_loc_change

            e_location = ft.Dropdown(
                label="Location",
                width=250,
                options=[ft.DropdownOption(item) for item in location],
                value=primary_loc if primary_loc in location else None,
                on_select=make_location_handler(e_land, e_ship, e_other)
            )

            e_serial = ft.TextField(label="Serial #", width=250, value=record[5] or "")
            e_expire = ft.TextField(label="Expiration", width=250, value=record[6] or "")
            e_notes = ft.TextField(label="Notes", width=250, multiline=True, value=record[7] or "")

            active_edit_fields.append({
                "id": str(record[0]),
                "name": e_name,
                "qty": e_qty,
                "category": e_category,
                "location": e_location,
                "land": e_land,
                "ship": e_ship,
                "other": e_other,
                "serial": e_serial,
                "expire": e_expire,
                "notes": e_notes
            })

            # Add this item's section to the scrolling column
            edit_items_column.controls.append(
                ft.Container(
                    bgcolor=gray,
                    border_radius=8,
                    padding=10,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Text(f"Item #{idx + 1}: {record[1] or 'Untitled'}", weight=ft.FontWeight.BOLD, color=dark_blue),
                            e_name,
                            e_qty,
                            e_category,
                            e_location,
                            e_land,
                            e_ship,
                            e_other,
                            e_serial,
                            e_expire,
                            e_notes,
                        ]
                    )
                )
            )
            # Add divider between items
            if idx < len(selected_rows) - 1:
                edit_items_column.controls.append(ft.Divider(color=light_blue, thickness=2))

        edit_dialog_popup.title = ft.Text(
            f"Edit Items ({len(selected_rows)})",
            weight=ft.FontWeight.BOLD,
            color=dark_blue
        )
        edit_dialog_popup.open = True
        page.update()

    edit_items_column = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
        spacing=15,
        controls=[]
    )

    edit_dialog_popup = ft.AlertDialog(
        modal=True,
        bgcolor= gray,
        title=ft.Text("Edit Items", weight=ft.FontWeight.BOLD, color=dark_blue),
        content=ft.Container(
            width=320,
            height=500,  # Defined height enables clean vertical scrolling for multiple items
            content=ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                tight=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[edit_items_column]
            )
        ),
        actions=[
            ft.Button("Cancel", on_click=close_popup, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ft.Button("Save All", on_click=save_edited_items, bgcolor=dark_blue, color=white, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    page.overlay.append(edit_dialog_popup)

    inventory_table = fdt.DataTable2(  # Displayed datatable
        fixed_top_rows=1,
        heading_row_color=dark_blue,
        data_text_style=ft.TextStyle(size=11, color=dark_blue),
        heading_text_style=ft.TextStyle(color=white, weight=ft.FontWeight.BOLD, size=11),
        data_row_color={
            ft.ControlState.SELECTED: "#B9D9EB",
            ft.ControlState.DEFAULT: "transparent",
        },
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

    cancel_btn = ft.Button(  # cancel button that navigates back to home page and clears all entry fields
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

    delete_btn = ft.Button(  # deletes the selected rows in the datatable when selected
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

    edit_btn = ft.Button(  # edits selected items in the data table and brings up a popup of the editable items
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
    item_name = ft.TextField(  # item name textfield
        label='Item Name',
        autofocus = True,
        width=210,
        hint_text='Enter item name',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK
    )

    def quantity_change(e):  # disables the item quantity textfield
        item_quantity.disabled = e.control.value
        item_quantity.value = ''
        item_quantity.update()

    item_quantity = ft.TextField(  # item quantity textfield
        label='Quantity',
        width=210,
        hint_text='# or click various',
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        disabled=False,
        input_filter=ft.NumbersOnlyInputFilter()
    )

    item_number_various = ft.Checkbox(  # checkbox that marks the item quantity as various and disables item quantity textfield
        label='Various',
        on_change=quantity_change
    )

    def location_visible(e):  # makes sublocations visible depending on main location selection
        selected_value = e.control.value

        land_location.visible = (selected_value == 'Newport')
        ship_location.visible = (selected_value == 'Ship')
        other_location.visible = (selected_value == 'OTHER')

        land_location.update()
        ship_location.update()
        other_location.update()

    item_location = ft.Dropdown(  # main item location dropdown (Newport, ship, other)
        label='Item Location',
        on_select=location_visible,
        width=210,
        options=location_dd
    )

    land_location = ft.Dropdown(  # Newport location dropdown (BFB, NAL, chem shed)
        label='Newport Location',
        visible=False,
        width=210,
        options=land_home_dd
    )

    ship_location = ft.Dropdown(  # ship location dropdown (wet lab, acoustics, chemlab)
        label='Ship Location',
        width=210,
        visible=False,
        options=ship_home_dd
    )

    other_location = ft.TextField(  # other location textfield
        label='Other location',
        visible=False,
        width=210
    )

    item_category = ft.Dropdown(  # item category dropdown
        label='Item Category',
        width=210,
        options=category_dd
    )

    notes = ft.TextField(  # item notes textfield
        label='Notes (optional)',
        width=210,
        hint_text='Optional',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK,
        multiline=True
    )

    def serial_change(e):  # enables the serial number textfield
        item_serial.disabled = not e.control.value
        item_serial.value = ''
        item_serial.update()

    item_serial = ft.TextField(  # item serial number textfield
        label='Item Serial #',
        width=210,
        keyboard_type=ft.KeyboardType.NUMBER,
        disabled=True
    )

    serial_toggle = ft.Checkbox(  # checkbox that enables the serial number textfield
        label='Serial Number',
        on_change=serial_change
    )

    def expire_change(e):  # enables the item expiration date textfield
        item_expire.disabled = not e.control.value
        item_expire.value = ''
        item_expire.update()

    item_expire = ft.TextField(  # item expiration date textfield
        label='Item Expiration Date',
        width=210,
        hint_text='(MM/YY)',
        keyboard_type=ft.KeyboardType.DATETIME,
        disabled=True
    )

    expire_toggle = ft.Checkbox(  # checkbox to enable the expiration date textfield
        label='Expiration Date',
        on_change=expire_change
    )

    add_page = ft.Container(  # ADD PAGE
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
                                item_name,
                                ft.Column(controls=[item_quantity, item_number_various]),
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
                                ft.Column(controls=[serial_toggle, item_serial]),
                                ft.Column(controls=[expire_toggle, item_expire]),
                                notes
                            ]
                        )
                    ]
                ),
                ft.Container(
                    height=330,
                    content=ft.Column(controls=[inventory_table])
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[cancel_btn, delete_btn, edit_btn, add_btn]
                        )
                    ]
                )
            ],
        ),
    )

    # SEARCH PAGE functions and items ---------------------------------------------------------------------------------------------------------
    def input_search(e):
        load_item(e.control.value)

    keyword_search = ft.TextField(
        label='Search items',
        hint_text="Name, location, category...",
        width=450,
        on_change=input_search
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
                ft.Column(controls=[
                    ft.Row(spacing=20, alignment=ft.MainAxisAlignment.CENTER,
                           controls=[cancel_btn, delete_btn, edit_btn]
                           )
                ]),
            ]
        )
    )

    # PACKING PAGE functions and items --------------------------------------------------------------------------------------------------------


    pack_items_column = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
        spacing=10,
        controls=[]
    )

    pack_new_location = ft.TextField(
        label="New Location for Selected Items",
        hint_text="Packing bin name....",
        width=280,
    )

    def close_pack_popup(e):
        pack_dialog_popup.open = False
        page.update()

    def save_packed_items(e):
        new_loc = (pack_new_location.value or "").strip()

        # Use selected_item_ids (or fallback to currently selected rows)
        target_ids = list(selected_item_ids) if selected_item_ids else [
            row.data for row in inventory_table.rows if row.selected
        ]

        for item_id in target_ids:
            cursor.execute(
                "UPDATE inventory SET location = ? WHERE id = ?",
                (new_loc, item_id)
            )
        conn.commit()

        pack_new_location.value = ""
        selected_item_ids.clear()
        pack_dialog_popup.open = False
        load_item(keyword_search.value or "")
        page.update()

    def pack_dialog(e):
        target_ids = list(selected_item_ids) if selected_item_ids else [
            row.data for row in inventory_table.rows if row.selected
        ]

        if not target_ids:
            page.overlay.append(
                ft.SnackBar(
                    content=ft.Text("Please select at least one item to pack!"),
                    open=True,
                    bgcolor=ft.Colors.RED_600
                )
            )
            page.update()
            return

        pack_items_column.controls.clear()
        pack_new_location.value = ""
        pack_new_location.error_text = None

        for idx, item_id in enumerate(target_ids):
            cursor.execute(
                "SELECT id, name, quantity, location FROM inventory WHERE id = ?",
                (item_id,)
            )
            record = cursor.fetchone()
            if not record:
                continue

            pack_items_column.controls.append(
                ft.Container(
                    bgcolor=gray,
                    border_radius=8,
                    padding=10,
                    width=280,
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(
                                f"#{idx + 1}: {record[1] or 'Untitled'}",
                                weight=ft.FontWeight.BOLD,
                                color=dark_blue
                            ),
                            ft.Text(
                                f"Qty: {record[2] or '0'}  |  Current Loc: {record[3] or 'None'}",
                                size=12,
                                color=dark_gray
                            ),
                        ]
                    )
                )
            )
            if idx < len(target_ids) - 1:
                pack_items_column.controls.append(ft.Divider(color=light_blue, thickness=1))

        pack_dialog_popup.title = ft.Text(
            f"Pack Items ({len(target_ids)})",
            weight=ft.FontWeight.BOLD,
            color=dark_blue
        )
        pack_dialog_popup.open = True
        page.update()

    pack_btn = ft.Button(  # pack item button
        on_click=pack_dialog,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.ADD,
                    size=25,
                    color=light_blue
                ),
                ft.Text('Pack Item(s)', size=15, color=dark_blue),
            ],
        ),
        width=160,
        height=62.5,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    pack_dialog_popup = ft.AlertDialog(
        modal=True,
        bgcolor=gray,
        title=ft.Text("Pack Items", weight=ft.FontWeight.BOLD, color=dark_blue),
        content=ft.Container(
            width=320,
            height=420,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    pack_new_location,
                    ft.Divider(color=dark_blue, thickness=1),
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.AUTO,
                            controls=[pack_items_column]
                        )
                    )
                ]
            )
        ),
        actions=[
            ft.Button("Cancel", on_click=close_pack_popup, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ft.Button("Save Location", on_click=save_packed_items, bgcolor=dark_blue, color=white, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    page.overlay.append(pack_dialog_popup)


    pack_unpack_page = ft.Container(
        content=ft.Column(
            controls=[
                ft.AppBar(
                    leading=ft.Container(
                        padding=ft.Padding.only(left=15),
                        content=ft.Row(
                            controls=[ft.Text('Pack and Unpack', size=20,
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
                ft.Column(controls=[
                    ft.Row(spacing=20, alignment=ft.MainAxisAlignment.CENTER,
                           controls=[cancel_btn, pack_btn]
                           )
                ]),
            ]
        )
    )

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
        # ITEM SEARCH ROUTE
        elif page.route == '/search_page':
            page.views.append(
                ft.View(
                    route='/search_page',
                    controls=[search_page],
                    padding=0,
                    spacing=0,
                )
            )
            page.update()
            load_item()  # Load AFTER rendering page
            return
        # PACK/UNPACK ROUTE
        elif page.route == '/pack_unpack':
            page.views.append(
                ft.View(
                    route='/pack_unpack',
                    controls=[pack_unpack_page],
                    padding=0,
                    spacing=0,
                )
            )
            page.update()
            load_item()
            return

    # Attach route listener & trigger initial view
    page.on_route_change = route_change
    page.route = "/"
    route_change(None)


if __name__ == '__main__':
    ft.run(main)  # runs the entire application
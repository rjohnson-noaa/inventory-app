import flet as ft
import flet_datatable2 as fdt
import sqlite3

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


# function that runs the entire app
def main(page: ft.Page):
    int_db()
    #setting up the window to fit the tablet
    page.window.height = 960
    page.window.width = 600
    page.window.resizable = True
    page.padding = 0
    page.spacing = 0
    page.window.center()

#definitions ---------------------------------------------------------------------------------------------------------
    def quantity_change(e):
        item_quantity.disabled = e.control.value
        item_quantity.value = ''
        item_quantity.update()

    def serial_change(e):
        item_serial.disabled = not e.control.value
        item_serial.value = ''
        item_serial.update()

    def expire_change(e):
        item_expire.disabled = not e.control.value
        item_expire.value = ''
        item_expire.update()

    def location_visible(e):
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

    def navigate_to(route_path):
        page.route = route_path
        route_change(None)

    def cell_text(val, size=13):
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



    def submit_item(e):
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

        # Inline ternary inside f-string for location display ("Newport / NAL" or "Newport")
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

    # Refresh the page or update the table control
        page.update()



    def clear_all_cancel (e):
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

    def handle_row_selection_change(e: ft.Event[fdt.DataRow2]):
        e.control.selected = not e.control.selected
        e.control.update()

    def load_item():

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


    def delete_selected(e):
        selected_rows = [row for row in inventory_table.rows if row.selected]

        if not selected_rows:
            return

        for row in selected_rows:
            item_id = row.data  # Gets the primary key 'id'
            cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))

        conn.commit()
        load_item()


    # Applicable lists and dropdowns----------------------------------------------------------------------------------------------
    category = ['','Sampling/Biology', 'Stationary', 'Hardware & Tools', 'Tech/Equipment', 'Chemicals', 'Rain Gear',
                'Safety', 'Deck', 'Miscellaneous']
    category_dd = [ft.DropdownOption(item) for item in category]
    land_home = ['','NAL', 'BFB', 'Chemical Shed']
    land_home_dd = [ft.DropdownOption(item) for item in land_home]
    ship_home = ['','Wet Lab', 'Acoustics', 'Chem Lab']
    ship_home_dd = [ft.DropdownOption(item) for item in ship_home]
    location = ['','Newport', 'Ship', 'OTHER'] #POPULATE SHIP, NEWPORT, OR OTHER
    location_dd = [ft.DropdownOption(item) for item in location]
    packing_bin = []  # append when bins are entered

# All other page elements ------------------------------------------------------------------------------------------
    dark_blue = '#003087'
    light_blue = '#0085CA'
    white = 'white'
    gray = '#F0F0F0'
    dark_gray = '#686868'

#data table
    inventory_table = fdt.DataTable2(
        fixed_top_rows=1,
        heading_row_color= dark_blue,
        data_text_style=ft.TextStyle(size=11, color = dark_blue),
        heading_text_style=ft.TextStyle(color = white, weight= ft.FontWeight.BOLD,size=11),
        show_checkbox_column=False,
        min_width = 600 ,
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
        expand = True
                )

#item name entry
    item_name = ft.TextField(
        label='Item Name',
        width = 210,
        hint_text='Enter item name',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK
    )

# various check box
    item_number_various = ft.Checkbox(
        label='Various',
        on_change=quantity_change
    )

#item quantity entry
    item_quantity = ft.TextField(
        label='Quantity',
        width=210,
        hint_text='# or click various',
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        disabled=False,
        input_filter = ft.NumbersOnlyInputFilter()
    )

#item location, newport, ship or other
    item_location = ft.Dropdown(
        label = 'Item Location',
        on_select=location_visible,
        width=210,
        options=location_dd
    )

#newport location
    land_location = ft.Dropdown(
        label='Newport Location',
        visible = False,
        width=210,
        options=land_home_dd
    )

#ship location
    ship_location = ft.Dropdown(
        label='Ship Location',
        width=210,
        visible = False,
        options=ship_home_dd
    )

#other location entry
    other_location = ft.TextField(
        label= 'Other location',
        visible = False,
        width=210
    )

#item category
    item_category = ft.Dropdown(
        label='Item Category',
        width=210,
        options=category_dd
    )

#notes text field
    notes = ft.TextField(
        label='Notes (optional)',
        width=210,
        hint_text='Optional',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK,
        multiline = True
    )

# serial number check box
    serial_toggle = ft.Checkbox(
        label = 'Serial Number',
        on_change = serial_change
    )

# serial number entry
    item_serial = ft.TextField(
        label = 'Item Serial #',
        width=210,
        keyboard_type=ft.KeyboardType.NUMBER,
        disabled=True
    )

# expiration date toggle
    expire_toggle = ft.Checkbox(
        label = 'Expiration Date',
        on_change = expire_change
    )

# expiration date entry
    item_expire = ft.TextField(
        label='Item Expiration Date',
        width=210,
        hint_text='(MM/YY)',
        keyboard_type=ft.KeyboardType.DATETIME,
        disabled=True
    )

#keyword textfield for searching
    keyword = ft.TextField(
        label = 'Keyword',
        width = 210
    )

#add item button on main page
    add_item_btn=ft.Button(
        on_click = lambda _: navigate_to('/add_page'),
        content = ft.Row(
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
        width = 300,
        height = 150,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

# search item button on main page
    search_item_btn = ft.Button(
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

# pack/unpack button on main page
    pack_unpack_btn = ft.Button(
        on_click = lambda _: navigate_to('/pack_unpack'),
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

# add button on item add page
    add_btn = ft.Button(
        on_click = submit_item,
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

# cancel button on add item page, item search page, and item pack page
    cancel_btn = ft.Button(
        on_click = clear_all_cancel,
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

    delete_btn = ft.Button(
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




    # Defined pages-------------------------------------------------------------------------------------------------

# Packing page --------------------------------------------------------------------------------------------------------
    pack_unpack_page = ft.Container()

# Search item page -----------------------------------------------------------------------------------------------------
    search_page = ft.Container(
        content=ft.Column(
            controls =[
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
                           keyword, item_category, item_location, land_location, ship_location, other_location
                       ]),
                       ft.Column(
                           spacing=15,
                           controls=[
                               ft.Column(controls=[serial_toggle, expire_toggle])
                           ]
                       )
                   ]
                ),
                ft.Container(height = 420, content = ft.Column(controls = [inventory_table])),
                ft.Column(controls=
                    ft.Row(
                        spacing=250,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[cancel_btn]#add search button
                    )
                ),
            ]
        )
    )

#Add item page----------------------------------------------------------------------------------------------------------
    add_page = ft.Container(expand=True, bgcolor = gray,
        content=ft.Column( expand=True,
            controls =[
                ft.AppBar(
                    leading = ft.Container(
                        padding = ft.Padding(left=15),
                        content= ft.Row(
                            controls = [ft.Text('Add Item', size=20, style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=white))],
                        )
                    ),
                    bgcolor=dark_gray,
                    center_title=False,
                ),
                ft.Row(spacing = 100 , alignment=ft.MainAxisAlignment.CENTER, vertical_alignment = ft.CrossAxisAlignment.START,
                    controls = [
                        ft.Column(spacing = 15, controls=[
                            item_name, ft.Column(controls =[item_quantity, item_number_various]), item_category, item_location, land_location, ship_location, other_location
                        ]),
                        ft.Column(spacing=15,
                            controls = [
                                ft.Column(controls=[serial_toggle, item_serial]), ft.Column(controls=[expire_toggle, item_expire]), notes

                            ]
                        )
                    ]
                ),
                ft.Container(height = 330, content = ft.Column(controls = [inventory_table])),
                ft.Column(controls =
                    ft.Row(spacing = 20, alignment = ft.MainAxisAlignment.CENTER,
                        controls = [cancel_btn, delete_btn, add_btn]
                    )
                )
            ],
        ),
    )
# Main page ------------------------------------------------------------------------------------------------------------
    main_page = ft.Container(
        expand=True,
        bgcolor=gray,
        content=ft.Column(expand=True,
            controls= [
                ft.AppBar(
                    leading = ft.Container(
                        padding = 15,
                        content=ft.Image(
                        src = '../inventory-app/noaalogo.png'
                        )
                    ),
                    leading_width = 90,
                    title = ft.Text('IWCPS Inventory', size=40, style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=white)),
                    center_title=True,
                    bgcolor=dark_gray,
                    toolbar_height = 100
                ),
                ft.Container(
                    height=130
                ),
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[add_item_btn]
                        ),
                        ft.Container(
                            height=20
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[search_item_btn]
                        ),
                        ft.Container(
                            height=20
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[pack_unpack_btn]
                        )
                    ]
                ),
            ]
        )
    )

# Routing definition -------------------------------------------------------------------------------------------------
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
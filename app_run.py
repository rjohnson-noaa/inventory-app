

import flet as ft

#####USE SORTABLE COLUMNS AND SELECTED ROWS FOR ITEM PAGE USE DATATABLE2


# function that runs the entire app
def main(page: ft.Page):
    #setting up the window to fit the tablet
    page.window.width = 600
    page.window.height = 960
    page.window.resizable = True
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

    #def entry_correct(e):
       # value = item_name.value.strip() if item_name.value else ''

        #if not value:
      #      item_name.error_text = "Please enter the item name"
      #  else:
       #     item_name.error_text = None
       # item_name.update()

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

    item_name = ft.TextField(
        label='Item Name',
        width = 210,
        hint_text='Enter item name',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK,
        autofocus=True
    ) # item name text box

    item_number_various = ft.Checkbox(
        label='Various',
        on_change=quantity_change
    ) #quantity checkbox

    item_quantity = ft.TextField(
        label='Quantity',
        width=210,
        hint_text='# or click various',
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        disabled=False,
        input_filter = ft.NumbersOnlyInputFilter()
    )# item quantity text box

    item_location = ft.Dropdown(
        label = 'Item Location',
        on_select=location_visible,
        width=210,
        options=location_dd
    )

    land_location = ft.Dropdown(
        label='Newport Location',
        visible = False,
        width=210,
        options=land_home_dd
    )  # land location drop down

    ship_location = ft.Dropdown(
        label='Ship Location',
        width=210,
        visible = False,
        options=ship_home_dd
    )  # ship location drop down

    other_location = ft.TextField(
        label= 'Other location',
        visible = False,
        width=210
    )

    item_category = ft.Dropdown(
        label='Item Category',
        width=210,
        options=category_dd
    )  # item category drop down

    notes = ft.TextField(
        label='Notes (optional)',
        width=210,
        hint_text='Optional',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK,
        multiline = True,
        min_lines = 7,
        max_lines = 10
    ) # notes textfield

    serial_toggle = ft.Checkbox(
        label = 'Serial Number?',
        on_change = serial_change
    ) # serial number checkbox

    item_serial = ft.TextField(
        label = 'Item Serial #',
        width=210,
        keyboard_type=ft.KeyboardType.NUMBER,
        disabled=True
    ) #serial number entry

    expire_toggle = ft.Checkbox(
        label = 'Expiration Date?',
        on_change = expire_change
    ) #expiration date toggle

    item_expire = ft.TextField(
        label='Item Expiration Date',
        width=210,
        hint_text='(MM/YY)',
        keyboard_type=ft.KeyboardType.DATETIME,
        disabled=True
    ) # expiration date entry

    add_item_btn=ft.Button(
        content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            #on_click = ,
            controls=[
                ft.Icon(
                    icon=ft.Icons.ADD,
                    size=40,
                    color=light_blue
                ),
                ft.Text('Add Item', size=35)
            ],
        ),
        width = 300,
        height = 150,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    search_item_btn = ft.Button(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.SEARCH,
                    size=40,
                    color=light_blue
                ),
                ft.Text('Item Search', size=35)
            ],
        ),
        width=300,
        height=150,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    pack_unpack_btn = ft.Button(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.INVENTORY_2_OUTLINED,
                    size=40,
                    color=light_blue
                ),
                ft.Text('Pack/Unpack', size=35)
            ],
        ),
        width=300,
        height=150,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    add_btn = ft.Button(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.ADD,
                    size=20,
                    color=ft.Colors.GREEN
                ),
                ft.Text('Add', size=15)
            ],
        ),
        width=125,
        height=62.5,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    cancel_btn = ft.Button(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icon=ft.Icons.CANCEL,
                    size=20,
                    color=ft.Colors.RED
                ),
                ft.Text('Cancel', size=15)
            ],
        ),
        width=125,
        height=62.5,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    # Defined page contents-------------------------------------------------------------------------------------------------

    add_page = ft.Container(
        content=ft.Column(
            controls =[
                ft.AppBar(
                    leading = ft.Container(
                        padding = ft.Padding(left=15),
                        content= ft.Row(
                            controls = [ft.Text('Add Item', size=20, style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=white))],
                        )
                    ),
                    bgcolor=dark_gray,
                    center_title=False
                ),
                #ft.Container(
                 # height = 40
                #),
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
                ft.Column(controls =
                    ft.Row(spacing = 250, alignment = ft.MainAxisAlignment.CENTER,
                        controls = [cancel_btn, add_btn]
                    )
                )
            ],
        ),
    )

    main_page = ft.Container(
        width=600,
        height=960,
        bgcolor=gray,
        content=ft.Column(
            controls= [
                ft.AppBar(
                    leading = ft.Container(
                        padding=ft.Padding(left=15),
                        content=ft.Image(
                        src = 'C:/Git/inventory-app/noaalogo.png'
                        )
                    ),
                    leading_width = 80,
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
    )  # what stays the entire time

    # Dictionary to combine pages as views into one and links the routing variables
    pages = {}

    # Add pages to the application, likely just the home page that runs the entire session
    page.add(add_page)


ft.run(main) #runs the entire application
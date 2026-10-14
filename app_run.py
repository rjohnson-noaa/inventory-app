import flet as ft


# function that runs the entire app
def main(page: ft.Page):
    #setting up the window to fit the tablet
    page.window.width = 600
    page.window.height = 960
    page.window.resizable = True
    page.window.center()
    page.padding = 15

    #definitions ---------------------------------------------------------------------------------------------------------
    def quantity_change(e):
        item_quantity.disabled = e.control.value
        item_quantity.value = ''
        item_quantity.update()

    def serial_change(e):
        item_serial.disabled = not e.control.value
        item_serial.update()

    def expire_change(e):
        item_expire.disabled = not e.control.value
        item_expire.update()

    def entry_correct(e):
        value = item_name.value.strip() if item_name.value else ''

        if not value:
            item_name.error_text = "Please enter the item name"
        else:
            item_name.error_text = None
        item_name.update()

    # Applicable lists and dropdowns----------------------------------------------------------------------------------------------
    category = ['Sampling/Biology', 'Stationary', 'Hardware & Tools', 'Tech/Equipment', 'Chemicals', 'Rain Gear',
                'Safety', 'Deck', 'Miscellaneous']
    category_dd = [ft.DropdownOption(item) for item in category]
    land_home = ['NAL', 'BFB', 'Chemical Shed']
    land_home_dd = [ft.DropdownOption(item) for item in land_home]
    ship_home = ['Wet Lab', 'Acoustics', 'Chem Lab']
    ship_home_dd = [ft.DropdownOption(item) for item in ship_home]
    packing_bin = []  # append when bins are entered

    # All other page elements ------------------------------------------------------------------------------------------
    dark_blue = '#003087'
    light_blue = '#0085CA'
    white = 'white'
    gray = '#F0F0F0'

    item_name = ft.TextField(
        label='Item Name',
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
        hint_text='Enter a number or click various',
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        disabled=False,
        input_filter = ft.NumbersOnlyInputFilter()
    )# item quantity text box

    item_location = ft.Dropdown(
        label='Land Location',
        width=220,
        options=land_home_dd
    )  # land location drop down

    ship_location = ft.Dropdown(
        label='Ship Location',
        width=220,
        options=ship_home_dd
    )  # ship location drop down

    item_category = ft.Dropdown(
        label='Item Category',
        width=220,
        options=category_dd
    )  # item category drop down

    notes = ft.TextField(
        label='Notes (optional)',
        hint_text='Optional',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK,
        multiline = True,
        min_lines = 2,
        max_lines = 5
    ) # notes textfield

    serial_toggle = ft.Checkbox(
        label = 'Serial Number?',
        on_change = serial_change
    ) # serial number checkbox

    item_serial = ft.TextField(
        label = 'Item Serial #',
        hint_text='Enter serial number if applicable',
        keyboard_type=ft.KeyboardType.NUMBER,
        disabled=True
    ) #serial number entry

    expire_toggle = ft.Checkbox(
        label = 'Expiration Date?',
        on_change = expire_change
    ) #expiration date toggle

    item_expire = ft.TextField(
        label='Item Expiration Date',
        hint_text='(MM/YY)',
        keyboard_type=ft.KeyboardType.DATETIME,
        disabled=True
    ) # expiration date entry

    add_item_btn=ft.Button(
        content=ft.Text('Add Item', size=20),
        width = 250,
        height = 100,
        icon=ft.Icons.ADD,
        icon_color=light_blue,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))


    # Defined page contents-------------------------------------------------------------------------------------------------
    home_page_contents = ft.Container()

    item_page_contents = ft.Container(
        content=ft.Column(
            controls=[item_quantity, ft.Row(controls=[item_expire, expire_toggle]), notes
                      ]
        )
    )

    main_page = ft.Container(
        width=600,
        height=960,
        bgcolor=gray,
        content=ft.Column(
            controls= [
                ft.AppBar(
                    title = ft.Text('IWCPS Inventory', size=40, style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=white)),
                    center_title=True,
                    bgcolor=light_blue
                )
            ]
        )
    )  # what stays the entire time

    # Dictionary to combine pages as views into one and links the routing variables
    pages = {}

    # Add pages to the application, likely just the home page that runs the entire session
    page.add(main_page)



ft.run(main) #runs the entire application
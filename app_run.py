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
        item_quantity.update() #disables the textbox in item_quantity

    def serial_change(e):
        item_serial.disabled = not e.control.value
        item_serial.update()

    # Applicable lists ----------------------------------------------------------------------------------------------------
    category = ['Sampling/Biology', 'Stationary', 'Hardware & Tools', 'Tech/Equipment', 'Chemicals', 'Rain Gear',
                'Safety', 'Deck', 'Miscellaneous']
    category_dd = [ft.DropdownOption(item) for item in category]
    land_home = ['NAL', 'BFB', 'Chemical Shed']
    land_home_dd = [ft.DropdownOption(item) for item in land_home]
    ship_home = ['Wet Lab', 'Acoustics', 'Chem Lab']
    ship_home_dd = [ft.DropdownOption(item) for item in ship_home]
    packing_bin = []  # append when bins are entered

    # Page elements and variables ------------------------------------------------------------------------------------------
    dark_blue = '#003087'
    light_blue = '#0085CA'
    white = 'white'

    item_input = ft.TextField(
        label='Item Name',
        hint_text='Enter item name',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK,
        autofocus=True
    )  # item name text box

    item_number_various = ft.Checkbox(
        label='Various',
        on_change=quantity_change
    ) #quantity checkbox

    item_quantity = ft.TextField(
        label='Quantity',
        hint_text='Enter a number or click various',
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        disabled=False
    )  # item quantity text box

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
        label='Notes',
        hint_text='Optional',
        keyboard_type=ft.KeyboardType.TEXT,
        color=ft.Colors.BLACK,
        multiline = True,
        min_lines = 2,
        max_lines = 5
    ) # notes textfield

    serial_num_toggle = ft.Checkbox(
        label = 'Serial Number?',
        on_change = serial_change
    )

    item_serial = ft.TextField(
        label = 'Item Serial #',
        hint_text='Enter serial number if applicable',
        keyboard_type=ft.KeyboardType.NUMBER,
        disabled=True
    )

    item_expire = ft.Text



    # Defined page contents-------------------------------------------------------------------------------------------------
    home_page_contents = ft.Container()

    item_page_contents = ft.Container(
        content=ft.Column(
            controls=[item_input, ft.Row(controls=[item_serial, serial_num_toggle]), notes
                      ]
        )
    )

    main_page = ft.Container(
        width=600,
        height=960,
        bgcolor=white,
        content=ft.Stack(
            controls=[item_page_contents]
        )
    )  # what stays the entire time

    # Dictionary to combine pages as views into one and links the routing variables
    pages = {}

    # Add pages to the application, likely just the home page that runs the entire session
    page.add(main_page)



ft.run(main) #runs the entire application
import flet as ft

# Variables that house all the components for all pages
dark_blue = '#003087'
light_blue = '#0085CA'
white = 'white'

# Applicable lists
category = ['Sampling/Biology', 'Stationary', 'Hardware & Tools', 'Tech/Equipment', 'Chemicals', 'Rain Gear', 'Safety', 'Deck', 'Miscellaneous']
land_home = ['NAL', 'BFB', 'Chemical Shed']
ship_home = ['Wet Lab', 'Acoustics', 'Chem Lab']
packing_bin = [] #append when bins are entered


item_input = ft.TextField(label = 'Item Name', hint_text='Enter item name', keyboard_type=ft.KeyboardType.TEXT, color = ft.Colors.BLACK)
item_quantity = ft.TextField(label = 'Quantity', hint_text='Enter a number or click various', keyboard_type=ft.KeyboardType.NUMBER, color = ft.Colors.BLACK)


home_contents = ft.Container(ft.Column(item_input))

main_page = ft.Container(width=600, height=960, bgcolor= light_blue, content= ft.Stack(controls = [home_contents])) #what stays the entire time



# Dictionary to combine pages as views into one and links the routing variables
pages = {}


# function that runs the entire app
def main(page: ft.Page):
    #setting up the window to fit the tablet
    page.window.width = 600
    page.window.height = 960
    page.window.resizable = True
    page.window.center()
    page.padding = 15







# Add pages to the application, likely just the home page that runs the entire session
    page.add(home_contents)



ft.run(main) #runs the entire application
import flet as ft
from flet import * #import all actions/controls in flet package

# Variables that house all the components for all pages
dark_blue = '#003087'
light_blue = '#0085CA'
white = 'white'



home_page = Container(width=600, height=960, bgcolor= light_blue) #add content, such as stacked pages?






# Dictionary to combine pages as views into one and links the routing variables
pages = {}


# function that runs the entire app
def main(page: Page):
    #setting up the window to fit the tablet
    page.window.width = 600
    page.window.height = 960

    page.window.resizable = True
    page.window.center()







# Add pages to the application, likely just the home page that runs the entire session
    page.add(home_page)



ft.run(main) #runs the entire application
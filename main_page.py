import flet as ft
from flet import * #import all actions/controls in flet package


# main module where the entire app runs in. Page is a class in the flet module
def main(page: Page):
    BG = 'purple'  # create variables for unique colors

    categories_card = Row(
        scroll='auto'
    )

    categories = ['sleep', 'eat', 'drink']
    for category in categories:
        categories_card.controls.append(
            Container(
                bgcolor='blue',
                height=50,
                width=200,
                content=Column(
                    controls=[
                        Text('something goes here'),
                        Text(categories)
                    ]
                )
            )
        )

    home_page_contents = Container(
        content=Column(
            controls=[
                Row(
                    alignment='spaceBetween',
                    controls=[
                        Container(
                           content=Icon(Icons.MENU)),
                        Row(
                            controls=[
                                Icon(Icons.SEARCH),
                                Icon(Icons.NOTIFICATIONS_OUTLINED)
                            ]
                        )
                    ]
                ),
                Container(
                    height=20),
                Text(
                    value='hello world'),
                Text(
                    value='CATEGORIES'),
                Container(
                    padding=Padding(top=20, bottom=20),
                    content=categories_card
                )
            ]
        )
    )

    side_menu = Container()
    shrunk_home = Row(
        controls=[
            Container(
                width=400,
                height=850,
                bgcolor='green',
                border_radius=35,
                padding=Padding(top=50, left=20, right=20, bottom=5),
                content=Column(
                    controls=[
                        home_page_contents
                    ]
                )
            ) #container can only have one widget, so adding a column widget allows for widgets to be placed in said column
        ]
    ) #this is a row because it will be animated to "shrink" when the side menu is opened
    # container can only have one widget, so adding a column widget allows for widgets to be placed in said column

    home_page = Container(
        width=400,
        height=850,
        bgcolor=BG,
        border_radius=35,
        content=Stack(
            controls = [
                side_menu,
                shrunk_home
            ]

        ) #content = child to the main container
    )

    page.add(home_page)








ft.run(main) #runs the entire application

# to run in terminal to live update, flet -r main_page.py (DOES NOT WORK)
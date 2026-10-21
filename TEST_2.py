import flet as ft

#main function that stores everything --> class is called Page
def main(page: ft.Page):
    page.title = ('Temp Converter')
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 600
    page.window_resizable = True
    page.padding = 20

    c_input = ft.TextField(label = 'Celcius')

    f_input = ft.TextField(label = 'Farenheit')

    k_input = ft.TextField(label = 'Kelvin')






    page.add(
        ft.Column(
            controls = [ft.Text(
                "Temp converter",
                size = 28,
                weight = ft.FontWeight.BOLD,
                text_align = ft.TextAlign.CENTER,
            ),
            ft.Divider(height=20),
            c_input,
            ft.Divider(height=10),
            f_input,
            ft.Divider(height=10),
            k_input,

            ft.Divider(height=10),
            ft.Button(
                'Clear All',
                icon = ft.Icons.SEARCH
            ),

            ft.Divider(height=10),


            ]
        )
    )

if __name__ == '__main__':
    ft.run(main)
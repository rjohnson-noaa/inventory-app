import flet as ft


def main(page: ft.Page):
    page.title = "Global Search Table"
    page.padding = 20

    datax = [
        {"name": "joe", "last": "smith", "age": 12},
        {"name": "steve", "last": "smith", "age": 14},
        {"name": "rebecca", "last": "smith", "age": 12},
        {"name": "matt", "last": "jones", "age": 15},
        {"name": "jill", "last": "miller", "age": 18},
    ]

    # Helper function to convert a dictionary into an ft.DataRow
    def create_row(item):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(item["name"])),
                ft.DataCell(ft.Text(item["last"])),
                ft.DataCell(ft.Text(str(item["age"]))),
            ]
        )

    # Central function to populate the table and refresh the screen once
    def render_table(items):
        dt.rows = [create_row(item) for item in items]
        datanotfound.visible = len(items) == 0
        page.update()

    # Search filter matching query against name, last name, or age
    def inputsearch(e):
        query = search_input.value.strip().lower()

        if not query:
            filtered = datax
        else:
            filtered = [
                x for x in datax
                if query in x["name"].lower()
                or query in x["last"].lower()
                or query in str(x["age"])
            ]

        render_table(filtered)

    # UI Controls
    search_input = ft.TextField(
        label="Search by name, last name, or age...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=inputsearch,
    )

    dt = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("First Name")),
            ft.DataColumn(ft.Text("Last Name")),
            ft.DataColumn(ft.Text("Age")),
        ],
        rows=[],
    )

    datanotfound = ft.Text("No records match your search.", visible=False, color=ft.Colors.RED)

    # Initial render of all records
    render_table(datax)

    # Assemble page layout
    page.add(
        ft.Column(
            controls=[
                search_input,
                dt,
                datanotfound,
            ],
            spacing=15,
        )
    )


if __name__ == '__main__':
    ft.run(main)
import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        # Pagina
        self._page = page
        self._page.title = "Prova 6 - Generi co-acquistati per paese"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#eef4f7"
        self._page.window_width = 1000
        self._page.window_height = 700

        # Controller
        self._controller = None

        # Elementi grafici
        self._title = None

        self._ddPaese = None
        self._btnCreaGrafo = None

        self._ddStartGenre = None
        self._ddEndGenre = None
        self._txtK = None
        self._btnCercaCammino = None

        self.txt_result = None

    def load_interface(self):
        # Titolo
        self._title = ft.Text(
            "Prova 6 - Generi co-acquistati per paese",
            color="blue",
            size=24
        )

        self._page.controls.append(self._title)

        # Dropdown paese
        self._ddPaese = ft.Dropdown(
            label="Paese",
            width=300
        )
        self._controller.fillDDPaesi()
        # Bottone crea grafo
        self._btnCreaGrafo = ft.ElevatedButton(
            text="Crea Grafo",
            on_click=self._controller.handleCreaGrafo
        )

        row1 = ft.Row(
            [
                self._ddPaese,
                self._btnCreaGrafo
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self._page.controls.append(row1)

        # Dropdown genere iniziale
        self._ddStartGenre = ft.Dropdown(
            label="Start Genre",
            width=250
        )

        # Dropdown genere finale
        self._ddEndGenre = ft.Dropdown(
            label="End Genre",
            width=250
        )

        # TextField K
        self._txtK = ft.TextField(
            label="K",
            width=100
        )

        # Bottone cerca cammino
        self._btnCercaCammino = ft.ElevatedButton(
            text="Cerca cammino",
            on_click=self._controller.handleCercaCammino
        )

        row2 = ft.Row(
            [
                self._ddStartGenre,
                self._ddEndGenre,
                self._txtK,
                self._btnCercaCammino
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self._page.controls.append(row2)

        # Area risultati
        self.txt_result = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=False
        )

        self._page.controls.append(self.txt_result)

        # Riempio subito solo il dropdown Paese
        self._controller.fillDDPaesi()

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(
            title=ft.Text(message)
        )

        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
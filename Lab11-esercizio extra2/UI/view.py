import flet as ft


class View:
    def __init__(self, page: ft.Page):
        # Pagina
        self._page = page
        self._page.title = "Facsimile Chinook - Prova 2"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#eef4f7"
        self._page.window_width = 1000
        self._page.window_height = 700

        # Controller
        self._controller = None

        # Titolo
        self._title = None

        # Riga 1 - creazione grafo
        self._ddMediaType = None
        self._txtDurataMinima = None
        self._btnCreaGrafo = None
        self._btnDettagli = None

        # Riga 2 - punto 2
        self._ddStartComposer = None
        self._btnCercaPercorso = None

        # Area risultati
        self.txt_result = None

    def load_interface(self):
        # Titolo
        self._title = ft.Text(
            "Facsimile Chinook - Prova 2: Composer nelle stesse playlist",
            color="blue",
            size=24
        )

        self._page.controls.append(self._title)

        # Dropdown MediaType
        self._ddMediaType = ft.Dropdown(
            label="MediaType",
            width=300
        )
        self._controller.fillDDMediaType()

        # TextField durata minima
        self._txtDurataMinima = ft.TextField(
            label="Durata minima in minuti",
            width=220
        )

        # Bottone Crea grafo
        self._btnCreaGrafo = ft.Button(
            content="Crea grafo",
            on_click=self._controller.handleCreaGrafo
        )

        # Bottone Stampa dettagli
        self._btnDettagli = ft.Button(
            content="Stampa dettagli",
            on_click=self._controller.handleDettagli
        )

        row1 = ft.Row(
            controls=[
                self._ddMediaType,
                self._txtDurataMinima,
                self._btnCreaGrafo,
                self._btnDettagli
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self._page.controls.append(row1)

        # Dropdown Start Composer
        self._ddStartComposer = ft.Dropdown(
            label="Start Composer",
            width=350
        )

        # Bottone Cerca percorso
        self._btnCercaPercorso = ft.Button(
            content="Cerca percorso",
            on_click=self._controller.handleCercaPercorso
        )

        row2 = ft.Row(
            controls=[
                self._ddStartComposer,
                self._btnCercaPercorso
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

        # Riempio il dropdown iniziale dei MediaType
        self._controller.fillDDMediaType()

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
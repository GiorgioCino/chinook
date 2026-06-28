import flet as ft


class View:
    def __init__(self, page: ft.Page):
        # Pagina
        self._page = page
        self._page.title = "Facsimile Chinook - Prova 1"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#eef4f7"
        self._page.window_width = 1000
        self._page.window_height = 700

        # Controller
        self._controller = None

        # Titolo
        self._title = None

        # Riga 1 - input grafo
        self._ddCountry = None
        self._ddAnno = None
        self._btnCreaGrafo = None
        self._btnDettagli = None

        # Riga 2 - punto 2
        self._ddStartMediaType = None
        self._ddEndMediaType = None
        self._txtLunghezza = None
        self._btnCercaPercorso = None

        # Area risultati
        self.txt_result = None

    def load_interface(self):
        # Titolo
        self._title = ft.Text(
            "Facsimile Chinook - Prova 1: MediaType acquistati nello stesso mese",
            color="blue",
            size=24
        )

        self._page.controls.append(self._title)

        # Dropdown Country
        self._ddCountry = ft.Dropdown(
            label="Country",
            width=250
        )

        # Dropdown Anno
        self._ddAnno = ft.Dropdown(
            label="Anno",
            width=150
        )
        self._controller.fillDDAnni()

        # Bottone Crea Grafo
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
                self._ddCountry,
                self._ddAnno,
                self._btnCreaGrafo,
                self._btnDettagli
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self._page.controls.append(row1)

        # Dropdown Start MediaType
        self._ddStartMediaType = ft.Dropdown(
            label="Start MediaType",
            width=250
        )

        # Dropdown End MediaType
        self._ddEndMediaType = ft.Dropdown(
            label="End MediaType",
            width=250
        )

        # TextField lunghezza cammino
        self._txtLunghezza = ft.TextField(
            label="Lunghezza cammino",
            width=180
        )

        # Bottone Cerca percorso
        self._btnCercaPercorso = ft.Button(
            content="Cerca percorso",
            on_click=self._controller.handleCercaPercorso
        )

        row2 = ft.Row(
            controls=[
                self._ddStartMediaType,
                self._ddEndMediaType,
                self._txtLunghezza,
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

        # Riempio i dropdown iniziali
        self._controller.fillDDCountry()
        self._controller.fillDDAnni()

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
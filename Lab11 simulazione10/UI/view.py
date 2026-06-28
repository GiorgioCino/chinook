import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        # Pagina
        self._page = page
        self._page.title = "Facsimile 10 - Chinook Paesi"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#eef4f7"
        self._page.window_width = 1000
        self._page.window_height = 700

        # Controller
        self._controller = None

        # Elementi grafici
        self._title = None

        self._ddGenre = None
        self._btnCreaGrafo = None
        self._btnDettagli = None

        self._ddPaese = None
        self._btnPaesiRaggiungibili = None

        self.txt_result = None

    def load_interface(self):
        # Titolo
        self._title = ft.Text(
            "Facsimile 10 - Chinook: Paesi dei clienti",
            color="blue",
            size=24
        )

        self._page.controls.append(self._title)

        # Dropdown genere musicale
        self._ddGenre = ft.Dropdown(
            label="Genere musicale",
            width=300
        )
        self._controller.fillDDGenre()
        # Bottone crea grafo
        self._btnCreaGrafo = ft.ElevatedButton(
            text="Crea Grafo",
            on_click=self._controller.handleCreaGrafo
        )

        # Bottone dettagli
        self._btnDettagli = ft.ElevatedButton(
            text="Stampa dettagli",
            on_click=self._controller.handleDettagli
        )

        row1 = ft.Row(
            [
                self._ddGenre,
                self._btnCreaGrafo,
                self._btnDettagli
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self._page.controls.append(row1)

        # Dropdown paese per punto 2
        self._ddPaese = ft.Dropdown(
            label="Paese di partenza",
            width=300
        )

        # Bottone punto 2
        self._btnPaesiRaggiungibili = ft.ElevatedButton(
            text="Paesi raggiungibili",
            on_click=self._controller.handlePaesiRaggiungibili
        )

        row2 = ft.Row(
            [
                self._ddPaese,
                self._btnPaesiRaggiungibili
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

        # Riempio il dropdown iniziale dei generi
        self._controller.fillDDGenre()

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
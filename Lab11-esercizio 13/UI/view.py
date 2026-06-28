import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()

        # Pagina
        self._page = page
        self._page.title = "Facsimile 13 - Chinook Artisti in Playlist"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#eef4f7"
        self._page.window_width = 1000
        self._page.window_height = 700

        # Controller
        self._controller = None

        # Elementi grafici
        self._title = None

        self._ddPlaylist = None
        self._btnCreaGrafo = None
        self._btnDettagli = None

        self._ddArtistaStart = None
        self._btnArtistiRaggiungibili = None

        self.txt_result = None

    def load_interface(self):
        # Titolo
        self._title = ft.Text(
            "Facsimile 13 - Chinook: Artisti in playlist",
            color="blue",
            size=24
        )

        self._page.controls.append(self._title)

        # Dropdown playlist
        self._ddPlaylist = ft.Dropdown(
            label="Playlist",
            width=350
        )
        self._controller.fillDDPlaylist()

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
                self._ddPlaylist,
                self._btnCreaGrafo,
                self._btnDettagli
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self._page.controls.append(row1)

        # Dropdown artista di partenza per il punto 2
        self._ddArtistaStart = ft.Dropdown(
            label="Artista di partenza",
            width=350
        )

        # Bottone punto 2
        self._btnArtistiRaggiungibili = ft.ElevatedButton(
            text="Artisti raggiungibili",
            on_click=self._controller.handleArtistiRaggiungibili
        )

        row2 = ft.Row(
            [
                self._ddArtistaStart,
                self._btnArtistiRaggiungibili
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

        # Riempimento dropdown playlist
        self._controller.fillDDPlaylist()

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
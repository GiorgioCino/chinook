import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _get_selected_item(self, dropdown):
        for option in dropdown.options:
            if str(option.key) == str(dropdown.value):
                return option.data

        return None

    def fillDDGenre(self):
        lista_generi = DAO.get_all_genres()

        self._view._ddGenre.options.clear()

        for genere in lista_generi:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(
                    key=genere.GenreId,
                    text=str(genere),
                    data=genere
                )
            )

        self._view._ddGenre.value = None

    def fillDDArtist(self, lista_artisti):
        self._view._ddArtist.options.clear()

        for artista in lista_artisti:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(
                    key=artista.ArtistId,
                    text=str(artista),
                    data=artista
                )
            )

        self._view._ddArtist.value = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        genere = self._get_selected_item(self._view._ddGenre)

        if genere is None:
            self._view.create_alert("Seleziona un genere.")
            return

        n_nodi, n_archi = self._model.build_graph(genere)

        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {n_nodi}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {n_archi}")
        )

        self._view.update_page()

    def handleCammino(self, e):
        self._view.txt_result.controls.clear()

        artista = self._get_selected_item(self._view._ddArtist)

        if artista is None:
            self._view.create_alert("Seleziona un artista.")
            return

        cammino, peso = self._model.cerca_cammino(artista)

        if len(cammino) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Non esiste nessun cammino valido.")
            )
        else:
            self._view.txt_result.controls.append(
                ft.Text("Cammino trovato:")
            )

            for artista in cammino:
                self._view.txt_result.controls.append(
                    ft.Text(str(artista))
                )

            self._view.txt_result.controls.append(
                ft.Text(f"Peso finale: {peso}")
            )

        self._view.update_page()



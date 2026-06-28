import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _get_selected_item(self, dropdown):
        for option in dropdown.options:
            if str(option.key) == str(dropdown.value):
                return option.data

        return None

    def fillDDGeneri(self):
        lista_generi = DAO.getAllGenres()

        self._view._ddGenere.options.clear()

        for genere in lista_generi:
            self._view._ddGenere.options.append(
                ft.dropdown.Option(
                    key=genere.GenreId,
                    text=genere,
                    data=genere
                )
            )

        self._view._ddGenere.value = None

    def fillDDGeneriGrafo(self):
            playlists = self._model.get_nodi_grafo()

            self._view._ddPlaylistStart.options.clear()

            for playlist in playlists:
                self._view._ddPlaylistStart.options.append(
                    ft.dropdown.Option(
                        key=str(playlist.PlaylistId),
                        text=str(playlist),
                        data=playlist
                    )
                )

            self._view._ddPlaylistStart.value = None
            self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        genere = self._view._ddGenere.value

        if genere is None:
            self._view.create_alert("Seleziona un genere.")
            return

        n_nodi, n_archi = self._model.buildGraph(genere)

        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {n_nodi}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {n_archi}")
        )
        # PER INSERIRE GENERI DI PARTENZA DOPO LA CREAZIONE DEL GRAFO
        self.fillDDGeneriGrafo()
        self._view.update_page()

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodes() == 0:
            self._view.txt_result.controls.append(
                ft.Text("Crea prima il grafo.")
            )
            self._view.update_page()
            return

        archi = self._model.get_edges_info()

        self._view.txt_result.controls.append(
            ft.Text("Top 5 archi di peso maggiore:")
        )

        if len(archi) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun arco presente nel grafo.")
            )
        else:
            for c1, c2, peso in archi:
                self._view.txt_result.controls.append(
                    ft.Text(f"{c1} -> {c2}: peso = {peso}")
                )

        nodo, influenza = self._model.get_nodo_piu_influente()

        self._view.txt_result.controls.append(
            ft.Text(f"Nodo più influente: {nodo} - influenza: {influenza}")
        )

        self._view.update_page()

    def handleCercaPercorso(self,e):
        pass
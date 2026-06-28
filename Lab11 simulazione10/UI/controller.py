import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getAllGenres()

        self._view._ddGenre.options.clear()

        for genere in generi:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(
                    key=str(genere.GenreId),
                    text=str(genere),
                    data=genere
                )
            )

        self._view._ddGenre.value = None
        self._view.update_page()

    def get_selected_item(self, dropdown):
        for option in dropdown.options:
            if str(option.key) == str(dropdown.value):
                return option.data

        return None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        genere = self.get_selected_item(self._view._ddGenre)

        if genere is None:
            self._view.create_alert("Seleziona un genere.")
            return

        n_nodi, n_archi = self._model.build_graph(genere.GenreId)

        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato per il genere: {genere.Name}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi: {n_nodi}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {n_archi}")
        )
        # Riempio il dropdown dei paesi per il punto 2
        self.fillDDPaesi()

        self._view.update_page()

    def handleDettagli(self, e):

        self._view.txt_result.controls.clear()

        archi = self._model.get_edges_info()

        if len(archi) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun arco trovato. Crea prima il grafo.")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text("Dettagli degli archi:")
        )

        for c1, c2, peso in archi:
            self._view.txt_result.controls.append(
                ft.Text(f"{c1} - {c2}: {peso} arc condivisi")
            )

        sizeCompConn = self._model.getInfoCompConnessa()

        self._view.txt_result.controls.append(
            ft.Text(f"componente connessa contente oggetto è composta di {sizeCompConn} nodi"))

        compMaggiore = self._model.getComponenteMaggiore()
        mag = len(compMaggiore)

        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa di dimensione maggiore:{mag} ")
        )

        for nodo in compMaggiore:
            self._view.txt_result.controls.append(
                ft.Text(f"{nodo}")
            )

        self._view.update_page()

    def fillDDPaesi(self):
        """
        Riempie il dropdown dei paesi con i nodi presenti nel grafo.
        """

        paesi = self._model.get_nodi_grafo()

        self._view._ddPaese.options.clear()

        for paese in paesi:
            self._view._ddPaese.options.append(
                ft.dropdown.Option(
                    key=paese,
                    text=paese,
                    data=paese
                )
            )

        self._view._ddPaese.value = None
        self._view.update_page()

    def handlePaesiRaggiungibili(self, e):
        """
        Punto 2.
        Stampa la componente connessa del paese selezionato.
        """

        self._view.txt_result.controls.clear()

        paese = self.get_selected_item(self._view._ddPaese)

        if paese is None:
            self._view.create_alert("Seleziona un paese di partenza.")
            return

        componente = self._model.get_componente_connessa(paese)

        if len(componente) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun paese raggiungibile trovato.")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Paese di partenza: {paese}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero paesi raggiungibili: {len(componente)}")
        )

        self._view.txt_result.controls.append(
            ft.Text("Componente connessa:")
        )

        for p in componente:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )

        self._view.update_page()
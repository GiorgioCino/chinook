import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDPaesi(self):
        countries = self._model.getAllCountries()

        self._view._ddPaese.options.clear()

        for paese in countries:
            self._view._ddPaese.options.append(
                ft.dropdown.Option(
                    str(paese)
                )
            )

        self._view._ddPaese.value = None
        self._view.update_page()
# PER RIEMPIRE DROPDOWN SECONDA FILA DOPO CREAZIONE GRAFO
    def fillDDGeneriGrafo(self):
            generi = self._model.get_nodi_grafo()

            self._view._ddGenereStart.options.clear()

            for genere in generi:
                self._view._ddGenereStart.options.append(
                    ft.dropdown.Option(
                        key=str(genere.GenreId),
                        text=str(genere),
                        data=genere
                    )
                )

            self._view._ddGenereStart.value = None
            self._view.update_page()

    def get_selected_item(self, dropdown):
        for option in dropdown.options:
            if str(option.key) == str(dropdown.value):
                return option.data

        return None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        paese = self._view._ddPaese.value

        if paese is None:
            self._view.create_alert("Seleziona un paese.")
            return

        n_nodi, n_archi = self._model.build_graph(paese)

        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {n_nodi}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {n_archi}")
        )
        #PER INSERIRE GENERI DI PARTENZA DOPO LA CREAZIONE DEL GRAFO
        self.fillDDGeneriGrafo()
        self._view.update_page()

    def handleDettagli(self,e):
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
                ft.Text(f"{c1} - {c2}: {peso} piloti condivisi")
            )
        nodo, influenza = self._model.get_nodo_piu_influente()

        self._view.txt_result.controls.append(
            ft.Text(f"Nodo più influente: {nodo} - influenza: {influenza}")
        )
        self._view.update_page()

    def handleCercaPercorso(self, e):
            self._view.txt_result.controls.clear()

            genere_start = self.get_selected_item(self._view._ddGenereStart)

            if genere_start is None:
                self._view.create_alert("Seleziona un genere di partenza.")
                return

            cammino, peso_totale = self._model.get_cammino_peso_massimo_crescente(genere_start)

            if len(cammino) == 0:
                self._view.txt_result.controls.append(
                    ft.Text("Nessun cammino trovato.")
                )
                self._view.update_page()
                return

            self._view.txt_result.controls.append(
                ft.Text(f"Genere di partenza: {genere_start}")
            )

            self._view.txt_result.controls.append(
                ft.Text(f"Peso massimo del cammino: {peso_totale}")
            )

            self._view.txt_result.controls.append(
                ft.Text(f"Numero di nodi nel cammino: {len(cammino)}")
            )

            self._view.txt_result.controls.append(
                ft.Text("Cammino trovato:")
            )

            for genere in cammino:
                self._view.txt_result.controls.append(
                    ft.Text(str(genere))
                )

            self._view.txt_result.controls.append(
                ft.Text("Archi attraversati:")
            )

            archi = self._model.get_archi_cammino(cammino)

            for nodo1, nodo2, peso in archi:
                self._view.txt_result.controls.append(
                    ft.Text(f"{nodo1} -> {nodo2} | peso = {peso}")
                )

            self._view.update_page()
import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    # ---------------------------------------------------------
    # HELPER GENERICO PER LEGGERE L'OGGETTO SELEZIONATO
    # ---------------------------------------------------------
    def get_selected_item(self, dropdown):
        """
        Serve per recuperare l'oggetto salvato nel campo data
        dell'opzione selezionata nel dropdown.
        """
        for option in dropdown.options:
            if str(option.key) == str(dropdown.value):
                return option.data

        return None

    # ---------------------------------------------------------
    # RIEMPIMENTO DROPDOWN COUNTRY
    # ---------------------------------------------------------
    def fillDDCountry(self):
        countries = self._model.getAllCountries()

        self._view._ddCountry.options.clear()

        for country in countries:
            self._view._ddCountry.options.append(
                ft.dropdown.Option(
                    key=str(country),
                    text=str(country),
                    data=country
                )
            )

        self._view._ddCountry.value = None
        self._view.update_page()

    # ---------------------------------------------------------
    # RIEMPIMENTO DROPDOWN ANNI
    # ---------------------------------------------------------
    def fillDDAnni(self):
        anni = self._model.getAllYears()

        self._view._ddAnno.options.clear()

        for anno in anni:
            self._view._ddAnno.options.append(
                ft.dropdown.Option(
                    key=str(anno),
                    text=str(anno),
                    data=anno
                )
            )

        self._view._ddAnno.value = None
        self._view.update_page()

    # ---------------------------------------------------------
    # BOTTONE CREA GRAFO
    # ---------------------------------------------------------
    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        paese = self.get_selected_item(self._view._ddCountry)
        anno = self.get_selected_item(self._view._ddAnno)

        if paese is None:
            self._view.create_alert("Seleziona un paese.")
            return

        if anno is None:
            self._view.create_alert("Seleziona un anno.")
            return

        num_nodi, num_archi = self._model.build_graph(paese, anno)

        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente.")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Paese selezionato: {paese}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Anno selezionato: {anno}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi: {num_nodi}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {num_archi}")
        )

        # Dopo aver creato il grafo, riempio i dropdown del punto 2
        self.fillDDMediaTypeGrafo()

        self._view.update_page()

    # ---------------------------------------------------------
    # RIEMPIMENTO DROPDOWN START/END CON I NODI DEL GRAFO
    # ---------------------------------------------------------
    def fillDDMediaTypeGrafo(self):
        nodi = self._model.get_nodi_grafo()

        self._view._ddStartMediaType.options.clear()
        self._view._ddEndMediaType.options.clear()

        for nodo in nodi:
            self._view._ddStartMediaType.options.append(
                ft.dropdown.Option(
                    key=str(nodo.MediaTypeId),
                    text=str(nodo),
                    data=nodo
                )
            )

            self._view._ddEndMediaType.options.append(
                ft.dropdown.Option(
                    key=str(nodo.MediaTypeId),
                    text=str(nodo),
                    data=nodo
                )
            )

        self._view._ddStartMediaType.value = None
        self._view._ddEndMediaType.value = None

        self._view.update_page()

    # ---------------------------------------------------------
    # BOTTONE STAMPA DETTAGLI
    # ---------------------------------------------------------
    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodes() == 0:
            self._view.create_alert("Crea prima il grafo.")
            return

        self._view.txt_result.controls.append(
            ft.Text("Grafo attuale:")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi: {self._model.getNumNodes()}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {self._model.getNumEdges()}")
        )

        self._view.txt_result.controls.append(
            ft.Text("5 MediaType più influenti:")
        )

        top_5 = self._model.get_top_5_influenti()

        if len(top_5) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun nodo trovato.")
            )
            self._view.update_page()
            return

        for nodo, influenza in top_5:
            self._view.txt_result.controls.append(
                ft.Text(f"{nodo} - influenza = {influenza}")
            )

        self._view.update_page()

    # ---------------------------------------------------------
    # BOTTONE CERCA PERCORSO
    # ---------------------------------------------------------
    def handleCercaPercorso(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodes() == 0:
            self._view.create_alert("Crea prima il grafo.")
            return

        start = self.get_selected_item(self._view._ddStartMediaType)
        end = self.get_selected_item(self._view._ddEndMediaType)

        if start is None:
            self._view.create_alert("Seleziona il MediaType di partenza.")
            return

        if end is None:
            self._view.create_alert("Seleziona il MediaType di arrivo.")
            return

        if start == end:
            self._view.create_alert("Il nodo di partenza e quello di arrivo devono essere diversi.")
            return

        lunghezza_str = self._view._txtLunghezza.value

        if lunghezza_str is None or lunghezza_str.strip() == "":
            self._view.create_alert("Inserisci la lunghezza del cammino.")
            return

        try:
            lunghezza = int(lunghezza_str)
        except ValueError:
            self._view.create_alert("La lunghezza deve essere un numero intero.")
            return

        if lunghezza <= 0:
            self._view.create_alert("La lunghezza deve essere maggiore di zero.")
            return

        cammino, peso_totale = self._model.get_cammino_ottimo(
            start,
            end,
            lunghezza
        )

        if len(cammino) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato con le caratteristiche richieste.")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Cammino ottimo da {start} a {end}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Lunghezza richiesta: {lunghezza} archi")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Peso totale: {peso_totale}")
        )

        self._view.txt_result.controls.append(
            ft.Text("Nodi del cammino:")
        )

        for nodo in cammino:
            self._view.txt_result.controls.append(
                ft.Text(str(nodo))
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
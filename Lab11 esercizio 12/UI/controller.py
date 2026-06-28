import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDPaesi(self):
        paesi = self._model.getAllPaesi()

        self._view._ddPaese.options.clear()

        for paese in paesi:
            self._view._ddPaese.options.append(
                ft.dropdown.Option(str(paese)
                )
            )

        self._view._ddPaese.value = None
        self._view.update_page()

    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self,e):
        pass

    def handleCercaPercorso(self, e):
        self._view.txt_result.controls.clear()

        media_start = self.get_selected_item(self._view._ddMediaTypeStart)

        if media_start is None:
            self._view.create_alert("Seleziona un MediaType di partenza.")
            return

        cammino = self._model.get_cammino_piu_lungo(media_start)

        if len(cammino) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato.")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"MediaType di partenza: {media_start}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Cammino semplice più lungo: {len(cammino)} nodi, {len(cammino) - 1} archi")
        )

        self._view.txt_result.controls.append(
            ft.Text("Nodi del cammino:")
        )

        for media in cammino:
            self._view.txt_result.controls.append(
                ft.Text(str(media))
            )

        self._view.update_page()

    def handleCercaPercorso2(self, e):
        self._view.txt_result.controls.clear()

        media_start = self.get_selected_item(self._view._ddMediaTypeStart)

        if media_start is None:
            self._view.create_alert("Seleziona un MediaType di partenza.")
            return

        componente = self._model.get_componente_connessa(media_start)

        self._view.txt_result.controls.append(
            ft.Text(f"MediaType di partenza: {media_start}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi nella componente: {len(componente)}")
        )

        self._view.txt_result.controls.append(
            ft.Text("Componente connessa:")
        )

        for media in componente:
            self._view.txt_result.controls.append(
                ft.Text(str(media))
            )

        self._view.update_page()

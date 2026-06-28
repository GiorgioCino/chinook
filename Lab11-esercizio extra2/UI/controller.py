import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDMediaType(self):
        mediatypes = self._model.getAllMediatypes()

        self._view._ddMediaType.options.clear()

        for media in mediatypes:
            self._view._ddMediaType.options.append(
                ft.dropdown.Option(
                    key=str(media.MediaTypeId),
                    text=str(media),
                    data=media
                )
            )

        self._view._ddMediaType.value = None
        self._view.update_page()

    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self,e):
        pass

    def handleCercaPercorso(self,e):
        pass
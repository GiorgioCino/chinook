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

    def handleCreaGrafo(self, e):
        pass



    def handleCercaCammino(self,e):
        pass
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDPlaylist(self):
        playlists = self._model.getAllPlaylists()

        self._view._ddPlaylist.options.clear()

        for playlist in playlists:
            self._view._ddPlaylist.options.append(
                ft.dropdown.Option(
                    key=str(playlist.PlaylistId),
                    text=str(playlist),
                    data=playlist
                )
            )

        self._view._ddPlaylist.value = None
        self._view.update_page()

    def get_selected_item(self, dropdown):
        for option in dropdown.options:
            if str(option.key) == str(dropdown.value):
                return option.data

        return None


    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self,e):
        pass

    def handleArtistiRaggiungibili(self,e):
        pass
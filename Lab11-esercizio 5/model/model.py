import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_genres = DAO.getAllGenres()
        self._all_playlist = DAO.getAllPlaylists()
        self._id_map_playlist = {}
        for playlist in self._all_playlist:
            self._id_map_playlist[playlist.PlaylistId] = playlist
        self._graph = nx.DiGraph()

    def buildGraph(self, genere):
        self._graph.clear()


        nodes = DAO.getAllNodes(genere, self._id_map_playlist)
        self._graph.add_nodes_from(nodes)

        popolarita = DAO.getAllPopolarita(genere)
        playlist_track = DAO.get_track_per_playlist(genere)

        track_per_playlist = {}

        for playlist_id, track_id in playlist_track:
            if playlist_id not in  track_per_playlist:
                track_per_playlist[playlist_id] = set()

            track_per_playlist[playlist_id].add(track_id)

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):

                playlist1 = nodes[i]
                playlist2 = nodes[j]

                id1 = playlist1.PlaylistId
                id2 = playlist2.PlaylistId

                track1 =  track_per_playlist.get(id1, set())
                track2 =  track_per_playlist.get(id2, set())

                track_comuni = track1.intersection(track2)

                if len(track_comuni) > 0:

                    pop1 = popolarita.get(id1, 0)
                    pop2 = popolarita.get(id2, 0)

                    peso = pop1 + pop2

                    if pop1 > pop2:
                        self._graph.add_edge(playlist1, playlist2, weight=peso)

                    elif pop2 > pop1:
                        self._graph.add_edge(playlist2, playlist1, weight=peso)

                    else:
                        self._graph.add_edge(playlist1, playlist2, weight=peso)
                        self._graph.add_edge(playlist2, playlist1, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()


    def get_edges_info(self):
        result = []

        for c1, c2 in self._graph.edges:
            peso = self._graph[c1][c2]["weight"]
            result.append((c1, c2, peso))

        result.sort(key=lambda x: x[2], reverse=True)  #ordino dal peso piu alto al piu basso

        return result[:5]      #prendo i 3 archi di peso maggiore

    def get_nodo_piu_influente(self):
        best_nodo = None
        best_influenza = None


        for nodo in self._graph.nodes:

            peso_uscenti = 0
            peso_entranti = 0

            # Archi uscenti: nodo -> vicino
            for vicino in self._graph.successors(nodo):
                peso_uscenti += self._graph[nodo][vicino]["weight"]

            # Archi entranti: vicino -> nodo
            for vicino in self._graph.predecessors(nodo):
                peso_entranti += self._graph[vicino][nodo]["weight"]

            influenza = peso_uscenti - peso_entranti

            if best_influenza is None or influenza > best_influenza:
                best_nodo = nodo
                best_influenza = influenza
        return best_nodo, best_influenza



    def getAllGenres(self):
        return list(self._all_genres)

    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def get_nodi_grafo(self):
        result = list(self._graph.nodes)
        result.sort(key=lambda x: str(x))
        return result
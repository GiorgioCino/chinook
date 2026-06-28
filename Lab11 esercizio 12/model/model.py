import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_paesi = DAO.get_all_countries()
        self._all_mediaType = DAO.get_all_MediaType()
        self._id_map_mediaType = {}
        for mediaType in self._all_mediaType:
            self._id_map_mediaType[mediaType.MediaTypeId] = mediaType
        self._graph = nx.Graph()

    def build_graph(self, paese):
        self._graph.clear()
        nodes = DAO.get_all_Nodes(paese, self._id_map_mediaType)
        self._graph.add_nodes_from(nodes)

        # Archi = tuple (MediaTypeId1, MediaTypeId2, peso)
        archi = DAO.get_all_edges(paese)
        #nell'altro caso dei cpuntry non facevo questo sotto perch  non erano oggetti
        for id1, id2, peso in archi:
            media1 = self._id_map_mediaType[id1]
            media2 = self._id_map_mediaType[id2]

            if self._graph.has_node(media1) and self._graph.has_node(media2):
                self._graph.add_edge(media1, media2, weight=peso)
    def getNumNodes(self):
        return self._graph.number_of_nodes()


    def getNumEdges(self):
        return self._graph.number_of_edges()

    def getAllPaesi(self):
        return list(self._all_paesi)

    def get_cammino_piu_lungo(self, media_start):
        if not self._graph.has_node(media_start):
            return []

        self._best_path = []

        parziale = [media_start]

        self._ricorsione_cammino(parziale)

        return self._best_path

    def _ricorsione_cammino(self, parziale):
        ultimo = parziale[-1]

        if len(parziale) > len(self._best_path):
            self._best_path = list(parziale)

        for vicino in self._graph.neighbors(ultimo):
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione_cammino(parziale)
                parziale.pop()



        # CASO A A PARTITE DA NODO CLCOLO COMPONENTE CONNESSA PUNRTO 2
        #
    def get_componente_connessa(self, media_start):
            if not self._graph.has_node(media_start):
                return []

            visitati = set()

            self._ricorsione_visita(media_start, visitati)

            result = list(visitati)
            result.sort(key=lambda x: x.Name)

            return result

    def _ricorsione_visita(self, nodo_corrente, visitati):
            visitati.add(nodo_corrente)

            for vicino in self._graph.neighbors(nodo_corrente):
                if vicino not in visitati:
                    self._ricorsione_visita(vicino, visitati)
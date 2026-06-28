import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._paesi = DAO.getAllCountries()
        self._generi = DAO.getAllGenres()
        self._id_map_genere = {}
        for genere in self._generi:
            self._id_map_genere[genere.GenreId] = genere






        self._graph = nx.Graph()

    def build_graph(self, paese):
        self._graph.clear()
        nodes = DAO.getAllNodes(paese, self._id_map_genere)
        self._graph.add_nodes_from(nodes)

        # Archi = tuple (MediaTypeId1, MediaTypeId2, peso)
        archi = DAO.get_all_edges(paese)
        # nell'altro caso dei cpuntry non facevo questo sotto perch  non erano oggetti
        for id1, id2, peso in archi:
            genere1 = self._id_map_genere[id1]
            genere2 = self._id_map_genere[id2]

            if self._graph.has_node(genere1) and self._graph.has_node(genere2):
                self._graph.add_edge(genere1, genere2, weight=peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getAllCountries(self):
        return list(self._paesi)
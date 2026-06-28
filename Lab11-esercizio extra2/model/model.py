import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_mediatypes = DAO.get_all_MediaType()
        self._all_composer = DAO.get_all_composer()
        #self._id_map_composer = {}
        #for composer in self._all_composer:
        #    self._id_map_composer[composer.Composer] = composer
        self._graph = nx.Graph()

    def buildGraph(self, mils, media):
        self._graph.clear()
        nodes = DAO.get_all_nodes(mils,media)
        self._graph.add_nodes_from(nodes)

    def getNumNodes(self):
            return len(self._graph.nodes)

    def getNumEdges(self):
            return len(self._graph.edges)


    def getAllMediatypes(self):
        return list(self._all_mediatypes)
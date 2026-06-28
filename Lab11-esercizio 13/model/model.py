import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_playlists = DAO.getAllPlaylists()
        self._artists = DAO.getAllArtists()
        self._id_map_artist = {}
        for artist in self._artists:
            self._id_map_artist[artist.ArtistId] = artist
        self._graph = nx.Graph()


    def build_graph(self, playlist):
        self._graph.clear()
        nodes = DAO.getAllNodes(playlist, self._id_map_artist)
        self._graph.add_nodes_from(nodes)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)


    def getAllPlaylists(self):
        return list(self._all_playlists)

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_artists = DAO.get_all_artists()
        self._id_map_artists = {a.ArtistId: a for a in self._all_artists}
        self._graph = nx.DiGraph()

    def build_graph(self, genere):
        self._graph.clear()

        nodes = DAO.get_all_nodes(genere, self._id_map_artists)

        self._graph.add_nodes_from(nodes)

        popolarita = DAO.get_popolarita_artisti(genere)

        artisti_per_cliente = DAO.get_artisti_per_cliente(genere)

        clienti_artisti = {}

        for cliente_id, artista_id in artisti_per_cliente:
            if cliente_id not in clienti_artisti:
                clienti_artisti[cliente_id] = []

            if artista_id not in clienti_artisti[cliente_id]:
                clienti_artisti[cliente_id].append(artista_id)

        coppie = set()

        for cliente_id in clienti_artisti:
            lista_artisti = clienti_artisti[cliente_id]

            for i in range(len(lista_artisti)):
                for j in range(i + 1, len(lista_artisti)):
                    id1 = lista_artisti[i]
                    id2 = lista_artisti[j]

                    if id1 < id2:
                        coppie.add((id1, id2))
                    else:
                        coppie.add((id2, id1))

        for id1, id2 in coppie:
            artista1 = self._id_map_artists[id1]
            artista2 = self._id_map_artists[id2]

            if self._graph.has_node(artista1) and self._graph.has_node(artista2):

                pop1 = popolarita[id1]
                pop2 = popolarita[id2]
                peso = pop1 + pop2

                if pop1 > pop2:
                    self._graph.add_edge(artista1, artista2, weight=peso)

                elif pop2 > pop1:
                    self._graph.add_edge(artista2, artista1, weight=peso)

                else:
                    self._graph.add_edge(artista1, artista2, weight=peso)
                    self._graph.add_edge(artista2, artista1, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()


    def get_artists_in_graph(self):
        return sorted(list(self._graph.nodes()), key=lambda a: a.ArtistId)

    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()
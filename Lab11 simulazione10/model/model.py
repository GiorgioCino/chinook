import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_generi = DAO.get_all_genres()
        self._all_countries = DAO.get_all_countries()
        self._graph = nx.Graph()

    def build_graph(self, genere):
        self._graph.clear()

        nodes = DAO.get_all_nodes(genere)
        self._graph.add_nodes_from(nodes)

        archi = DAO.get_all_edges(genere)
        for paese1, paese2, peso in archi:
            self._graph.add_edge(paese1, paese2, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def get_edges_info(self):
        result = []

        for c1, c2 in self._graph.edges:
            peso = self._graph[c1][c2]["weight"]
            result.append((c1, c2, peso))

        result.sort(key=lambda x: x[2], reverse=True)  #ordino dal peso piu alto al piu basso

        return result[:3]      #prendo i 3 archi di peso maggiore

    def getInfoCompConnessa(self):

        #se volessi solo stampare il numero di componenti connesse
        return nx.number_connected_components(self._graph)  #per contare direttamente il numero di componenti connesse
        #se voglio sapere quanti nodi ci sono in ogni componente:
        componenti = list(nx.connected_components(self._graph))

        if len(componenti) == 0:
            return []

        componente_max = max(componenti, key=len)

        result = []

        for nodo in componente_max:
            grado = self._graph.degree[nodo]
            result.append((nodo, grado))

        result.sort(key=lambda x: x[1], reverse=True)

        return result

    def getComponenteMaggiore(self):
        componenti = list(nx.connected_components(self._graph))

        if len(componenti) == 0:
            return []

        componente_max = max(componenti, key=len)

        result = []

        for nodo in componente_max:
            grado = self._graph.degree[nodo]
            result.append(nodo)



        return result

    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def getAllGenres(self):
        return list(self._all_generi)

    def get_nodi_grafo(self):
        """
        Restituisce tutti i nodi presenti nel grafo.
        In questo esercizio i nodi sono i paesi.
        Serve per riempire il dropdown dei paesi.
        """
        result = list(self._graph.nodes)
        result.sort()
        return result

    def get_componente_connessa(self, paese_start):
        """
        Trova tutti i paesi raggiungibili dal paese selezionato.
        Poiché il grafo è non orientato, uso neighbors().
        """

        if not self._graph.has_node(paese_start):
            return []

        visitati = set()

        self._ricorsione_visita(paese_start, visitati)

        result = list(visitati)
        result.sort()

        return result

    def _ricorsione_visita(self, paese_corrente, visitati):
        """
        Visita ricorsiva in profondità.
        """

        visitati.add(paese_corrente)

#fosse stato orientato avrei usato
  #      for vicino in self._graph.successors(paese_corrente):
        for vicino in self._graph.neighbors(paese_corrente):
            if vicino not in visitati:
                self._ricorsione_visita(vicino, visitati)
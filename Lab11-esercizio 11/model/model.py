import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._paesi = DAO.getAllCountries()
        self._dipendenti = DAO.getAllDipendenti()
        self._id_map_dipendente = {}
        for dipendente in self._dipendenti:
            self._id_map_dipendente[dipendente.EmployeeId] = dipendente

        self._graph = nx.DiGraph()

    def build_graph(self, paese):
        self._graph.clear()
        self._graph = nx.DiGraph()

        nodes = DAO.getAllNodes(paese, self._id_map_dipendente)
        self._graph.add_nodes_from(nodes)

        fatturato = DAO.get_fatturato_dipendenti(paese)
        generi_per_dipendente = DAO.get_generi_per_dipendente(paese)

        dipendenti_generi = {}

        for dipendente_id, genere_id in generi_per_dipendente:
            if dipendente_id not in dipendenti_generi:
                dipendenti_generi[dipendente_id] = set()

            dipendenti_generi[dipendente_id].add(genere_id)

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):

                dipendente1 = nodes[i]
                dipendente2 = nodes[j]

                id1 = dipendente1.EmployeeId
                id2 = dipendente2.EmployeeId

                #prendo i generi del dipendente 1
#               prendo i generi del dipendente 2
#                guardo quali generi hanno in comune
                generi1 = dipendenti_generi.get(id1, set())
                generi2 = dipendenti_generi.get(id2, set())

                generi_comuni = generi1.intersection(generi2)

                if len(generi_comuni) > 0:
                    fatturato1 = fatturato.get(id1, 0)
                    fatturato2 = fatturato.get(id2, 0)

                    peso = fatturato1 + fatturato2

                    if fatturato1 > fatturato2:
                        self._graph.add_edge(dipendente1, dipendente2, weight=peso)

                    elif fatturato2 > fatturato1:
                        self._graph.add_edge(dipendente2, dipendente1, weight=peso)

                    else:
                        self._graph.add_edge(dipendente1, dipendente2, weight=peso)
                        self._graph.add_edge(dipendente2, dipendente1, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()
    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getAllCountries(self):
        return list(self._paesi)
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._paesi = DAO.getAllCountries()
        self._generi = DAO.getAllGenres()
        self._id_map_genere = {}
        for genere in self._generi:
            self._id_map_genere[genere.GenreId] = genere

        self._graph = nx.DiGraph()

    def build_graph(self, paese):
        self._graph.clear()
        self._graph = nx.DiGraph()

        # 1. Nodi = generi acquistati nel paese
        nodes = DAO.getAllNodes(paese, self._id_map_genere)
        self._graph.add_nodes_from(nodes)

        # 2. Fatturato per genere
        fatturato = DAO.get_fatturato_genere(paese)

        # 3. Coppie genere-cliente
        clienti_per_genere = DAO.get_clienti_per_genere(paese)

        # 4. Creo dizionario:
        # GenreId -> insieme dei CustomerId che hanno acquistato quel genere
        generi_clienti = {}

        for genere_id, cliente_id in clienti_per_genere:
            if genere_id not in generi_clienti:
                generi_clienti[genere_id] = set()

            generi_clienti[genere_id].add(cliente_id)

        # 5. Confronto coppie di generi
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):

                genere1 = nodes[i]
                genere2 = nodes[j]

                id1 = genere1.GenreId
                id2 = genere2.GenreId

                clienti1 = generi_clienti.get(id1, set())
                clienti2 = generi_clienti.get(id2, set())

                clienti_comuni = clienti1.intersection(clienti2)

                if len(clienti_comuni) > 0:

                    fatturato1 = fatturato.get(id1, 0)
                    fatturato2 = fatturato.get(id2, 0)

                    peso = fatturato1 + fatturato2

                    if fatturato1 > fatturato2:
                        self._graph.add_edge(genere1, genere2, weight=peso)

                    elif fatturato2 > fatturato1:
                        self._graph.add_edge(genere2, genere1, weight=peso)

                    else:
                        self._graph.add_edge(genere1, genere2, weight=peso)
                        self._graph.add_edge(genere2, genere1, weight=peso)

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
                best_influenza = influenza
                best_nodo = nodo

        return best_nodo, best_influenza

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getAllCountries(self):
        return list(self._paesi)

    def get_cammino_peso_massimo_crescente(self, genere_start):
        if not self._graph.has_node(genere_start):
            return [], 0

        self._best_path = []
        self._best_peso = 0

        parziale = [genere_start]

        self._ricorsione_peso_massimo_crescente(
            parziale,
            None,
            0
        )

        return self._best_path, self._best_peso

    def _ricorsione_peso_massimo_crescente(self, parziale, ultimo_peso, peso_parziale):
        ultimo = parziale[-1]

        # Aggiorno la soluzione migliore se il peso totale è maggiore
        if peso_parziale > self._best_peso:
            self._best_peso = peso_parziale
            self._best_path = list(parziale)

        # Essendo un grafo orientato, uso successors()
        for vicino in self._graph.successors(ultimo):

            # Cammino semplice: non posso ripetere nodi
            if vicino not in parziale:

                peso_arco = self._graph[ultimo][vicino]["weight"]

                # Primo arco: sempre accettato
                # Archi successivi: peso strettamente crescente
                if ultimo_peso is None or peso_arco > ultimo_peso:
                    parziale.append(vicino)

                    self._ricorsione_peso_massimo_crescente(
                        parziale,
                        peso_arco,
                        peso_parziale + peso_arco
                    )

                    parziale.pop()

    def get_archi_cammino(self, cammino):
        result = []

        for i in range(len(cammino) - 1):
            nodo1 = cammino[i]
            nodo2 = cammino[i + 1]

            peso = self._graph[nodo1][nodo2]["weight"]

            result.append((nodo1, nodo2, peso))

        return result
    #PER RIEMPIRE DROP DOWN SECONDA FILA
    def get_nodi_grafo(self):
        result = list(self._graph.nodes)
        result.sort(key=lambda x: str(x))
        return result
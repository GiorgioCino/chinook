import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._all_paesi = DAO.getAllCountries()
        self._all_years = DAO.getAllYears()
        self._all_mediatypes = DAO.getAllMediaTypes()
        self._id_map_mediatype = {}
        for mediatype in self._all_mediatypes:
            self._id_map_mediatype[mediatype.MediaTypeId] = mediatype
        self._graph = nx.Graph()

    def build_graph(self, paese, anno):
        self._graph.clear()
        self._graph = nx.DiGraph()

        # 1. Prendo tutti i MediaType come nodi
        nodes = DAO.getAllNodes(self._id_map_mediatype)

        # 2. Aggiungo i nodi al grafo
        self._graph.add_nodes_from(nodes)

        # 3. Prendo le vendite per ogni MediaType
        # Dizionario: MediaTypeId -> numero vendite
        vendite = DAO.get_quantita_vendute(paese, anno)

        # 4. Prendo la relazione:
        # lista di tuple (MediaTypeId, CustomerId, mese)
        dati_relazione = DAO.get_clienti_per_media(paese, anno)

        # 5. Costruisco il dizionario:
        # MediaTypeId -> set di coppie (CustomerId, mese)
        clienti_mese_per_media = {}

        for media_id, cliente_id, mese in dati_relazione:
            if media_id not in clienti_mese_per_media:
                clienti_mese_per_media[media_id] = set()

            clienti_mese_per_media[media_id].add((cliente_id, mese))

        # 6. Confronto tutte le coppie di MediaType
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):

                media1 = nodes[i]
                media2 = nodes[j]

                id1 = media1.MediaTypeId
                id2 = media2.MediaTypeId

                insieme1 = clienti_mese_per_media.get(id1, set())
                insieme2 = clienti_mese_per_media.get(id2, set())

                comuni = insieme1.intersection(insieme2)

                # 7. Se hanno almeno una coppia (cliente, mese) in comune, creo arco
                if len(comuni) > 0:

                    vendite1 = vendite.get(id1, 0)
                    vendite2 = vendite.get(id2, 0)

                    peso = vendite1 + vendite2

                    if vendite1 > vendite2:
                        self._graph.add_edge(media1, media2, weight=peso)

                    elif vendite2 > vendite1:
                        self._graph.add_edge(media2, media1, weight=peso)

                    else:
                        self._graph.add_edge(media1, media2, weight=peso)
                        self._graph.add_edge(media2, media1, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllCountries(self):
        return list(self._all_paesi)

    def getAllYears(self):
        return list(self._all_years)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def get_nodi_grafo(self):
        result = list(self._graph.nodes)
        result.sort(key=lambda x: str(x))
        return result

    def get_top_5_influenti(self):
        result = []

        for nodo in self._graph.nodes:

            peso_uscenti = 0
            peso_entranti = 0

            for vicino in self._graph.successors(nodo):
                peso_uscenti += self._graph[nodo][vicino]["weight"]

            for vicino in self._graph.predecessors(nodo):
                peso_entranti += self._graph[vicino][nodo]["weight"]

            influenza = peso_uscenti - peso_entranti

            result.append((nodo, influenza))

        result.sort(key=lambda x: x[1], reverse=True)

        return result[:5]

    def get_cammino_ottimo(self, start, end, lunghezza):
        """
        Cerca il cammino di peso massimo da start a end
        con esattamente 'lunghezza' archi.

        start = nodo MediaType di partenza
        end = nodo MediaType di arrivo
        lunghezza = numero di archi da attraversare
        """

        # Controllo che i nodi esistano nel grafo
        if not self._graph.has_node(start):
            return [], 0

        if not self._graph.has_node(end):
            return [], 0

        # Variabili globali del Model per salvare la soluzione migliore
        self._best_path = []
        self._best_peso = 0

        # Cammino parziale iniziale: contiene solo il nodo di partenza
        parziale = [start]

        # Lancio la ricorsione
        self._ricorsione_cammino(
            parziale,
            end,
            lunghezza,
            0
        )

        return self._best_path, self._best_peso

    def _ricorsione_cammino(self, parziale, end, lunghezza, peso_parziale):
        """
        parziale = lista dei nodi già inseriti nel cammino
        end = nodo finale desiderato
        lunghezza = numero di archi richiesto
        peso_parziale = peso accumulato fino a questo momento
        """

        # Ultimo nodo raggiunto nel cammino attuale
        ultimo = parziale[-1]

        # Numero di archi già usati
        archi_usati = len(parziale) - 1

        # CASO TERMINALE
        # Se ho usato esattamente il numero di archi richiesto,
        # controllo se sono arrivato al nodo finale.
        if archi_usati == lunghezza:

            if ultimo == end:
                if peso_parziale > self._best_peso:
                    self._best_peso = peso_parziale
                    self._best_path = list(parziale)

            return

        # CASO RICORSIVO
        # Essendo un grafo orientato, posso andare solo verso i successori.
        for vicino in self._graph.successors(ultimo):

            # Evito di ripetere nodi nel cammino
            if vicino not in parziale:
                peso_arco = self._graph[ultimo][vicino]["weight"]

                parziale.append(vicino)

                self._ricorsione_cammino(
                    parziale,
                    end,
                    lunghezza,
                    peso_parziale + peso_arco
                )

                parziale.pop()
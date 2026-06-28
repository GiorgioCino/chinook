from model.model import Model

mdl = Model()
mdl.buildGraph(5, 4)
print(f"Grafo creato contiene {mdl.getNumNodes()} nodes e {mdl.getNumEdges()} archi")

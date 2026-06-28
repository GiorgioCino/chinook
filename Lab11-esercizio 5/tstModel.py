from model.model import Model

mdl = Model()
mdl.buildGraph(1)
print(f"Grafo creato contiene {mdl.getNumNodes()} e {mdl.getNumEdges()}")

#mdl.getInfoCompConnessa(1224)
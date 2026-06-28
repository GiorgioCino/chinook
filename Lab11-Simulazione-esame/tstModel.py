from model.model import Model

mdl = Model()
mdl.build_graph(1)
print(f"Grafo creato contiene {mdl.getNumNodes()} e {mdl.getNumEdges()}")

#mdl.getInfoCompConnessa(1224)
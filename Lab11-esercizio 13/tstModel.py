from model.model import Model

mdl = Model()
mdl.build_graph('Brazilian Music')
print(f"Grafo creato contiene {mdl.getNumNodes()} e {mdl.getNumEdges()}")

#mdl.getInfoCompConnessa(1224)
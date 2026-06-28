from model.model import Model

mdl = Model()
mdl.build_graph('France', 2024)
print(f"Grafo creato contiene {mdl.getNumNodes()} e {mdl.getNumEdges()}")

#mdl.getInfoCompConnessa(1224)
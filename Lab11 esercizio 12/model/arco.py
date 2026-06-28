class Arco:
    def __init__(self, map1, map2, peso):
        self.map1 = map1
        self.map2 = map2
        self.peso = peso

    def __str__(self):
        return f"{self.map1} - {self.map2} - {self.peso}"
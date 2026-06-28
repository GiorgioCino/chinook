class Arco:
    def __init__(self, country1, country2, peso):
        self.country1 = country1
        self.country2 = country2
        self.peso = peso

    def __str__(self):
        return f"{self.country1} - {self.country2} - {self.peso}"
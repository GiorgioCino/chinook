from dataclasses import dataclass

@dataclass
class Genere:
    GenreId: int
    Name: str




    def __str__(self):
        return f"{self.Name}"

    def __hash__(self):
        return hash(self.GenreId)
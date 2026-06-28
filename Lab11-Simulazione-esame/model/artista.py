from dataclasses import dataclass

@dataclass
class Artista:
    ArtistId: int
    Name: str

    def __str__(self):
        return f"{self.ArtistId}"

    def __hash__(self):
        return hash(self.ArtistId)
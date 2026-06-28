from dataclasses import dataclass

@dataclass
class Country:
    ArtistId: int
    Name: str




    def __str__(self):
        return f"{self.Name}"

    def __hash__(self):
        return hash(self.ArtistId)
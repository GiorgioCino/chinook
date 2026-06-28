from dataclasses import dataclass

@dataclass
class Composer:
    Composer: str


    def __str__(self):
        return f"{self.Composer}"

    def __hash__(self):
        return hash(self.Composer)
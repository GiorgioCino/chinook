from dataclasses import dataclass

@dataclass
class MediaType:
    MediaTypeId: int
    Name: str




    def __str__(self):
        return f"{self.Name}"

    def __hash__(self):
        return hash(self.MediaTypeId)
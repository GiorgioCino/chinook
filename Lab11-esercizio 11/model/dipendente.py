from dataclasses import dataclass

@dataclass
class Dipendente:
    EmployeeId: int
    LastName: str




    def __str__(self):
        return f"{self.LastName}"

    def __hash__(self):
        return hash(self.EmployeeId)
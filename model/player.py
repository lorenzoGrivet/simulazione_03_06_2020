from dataclasses import  dataclass

@dataclass
class Player:
    PlayerID: int
    Name: str
    # AvgGoal: float


    def __hash__(self):
        return hash(self.PlayerID)

    def __str__(self):
        return f"{self.Name}"
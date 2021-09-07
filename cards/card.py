from dataclasses import dataclass

@dataclass
class Card:
    number: int
    color: str

    def __lt__(self, other_card):
        return self.number < other_card.number

    def __gt__(self, other_card):
        return self.number > other_card.number
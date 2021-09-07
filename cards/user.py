from dataclasses import dataclass
from cards.card_pile import CardPile


@dataclass
class User:
    name: str
    hand: CardPile
    hold: CardPile
    pile1: CardPile
    pile2: CardPile
    pile3: CardPile
    computer: int

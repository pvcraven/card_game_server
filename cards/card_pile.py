from dataclasses import dataclass
from cards.card import Card
from typing import List

@dataclass
class CardPile:
    card_list: List[Card]

    def __init__(self):
        self.card_list = []

    def append(self, item: Card):
        self.card_list.append(item)

    def remove(self, item: Card):
        self.card_list.remove(item)

    def get_card_by_id(self, id):
        for card in self.card_list:
            if card.number == id:
                return card
        return None

    def sort(self):
        self.card_list.sort()

    def __len__(self):
        return len(self.card_list)

    def pop(self, index=-1):
        return self.card_list.pop(index)

    def __getitem__(self, index):
        return self.card_list[index]

    def insert(self, index, item):
        self.card_list.insert(index, item)
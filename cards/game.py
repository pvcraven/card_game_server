import json
import random

from dataclasses import dataclass
from typing import List

from cards.constants import MODE_PICK_FROM_HAND
from cards.constants import MODE_PICK_FROM_HOLD
from cards.constants import CARDS_TO_DEAL
from cards.constants import CARDS_IN_DECK
from cards.encoder import EnhancedJSONEncoder
from cards.card import Card
from cards.card_pile import CardPile


@dataclass
class Game:

    user_list: dict
    game_code: str
    mode: str
    cards: CardPile
    discard: List
    round: int

    def to_json(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)

    def shuffle(self):
        """
        Create deck, piles, and then shuffle
        """

        # Create deck
        self.cards = []
        for i in range(1, CARDS_IN_DECK + 1):
            color = "Blue"
            if i % 2 == 0:
                color = "Green"
            if i % 3 == 0:
                color = "Gray"
            card = Card(number=i, color=color)
            self.cards.append(card)

        # Shuffle
        random.shuffle(self.cards)

        # Create piles
        for user_name in self.user_list:
            user = self.user_list[user_name]
            user.hand = CardPile()
            user.hold = CardPile()
            user.discard = CardPile()
            user.pile1 = CardPile()
            user.pile2 = CardPile()
            user.pile3 = CardPile()

    def deal(self):
        """
        Deal cards from deck to each player
        """
        for user_name in self.user_list:
            user = self.user_list[user_name]
            for i in range(CARDS_TO_DEAL):
                user.hand.append(self.cards.pop())
            user.hand.sort()

    def change_hands(self):
        """
        Change hands. Pass to the right.
        """
        list_1 = [user_name for user_name in self.user_list]

        h1 = self.user_list[list_1[0]].hand
        for i in range(1, len(list_1)):
            h2 = self.user_list[list_1[i]].hand
            self.user_list[list_1[i]].hand = h1
            h1 = h2

        self.user_list[list_1[0]].hand = h1

    def computer_move(self):
        for user_name in self.user_list:
            user = self.user_list[user_name]
            if user.computer:
                if self.mode == MODE_PICK_FROM_HAND:
                    while len(user.hold) < 2:
                        user.hold.append(user.hand.pop())
                elif self.mode == MODE_PICK_FROM_HOLD:
                    while len(user.hold) > 0:
                        card = user.hold[0]
                        user.hold.remove(card)

                        if len(user.pile1) == 0 or card < user.pile1[0]:
                            user.pile1.insert(0, card)
                        elif card > user.pile1[-1]:
                            user.pile1.append(card)

                        elif len(user.pile2) == 0 or card < user.pile2[0]:
                            user.pile2.insert(0, card)
                        elif card > user.pile2[-1]:
                            user.pile2.append(card)

                        elif len(user.pile3) == 0 or card < user.pile3[0]:
                            user.pile3.insert(0, card)
                        elif card > user.pile3[-1]:
                            user.pile3.append(card)

                        else:
                            self.discard.append(card)

    def move_to_pile(self, user_name, card_id, pile):
        """
        Move from the users hand to the two-card pick pile
        """
        try:
            user = self.user_list[user_name]
            hold = user.hold

            if self.mode != MODE_PICK_FROM_HOLD or len(hold) == 0:
                data = {'error': 'Invalid move'}
                print(f"Invalid move {self.mode} -- {len(hold)}")
                return data

            hold = user.hold.card_list
            successful_move = True
            card = user.hold.get_card_by_id(card_id)

            if card not in hold:
                data = {'error': 'No such card'}
                print(f"No such card {card} -- {hold} ")
                return data

            print("BBB")

            if pile == 0:
                self.discard.append(card)
                successful_move = True
            elif pile == 1:
                pile = user.pile1
                if len(pile) == 0 or card < pile[0]:
                    pile.insert(0, card)
                    successful_move = True
                elif card > pile[-1]:
                    pile.append(card)
                    successful_move = True
                else:
                    data = {'error': 'Invalid move'}
            elif pile == 2:
                pile = user.pile2
                if len(pile) == 0 or card < pile[0]:
                    pile.insert(0, card)
                    successful_move = True
                elif card > pile[-1]:
                    pile.append(card)
                    successful_move = True
                else:
                    data = {'error': 'Invalid move'}
            elif pile == 3:
                pile = user.pile3
                if len(pile) == 0 or card < pile[0]:
                    pile.insert(0, card)
                    successful_move = True
                elif card > pile[-1]:
                    pile.append(card)
                    successful_move = True
                else:
                    data = {'error': 'Invalid move'}
            else:
                data = {'error': 'Invalid move'}

            print("CCC")

            if successful_move:
                hold.remove(card)

                # Has everyone played all the cards in their hold?
                change_mode = True
                for user_name in self.user_list:
                    user = self.user_list[user_name]
                    if len(user.hold) != 0:
                        change_mode = False

                # If so, change modes
                if change_mode and self.mode == MODE_PICK_FROM_HOLD:
                    self.mode = MODE_PICK_FROM_HAND

                    if len(user.hand) == 0:
                        self.deal()
                        self.round += 1
                    else:
                        self.change_hands()

                self.computer_move()

                data = json.dumps(self, cls=EnhancedJSONEncoder)

        except Exception as e:
            data = {'error': 'Exception'}
            print(f"Exception {e}")

        return data

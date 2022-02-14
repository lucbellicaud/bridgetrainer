from __future__ import annotations
from typing import Dict, List
from .PlayerHand import PlayerHand
from common_utils import Direction, Suit,Card,TOTAL_DECK
# from ddstable import ddstable


class Diag:
    def __init__(self, hands: Dict[Direction, PlayerHand]):
        self.hands = hands
        self.auto_complete()
        self.player_cards = {
            direction: self.hands[direction].cards for direction in self.hands}

    def __str__(self) -> str:
        string = ""
        for direction in Direction:
            string += direction.name + " : " + \
                self.hands[direction].__str__() + "\n"
        return string

    @staticmethod
    def init_from_pbn(string: str) -> Diag:
        """ Create a diag from this syntax : 'N:752.Q864.84.AT62 A98.AT9.Q753.J98 KT.KJ73.JT.K7543 QJ643.52.AK962.Q'"""
        dealer = Direction.from_str(string[0])
        string = string[2:]
        hand_list = string.split(" ")
        hands = {}
        hands[Direction.NORTH] = PlayerHand.from_pbn(hand_list[0])
        hands[Direction.EAST] = PlayerHand.from_pbn(hand_list[1])
        hands[Direction.SOUTH] = PlayerHand.from_pbn(hand_list[2])
        hands[Direction.WEST] = PlayerHand.from_pbn(hand_list[3])

        rotate = 0
        if dealer == Direction.NORTH:
            pass
        if dealer == Direction.EAST:
            rotate = 1
        if dealer == Direction.WEST:
            rotate = 2
        if dealer == Direction.SOUTH:
            rotate = 3

        return Diag(hands).rotate(rotate)

    @staticmethod
    def init_from_lin(string: str) -> Diag:
        """Create a deal from this syntax : 3SK7HAQT632DK4CQ62,S82H98DAT632CKT43,S965HKJ5DQJ985CA5"""
        string=string[1:] #Delete the dealer carac
        hand_list = string.split(",")
        hands = {}
        hands[Direction.SOUTH] = PlayerHand.from_lin(hand_list[0])
        hands[Direction.WEST] = PlayerHand.from_lin(hand_list[1])
        hands[Direction.NORTH] = PlayerHand.from_lin(hand_list[2])

        return Diag(hands)

    def missing_cards(self) -> List[Card]:
        list_of_cards = []
        for player_hand in self.hands.values():
            for card in player_hand.cards:
                if card in list_of_cards :
                    print("Cette carte est en double",card)
                assert card not in list_of_cards
                list_of_cards.append(card)
        missing_cards = [
            card for card in TOTAL_DECK if card not in list_of_cards]
        return missing_cards

    def auto_complete(self) -> Dict[Direction, PlayerHand]:
        missing_cards = self.missing_cards()
        for dir in Direction:
            if dir not in self.hands:
                self.hands[dir] = PlayerHand({suit: [] for suit in Suit})
            while self.hands[dir].len() < 13:

                self.hands[dir].append(missing_cards.pop())
        return self.hands

    def rotate(self, rotato: int) -> Diag:
        temp = []
        hands = {}
        for dir in Direction:
            temp.append(self.hands[dir])
        for i in range(rotato):
            temp.insert(0, temp.pop())

        hands[Direction.NORTH] = temp[0]
        hands[Direction.EAST] = temp[1]
        hands[Direction.SOUTH] = temp[2]
        hands[Direction.WEST] = temp[3]

        return Diag(hands)

    def is_valid(self) -> bool:
        list_of_cards = []
        for player_hand in self.hands.values():
            for card in player_hand.cards:
                if card in list_of_cards:
                    print('Cette carte est en double !', card)
                    return False
                else:
                    list_of_cards.append(card)
        if len(list_of_cards) == 52:
            return True
        else:
            print('Le diagramme contient ', len(list_of_cards), ' cartes')
            return False

    # def calculate_DD_table(self) :
    #     string = ""
    #     for dir in Direction:
    #         string += self.hands[dir].print_as_lin()
    #         string += " "
    #     print(ddstable.get_ddstable(string))

    def print_as_lin(self) -> str:
        string = ""
        for dir in Direction:
            string += self.hands[dir].print_as_lin()
            string += ","
        return string

    def print_as_pbn(self) -> str:
        string = '[Deal "N:'
        for dir in Direction:
            string += self.hands[dir].print_as_lin()
            string += " "
        return string[:-1]+'"]'

if __name__ == '__main__':
    pass
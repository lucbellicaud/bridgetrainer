from __future__ import annotations
from typing import Dict, Iterable, List

from common_utils import Suit, Rank, Card


class PlayerHand():
    """Contain one hand"""

    def __init__(self, suits: Dict[Suit, List[Rank]]):
        self.suits: Dict[Suit, List[Rank]] = suits
        self.cards: List[Card] = []
        for suit in reversed(Suit):
            for rank in self.suits[suit]:
                self.cards.append(Card(suit, rank))

    @staticmethod
    def from_string_lists(spades: List[str], hearts: List[str], diamonds: List[str], clubs: List[str]) -> PlayerHand:
        """
        Build a PlayerHand out of Lists of Strings which map to Ranks for each suit. e.g. ['A', 'T', '3'] to represent
        a suit holding of Ace, Ten, Three
        :return: PlayerHand representing the holdings provided by the arguments
        """
        suits = {
            Suit.SPADES: sorted([Rank.from_str(card_str) for card_str in spades], reverse=True),
            Suit.HEARTS: sorted([Rank.from_str(card_str) for card_str in hearts], reverse=True),
            Suit.DIAMONDS: sorted([Rank.from_str(card_str) for card_str in diamonds], reverse=True),
            Suit.CLUBS: sorted([Rank.from_str(card_str) for card_str in clubs], reverse=True),
        }
        return PlayerHand(suits)

    @staticmethod
    def from_cards(cards: Iterable[Card]) -> PlayerHand:
        suits = {
            Suit.CLUBS: sorted([card.rank for card in cards if card.suit == Suit.CLUBS], reverse=True),
            Suit.DIAMONDS: sorted([card.rank for card in cards if card.suit == Suit.DIAMONDS], reverse=True),
            Suit.HEARTS: sorted([card.rank for card in cards if card.suit == Suit.HEARTS], reverse=True),
            Suit.SPADES: sorted([card.rank for card in cards if card.suit == Suit.SPADES], reverse=True),
        }
        return PlayerHand(suits)

    @staticmethod
    def from_pbn(string: str) -> PlayerHand:
        """Create a hand from a string with the following syntax '752.Q864.84.AT62'"""
        tab_of_suit = string.split('.')
        cards = []
        for index, suit in enumerate(tab_of_suit):
            for rank in suit:
                match index:
                    case 0:
                        cards.append(Card(Suit.SPADES, Rank.from_str(rank)))
                    case 1:
                        cards.append(Card(Suit.HEARTS, Rank.from_str(rank)))
                    case 2:
                        cards.append(Card(Suit.DIAMONDS, Rank.from_str(rank)))
                    case 3:
                        cards.append(Card(Suit.CLUBS, Rank.from_str(rank)))

        return PlayerHand.from_cards(cards)

    @staticmethod
    def from_lin(string: str) -> PlayerHand:
        """Create a hand from a string with the following syntax SK7HAQT632DK4CQ62"""
        current_suit = Suit.SPADES
        cards = []
        for str_card in string:
            if str_card in ["S", "H", "D", "C"]:
                current_suit = Suit.from_str(str_card)
            else:
                cards.append(Card(current_suit, Rank.from_str(str_card)))

        return PlayerHand.from_cards(cards)

    def print_as_lin(self) -> str:
        suit_arrays = [["C"], ["D"], ["H"], ["S"]]
        for card in self.cards:
            suit_arrays[card.suit.value].append(repr(card))
        repr_str = "".join("".join(suit) for suit in reversed(suit_arrays))
        return repr_str

    def print_as_pbn(self) -> str:
        suit_arrays = [[], [], [], []]
        for card in self.cards:
            suit_arrays[card.suit.value].append(repr(card))
        repr_str = ".".join("".join(suit) for suit in reversed(suit_arrays))
        return repr_str

    def __repr__(self) -> str:
        suit_arrays = [[], [], [], []]
        for card in self.cards:
            suit_arrays[card.suit.value].append(repr(card))
        repr_str = "|".join("".join(suit) for suit in reversed(suit_arrays))
        return f"PlayerHand({repr_str})"

    def __str__(self) -> str:
        suit_arrays = [['♣'], ['♦'], ['♥'], ['♠']]
        for card in self.cards:
            suit_arrays[card.suit.value].append(repr(card))
        repr_str = " ".join("".join(suit) for suit in reversed(suit_arrays))
        return f"{repr_str}"

    def __eq__(self, other) -> bool:
        return self.suits == other.suits

    def __hash__(self) -> int:
        return hash(set(self.cards))

    def append(self, card: Card):
        self.cards.append(card)
        self.suits[card.suit].append(card.rank)

    def len(self) -> int:
        return sum([len(ranks) for suit, ranks in self.suits.items()])


if __name__ == '__main__':
    pass

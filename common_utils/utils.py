from __future__ import annotations

from enum import Enum
from functools import total_ordering

"""
Common bridge concepts such as Cardinal Direction, Suit, and Card Rank represented as Enums
"""


@total_ordering
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    __from_str_map__ = {"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}
    __to_str__ = {NORTH : "North",SOUTH : "South",EAST : "East",WEST : "West"}

    @classmethod
    def from_str(cls, direction_str: str) -> Direction:
        return Direction(cls.__from_str_map__[direction_str.upper()])

    def __lt__(self, other: Direction) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.name

    def next(self) -> Direction:
        return self.offset(1)

    def partner(self) -> Direction:
        return self.offset(2)

    def previous(self) -> Direction:
        return self.offset(3)

    def offset(self, offset: int) -> Direction:
        return Direction((self.value + offset) % 4)

    def abbreviation(self) -> str:
        return self.name[0]

    def to_str(self) -> str :
        return self.__to_str__[self.value]


@total_ordering
class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

    __from_str_map__ = {"S": SPADES, "H": HEARTS, "D": DIAMONDS,
                        "C": CLUBS, '♠': SPADES, '♥': HEARTS, '♦': DIAMONDS, '♣': CLUBS}

    __to_symbol__ = {SPADES : '♠',HEARTS : '♥',DIAMONDS:'♦',CLUBS:'♣'}

    __4_colors__ = {SPADES : 'blue',HEARTS : 'red',DIAMONDS:'orange',CLUBS:'green'}

    @classmethod
    def from_str(cls, suit_str: str) -> Suit:
        return Suit(cls.__from_str_map__[suit_str.upper()])

    def __lt__(self, other: Suit) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.name

    def abbreviation(self) -> str:
        return self.name[0]

    def symbol(self) -> str :
        return self.__to_symbol__[self.value]

    def color(self) -> str :
        return self.__4_colors__[self.value]


@total_ordering
class Rank(Enum):
    TWO = 2, "2", 0
    THREE = 3, "3", 0
    FOUR = 4, "4", 0
    FIVE = 5, "5", 0
    SIX = 6, "6", 0
    SEVEN = 7, "7", 0
    EIGHT = 8, "8", 0
    NINE = 9, "9", 0
    TEN = 10, "T", 0
    JACK = 11, "J", 1
    QUEEN = 12, "Q", 2
    KING = 13, "K", 3
    ACE = 14, "A", 4

    __from_str_map__ = {
        "2": TWO,
        "3": THREE,
        "4": FOUR,
        "5": FIVE,
        "6": SIX,
        "7": SEVEN,
        "8": EIGHT,
        "9": NINE,
        "10": TEN,
        "T": TEN,
        "J": JACK,
        "Q": QUEEN,
        "K": KING,
        "A": ACE,
    }

    @classmethod
    def from_str(cls, rank_str: str) -> Rank:
        return Rank(cls.__from_str_map__[rank_str.upper()])

    def __lt__(self, other: Rank) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.name

    def rank(self) -> int:
        return self.value[0]

    def __str__(self) -> str:
        return self.value[1]

    def abbreviation(self) -> str:
        return self.value[1]

    def hcp(self) -> int:
        return self.value[2]


@total_ordering
class BiddingSuit(Enum):
    CLUBS = 0, Suit.CLUBS
    DIAMONDS = 1, Suit.DIAMONDS
    HEARTS = 2, Suit.HEARTS
    SPADES = 3, Suit.SPADES
    NO_TRUMP = 4, None

    __from_str_map__ = {"S": SPADES, "H": HEARTS,
                        "D": DIAMONDS, "C": CLUBS, "N": NO_TRUMP, "NT": NO_TRUMP,
                        '♠': SPADES, '♥': HEARTS, '♦': DIAMONDS, '♣': CLUBS, 'SA': NO_TRUMP}
    __to_symbol__ = {SPADES : '♠',HEARTS : '♥',DIAMONDS:'♦',CLUBS:'♣', NO_TRUMP : "NT"}
    __4_colors__ = {SPADES : 'blue',HEARTS : 'red',DIAMONDS:'orange',CLUBS:'green',NO_TRUMP : 'black'}

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.name

    def to_suit(self) -> Suit:
        return self.value[1]

    def abbreviation(self, verbose_no_trump=True) -> str:
        if self.value == BiddingSuit.NO_TRUMP.value and verbose_no_trump:
            return "NT"
        return self.name[0]

    def symbol(self) -> str :
        return self.__to_symbol__[self.value]
    
    def color(self) -> str :
        return self.__4_colors__[self.value]

    @classmethod
    def from_str(cls, bidding_suit_str: str) -> BiddingSuit:
        return BiddingSuit(cls.__from_str_map__[bidding_suit_str.upper()])


@total_ordering
class Card:
    """A single card in a hand or deal of bridge"""

    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other) -> bool:
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other) -> bool:
        return self.rank < other.rank

    def __str__(self) -> str:
        return self.rank.abbreviation() + self.suit.abbreviation()

    def to_pbn(self) -> str:
        return self.suit.abbreviation() + self.rank.abbreviation()

    def __repr__(self) -> str:
        return self.rank.abbreviation()

    @classmethod
    def from_str(cls, card_str) -> Card:
        try:
            return Card(Suit.from_str(card_str[0]), Rank.from_str(card_str[1]))
        except:
            return Card(Suit.from_str(card_str[1]), Rank.from_str(card_str[0]))


TOTAL_DECK = []
for rank in Rank:
    for suit in Suit:
        TOTAL_DECK.append(Card(suit, rank))

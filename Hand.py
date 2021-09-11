from dataclasses import dataclass, field
from abc import ABC,abstractmethod

SUITS = 'S H D C'.split()
LEVELS = '2 3 4 5 6 7 8 9 T J Q K A'.split()

@dataclass
class Card(ABC) :
    sort_index: int = field(init=False, repr=False)
    level: str
    hcp_value : int = 0

    def __post_init__(self):
        if self.level not in LEVELS :
            raise ErrorBid("Invalid level (must be in 1-7 range)")
        self.sort_index = LEVELS.index(self.level)+2
        if self.level == 'J' :
            self.hcp_value = 1
        if self.level == 'Q' :
            self.hcp_value = 2
        if self.level == 'K' :
            self.hcp_value = 3
        if self.level == 'A' :
            self.hcp_value = 4

    def __str__(self) :
        return self.level

    def __lt__(self,other) :
        return self.sort_index < other.sort_index

@dataclass
class Spade(Card) :
    pass

@dataclass
class Heart(Card) :
    pass

@dataclass
class Diamond(Card) :
    pass

@dataclass
class Club(Card) :
    pass

@dataclass
class Hand() :
    """Contain one hand"""
    spades : list[Spade]=field(default_factory=list)
    hearts : list[Heart]=field(default_factory=list)
    diamonds : list[Diamond]=field(default_factory=list)
    clubs : list[Club]=field(default_factory=list)
    hcp_value : int = field(init=False, repr=False)

    def __post_init__(self) :
        self.hcp_value=0
        for card in self.spades :
            self.hcp_value += spade.hcp_value
        for card in self.hearts :
            self.hcp_value += spade.hcp_value
        for card in self.diamonds :
            self.hcp_value += spade.hcp_value
        for card in self.clubs :
            self.hcp_value += spade.hcp_value

    def clear(self) :
        for suit in [self.spades,self.hearts,self.diamonds,self.clubs] :
            suit.clear()

    def get_every_suit(self) -> list[list[Card]] :
        return [self.spades,self.hearts,self.diamonds,self.clubs]

    def create_from_string(self, string : str) : #return self
        """Create a hand from a string with the following syntax '752.Q864.84.AT62'"""
        self.clear()
        tab_of_suit = string.split('.')
        for index,suit in enumerate(tab_of_suit) :
            for card in suit :
                if index == 0 : #Spade
                    self.spades.append(Spade(card))
                if index == 1 :
                    self.hearts.append(Heart(card))
                if index == 2 :
                    self.diamonds.append(Diamond(card))
                if index == 3 :
                    self.clubs.append(Club(card))

        self.spades.sort(reverse=True)
        self.hearts.sort(reverse=True)
        self.diamonds.sort(reverse=True)
        self.clubs.sort(reverse=True)
        print(self)
        return self

    def __str__(self) :
        string=""
        for suit in [self.spades,self.hearts,self.diamonds,self.clubs] :
            for card in suit :
                string += card.__str__()
            string+='\n'
        return string

@dataclass
class Diagramm() :
    south : Hand()
    north : Hand()
    west : Hand()
    east : Hand()

    def __str__(self) :
        string = ""
        for hand in [self.north,self.south,self.west,self.east] :
            string += hand.__str__() +"\n"
        return string

    def __init__(self, string : str,dealer : str) :
        """ Create a diagramm from this syntax : 'N:752.Q864.84.AT62 A98.AT9.Q753.J98 KT.KJ73.JT.K7543 QJ643.52.AK962.Q'"""
        string = string[4:-2]
        hand_list = string.split(" ")

        """This spagetthi code ranks the hands in the right order"""
        if dealer == "N" :
            pass
        if dealer == "E" :
            hand_list.insert(0,hand_list.pop()) #1 rotato
        if dealer == "S" :
            hand_list.insert(0,hand_list.pop())
            hand_list.insert(0,hand_list.pop())  #2 rotatoes
        if dealer == "W" :
            hand_list.insert(0,hand_list.pop())
            hand_list.insert(0,hand_list.pop())
            hand_list.insert(0,hand_list.pop())  #3 rotatoes

        self.north = Hand().create_from_string(hand_list[0])
        self.east = Hand().create_from_string(hand_list[1])
        self.south = Hand().create_from_string(hand_list[2])
        self.west = Hand().create_from_string(hand_list[3])

    def is_valid(self) -> bool :
        list_of_cards = []
        for hand in [self.north,self.south,self.west,self.east] :
            for suit in hand.get_every_suit() :
                for card in suit :
                    if card in list_of_cards :
                        """
                        print(self)
                        print(list_of_cards)
                        print(card)
                        """
                        return False
                    else :
                        list_of_cards.append(card)
        if len(list_of_cards) == 52 :
            return True
        else :
            return False

if __name__ == '__main__':
    pass

from dataclasses import dataclass, field
from abc import ABC,abstractmethod
from os import error
from Séquence import ErrorBid

SUITS = 'S H D C'.split()
LEVELS = '2 3 4 5 6 7 8 9 T J Q K A'.split()

@dataclass
class Card(ABC) :
    sort_index: int = field(init=False, repr=False)
    level: str
    hcp_value : int = 0

    def __post_init__(self):
        if self.level not in LEVELS :
            raise ErrorBid("Invalid level (must be in 2 3 4 5 6 7 8 9 T J Q K A)")
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
    def __str__(self) :
        return self.level

@dataclass
class Heart(Card) :
    def __str__(self) :
        return self.level

@dataclass
class Diamond(Card) :
    def __str__(self) :
        return self.level

@dataclass
class Club(Card) :
    def __str__(self) :
        return self.level

total_deck = []                
for level in LEVELS :
    total_deck.append(Spade(level))
    total_deck.append(Heart(level))
    total_deck.append(Diamond(level))
    total_deck.append(Club(level))

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
            self.hcp_value += card.hcp_value
        for card in self.hearts :
            self.hcp_value += card.hcp_value
        for card in self.diamonds :
            self.hcp_value += card.hcp_value
        for card in self.clubs :
            self.hcp_value += card.hcp_value

    def clear(self) :
        for suit in [self.spades,self.hearts,self.diamonds,self.clubs] :
            suit.clear()
        return self

    def get_every_suit(self) -> list[list[Card]] :
        return [self.spades,self.hearts,self.diamonds,self.clubs]

    def len(self) -> int :
        length = 0
        for suit in [self.spades,self.hearts,self.diamonds,self.clubs] :
            length += len(suit)
        return length


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

        self.order()
        return self

    def init_from_lin(self, string : str) : #return self
        """Create a hand from a string with the following syntax SK7HAQT632DK4CQ62"""
        tab_of_suit = string.replace('S',' ').replace('H',' ').replace('D',' ').replace('C',' ').split()
        i=0
        if 'S' in string and string[string.find('S')+1] not in SUITS:
            for card in tab_of_suit[i] :
                self.spades.append(Spade(card))
            i+=1
        if 'H' in string and string[string.find('H')+1] not in SUITS:
            for card in tab_of_suit[i] :
                self.hearts.append(Heart(card))
            i+=1
        if 'D' in string and string[string.find('D')+1] not in SUITS:
            for card in tab_of_suit[i] :
                self.diamonds.append(Diamond(card))
            i+=1
        if string[-1]!='C' :
            for card in tab_of_suit[i] :
                self.clubs.append(Club(card))

        self.order()
        return self

    def order(self) -> None :
        self.spades.sort(reverse=True)
        self.hearts.sort(reverse=True)
        self.diamonds.sort(reverse=True)
        self.clubs.sort(reverse=True)


    def __str__(self) :
        string=""
        for suit in [self.spades,self.hearts,self.diamonds,self.clubs] :
            for card in suit :
                string += card.__str__()
            string+='\n'
        return string

    def print_as_lin(self) -> str:
        string=""
        for i,suit in enumerate([self.spades,self.hearts,self.diamonds,self.clubs]) :
            string += SUITS [i]
            for card in suit :
                string += card.__str__()
            
        return string

    def print_as_pbn(self) -> str :
        string=""
        for i,suit in enumerate([self.spades,self.hearts,self.diamonds,self.clubs]) :
            for card in suit :
                string += card.__str__()
            string+='.'
            
        return string[:-1]

    def append(self, card : Card) :
        if type(card) is Spade :

            self.spades.append(card)
        if type(card) is Heart :
            self.hearts.append(card)
        if type(card) is Diamond :
            self.diamonds.append(card)
        if type(card) is Club :
            self.clubs.append(card)


@dataclass
class Diagramm() :
    south : Hand = field(init=False)
    north : Hand = field(init=False)
    west : Hand = field(init=False)
    east : Hand = field(init=False)

    def __str__(self) :
        string = ""
        for hand in [self.north,self.south,self.west,self.east] :
            string += hand.__str__() +"\n"
        return string

    def clear(self) : #return self
        for hand in [self.north,self.south,self.west,self.east] :
            hand.clear()
        return self

    def init_from_string(self, string : str,dealer : str) :
        """ Create a diagramm from this syntax : 'N:752.Q864.84.AT62 A98.AT9.Q753.J98 KT.KJ73.JT.K7543 QJ643.52.AK962.Q'"""
        string = string[4:-2]
        hand_list = string.split(" ")

        self.north = Hand().create_from_string(hand_list[0])
        self.east = Hand().create_from_string(hand_list[1])
        self.south = Hand().create_from_string(hand_list[2])
        self.west = Hand().create_from_string(hand_list[3])

        if dealer == "N" :
            pass
        if dealer == "E" :
            self.rotate(1)
        if dealer == "S" :
            self.rotate(2)
        if dealer == "W" :
            self.rotate(3)

        return self

    def init_from_lin(self,string : str, dealer : str) :
        """Create a diagramm from this syntax : SK7HAQT632DK4CQ62,S82H98DAT632CKT43,S965HKJ5DQJ985CA5"""
        hand_list = string.split(",")

        self.south = Hand().init_from_lin(hand_list[0])
        self.west = Hand().init_from_lin(hand_list[1])
        self.north = Hand().init_from_lin(hand_list[2])
        self.east = Hand().clear()
        self.auto_complete()

        # if dealer == "N" :
        #     pass
        # if dealer == "E" :
        #     self.rotate(1)
        # if dealer == "S" :
        #     self.rotate(2)
        # if dealer == "W" :
        #     self.rotate(3)

        print(hand_list)
        print(self.print_as_pbn())

        return self

    def rotate(self, rotato : int) :
        temp=[]
        for hand in [self.south,self.west,self.north,self.east] :
            temp.append(hand)
        for i in range(rotato) :
            temp.insert(0, temp.pop())
            
        self.south = temp[0]
        self.west = temp[1]
        self.north = temp[2]
        self.east = temp[3]

    def is_valid(self) -> bool :
        list_of_cards = []
        for hand in [self.north,self.south,self.west,self.east] :
            for suit in hand.get_every_suit() :
                for card in suit :
                    if card in list_of_cards :
                        print('Cette carte est en double !', card)
                        return False
                    else :
                        list_of_cards.append(card)
        if len(list_of_cards) == 52 :
            return True
        else :
            print('Le diagramme contient ', len(list_of_cards), ' cartes')
            return False

    def missing_cards(self) -> list :
        list_of_cards = []
        for hand in [self.north,self.south,self.west,self.east] :
            for suit in hand.get_every_suit() :
                for card in suit :
                    if card in list_of_cards :
                        print("Cette carte est en double",card)
                        raise error("Diagramme invalide")
                    else :
                        list_of_cards.append(card)

        missing_cards = []
        for card in total_deck :
            if card not in list_of_cards :
                missing_cards.append(card)
        return missing_cards

    def auto_complete(self) -> None :
        missing_cards = self.missing_cards()
        for hand in [self.north,self.south,self.west,self.east] :
            while hand.len()<13 :
                hand.append(missing_cards.pop())


        if not self.is_valid() :
            raise error("L'auto-complete n'est pas valide")
                
    def print_as_lin(self) -> str :
        string = ""
        for hand in [self.south,self.west,self.north,self.east] :
            string += hand.print_as_lin()
            string += ","
        return string[:-1]

    def print_as_pbn(self) -> str :
        string = "S:"
        for hand in [self.south,self.west,self.north,self.east] :
            string += hand.print_as_pbn()
            string += " "
        return string[:-1]

if __name__ == '__main__':
    pass
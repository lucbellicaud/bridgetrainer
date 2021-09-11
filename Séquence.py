from dataclasses import dataclass, field
from abc import ABC,abstractmethod
from typing import List

LEVELS = [1,2,3,4,5,6,7]
SUITS = 'C D H S N'.split()
DECLARATIONS = 'P X XX'.split()

@dataclass
class SequenceAtom(ABC) :
    """A SequenceAtom represents an action by a player during the biding"""

@dataclass(order=True)
class Bid(SequenceAtom):
    """"""
    sort_index: int = field(init=False, repr=False)
    level: int
    suit: str
    description : str=""

    def __post_init__(self):
        if self.level not in LEVELS :
            raise ErrorBid("Invalid level (must be in 1-7 range)")
        if self.suit not in SUITS :
            raise ErrorBid("Invalid suit, must be C/D/H/S/N")


        self.sort_index = (self.level-1)*5 + SUITS.index(self.suit)

    def __str__(self):
        return f'{self.level}{self.suit}'

@dataclass
class Declaration(SequenceAtom) :
    """Classe des déclarations"""
    type : str
    description : str=""

    def __post_init__(self):
        if self.type not in DECLARATIONS :
            raise ErrorBid("Only P, X and XX are valid declarations")
    def __str__(self):
        return self.type

class ErrorBid(Exception):
    def __init__(self, value):
        self.value = value
        print("Incorrect bid")
        print(value)
    def __str__(self):
        return repr(self.value)

def sequence_atom_filter(s : str) -> SequenceAtom :
    """return a declaration or a bid bases on the string"""
    if s in DECLARATIONS :
        return Declaration(s)
    else :
        return Bid(int(s[0]),s[1])


@dataclass
class Sequence() :
    """Bridge sequence"""
    sequence : List[SequenceAtom]=field(default_factory=list)
    description : str =""
    done : bool = False

    def set_sequence(self, sq : list[SequenceAtom]) -> None :
        self.sequence = sq

    def get_sequence(self) -> list[SequenceAtom] :
        return self.sequence

    def append(self,at : SequenceAtom) -> None :
        """Add a bid at the end of the sequence"""
        if self.done == True :
            raise ErrorBid ("Bidding is done !")

        if self.check_append_validity(at) == False :
            raise ErrorBid("L'enchère n'est pas valable")
        self.sequence.append(at)
        self.check_if_done()

    def check_if_done(self) -> None :
        if len(self.sequence)==4 : #Check if 4 passes
            for at in self.sequence :
                if not(type(at) is Declaration and at.type == 'P') :
                    self.done = False
                    return
            self.done = True
            return
        if len(self.sequence)>=5 : # Check is 3 passes
            for at in self.sequence[-3:] :
                if not(type(at) is Declaration and at.type == 'P') :
                    self.done = False
                    return
            self.done = True
            return
        self.done = False
        return

    def check_append_validity(self,at : SequenceAtom) -> bool :
        """Check if a new bid is valid"""
        if type(at) is Bid :
            for seq_atom in reversed(self.sequence) :
                if type(seq_atom) is Bid :
                    if at<= seq_atom :
                        return False
                    return True
            return True
        else : #Déclaration
            if at.type == 'X' :
                if self.sequence and type(self.sequence[-1]) is Bid :
                    return True
                if len(self.sequence)>=3 and type(self.sequence[-1]) is Declaration and self.sequence[-1].type =="P" and type(self.sequence[-2]) is Declaration and self.sequence[-2].type =="P" and type(self.sequence[-3]) is Bid :
                    return True
                else :
                    return False
            elif at.type == 'XX' :
                if self.sequence and type(self.sequence[-1]) is Declaration and self.sequence[-1].type =="X" :
                    return True
                if len(self.sequence)>=3 and type(self.sequence[-1]) is Declaration and self.sequence[-1].type =="P" and type(self.sequence[-2]) is Declaration and self.sequence[-2].type =="P" and type(self.sequence[-3]) is Declaration and self.sequence[-3].type =="X":
                    return True
                else :
                    return False
            return True #Pass is always valid

    def sequence_is_valid (self, seq : List[SequenceAtom]) -> bool :
        checking_seq = Sequence()
        for atom in seq :
            checking_seq.append(atom)
        return True

    def delete(self) -> None :
        """Delete the last bid"""
        self.sequence.pop()
        self.done = False

    def replace_with_index (self, index : int, at : SequenceAtom) -> None :
        """Replace a bid with it's index with a new one"""
        new_seq = self.sequence
        new_seq[index] = at
        if self.sequence_is_valid(new_seq) :
            self.sequence[index]=at

    def replace_bid (self, old_atom : str, new_atom : str) -> None :
        """Replace a bid with a certain value with a new one"""
        self.replace_with_index(self.sequence.index(sequence_atom_filter(old_atom)), sequence_atom_filter(new_atom))

    def append_multiple_from_string(self,string : str) :
        """Add multiple bids from a string, each bid being separated with a coma"""
        for s in string.split(",") :
            self.append(sequence_atom_filter(s))

    def __str__(self) :
        """Print the bidding""" #To be improved
        string =""
        for atom in self.sequence :
            string += atom.__str__() +" "
        return string

if __name__ == '__main__':
    seq = Sequence()
    seq.append_multiple_from_string('P,P,P,1C,X,2C,X,XX,3C')
    seq.replace_with_index(4,Bid(1,'D'))
    seq.replace_bid('3C','3D')
    print(seq)

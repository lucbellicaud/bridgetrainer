from dataclasses import dataclass, field
from abc import ABC,abstractmethod
from typing import List

LEVELS = [1,2,3,4,5,6,7]
SUITS = 'C D H S N'.split()
DECLARATIONS = 'Pass X XX'.split()

@dataclass
class SequenceAtom(ABC) :
    """A SequenceAtom represents an action by a player during the biding"""

    def sequence_atom_filter(s : str) : #return SequenceAtom
        """return a declaration or a bid bases on the string"""
        if s in DECLARATIONS :
            return Declaration(s)
        else :
            return Bid(int(s[0]),s[1])

@dataclass(order=True)
class Bid(SequenceAtom):
    """A bid."""
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
            raise ErrorBid("Only Pass, X and XX are valid declarations")
    def __str__(self):
        return self.type

    def get_type(self) -> str :
        return self.type

@dataclass
class FinalContract() :
    bid : Bid = None
    declaration : Declaration = 'Pass'
    joueur : str = ''
    valeur : int = 0

    def set_bid (self,bid : Bid) -> None :
        self.bid = bid

    def get_bid (self) -> Bid :
        return self.bid

    def set_declaration (self,decla : Declaration) -> None :
        self.declaration = decla

    def get_declaration (self) -> Declaration :
        return self.declaration

    def set_joueur (self,joueur : str) -> None :
        self.joueur = joueur

    def get_joueur (self) -> str :
        return self.joueur

    def set_valeur (self,valeur : int) -> None :
        self.valeur = valeur

    def get_valeur (self) -> int :
        return self.valeur

    def clear(self) -> None :
        self.bid = None
        self.declaration = None

    

    def init_from_string(self,s : str) : # -> return self
        if len(s)==0 or len(s)>4 :
            raise ErrorBid ("Invalid final contract !")
        if len(s)==2 : #contract without double or redouble
            self.bid = Bid(int(s[0]),s[1])
        if len(s)==3 : #Doubled contract
            if s[2] != 'X' :
                raise ErrorBid ("Invalid final contract !")
            self.bid = Bid(int(s[0]),s[1])
            self.declaration = Declaration('X')
        if len(s)==4 : #Pull off the blue card !
            if s=="Pass" :
                self.declaration = Declaration('Pass')
            elif s[3:]!="XX" :
                raise ErrorBid ("Invalid final contract !")
            self.bid = Bid(int(s[0]),s[1])
            self.declaration = Declaration('XX')

        return self

    def __eq__(self,other) :
        return self.get_bid()==other.get_bid() and other.get_declaration()==self.declaration

    def __hash__(self):
        return id(self)


@dataclass
class Sequence() :
    """Bridge sequence"""
    sequence : List[SequenceAtom]=field(default_factory=list)
    description : str =""
    done : bool = False
    final_contract : FinalContract = None

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
                if not(type(at) is Declaration and at.type == 'Pass') :
                    self.done = False
                    return
            self.done = True
            self.set_final_contract(self.get_last_bid(),self.get_last_declaration())
            return
        if len(self.sequence)>=5 : # Check is 3 passes
            for at in self.sequence[-3:] :
                if not(type(at) is Declaration and at.type == 'Pass') :
                    self.done = False
                    return
            self.done = True
            self.set_final_contract(self.get_last_bid(),self.get_last_declaration())
            return
        self.done = False
        return

    def get_last_bid(self) -> Bid :
        """Return the last bid made"""
        for seq_atom in reversed(self.get_sequence()) :
            if type(seq_atom) is Bid :
                return seq_atom
        return None

    def get_last_declaration(self) -> Declaration :
        """Return if the final contract is passed, doubled or redoubled"""
        for seq_atom in reversed(self.get_sequence()) :
            if (type(seq_atom) is not Bid) :
                break
            if seq_atom.get_type()!="Pass" :
                 return seq_atom
            return Declaration('Pass')

    def set_final_contract(self, bid : Bid, declaration : Declaration) :
        self.final_contract = FinalContract(bid,declaration)

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
                if len(self.sequence)>=3 and type(self.sequence[-1]) is Declaration and self.sequence[-1].type =="Pass" and type(self.sequence[-2]) is Declaration and self.sequence[-2].type =="Pass" and type(self.sequence[-3]) is Bid :
                    return True
                else :
                    return False
            elif at.type == 'XX' :
                if self.sequence and type(self.sequence[-1]) is Declaration and self.sequence[-1].type =="X" :
                    return True
                if len(self.sequence)>=3 and type(self.sequence[-1]) is Declaration and self.sequence[-1].type =="Pass" and type(self.sequence[-2]) is Declaration and self.sequence[-2].type =="Pass" and type(self.sequence[-3]) is Declaration and self.sequence[-3].type =="X":
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
        self.replace_with_index(self.sequence.index(SequenceAtom.sequence_atom_filter(old_atom)), SequenceAtom.sequence_atom_filter(new_atom))

    def append_multiple_from_string(self,string : str) :
        """Add multiple bids from a string, each bid being separated with a coma"""
        for s in string.split(",") :
            self.append(SequenceAtom.sequence_atom_filter(s))
        return self

    def __str__(self) :
        string=""
        # string += '{0:6}{1:6}{2:6}{3:6}\n'.format('N','E','S','W')
        seq = self.get_sequence()
        for i in range(0,len(seq)) :
            string+='{0:6}'.format(seq[i].__str__())
            if i%4==3 :
                string+="\n"
        return string

    def print_as_pbn(self) :
        string=""
        seq = self.get_sequence()
        for i in range(0,len(seq)) :
            atom = seq[i].__str__()
            string+='{0:6}'.format(atom)
            if i%4==3 :
                string+="\n"
        print(string)

class ErrorBid(Exception):
    def init(self, value):
        self.value = value
        print("Incorrect bid")
        print(value)
    def str(self):
        return repr(self.value)
        
if __name__ == '__main__':
    seq = Sequence()
    seq.append_multiple_from_string('Pass,Pass,Pass,1C,X,2C,X,XX,3C')
    seq.print_as_pbn()
    print(seq.__str__())
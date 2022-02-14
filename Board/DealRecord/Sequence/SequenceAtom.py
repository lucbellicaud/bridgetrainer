from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import List, Optional, Tuple
from common_utils import BiddingSuit
from common_utils.parsing_tools import Pbn
from common_utils.utils import Direction


@dataclass
@total_ordering
class Bid:
    level: int
    suit: BiddingSuit

    def __post_init__(self):
        if self.level not in range(1, 8):
            raise Exception("Invalid level (must be in 1-7 range)")

    def __lt__(self, other) -> bool:
        return self.level*5 + self.suit.value[0] < other.level*5 + other.suit.value[0]

    def __repr__(self) -> str:
        return str(self.level) + self.suit.abbreviation()

    def print_as_lin(self) -> str:
        return str(self.level)+self.suit.abbreviation(verbose_no_trump=False)

    def print_as_pbn(self) -> str:
        return str(self.level)+self.suit.abbreviation(verbose_no_trump=True)

    @staticmethod
    def from_str(string: str) -> Bid:
        return Bid(int(string[0]), BiddingSuit.from_str(string[1:]))


class Declaration(Enum):
    PASS = 0, "Pass", "p"
    DOUBLE = 1, 'X', "d"
    REDOUBLE = 2, "XX", "r"

    __from_str_map__ = {"PASS": PASS, "P": PASS, "X": DOUBLE, "XX": REDOUBLE}

    @classmethod
    def from_str(cls, declaration_str: str) -> Declaration:
        return Declaration(cls.__from_str_map__[declaration_str.upper()])

    @classmethod
    def from_int(cls, declaration_int: int) -> Declaration:
         if declaration_int==1 : return Declaration.DOUBLE
         if declaration_int==2 : return Declaration.REDOUBLE
         return Declaration.PASS


    def print_as_lin(self) -> str:
        return self.value[2]

    def print_as_pbn(self) -> str:
        return self.value[1]

    @classmethod
    def is_str_declaration(cls, bidding_suit_str) -> bool:
        if bidding_suit_str.upper() in cls.__from_str_map__:
            return True
        return False

    def __str__(self) -> str:
        return self.value[1]


@dataclass
class SequenceAtom():
    declaration: Optional[Declaration]
    bid: Optional[Bid]
    alert: Optional[str]

    def __post_init__(self):
        if self.declaration and self.bid:
            raise Exception("A sequenceAtom can't be a bid and a declaration")

    @staticmethod
    def from_str(string: str) -> SequenceAtom:
        if Declaration.is_str_declaration(string):
            return SequenceAtom(declaration=Declaration.from_str(string), bid=None, alert=None)
        return SequenceAtom(bid=Bid.from_str(string), declaration=None, alert=None)

    def __str__(self) -> str:
        string = ""
        if self.declaration != None:
            string += self.declaration.__str__()
        elif self.bid != None:
            string += self.bid.__str__()
        if self.alert != None:
            string += "("+self.alert+")"
        return string

    def print_as_lin(self) -> str:
        if self.declaration != None:
            return self.declaration.print_as_lin()
        elif self.bid != None:
            return self.bid.print_as_lin()
        raise Exception("print_as_lin : Invalid sequence atom")

    def print_as_pbn(self) -> str:
        if self.declaration != None:
            return self.declaration.print_as_pbn()
        elif self.bid != None:
            return self.bid.print_as_pbn()
        raise Exception("print_as_lin : Invalid sequence atom")


@dataclass
class FinalContract:
    bid: Optional[Bid]
    declaration: Declaration
    declarer: Optional[Direction]

    @staticmethod
    def from_str(string: str) -> FinalContract:
        """
        4SXN,Pass...
        """
        if string == 'Pass':
            return FinalContract(bid=None, declaration=Declaration.PASS, declarer=None)
        declarer = Direction.from_str(string[-1])
        string = string[:-1]
        declaration = Declaration.from_int(string.count('X'))
        string = string.replace('X', '')
        if string.upper()=="PASS" or string.upper()=="P" :
            return FinalContract(bid=None, declaration=declaration, declarer=declarer)
        return FinalContract(bid=Bid.from_str(string), declaration=declaration, declarer=declarer)

    @staticmethod
    def from_pbn(string : str) -> Optional[FinalContract] :
        final_contract = Pbn.get_tag_content(string,"Contract")+Pbn.get_tag_content(string,"Declarer")
        if final_contract :
            return FinalContract.from_str(final_contract)
        else :
            return None
    
    def print_as_pbn(self) -> str:
        string = ""
        if self.declarer:
            string += Pbn.print_tag("Declarer", self.declarer.abbreviation())
        if not self.bid:
            return string + Pbn.print_tag("Contract", "Pass")
        elif self.declaration == Declaration.PASS:
            return string + Pbn.print_tag("Contract", self.bid.print_as_pbn())
        else:
            return string + Pbn.print_tag("Contract", self.bid.print_as_pbn()+self.declaration.print_as_pbn())

    def __str__(self) -> str:
        if not self.bid or not self.declarer:
            return "Contrat final : passe général"
        else:
            return self.bid.__str__()+self.declaration.value[1]+self.declarer.abbreviation()

from __future__ import annotations
from dataclasses import dataclass
import logging
from typing import Dict, List, Optional, Tuple

from common_utils import Direction, Card, BiddingSuit, Suit
from common_utils.parsing_tools import Pbn


@dataclass
class PlayRecord:
    tricks: int
    leader: Direction
    record: Optional[List[Trick]]

    @staticmethod
    def from_pbn(string: str) -> Optional[PlayRecord]:
        str_leader = Pbn.get_tag_content(string, "Play")
        str_result = Pbn.get_tag_content(string, "Result")
        if not str_result:
            return None

        str_declarer = Pbn.get_tag_content(
            string, "Declarer") if not str_leader else None
        leader = Direction.from_str(str_leader) if str_leader else Direction.from_str(
            str_declarer) if str_declarer else None
        if not leader:
            return None
        result = int(str_result)
        trump = BiddingSuit.from_str(
            Pbn.get_tag_content(string, "Contract").replace('X', '')[1:])
        raw_tricks_data = Pbn.get_content_under_tag(string, "Play")
        str_tricks = raw_tricks_data.split('\n') if raw_tricks_data else None
        if str_tricks is None:
            return PlayRecord(tricks=int(result), leader=leader, record=None)
        tricks = []
        trick_winner = leader
        for str_trick in str_tricks:
            current_dir = leader
            trick_record = {}
            cards_str = str_trick.split()
            for card in cards_str:
                try:
                    trick_record[current_dir] = Card.from_str(card)
                except IndexError:
                    pass
                current_dir = current_dir.next()
            trick = Trick(trick_winner, trick_record)
            trick_winner = trick.winner(
                trump=trump)
            tricks.append(trick)
        return PlayRecord(tricks=result, leader=leader, record=tricks)

    def __str__(self) -> str:
        string = "Tricks : " + str(self.tricks) + "\n"
        if self.record:
            string += '{0:3}{1:3}{2:3}{3:3}\n'.format('N', 'E', 'S', 'W')
            for trick in self.record:
                string += trick.__str__() + "\n"
        return string

    def print_as_pbn(self) -> str:
        string = ""
        string += Pbn.print_tag("Play", self.leader.abbreviation())
        if self.record:
            for trick in self.record:
                string += trick.print_as_pbn(self.leader)+"\n"
        return string + "*"

    def __len__(self) :
        if self.record is None :
            return 0
        else :
            return len(self.record)


@dataclass
class Trick():
    lead: Direction
    cards: Dict[Direction, Card]

    def winner(self, trump: BiddingSuit) -> Direction:
        winner = self.lead
        suit_led = self.lead #Default value, should not append
        try :
            suit_led = self.cards[winner].suit
        except :
            logging.warning("The winner of the last trick didn't play in the following one")
            return winner
        if trump == BiddingSuit.NO_TRUMP:
            for dir, card in self.cards.items():
                if card.suit == suit_led:
                    if card > self.cards[winner]:
                        winner = dir
        else:  # Trump
            for dir, card in self.cards.items():
                if card.suit == trump.to_suit():
                    if self.cards[winner].suit == suit_led:
                        winner = dir
                    if self.cards[winner].suit == trump.to_suit():
                        if card > self.cards[winner]:
                            winner = dir
                elif card.suit == suit_led and self.cards[winner].suit == suit_led:
                    if card > self.cards[winner]:
                        winner = dir

        return winner

    def __str__(self) -> str:
        string = ""
        for dir in Direction:
            if dir in self.cards:
                string += '{0:3}'.format(self.cards[dir].__str__())
        return string

    def print_as_pbn(self, first_dir: Direction) -> str:
        string = ""
        for i in range(len(Direction)):
            if self.cards[first_dir]:
                string += self.cards[first_dir].to_pbn()+" "
            else:
                string += "-  "
            first_dir = first_dir.offset(1)
        return string[:-1]

    def __trick_as_list__(self) -> List[Tuple[Direction,Card]] :
        trick_as_list : List[Tuple[Direction,Card]]= []
        dir : Direction = self.lead
        for _ in range(len(self.cards)) :
            trick_as_list.append((dir,self.cards[dir]))
            dir = dir.offset(1)
        return trick_as_list

    def __getitem__(self,key) :
        return self.__trick_as_list__()[key]

    def __len__(self) :
        return len(self.cards)
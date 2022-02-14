from __future__ import annotations
from dataclasses import dataclass
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
        if not str_leader or not str_result :
            return None
        leader = Direction.from_str(str_leader)
        result = int(str_result)
        trump = BiddingSuit.from_str(
            Pbn.get_tag_content(string, "Contract").replace('X','')[1:])
        str_tricks = Pbn.get_play_record(string).split('\n')

        tricks = []
        trick_winner = leader
        for str_trick in str_tricks:
            current_dir = leader
            trick_record = {}
            cards_str = str_trick.split()
            for card in cards_str:
                try:
                    trick_record[current_dir] = Card.from_str(card)
                except KeyError:
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

    def print_as_pbn(self) -> str :
        string = ""
        string += Pbn.print_tag("Play",self.leader.abbreviation())
        if self.record :
            for trick in self.record :
                string+=trick.print_as_pbn(self.leader)+"\n"
        return string +"*"


@dataclass
class Trick():
    lead: Direction
    cards: Dict[Direction, Card]

    def winner(self, trump: BiddingSuit) -> Direction:
        winner = self.lead
        suit_led = self.cards[winner].suit
        if trump == BiddingSuit.NO_TRUMP:
            for dir, card in self.cards.items():
                if card.suit == suit_led:
                    if card > self.cards[winner]:
                        winner = dir
        else:  # Trump
            for dir, card in self.cards.items():
                if card.suit == trump:
                    if self.cards[winner].suit == suit_led:
                        winner = dir
                    if self.cards[winner].suit == trump:
                        if card > self.cards[winner]:
                            winner = dir
                elif card.suit == suit_led and self.cards[winner].suit == suit_led:
                    if card > self.cards[winner]:
                        winner = dir

        return winner

    def __str__(self) -> str:
        string = ""
        for dir in Direction:
            if self.cards[dir]:
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

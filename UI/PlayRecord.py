import tkinter as tk
from typing import Dict, Optional, Tuple
from Board import PlayRecord, Trick
from common_utils import Card, Direction
from UI import MAIN_FONT_SMALL,MAIN_FONT_BIG,MAIN_FONT_STD,position_dict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Deal import FixedDealUI


class CardUI(tk.Frame):
    def __init__(self, parent, card: Optional[Card]) -> None:
        self.font = MAIN_FONT_BIG
        tk.Frame.__init__(self, parent, highlightbackground="black",
                          highlightthickness=1 if card else 0)
        self.rank_txt: tk.StringVar = tk.StringVar(
            self, value=card.rank.abbreviation() if card is not None else ' ')
        self.suit_txt: tk.StringVar = tk.StringVar(
            self, value=card.suit.symbol() if card is not None else ' ')

        self.rank_label = tk.Label(
            self, textvariable=self.rank_txt, font=self.font, width=3)
        self.suit_label = tk.Label(self, textvariable=self.suit_txt, fg=card.suit.color(
        ) if card is not None else 'black', font=self.font)
        self.suit_label.grid(row=1, column=0)
        self.rank_label.grid(row=0, column=0)

    def set_values(self, card: Card):
        self.config(background='white')
        self.rank_label.config(background='white')
        self.suit_label.config(background='white')
        self.rank_txt.set(card.rank.abbreviation())
        self.suit_txt.set(value=card.suit.symbol())
        self.suit_label.config(fg=card.suit.color())

    def clear_values(self):
        self.config(background='#F0F0F0')
        self.rank_label.config(background='#F0F0F0')
        self.suit_label.config(background='#F0F0F0')
        self.rank_txt.set(' ')
        self.suit_txt.set(' ')


class PlayRecordNavigationBar(tk.Frame):
    """Navigate trought the set of boards"""

    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.previous_trick = tk.Button(
            self, text=" << ", command=parent.previous_trick)
        self.previous_card = tk.Button(
            self, text=" < ", command=parent.previous_card)
        self.next_card = tk.Button(
            self, text=" > ", command=parent.display_next_card)
        self.next_trick = tk.Button(
            self, text=" >> ", command=parent.display_next_trick)

        self.previous_trick.grid(column=0, row=0)
        self.previous_card.grid(column=1, row=0)
        self.next_card.grid(column=2, row=0)
        self.next_trick.grid(column=3, row=0)


class PlayRecordUI(tk.Frame):
    def __init__(self, parent, play_record: PlayRecord) -> None:
        if play_record.record is None:
            return
        tk.Frame.__init__(self, parent)
        self.master: FixedDealUI
        self.play_record = play_record
        self.trick_index = -1
        self.card_index = -1
        self.current_trick = play_record.record[0]
        self.currents_cards: Dict[Direction, CardUI] = {
            dir: CardUI(self, None) for dir in Direction}
        self.init_cards()
        self.play_record_navigation_bar = PlayRecordNavigationBar(self)
        self.play_record_navigation_bar.grid(
            row=3, column=0, columnspan=3, sticky=tk.S)
        self.display_next_card()

    def get_next_card(self) -> Tuple[Direction, Card]:
        if self.play_record.record is None:
            raise Exception("No play record !")
        self.card_index = (self.card_index+1) % 4
        if self.card_index == 0:
            self.clear_cards()
            self.trick_index += 1
            self.current_trick = self.play_record.record[self.trick_index]
        return self.current_trick[self.card_index]

    def display_next_card(self) -> None:
        dir, card = self.get_next_card()
        self.currents_cards[dir].set_values(card)
        self.master.play_a_card(dir=dir, card=card)
        self.check_buttons_availability()
        return

    def display_next_trick(self) -> None:
        self.display_next_card()
        while self.card_index != 3:
            self.display_next_card()

    def previous_card(self) -> None:
        if self.play_record.record is None:
            raise Exception("No play record !")
        dir, last_card = self.current_trick[self.card_index]
        self.master.give_back_a_card(dir=dir, card=last_card)
        self.card_index = (self.card_index-1) % 4
        if self.card_index != 3:
            self.clear_card(dir)
        else:  # go to last trick
            self.trick_index -= 1
            self.current_trick = self.play_record.record[self.trick_index]
            self.clear_cards()
            for dir, card in self.current_trick:
                self.currents_cards[dir].set_values(card)
        self.check_buttons_availability()

    def previous_trick(self) -> None:
        self.previous_card()
        while self.card_index != 3 and not (self.card_index == 0 and self.trick_index == 0):
            self.previous_card()

    def clear_card(self, dir: Direction) -> None:
        self.currents_cards[dir].clear_values()

    def clear_cards(self) -> None:
        [self.clear_card(dir) for dir in Direction]

    def init_cards(self) -> None:
        for dir in Direction:
            self.currents_cards[dir].grid(
                row=position_dict[dir][0], column=position_dict[dir][1])

    def check_if_max_tricks(self) :
        if len(self.play_record)==self.trick_index+1 :
            self.play_record_navigation_bar.next_trick['state']= tk.DISABLED
        else :
            self.play_record_navigation_bar.next_trick['state']= tk.NORMAL

    def check_if_end_of_record(self) :
        if len(self.play_record)+len(self.current_trick)==self.trick_index+1+self.card_index+1 :
            self.play_record_navigation_bar.next_trick['state']= tk.DISABLED
            self.play_record_navigation_bar.next_card['state']= tk.DISABLED
        elif len(self.play_record)==self.trick_index+1 :
            self.play_record_navigation_bar.next_card['state']= tk.NORMAL
            self.play_record_navigation_bar.next_trick['state']= tk.DISABLED
        else :
            self.play_record_navigation_bar.next_trick['state']= tk.NORMAL
            self.play_record_navigation_bar.next_card['state']= tk.NORMAL


    def check_if_record_begining(self) :
        if self.trick_index==0 and self.card_index==0 :
            self.play_record_navigation_bar.previous_card['state']= tk.DISABLED
            self.play_record_navigation_bar.previous_trick['state']= tk.DISABLED
        elif self.trick_index==0 :
            self.play_record_navigation_bar.previous_card['state']= tk.NORMAL
            self.play_record_navigation_bar.previous_trick['state']= tk.DISABLED
        else :
            self.play_record_navigation_bar.previous_card['state']= tk.NORMAL
            self.play_record_navigation_bar.previous_trick['state']= tk.NORMAL

    def check_buttons_availability(self) :
        self.check_if_end_of_record()
        self.check_if_record_begining()
        
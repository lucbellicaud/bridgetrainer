import logging
import tkinter as tk
from tkinter import messagebox
from typing import Dict, List, Optional, Tuple
from Board import PlayRecord, Trick
from common_utils import Card, Direction,BiddingSuit
from UI import MAIN_FONT_SMALL, MAIN_FONT_BIG, MAIN_FONT_STD, position_dict

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
            self, text=" << ", command=parent.previous_trick, font=MAIN_FONT_SMALL)
        self.previous_card = tk.Button(
            self, text=" < ", command=parent.previous_card, font=MAIN_FONT_SMALL)
        self.next_card = tk.Button(
            self, text=" > ", command= lambda : parent.display_next_card(None,None), font=MAIN_FONT_SMALL)
        self.next_trick = tk.Button(
            self, text=" >> ", command=parent.display_next_trick, font=MAIN_FONT_SMALL)

        self.previous_trick.grid(column=0, row=0)
        self.previous_card.grid(column=1, row=0)
        self.next_card.grid(column=2, row=0)
        self.next_trick.grid(column=3, row=0)


class PlayRecordEditOptions(tk.Frame):
    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.master: PlayRecordUI
        self.edit_from_start = tk.Button(
            self, text="Edit from start", font=MAIN_FONT_SMALL)
        self.edit_from_here = tk.Button(
            self, text="Edit from here", font=MAIN_FONT_SMALL, command=self.master.edit_play_record_from_current_state)

        self.edit_from_start.grid(column=0, row=0)
        self.edit_from_here.grid(column=1, row=0)


class PlayRecordUI(tk.Frame):
    """Class to navigate through a recorded card play"""

    def __init__(self, parent, play_record: PlayRecord, trump : BiddingSuit) -> None:
        if play_record.record is None:
            return
        tk.Frame.__init__(self, parent)
        self.master: FixedDealUI
        self.trump : BiddingSuit = trump
        self.play_record: PlayRecord = play_record
        self.trick_index: int = -1
        self.card_index: int = -1
        self.current_trick: Trick = play_record.record[0]
        self.currents_cards: Dict[Direction, CardUI] = {
            dir: CardUI(self, None) for dir in Direction}
        self.init_cards()
        self.navigation_bar = PlayRecordNavigationBar(self)
        self.navigation_bar.grid(
            row=3, column=0, columnspan=3, sticky=tk.S)
        self.edit_options = PlayRecordEditOptions(self)
        self.edit_options.grid(row=4, column=0, columnspan=3, sticky=tk.S)
        self.edit_mode = False
        self.new_record: List[Trick] = []
        self.check_buttons_availability()

    def get_next_card(self) -> Tuple[Direction, Card]:
        if self.play_record.record is None:
            raise Exception("No play record !")
        self.card_index = (self.card_index+1) % 4
        if self.card_index == 0:
            self.clear_cards()
            self.trick_index += 1
            self.current_trick = self.play_record.record[self.trick_index]
        return self.current_trick[self.card_index]

    def display_next_card(self, card: Optional[Card], dir: Optional[Direction]) -> None:
        # Not in edit mode
        if not self.edit_mode and card is None and dir is None:
            dir, card = self.get_next_card()
            self.currents_cards[dir].set_values(card)
            self.master.play_a_card(dir=dir, card=card)
            if self.card_index!=3 :
                self.master.has_to_play(dir.next(),self.current_trick[0][1].suit)
            else :
                self.master.has_to_play(self.current_trick.winner(self.trump),None)

        # In edit mode
        elif self.edit_mode and card and dir:            
            if self.new_record == [] or len(self.new_record[-1]) == 4:
                self.clear_cards()
                self.new_record.append(Trick(lead=dir, cards={dir: card}))
            else:
                self.new_record[-1].cards[dir] = card
            self.currents_cards[dir].set_values(card)
            if len(self.new_record[-1])!=4 :
                self.master.has_to_play(dir.next(),self.new_record[-1][0][1].suit)
            else :
                self.master.has_to_play(self.new_record[-1].winner(self.trump),None)
        else:
            messagebox.showerror(
                "You're in edit mode and didn't submit a card or submited a card and wasn't in edit mode")
            logging.error(
                "You're in edit mode and didn't submit a card or submited a card and wasn't in edit mode")
        self.check_buttons_availability()

    def display_next_trick(self) -> None:
        self.display_next_card(None, None)
        while self.card_index != 3:
            self.display_next_card(None, None)

    def previous_card(self) -> None:
        if self.play_record.record is None:
            raise Exception("No play record !")

        #Not in edit mode
        self.master.end_of_turn_for_everyone()
        if not self.edit_mode:
            dir, last_card = self.current_trick[self.card_index]
            self.master.give_back_a_card(dir=dir, card=last_card)
            self.card_index = (self.card_index-1) % 4
            if self.card_index != 3:
                self.clear_card(dir)
                self.master.has_to_play(dir,self.current_trick[0][1].suit)
            elif self.card_index==3 and self.trick_index==0 : #Case of first card
                self.clear_card(dir)
                self.master.has_to_play(dir,None)
                self.card_index=-1
                self.trick_index=-1
            else:  # go to last trick
                self.trick_index -= 1
                self.current_trick = self.play_record.record[self.trick_index]
                self.clear_cards()
                self.master.has_to_play(self.current_trick.winner(self.trump),None)
                for dir, card in self.current_trick:
                    self.currents_cards[dir].set_values(card)
        #In edit mode
        elif self.edit_mode:
            if len(self.new_record[-1]) == 1:
                dir, last_card = self.new_record.pop()[0]
                self.master.give_back_a_card(dir=dir, card=last_card)
                self.clear_cards()
                if self.new_record!=[] :
                    self.master.has_to_play(self.new_record[-1].winner(self.trump),None)
                    for dir, card in self.new_record[-1]:
                        self.currents_cards[dir].set_values(card)
                else :
                    self.master.has_to_play(dir=dir,suit=None)
            else:
                dir, last_card = self.new_record[-1][-1]
                self.new_record[-1].cards.pop(dir)
                self.master.give_back_a_card(dir=dir, card=last_card)
                self.master.has_to_play(dir,self.new_record[-1][0][1].suit)
                self.clear_card(dir)

        self.check_buttons_availability()

    def previous_trick(self) -> None:
        self.previous_card()
        if not self.edit_mode :
            while self.card_index != 3 and not (self.card_index == 0 and self.trick_index == 0):
                self.previous_card()
        elif self.edit_mode :
            while self.new_record and len(self.new_record[-1]) != 4 :
                self.previous_card()


    def clear_card(self, dir: Direction) -> None:
        self.currents_cards[dir].clear_values()

    def clear_cards(self) -> None:
        [self.clear_card(dir) for dir in Direction]

    def init_cards(self) -> None:
        for dir in Direction:
            self.currents_cards[dir].grid(
                row=position_dict[dir][0], column=position_dict[dir][1])

    def check_if_end_of_record(self):
        if (len(self.play_record)+len(self.current_trick) == self.trick_index+1+self.card_index+1) or self.edit_mode:
            self.navigation_bar.next_trick['state'] = tk.DISABLED
            self.navigation_bar.next_card['state'] = tk.DISABLED
        elif len(self.play_record) == self.trick_index+1:
            self.navigation_bar.next_card['state'] = tk.NORMAL
            self.navigation_bar.next_trick['state'] = tk.DISABLED
        else:
            self.navigation_bar.next_trick['state'] = tk.NORMAL
            self.navigation_bar.next_card['state'] = tk.NORMAL

    def check_if_record_begining(self):
        if not self.edit_mode :
            if self.trick_index <= 0 and self.card_index <= -1:
                self.navigation_bar.previous_card['state'] = tk.DISABLED
                self.navigation_bar.previous_trick['state'] = tk.DISABLED
            elif self.trick_index <= 0:
                self.navigation_bar.previous_card['state'] = tk.NORMAL
                self.navigation_bar.previous_trick['state'] = tk.DISABLED
            else:
                self.navigation_bar.previous_card['state'] = tk.NORMAL
                self.navigation_bar.previous_trick['state'] = tk.NORMAL
        elif self.edit_mode :
            if len(self.new_record)==0:
                self.navigation_bar.previous_card['state'] = tk.DISABLED
                self.navigation_bar.previous_trick['state'] = tk.DISABLED
            elif len(self.new_record)==1:
                self.navigation_bar.previous_card['state'] = tk.NORMAL
                self.navigation_bar.previous_trick['state'] = tk.DISABLED
            else:
                self.navigation_bar.previous_card['state'] = tk.NORMAL
                self.navigation_bar.previous_trick['state'] = tk.NORMAL
                
    def check_buttons_availability(self):
        self.check_if_end_of_record()
        self.check_if_record_begining()

    def edit_play_record_from_current_state(self):
        if not self.play_record.record:
            return
        self.edit_mode = True
        self.new_record = self.play_record.record[:self.trick_index] if self.trick_index > 0 else [
        ]
        last_trick = Trick(self.current_trick.lead, cards={
                           self.current_trick[i][0]: self.current_trick[i][1] for i in range(self.card_index+1)})
        self.new_record.append(last_trick)
        self.master.edit_play_record_from_current_state()
        self.check_buttons_availability()

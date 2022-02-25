import logging
import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Dict, List, Optional
from Board import PlayerHand
from common_utils import Suit, Direction, Card, Rank
from UI import MAIN_FONT_STD, MAIN_FONT_SMALL,LIGHT_BLUE,DEFAULT_GREY

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Deal import FixedDealUI

class PlayerHandUI(tk.Frame):
    """Construct one hand of a diagramm"""

    def __init__(self, parent, hand: PlayerHand, name: Optional[str], direction: Direction) -> None:
        tk.Frame.__init__(self, parent, bg="white")
        self.player_hand = hand
        self.direction = direction
        self.his_turn = False
        self.master : FixedDealUI
        self.edit_mode: bool = False

        # Create the symbol label for each suit
        self.suit_symbol_labels = {suit: tk.Label(self, text=suit.symbol(
        ), fg=suit.color(), font=MAIN_FONT_STD, bg='white') for suit in Suit}

        # Create string variable for each suit
        self.suit_cards: Dict[Suit, tk.StringVar] = {}
        for suit in Suit:
            self.suit_cards[suit] = tk.StringVar(value="".join(
                card.abbreviation() for card in hand.suits[suit]))

        # Create each suit label
        self.suits_labels: Dict[Suit, tk.Label] = {suit: tk.Label(
            self, textvariable=self.suit_cards[suit], bg='white', font=MAIN_FONT_STD, width=10, anchor=tk.W) for suit in Suit}

        # Grid each suit
        for i, suit in enumerate(reversed(Suit)):
            self.suit_symbol_labels[suit].grid(
                row=i, column=0)
            self.suits_labels[suit].grid(row=i, column=1, sticky=tk.W)

        name_label_txt = f'{direction.abbreviation()} : {name if name is not None else "-"}'
        self.name_label = tk.Label(self, text=name_label_txt, width=25,
                                   font=MAIN_FONT_SMALL, background=DEFAULT_GREY, anchor=tk.W, padx=22)
        self.name_label.grid(row=4, column=0, columnspan=2)

        # Create buttons
        self.buttons_dicts: Dict[Suit, SuitButtons] = {}
        for i, suit in enumerate(reversed(Suit)):
            self.buttons_dicts[suit] = SuitButtons(
                self, self.player_hand.suits[suit], suit)

    def play_a_card(self, card: Card):
        if self.edit_mode and not self.his_turn :
            messagebox.showerror(message=f'It is not {self.direction.to_str()} to play !')
            return
        current_state = self.suit_cards[card.suit].get()
        if card.rank.abbreviation() not in current_state:
            if card in self.player_hand.cards:
                logging.error(
                    f'{card.__str__()} not anymore in {self.direction.to_str()} hand - invalid play record')
                messagebox.showerror(
                    f'{card.__str__()} not anymore in {self.direction.to_str()} hand - invalid play record')
            else:
                logging.error(
                    f'{card.__str__()} not in {self.direction.to_str()} hand - invalid play record')
                messagebox.showerror(
                    f'{card.__str__()} not in {self.direction.to_str()} hand - invalid play record')
            return

        current_state = current_state.replace(card.rank.abbreviation(), '')
        self.suit_cards[card.suit].set(current_state)
        self.end_of_turn()

        if self.edit_mode :
            self.master.display_a_card(self.direction,card)

    def give_back_a_card(self, card: Card):
        current_state = self.suit_cards[card.suit].get()
        if card.rank.abbreviation() in current_state:
            logging.error(
                f"{card.__str__()} already in {self.direction.to_str()} hand - can't be given back")
            messagebox.showerror(
                f"{card.__str__()} already in {self.direction.to_str()} hand - can't be given back")
            return
        new_state_list: List[Rank] = [card.rank]
        for c in current_state:
            new_state_list.append(Rank.from_str(c))
        new_state_list.sort(reverse=True)
        self.suit_cards[card.suit].set(
            ("".join(rank.__str__() for rank in new_state_list)))

    def switch_to_edit_mode(self):
        self.edit_mode = True
        for i, suit in enumerate(reversed(Suit)):
            self.suits_labels[suit].grid_forget()
            self.buttons_dicts[suit].grid(row=i, column=1, sticky=tk.W)

    def has_to_play(self,suit_played : Optional[Suit]) :
        self.his_turn=True
        self.name_label.config(bg=LIGHT_BLUE,fg='white')
        for suit,button_list in self.buttons_dicts.items() :
            button_list.disable_all_buttons()
            if suit_played is None or suit == suit_played or self.suit_cards[suit_played].get()=='':
                button_list.enable_not_played([Rank.from_str(c) for c in self.suit_cards[suit].get()])

    def end_of_turn(self) :
        self.his_turn=False
        self.name_label.config(bg=DEFAULT_GREY)
        for button_list in self.buttons_dicts.values():
            button_list.disable_all_buttons()

    def switch_color(self, color_hexa : str) :
        self.config(bg=color_hexa)
        for label in self.suit_symbol_labels.values() :
            label.config(bg=color_hexa)
        for label in self.suits_labels.values() :
            label.config(bg=color_hexa)
        for suit_buttons in self.buttons_dicts.values() :
            for button in suit_buttons.buttons_list.values() :
                button.config(bg=color_hexa)

class SuitButtons(tk.Frame):
    def __init__(self, parent, hand: List[Rank], suit: Suit) -> None:
        tk.Frame.__init__(self, parent)
        self.buttons_list: Dict[Rank, tk.Button] = {}
        self.suit = suit
        self.master: PlayerHandUI
        for j, rank in enumerate(hand):
            self.buttons_list[rank] = tk.Button(self, text=rank.abbreviation(
            ), command=lambda rank=rank : self.play_card(rank),font=MAIN_FONT_STD,bg='white',border=0)
            self.buttons_list[rank].grid(row=0, column=j+1, sticky=tk.W)

    def play_card(self, rank: Rank):
        self.master.play_a_card(Card(self.suit, rank))

    def disable_button(self, rank: Rank):
        self.buttons_list[rank].config(state=tk.DISABLED)

    def disable_all_buttons(self) :
        for button in self.buttons_list.values() :
            button.config(state=tk.DISABLED)

    def enable_not_played(self,not_played_ranks : List[Rank]) : 
        for rank,button in self.buttons_list.items() :
            if rank in not_played_ranks :
                button.config(state=tk.NORMAL)
    
    def enable_all_buttons(self) :
        for button in self.buttons_list.values() :
            button.config(state=tk.NORMAL)

    def enable_button(self, rank: Rank):
        self.buttons_list[rank].config(state=tk.NORMAL)

import logging
import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Dict, List, Optional
from Board import PlayerHand
from common_utils import Suit, Direction, Card,Rank
from UI import MAIN_FONT_STD,MAIN_FONT_SMALL


class FixedPlayerHandUI(tk.Frame):
    """Construct one hand of a diagramm"""

    def __init__(self, parent, hand: PlayerHand, name: Optional[str], direction: Direction) -> None:
        tk.Frame.__init__(self, parent, bg="white")
        self.player_hand = hand
        self.direction = direction

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
            self.suits_labels[suit].grid(row=i, column=1,sticky=tk.W)

        name_label_txt = f'{direction.abbreviation()} : {name if name is not None else "-"}'
        self.name_label = tk.Label(self, text=name_label_txt, width=25, font=MAIN_FONT_SMALL, background='#D3D3D3', anchor=tk.W, padx=22)
        self.name_label.grid(row=4, column=0, columnspan=2)

    def play_a_card(self, card: Card):
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

    def give_back_a_card(self, card: Card):
        current_state = self.suit_cards[card.suit].get()
        if card.rank.abbreviation() in current_state:
            logging.error(
                f"{card.__str__()} already in {self.direction.to_str()} hand - can't be given back")
            messagebox.showerror(
                f"{card.__str__()} already in {self.direction.to_str()} hand - can't be given back")
            return
        new_state_list : List[Rank]=[card.rank]
        for c in current_state :
            new_state_list.append(Rank.from_str(c))
        new_state_list.sort(reverse=True)
        self.suit_cards[card.suit].set(("".join(rank.__str__() for rank in new_state_list)))

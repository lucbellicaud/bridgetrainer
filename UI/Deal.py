import tkinter as tk
from typing import Optional,Dict
from Board import Deal, DealRecord, Sequence
from common_utils.utils import Direction,Card, Suit
from UI import MAIN_FONT_SMALL,MAIN_FONT_HUGE,position_dict,ColorDic
from .PlayRecord import PlayRecordUI
from .Hand import PlayerHandUI
from .FinalContract import FinalContractUI
from .Sequence import BiddingSequenceUI




class FixedDealUI(tk.Frame):
    def __init__(self, parent, deal: Deal, deal_record: Optional[DealRecord]) -> None:
        tk.Frame.__init__(self, parent)
        diag = deal.diag
        self.deal = deal
        self.diag = diag
        self.deal_record = deal_record
        self.handsUI : Dict[Direction,PlayerHandUI] = {dir:PlayerHandUI(self,diag.hands[dir],deal_record.names[dir] if deal_record and deal_record.names and dir in deal_record.names else None, dir) for dir in Direction}
        self.handsUI[deal.dealer].has_to_play(None)
        for dir in Direction :
            self.handsUI[dir].grid(
                row=position_dict[dir][0], column=position_dict[dir][1])

        self.vul_and_board = VulAndBoardNumberUI(
            self, deal.dealer, deal.ns_vulnerable, deal.ew_vulnerable, deal.board_number)
        self.vul_and_board.grid(row=0, column=0)

        if self.deal_record and self.deal_record.sequence is not None:
            self.sequence = BiddingSequenceUI(
                self, self.deal_record.sequence, deal.dealer, deal.ns_vulnerable, deal.ew_vulnerable)
            self.sequence.grid(row=1, column=1, padx=10)
            if self.deal_record.sequence.final_contract is not None:
                self.final_contract = FinalContractUI(
                    self, self.deal_record.sequence.final_contract, self.deal_record.play_record.tricks if self.deal_record.play_record else None, self.deal_record.score)
                self.final_contract.grid(row=0, column=2)
            if self.deal_record.play_record is not None and self.deal_record.play_record.record is not None and self.deal_record.sequence and self.deal_record.sequence.final_contract and self.deal_record.sequence.final_contract.bid:
                self.play_record = PlayRecordUI(self, self.deal_record.play_record,self.deal_record.sequence.final_contract.bid.suit)
                self.button_to_play_record = tk.Button(self,text="Play record",command=self.display_play_record,font=MAIN_FONT_SMALL)
            else :
                self.button_to_play_record = tk.Button(self,text="Create play record",font=MAIN_FONT_SMALL)
            self.button_to_play_record.grid(row=2,column=2)

        else:
            self.sequence_bouton = tk.Button(
                self, text="Add a bidding sequence", command=self.create_sequence, bg="white", font=MAIN_FONT_SMALL)
            self.sequence_bouton.grid(row=1, column=1, padx=10)

    def create_sequence(self):
        self.sequence = BiddingSequenceUI(
            self, Sequence([], None), self.deal.dealer, self.deal.ns_vulnerable, self.deal.ew_vulnerable)
        self.sequence.grid(row=1, column=1, padx=10)
        self.sequence_bouton.destroy()

    def display_play_record(self) :
        self.sequence.grid_forget()
        self.play_record .grid(row=1, column=1,sticky='s')

    def play_a_card(self,dir : Direction,card : Card) :
        self.handsUI[dir].play_a_card(card)

    def give_back_a_card(self,dir : Direction, card : Card) :
        self.handsUI[dir].give_back_a_card(card)

    def display_a_card(self,dir : Direction, card : Card) :
        self.play_record.display_next_card(card,dir)

    def edit_play_record_from_current_state(self) :
        for dir in Direction :
            self.handsUI[dir].switch_to_edit_mode()

    def has_to_play(self, dir : Direction, suit : Optional[Suit]) :
        self.handsUI[dir].has_to_play(suit)
    
    def end_of_turn_for_everyone(self) :
        for dir in Direction :
            self.handsUI[dir].end_of_turn()

    


class VulAndBoardNumberUI(tk.Frame):
    """Visual for board number and vulnerability"""

    def __init__(self, parent, dealer: Direction, ns_vul: bool, ew_vul: bool, board_number: int):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, height=150, width=150)
        x0 = 5
        y0 = 5
        len_rec = 80
        width_rec = 20

        match dealer:
            case Direction.NORTH:
                self.dealer_p = (x0+width_rec+len_rec/2, y0+width_rec/2)
            case Direction.SOUTH:
                self.dealer_p = (x0+width_rec+len_rec/2,
                                 y0+3*width_rec/2+len_rec)
            case Direction.WEST:
                self.dealer_p = (x0+width_rec/2, y0+width_rec + len_rec/2)
            case Direction.EAST:
                self.dealer_p = (x0+3*width_rec/2+len_rec,
                                 y0+width_rec + len_rec/2)

        self.canvas.create_rectangle(
            x0+width_rec, y0, x0+len_rec+width_rec, y0+width_rec, fill=ColorDic[ns_vul])
        self.canvas.create_rectangle(x0+width_rec, y0+len_rec+width_rec, x0+len_rec +
                                     width_rec, y0+2*width_rec+len_rec, fill=ColorDic[ns_vul])
        self.canvas.create_rectangle(
            x0, y0+width_rec, x0+width_rec, y0+len_rec+width_rec, fill=ColorDic[ew_vul])
        self.canvas.create_rectangle(
            x0+width_rec, y0+width_rec, x0+width_rec+len_rec, y0+width_rec+len_rec, fill='white')
        self.canvas.create_rectangle(x0+len_rec+width_rec, y0+width_rec, x0+len_rec +
                                     2*width_rec, y0+len_rec+width_rec, fill=ColorDic[ew_vul])
        self.canvas.create_text(x0+width_rec+len_rec/2, y0+width_rec +
                                len_rec/2, font=MAIN_FONT_HUGE, text=str(board_number))
        self.canvas.create_text(self.dealer_p[0], self.dealer_p[1], font=MAIN_FONT_SMALL, text="D", fill="white")

        self.canvas.pack()

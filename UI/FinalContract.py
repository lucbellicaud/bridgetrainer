import tkinter as tk
from typing import Optional
from Board import FinalContract, Declaration
from UI import MAIN_FONT_BIG


class FinalContractUI(tk.Frame):
    def __init__(self, parent, final_contract: FinalContract, tricks = Optional[int], score = Optional[int]):
        tk.Frame.__init__(self, parent)
        self.font = MAIN_FONT_BIG
        self.final_contract = final_contract
        self.tricks = tricks
        self.score = score
        self.display_contract()
        self.display_declarer()
        self.display_tricks()

    def display_contract(self) -> None:
        if self.final_contract.bid:
            self.level_variable = tk.StringVar(
                self, value=str(self.final_contract.bid.level))
            self.level_label = tk.Label(
                self, textvariable=self.level_variable, font=self.font)
            self.level_label.grid(row=0, column=0, sticky=tk.E)

            self.suit_variable = tk.StringVar(
                self, value=self.final_contract.bid.suit.symbol())
            self.suit_label = tk.Label(
                self, textvariable=self.suit_variable, fg=self.final_contract.bid.suit.color(), font=self.font)
            self.suit_label.grid(row=0, column=1, sticky=tk.W)

            if self.final_contract.declaration != Declaration.PASS:
                self.double_variable = tk.StringVar(
                    self, value=self.final_contract.declaration.__str__())
                self.double_label = tk.Label(
                    self, textvariable=self.double_variable, fg=self.final_contract.declaration.color(), font=self.font)
                self.double_label.grid(row=0, column=2, sticky=tk.W)

        else:
            self.level_variable = tk.StringVar(
                self, value='Pass')
            self.level_label = tk.Label(
                self, textvariable=self.level_variable, font=self.font)
            self.level_label.grid(row=0, column=0, sticky=tk.E)

    def display_declarer(self) -> None :
        if self.final_contract.declarer is not None :
            self.declarer_variable = tk.StringVar(
                self, value=self.final_contract.declarer.to_str())
            self.declarer_label = tk.Label(
                self, textvariable=self.declarer_variable, font=self.font)
            self.declarer_label.grid(row=1, column=0,columnspan=3)

    def display_tricks(self) -> None : 
        if self.tricks is not None and self.score is not None and self.final_contract.bid :
            self.tricks_variable = tk.StringVar(
                self, value=str(self.score)) 
            self.tricks_label = tk.Label(
                self, textvariable=self.tricks_variable, font=self.font)
            self.tricks_label.grid(row=2, column=0,columnspan=3)


    
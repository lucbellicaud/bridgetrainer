import logging
import tkinter as tk
from UI.Deal import FixedDealUI
from Board import PlayerHand, Diag, Deal, SetOfPairsBoard
import os
script_dir = os.path.dirname(__file__)


logging.basicConfig(filename='bridgetrainer.log', level=logging.INFO)

root = tk.Tk()
set_1 = SetOfPairsBoard.from_pbn(
     os.path.join(script_dir,"Boards\\Pbns\\41284.pbn"))
dealUI = FixedDealUI(
    root, set_1.boards[0].deal, set_1.boards[0].main_deal_record)
dealUI.pack()

root.mainloop()

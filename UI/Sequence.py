import tkinter as tk
from typing import List
from Board import Sequence,SequenceAtom,FinalContract
from UI import MAIN_FONT_STD_BOLD,MAIN_FONT_STD,ColorDic
from common_utils.utils import Direction
from .Tooltip import ToolTip

class BiddingSequenceUI(tk.Frame):
    """Represents a bidding sequence"""

    def __init__(self, parent, sequence : Sequence, dealer : Direction, ns_vul : bool, ew_vul : bool):
        tk.Frame.__init__(self, parent)
        self.width = 8
        self.sequence=sequence
        self.text_variables: List[tk.StringVar] = []
        self.entry_list: List[BidUI] = []
        self.current_index = 0
        self.init_top(dealer,ns_vul,ew_vul)
        if not sequence.sequence :
            for i in range(4) :
                self.append()
                self.text_variables[-1].set("") 
        for atom in sequence.sequence:
            self.append()
            self.text_variables[-1].set(atom.bid.__str__() if atom.bid else atom.declaration.__str__())

    def init_top(self, dealer : Direction,ns_vul : bool, ew_vul : bool):
        i = dealer.value
        for i, pos in enumerate(self.rotate(i, [dir for dir in Direction])):
            if Direction.NORTH or Direction.SOUTH:
                lab = tk.Label(
                    self, text=pos.abbreviation(), background=ColorDic[ns_vul], borderwidth=1, relief="ridge",fg='White',font=MAIN_FONT_STD_BOLD)
                lab.grid(row=0, column=i, sticky="ew", pady=2)
            else:
                lab = tk.Label(
                    self, text=pos.abbreviation(), background=ColorDic[ew_vul], borderwidth=1, relief="ridge",fg='White',font=MAIN_FONT_STD_BOLD)
                lab.grid(row=0, column=i, sticky="ew", pady=2)

    def append(self, alert=""):
        self.text_variables.append(tk.StringVar(self))
        entry = BidUI(self, textvariable=self.text_variables[-1], index=len(
            self.entry_list), alert=alert, width=self.width)
        self.entry_list.append(entry)
        entry.grid(row=1+(len(self.entry_list)-1)//4,
                   column=(len(self.entry_list)-1) % 4)

    def focus_next_widget(self, event):
        self.current_index += 1
        if self.current_index == len(self.entry_list):
            self.append()
        self.focus_with_index(self.current_index)
        return("break")

    def focus_previous_widget(self, event):
        if self.current_index != 0:
            self.current_index -= 1
            if self.current_index == len(self.entry_list):
                self.append()
            self.focus_with_index(self.current_index)
        return("break")

    def up(self, event):
        if self.current_index//4 != 0:
            self.current_index -= 4
            self.focus_with_index(self.current_index)
        return("break")

    def down(self, event):
        if self.current_index <= len(self.entry_list)-4:
            self.current_index += 4
            self.focus_with_index(self.current_index)
        return("break")

    def on_click(self, event):
        self.current_index = event.widget.index

    def rotate(self, rotato: int, liste: list):
        for i in range(rotato):
            liste.insert(0, liste.pop())
        return liste

    def focus_with_index(self, i: int):
        self.entry_list[i].focus()
        self.entry_list[i].select_range(0, 'end')

    def write_alert(self, event):
        event.widget.configure(state='disabled')
        textalert = tk.StringVar(self, value=event.widget.alert)
        alert = tk.Entry(self, textvariable=textalert)
        alert.index = event.widget.index
        alert.grid(row=2+(len(self.entry_list)//4), column=0, columnspan=4)
        alert.focus()
        alert.bind("<Return>", self.return_alert)
        alert.bind("<FocusOut>", self.return_alert)

    def return_alert(self, event):
        self.entry_list[event.widget.index].configure(state='normal')
        self.entry_list[event.widget.index].set_alert(event.widget.get())
        self.entry_list[self.current_index].focus()
        event.widget.destroy()


class BidUI(tk.Entry):
    def __init__(self, parent, textvariable, index, alert, width):
        tk.Entry.__init__(
            self, parent, textvariable=textvariable, justify='center',width=width,font=MAIN_FONT_STD)
        self.index = index
        self.alert = alert
        self.set_alert(alert)
        self.refresh_tooltip()
        self.bind("<Tab>", parent.focus_next_widget)
        self.bind("<Shift-Tab>", parent.focus_previous_widget)
        self.bind("<Right>", parent.focus_next_widget)
        self.bind("<Left>", parent.focus_previous_widget)
        self.bind("<Up>", parent.up)
        self.bind("<Down>", parent.down)
        self.bind("<Button-1>", parent.on_click)
        self.bind('a', parent.write_alert)

    def set_alert(self, alert: str):
        if not alert:
            return
        self.alert = alert
        self.refresh_tooltip()
        self.config({"background": "Yellow"})

    def refresh_tooltip(self):
        if self.alert:
            self.tooltip = ToolTip(self, self.alert)
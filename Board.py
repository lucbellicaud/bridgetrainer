from dataclasses import dataclass, field
from Séquence import Sequence,FinalContract
from Hand import Diagramm
import os
from Parameters import MAIN_REPERTORY
from ast import literal_eval
from ddstable import ddstable

PBN_TO_LIN_VUL = {'None' : "0", "NS" : "N", "EW" : "E", "All" : "B"}
LIN_DEALER_DICT = {'S' : str(1),'O' : str(2), 'N' : str(3), 'E' : str(4)}

@dataclass
class Board() :
    """A board contains a diagramm and two sequences : one made by the user and one made by the teacher"""
    """Should board number, vul and dealer be here ?"""
    diag : Diagramm = field(init=False)
    sequence_user : Sequence = field(init=False)
    sequence_correction : Sequence = field(init=False)
    points_scale : dict = field(default_factory=list)
    title : str = ""
    board_number : int = 0
    vul : str = "" # "None" "NS" "EW" "All"
    dealer : str = "" # in N,S,W,E


    def init_from_pbn (self,board_str : str) : #return self
        """read one pbn board and return it"""
        for line in board_str.split("\n") :
            if 'Board' in line :
                self.set_board_number(int(line.split('"')[1]))
            if 'Vul' in line :
                self.set_vul(line.split('"')[1])
            if 'Dealer ' in line :
                self.set_dealer(line.split('"')[1])
            if 'Deal ' in line :
                deal = line.replace("Deal ","")
                self.set_diagramm(Diagramm().init_from_string(deal,self.get_dealer()))
            if 'Exercice Title' in line :
                self.set_title(line.split('"')[1])
            if 'Points Scale' in line :
                self.set_points_scale(self.dictionnarize_string(line.split('{')[1].split('}')[0]))
            if 'User Sequence' in line :
                self.set_sequence_user(Sequence().append_multiple_from_string(line.split('"')[1]))
            if 'Correction Sequence' in line :
                self.set_sequence_correction(Sequence().append_multiple_from_string(line.split('"')[1]))
        return self

    def is_valid(self) -> bool :
        if self.get_board_number() == 0 or  self.get_vul() == "" or self.get_dealer() == "" :
            return False
        if self.get_diagramm().is_valid() == False :
            PbnError(f"Invalid diagramm on board {self.board_number}")
            return False
        return True


    def __str__(self) :
        return str(self.get_board_number())

    def dictionnarize_string(self,s : str) -> dict :
        dict = {}
        for step in s.split(",") :
            dict[FinalContract().init_from_string(step.split(":")[0])]=int(step.split(":")[1])
        return dict

    def print_as_lin(self) :
        """Print as in a .lin file"""
        string = "qx|o%d|md|" % (self.get_board_number())
        string += LIN_DEALER_DICT[self.get_dealer()]
        string += self.get_diagramm().print_as_lin()
        string += '|rh||ah|Board %d|sv|%s|pg||' %(self.get_board_number(), PBN_TO_LIN_VUL[self.get_vul()])
        return string

    def print_as_pbn(self) :
        """print as in a .pbn file"""
        return self.get_diagramm().print_as_pbn()

    """set and get"""
    def get_board_number(self) -> int :
        return int(self.board_number)

    def set_board_number(self, board_number : int) -> None :
        self.board_number = board_number

    def get_vul(self) -> str :
        return self.vul

    def set_vul(self, vul : str) -> None :
        self.vul = vul

    def get_title(self) -> str :
        return self.title

    def set_title(self, title : str) -> None :
        self.title = title

    def get_dealer(self) -> str :
        return self.dealer

    def set_points_scale(self, dict : dict) -> None :
        self.points_scale = dict

    def get_points_scale(self) -> dict :
        return self.points_scale

    def set_dealer(self, dealer : str) -> None :
        self.dealer = dealer

    def set_sequence_user(self,sq : Sequence) -> None :
        self.sequence_user = sq

    def set_sequence_correction(self,sq : Sequence) -> None :
        self.sequence_correction = sq

    def set_diagramm(self,diag : Diagramm) -> None :
        self.diag = diag

    def get_sequence_user(self) -> Sequence :
        return self.sequence_user

    def get_sequence_correction(self) -> Sequence :
        return self.sequence_correction

    def get_diagramm(self) -> Diagramm :
        return self.diag
    """set and get end"""

@dataclass
class SetOfBoards() :
    """List of boards"""
    boards : list[Board] = field(default_factory=list)
    title : str = ""
    date : str = ""

    def init_from_pbn(self,file) -> None :
        """open a file given its name and return the set of boards included"""
        os.chdir(MAIN_REPERTORY+'/Pbns')
        with open (file,'r') as f :
            list_of_boards = f.read().split("\n\n")
            at_the_head = list_of_boards[0].split("\n")

            if  "<Main infos>" in at_the_head : #in the head infos
                for line in at_the_head :
                    if 'Title' in line :
                        self.set_title(line.split('"')[1])
                    if 'Date' in line :
                        self.set_date(line.split('"')[1])
                    if "</Main infos>" in line :
                        break
                list_of_boards = list_of_boards[1:]

            for board_str in list_of_boards :
                board = Board()
                board.init_from_pbn(board_str)
                if board.is_valid() :
                    self.append(board) #read and add each bords

    def __str__(self) :
        string = ""
        string += "Title : " + self.get_title() +"\nDate : " + self.get_date() +"\n"
        for board in self.get_boards() :
            string += board.__str__() +"\n"
        return string

    def get_title (self)-> str :
        return self.title
    def get_date (self) -> str :
        return self.date
    def set_title (self, title : str) -> None :
        self.title = title
    def set_date (self, date : str) -> None :
        self.date = date
    def get_boards(self) -> list[Board] :
        return self.boards
    def get_board_by_board_number (self, board_number : int) -> Board :
        for board in self.boards :
            if board.get_diagramm().get_board_number() == board_number :
                return board

    def print_as_lin(self) :
        #https://stackoverflow.com/questions/66663179/how-to-use-windows-file-explorer-to-select-and-return-a-directory-using-python
        os.chdir(MAIN_REPERTORY+'/CreatedLin')
        with open(self.get_title()+".lin",'w') as f :
            for board in self.get_boards() :
                f.write(board.print_as_lin()+"\n")
            

    def print_as_pbn(self) :
        #https://stackoverflow.com/questions/66663179/how-to-use-windows-file-explorer-to-select-and-return-a-directory-using-python
        os.chdir(MAIN_REPERTORY+'/CreatedPBN')
        with open(self.get_title()+".pbn",'w') as f :
            for board in self.get_boards() :
                f.write(board.print_as_pbn()+"\n")
            
    def append(self,board : Board) -> None :
        self.boards.append(board)

class PbnError(Exception):
    def __init__(self, value):
        self.value = value
        print("Pbn Error")
        print(value)
    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    # set_of_boards = SetOfBoards()
    # set_of_boards.init_from_pbn('DF1.pbn')
    # set_of_boards.print_as_pbn()

    PBN = b"E:QJT5432.T.6.QJ82 .J97543.K7532.94 87.A62.QJT4.AT75 AK96.KQ8.A98.K63"
    all = ddstable.get_ddstable(PBN)
    print("{:>5} {:>5} {:>5} {:>5} {:>5} {:>5}".format("", "S", "H", "D", "C", "NT"))
    # may use  card_suit=["C", "D", "H", "S", "NT"]
    for each in all.keys():
        print("{:>5}".format(each),end='')
        for suit in ddstable.dcardSuit:
            trick=all[each][suit]
            if trick>7:
                print(" {:5}".format(trick - 6),end='')
            else:
                print(" {:>5}".format("-"),end='')
        print("")

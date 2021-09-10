from dataclasses import dataclass, field
from Séquence import Sequence
from Hand import Diagramm
from Pbnreader import PbnReader

@dataclass
class Board() :
    """A board contains a diagramm and two sequences : one made by the user and one made by the teacher"""
    """Should board number, vul and dealer be here ?"""
    diag : Diagramm
    sequence_user : Sequence
    sequence_correction : Sequence
    """Optionnal ?"""

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

@dataclass
class SetOfBoards() :
    """List of boards"""
    boards : list[Board]
    title : str
    date : str #meilleur format ?

    def get_title (self)-> str :
        return self.title
    def get_date (self) -> str :
        return self.date
    def set_title (self, title : str) -> None :
        self.title = title
    def set_date (self, date : str) -> None :
        self.date = date
    def get_board (self, board_number : int) -> Board :
        for board in boards :
            if board.get_diagramm().get_board_number()=board_number :
                return board
    def append(self,board : Board) -> None :
        boards.append(board)







if __name__ == '__main__':
    pbn_reader = PbnReader()
    pbn_reader.open_file('Match4.pbn')

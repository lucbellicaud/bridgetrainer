import os
from Hand import Diagramm
from Parameters import MAIN_REPERTORY
from Board import Board,SetOfBoards

class PbnReader() :
    """This class reads pbns files"""
    def listfiles(self) :
        os.chdir(MAIN_REPERTORY+'/Pbns')
        for file in os.listdir() :
            #print(file)
            pass

    def open_file(self,file) -> SetOfBoards :
        """open a file given its name and return the set of boards included"""
        os.chdir(MAIN_REPERTORY+'/Pbns')
        title = ""
        set_of_boards = SetOfBoards()
        with open (file,'r') as f :
            list_of_boards = f.read().split("\n\n")
            for board_str in list_of_boards :
                set_of_boards.append(read_pbn_board(board_str)) #read and add each bords

        return set_of_boards


    def read_pbn_board(self,board_str : str) ->Board :
        """read one pbn board and return it"""
        for line in board_str.split("\n") :
            board_number = 0
            vul = "N"
            dealer ="None"
            if 'Board' in line :
                board_number = int(line.split('"')[1])
            if 'Vul' in line :
                vul = line.split('"')[1]
            if 'Dealer ' in line :
                dealer = line.split('"')[1]
            if 'Deal ' in line :
                deal = line.replace("Deal ","")
            if 'Exercice Title' in line :
                title = line.split('"')[1]
            if 'Points Scale' in line :
                """possible de dictionnariser un string ?"""
            if 'User Sequence' in line :
                """To do"""
            if 'Correction Sequence' in line :
                """To do"""

        diag = Diagramm(deal, board_number, vul, dealer)
        print(diag)


if __name__ == '__main__':
    pbnreader=PbnReader()
    pbnreader.listfiles()
    pbnreader.open_file('Match4.pbn')

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




if __name__ == '__main__':
    pbnreader=PbnReader()
    pbnreader.listfiles()
    pbnreader.open_file('Match4.pbn')

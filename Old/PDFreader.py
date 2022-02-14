from Old.Board import SetOfBoards
from Parameters import MAIN_REPERTORY

import fitz
import os
import shutil
from Hand import Hand,Diagramm
from Consts import PDF_TO_PBN_DEALER
from Old.Board import Board,SetOfBoards

VUL_TRAD={'Personne' : "None", "NS" : "NS", "EO" : "EW", "Tous" : "All"}

def readPDF(path) -> SetOfBoards :
    doc = fitz.open(path)
    set_of_boards = SetOfBoards()
    set_of_boards.set_title(path)
    set_of_boards.set_date("01/10")
    for i,page in enumerate(doc) :
        pdftext = page.get_text()
        if 'DONNE' in pdftext :
            board = Board()
            board.set_diagramm(get_hands(pdftext,page))
            board.set_dealer(PDF_TO_PBN_DEALER[pdftext[pdftext.find('Donneur : ')+len('Donneur : ')]])
            board.set_vul(VUL_TRAD[pdftext[pdftext.find('Vulnérabilité : ')+len('Vulnérabilité : ') : pdftext.find('\n',pdftext.find('Vulnérabilité : ')+len('Vulnérabilité : '))]])
            board.set_board_number(pdftext[pdftext.find('DONNE N°')+len('DONNE N°') : pdftext.find('\n',pdftext.find('DONNE N°')+len('DONNE N°'))])
            set_of_boards.append(board)
    return set_of_boards

def get_hands(pdftext,page : int) -> Diagramm :
    cursor = 0
    diag = Diagramm()
    diag.west,cursor = get_hand(pdftext,cursor)
    diag.east,cursor = get_hand(pdftext,cursor)
    diag.north,cursor = get_hand(pdftext,cursor)
    diag.south,cursor = get_hand(pdftext,cursor)
    
    return diag
    
def get_hand(pdftext : str,begining :int=0) : # return cursor and hand
    symbole_pique = pdftext.find('♠',begining)
    symbole_coeur = pdftext.find('♥',begining)
    symbole_carreau = pdftext.find('♦',begining)
    symbole_trèfle = pdftext.find('♣',begining)
    fin_de_la_main = pdftext.find('\n',symbole_trèfle)

    pique = angliciser(pdftext[symbole_pique+2:symbole_coeur])
    coeur = angliciser(pdftext[symbole_coeur+2:symbole_carreau])
    carreau = angliciser(pdftext[symbole_carreau+2:symbole_trèfle])
    trèfle = angliciser(pdftext[symbole_trèfle+2:fin_de_la_main])
    return Hand().create_from_string(pique+'.'+coeur+'.'+carreau+'.'+trèfle),fin_de_la_main

def angliciser(string : str) -> str :
    string = string.replace('R','K')
    string = string.replace('D','Q')
    string = string.replace('V','J')
    string = string.replace('10','T')
    string = string.replace(' ','')
    string = string.replace('\n','')
    return string

def convert_all_pdfs_to_lin() :
    """Convert all the pdfs in New PDFS folder into lin files"""
    os.chdir(MAIN_REPERTORY+'/New PDFS')
    for file in os.listdir() :
        print(file)
        set_of_boards = readPDF(file)
        set_of_boards.print_as_lin()
        os.chdir(MAIN_REPERTORY+'/New PDFS')
    file_names = os.listdir()
    
    for file_name in file_names:
        shutil.move(os.path.join(MAIN_REPERTORY+'/New PDFS', file_name), MAIN_REPERTORY+'/Old PDFS')

if __name__ == '__main__':
    convert_all_pdfs_to_lin()


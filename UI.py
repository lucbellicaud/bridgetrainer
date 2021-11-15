import tkinter as tk
from abc import ABC,abstractmethod
import os
from Board import Board,SetOfBoards
from Hand import Diagramm, Hand
from Parameters import MAIN_REPERTORY

menubar_options = ["Play","File","Parameters"]

class MenuOptions(ABC) :
    def __init__(self) :
        #root.clear()
        self.__post_init__()

    def clear():
        list = root.grid_slaves()
        for l in list:
            l.destroy()

    @abstractmethod
    def __post_init__(self) :
        pass

class Play(MenuOptions) :
    def __post_init__(self) :
        os.chdir(MAIN_REPERTORY+'/Pbns')
        
        liste = [x for x in os.listdir() if x.endswith(".pbn")]

        self.set_of_boards = tk.StringVar(root,"Chose your set of boards")
        list_of_set_of_boards = tk.OptionMenu(root, self.set_of_boards,*liste)
        list_of_set_of_boards.grid(column=0,row=0)

        self.position = tk.StringVar(root,"Chose your position")
        list_of_position = tk.OptionMenu(root,self.position, "South","North")
        list_of_position.grid(column=0,row=1)

class SetofBoardsUI(tk.Frame) :
    """Navigate trought the set of boards"""
    def __init__(self, parent, set_of_boards : SetOfBoards) -> None:
        tk.Frame.__init__(self, parent)
        self.board_index = 0
        self.current_board = set_of_boards.get_boards()[self.board_index]
        self.boardUI = BoardEditUI(self,self.current_board)
        self.boardUI.grid(row=0,column=0)

        self.navigation = SetOfBoardsNavigation(self)
        self.navigation.grid(row=1, column=0)

        self.pack()

    def save(self) : 
        """Save the board as a pbn in the file indicated"""
        print("save")
        print(self.board_index)
        
class SetOfBoardsNavigation(tk.Frame) :
    """Navigate trought the set of boards"""
    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.previous_board = tk.Button(self, text=" < ")
        self.save = tk.Button(self, text= "Save", command=parent.save)
        self.next_board = tk.Button(self, text=" > ")

        self.previous_board.grid(column=0,row=0)
        self.save.grid(column=1,row=0)
        self.next_board.grid(column=2,row=0)



class BoardEditUI(tk.Frame) :
    """Main class of the board : contains all the sub elements"""
    def __init__(self, parent, board : Board) -> None:
        tk.Frame.__init__(self, parent)
        
        self.diag = DiagrammEditUI(self,board.get_diagramm())
        self.save_options = BoardOptionsUI(self)

        self.diag.grid(row=0,column=0)
        self.save_options.grid(row=0,column=1)
        


class DiagrammEditUI(tk.Frame) :
    """Interact with a board"""
    def __init__(self, parent, diag : Diagramm) -> None:
        tk.Frame.__init__(self, parent)
        self.north = HandEditUI(self, diag.north,2,0)
        self.north.grid(row=0,column=1)
        self.south = HandEditUI(self,diag.south,2,9)
        self.south.grid(row=2,column=1)
        self.west = HandEditUI(self, diag.west,0,5)
        self.west.grid(row=1,column=2)
        self.east = HandEditUI(self, diag.east,4,5)
        self.east.grid(row=1,column=0)

class HandEditUI(tk.Frame) :
    """Construct one hand of a diagramm"""
    def __init__(self, parent, hand : Hand,col : int, line : int) -> None:
        tk.Frame.__init__(self, parent)

        self.spadelabel = tk.Label(parent,text='♠')
        self.heartlabel = tk.Label(parent,text='♥')
        self.diamondlabel = tk.Label(parent,text='♦')
        self.clublabel = tk.Label(parent,text='♥')
        self.spadelabel.grid(column=col, row=line)
        self.heartlabel.grid(column=col, row=line+1)
        self.diamondlabel.grid(column=col, row=line+2)
        self.clublabel.grid(column=col, row=line+3)

        self.spadestext = tk.StringVar(value= hand.get_spades_as_text())
        self.heartstext = tk.StringVar(value=hand.get_hearts_as_text())
        self.diamondstext = tk.StringVar(value=hand.get_diamonds_as_text())
        self.clubstext = tk.StringVar(value=hand.get_clubs_as_text())

        self.spades = tk.Entry(parent, textvariable=self.spadestext)
        self.spades.grid(column=col+1, row=line+0)
        self.hearts = tk.Entry(parent, textvariable=self.heartstext)
        self.hearts.grid(column=col+1, row=line+1)
        self.diamonds = tk.Entry(parent, textvariable=self.diamondstext)
        self.diamonds.grid(column=col+1, row=line+2)
        self.clubs = tk.Entry(parent, textvariable=self.clubstext)
        self.clubs.grid(column=col+1, row=line+3)

class BoardOptionsUI(tk.Frame) :
    """Options to save a board"""
    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        os.chdir(MAIN_REPERTORY+'/Board type')      
        liste = [x for x in os.listdir()]
        self.text_chose_where_to_save = tk.StringVar(self,"Type of the board")
        self.where_to_save = tk.OptionMenu(self, self.text_chose_where_to_save,*liste)

        self.text_difficulty_level = tk.StringVar(self,"Difficulty level")
        self.difficulty_level = tk.OptionMenu(self,self.text_difficulty_level,"None","Easy","Inter","Hard","Expert")

        self.comment_label=tk.Label(self, text="Comment")
        self.comment = tk.Text(self,height=3, width=20)


        self.where_to_save.grid(column=0,row=0,sticky="w")
        self.difficulty_level.grid(column=0, row=1,sticky="w")
        self.comment_label.grid(column=0,row=2,sticky="w")
        self.comment.grid(column=0,row=3,sticky="w")




if __name__ == '__main__':
    set_of_boards2 = SetOfBoards()
    fichier = 'MAIN NUMÉRO 1 BURN.LIN'
    set_of_boards2.init_from_lin(fichier)
    set_of_boards2.print_as_pbn()
    my_board = set_of_boards2.get_board_by_board_number(1)
    root = tk.Tk()
    play = SetofBoardsUI(root, set_of_boards2)
    root.mainloop()


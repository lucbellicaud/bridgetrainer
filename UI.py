import tkinter as tk
from abc import ABC,abstractmethod
import os
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
        

root = tk.Tk()
play = Play()


root.mainloop()
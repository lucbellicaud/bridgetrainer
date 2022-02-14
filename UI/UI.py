import tkinter as tk
import tkinter.messagebox as messagebox
from UI.Tooltip import ToolTip
from abc import ABC,abstractmethod
import os
from Old.Board import Board,SetOfBoards
from Hand import Diagramm, Hand
from Parameters import MAIN_REPERTORY
from Séquence import Sequence
from Consts import POSITIONS

class SetofBoardsUI(tk.Frame) :
    """Navigate trought the set of boards"""
    def __init__(self, parent, set_of_boards : SetOfBoards) -> None:
        tk.Frame.__init__(self, parent)
        self.set_of_boards = set_of_boards
        self.board_index = 0
        self.current_board = self.set_of_boards.get_board_by_index(self.board_index)
        self.length_of_set = len(self.set_of_boards.get_boards())
        self.boardUI = BoardEditUI(self,self.current_board)
        self.boardUI.grid(row=0,column=0)

        self.navigation = SetOfBoardsNavigation(self)
        self.navigation.grid(row=1, column=0)

        self.pack()

    def save(self) : 
        """Save the board as a pbn in the file indicated"""
        file = self.boardUI.save_options.text_chose_where_to_save.get()
        if file == "Type of the board" :
            messagebox.showerror(title="error",message="Please chose a place to save the board")
            return
        level = self.boardUI.save_options.text_difficulty_level.get()
        if level=="Difficulty level" :
            level = "None"

        board = Board()
        board.set_title(self.set_of_boards.get_title())
        board.set_dealer(self.current_board.get_dealer())
        board.set_vul(self.current_board.get_vul())
        board.set_board_number(self.current_board.get_board_number())
        board.set_comment(self.boardUI.save_options.comment.get("1.0","end-1c"))
        board.set_level(level)
        board.set_diagramm(Diagramm().init_from_pbn(self.boardUI.get_diagramm_as_pbn(), board.get_dealer()))

        if not board.is_valid() :
            messagebox.showerror(title="error",message="Invalid board")
            return

        os.chdir(MAIN_REPERTORY+'/Board type')
        with open(file,'a', encoding="utf-8") as f :
            f.write(board.print_as_pbn())

    def refresh(self) :
        self.boardUI = BoardEditUI(self,self.current_board)
        self.boardUI.grid(row=0,column=0)

    def next(self) : 
        if self.board_index+1==self.length_of_set :
            messagebox.showerror(title="error",message="This was the last board of the set")
            return

        self.board_index+=1
        self.current_board = self.set_of_boards.get_board_by_index(self.board_index)
        self.refresh()

    def previous(self) :
        if self.board_index==0 :
            messagebox.showerror(title="error",message="This is the first board of the set")
            return 

        self.board_index-=1
        self.current_board = self.set_of_boards.get_board_by_index(self.board_index)
        self.refresh()  
        
class SetOfBoardsNavigation(tk.Frame) :
    """Navigate trought the set of boards"""
    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.previous_board = tk.Button(self, text=" < ", command=parent.previous)
        self.save = tk.Button(self, text= "Save", command=parent.save)
        self.next_board = tk.Button(self, text=" > ",command=parent.next)

        self.previous_board.grid(column=0,row=0)
        self.save.grid(column=1,row=0)
        self.next_board.grid(column=2,row=0)



class BoardEditUI(tk.Frame) :
    """Main class of the board : contains all the sub elements"""
    def __init__(self, parent, board : Board) -> None:
        tk.Frame.__init__(self, parent)
        
        self.diag = DiagrammEditUI(self,board.get_diagramm(),board.get_board_number(),board.get_vul(),board.get_dealer())
        self.save_options = BoardOptionsUI(self)

        self.diag.grid(row=0,column=0)
        self.save_options.grid(row=0,column=1)

    def get_diagramm_as_pbn(self) -> str :
        return self.diag.get_as_pbn()
        
class VulAndBoardNumberUI(tk.Frame) :
    """Visual for board number and vulnerability"""
    def __init__(self,parent, board_number : int, vul : str, dealer : str) :
        tk.Frame.__init__(self, parent)
        self.canvas=tk.Canvas(self, height = 70, width = 70)
        x0 = 5
        y0 = 5
        len_rec = 40
        width_rec = 10
        match vul :
            case "NS" :
                self.vulNS='red'
                self.vulEW='green'
            case "EW" :
                self.vulNS='green'
                self.vulEW='red'
            case "All" :
                self.vulNS='red'
                self.vulEW='red'
            case _ :
                self.vulNS='green'
                self.vulEW='green'

        match dealer :
            case "N" :
                self.dealer_p=(x0+width_rec+len_rec/2,y0+width_rec/2)
            case "S" :
                self.dealer_p=(x0+width_rec+len_rec/2,y0+3*width_rec/2+len_rec)
            case "W" :
                self.dealer_p=(x0+width_rec/2,y0+width_rec + len_rec/2)
            case "E" :
                self.dealer_p=(x0+3*width_rec/2+len_rec,y0+width_rec + len_rec/2)
        
        self.canvas.create_rectangle(x0+width_rec,y0,x0+len_rec+width_rec,y0+width_rec,fill=self.vulNS)
        self.canvas.create_rectangle(x0+width_rec,y0+len_rec+width_rec,x0+len_rec+width_rec,y0+2*width_rec+len_rec,fill=self.vulNS)
        self.canvas.create_rectangle(x0,y0+width_rec,x0+width_rec,y0+len_rec+width_rec,fill=self.vulEW)
        self.canvas.create_rectangle(x0+len_rec+width_rec,y0+width_rec,x0+len_rec+2*width_rec,y0+len_rec+width_rec,fill=self.vulEW)
        self.canvas.create_text(x0+width_rec+len_rec/2,y0+width_rec+len_rec/2,font=("Purisa", 20),text=str(board_number))
        self.canvas.create_text(self.dealer_p[0],self.dealer_p[1],font=("Purisa", 8),text="D",fill="white")

        self.canvas.pack()
        



class DiagrammEditUI(tk.Frame) :
    """Interact with a board"""
    def __init__(self, parent, diag : Diagramm,board_number : int, vul : str, dealer : str) -> None:
        tk.Frame.__init__(self, parent)
        self.north = HandEditUI(self, diag.north,2,0)
        self.north.grid(row=0,column=1)
        self.south = HandEditUI(self,diag.south,2,9)
        self.south.grid(row=2,column=1)
        self.west = HandEditUI(self, diag.west,0,5)
        self.west.grid(row=1,column=2)
        self.east = HandEditUI(self, diag.east,4,5)
        self.east.grid(row=1,column=0)
        self.vul_and_board = VulAndBoardNumberUI(self,board_number,vul,dealer)
        self.vul_and_board.grid(row=0,column=0,rowspan=4,columnspan=2)

    def get_as_pbn(self) -> str :
        "E:K985.J54.AJ92.T4 AQT632.K7.K4.Q62 J74.T93.75.AJ975 .AQ862.QT863.K83"
        string ='"S:'
        for player in [self.south,self.west,self.north,self.east] :
            for suit in [player.spadestext,player.heartstext,player.diamondstext,player.clubstext] :
                string += suit.get()
                string +='.'
            string = string[:-1]+" "
        print(string[:-1]+'"')
        return string+'"'

class HandEditUI(tk.Frame) :
    """Construct one hand of a diagramm"""
    def __init__(self, parent, hand : Hand,col : int, line : int) -> None:
        tk.Frame.__init__(self, parent)

        self.spadelabel = tk.Label(parent,text='♠')
        self.heartlabel = tk.Label(parent,text='♥')
        self.diamondlabel = tk.Label(parent,text='♦')
        self.clublabel = tk.Label(parent,text='♣')
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

class BiddingSequenceUI(tk.Frame) :
    """Represents a bidding sequence"""
    def __init__(self,parent,dealer :str,vul :str,bidding_seq : Sequence) :
        self.height=1
        self.width=17
        tk.Frame.__init__(self, parent)
        self.text_variables=[]
        self.entry_list=[]
        self.current_index=0
        self.init_top(dealer,vul)
        for i,bid_atom in enumerate(bidding_seq.get_sequence()) :
            self.append(bid_atom.description)
            self.text_variables[-1].set(bid_atom.__str__())
        self.pack()

    def init_top(self,dealer :str,vul :str) :
        i=0
        if dealer == "N" :
            pass
        if dealer == "E" :
            i=1
        if dealer == "S" :
            i=2
        if dealer == "W" :
            i=3
        dic={}
        match vul :
                case "NS" :
                    dic["NS"]="red"
                    dic["EW"]="green"
                case "All" :
                    dic["NS"]="red"
                    dic["EW"]="red"
                case "None" :
                    dic["NS"]="green"
                    dic["EW"]="green"
                case "EW" :
                    dic["NS"]="red"
                    dic["EW"]="red"

        for i,pos in enumerate(self.rotate(i,POSITIONS)):
            if pos=="N" or pos=="S" :
                lab = tk.Label(self,text=pos,background=dic["NS"],borderwidth=1,relief="ridge")
                lab.grid(row=0,column=i,sticky="ew",pady=2)
            else :
                lab = tk.Label(self,text=pos,background=dic["EW"],borderwidth=1,relief="ridge")
                lab.grid(row=0,column=i,sticky="ew",pady=2)

    def append(self,alert="") :
        self.text_variables.append(tk.StringVar(self))
        entry = BidUI(self,textvariable=self.text_variables[-1],index=len(self.entry_list),alert=alert,width=self.width,height=self.height)
        self.entry_list.append(entry)
        entry.grid(row=1+(len(self.entry_list)-1)//4, column=(len(self.entry_list)-1)%4)

    def focus_next_widget(self,event):
        self.current_index+=1
        if self.current_index == len(self.entry_list) :
            self.append()
        self.focus_with_index(self.current_index)
        return("break")

    def focus_previous_widget(self,event):
        if self.current_index!=0 :
            self.current_index-=1
            if self.current_index == len(self.entry_list) :
                self.append()
            self.focus_with_index(self.current_index)
        return("break")

    def up(self,event) :
        if self.current_index//4!=0 :
            self.current_index-=4
            self.focus_with_index(self.current_index)
        return("break")

    def down(self,event) :
        if self.current_index<=len(self.entry_list)-4 :
            self.current_index+=4
            self.focus_with_index(self.current_index)
        return("break")

    def on_click(self,event) :
        self.current_index=event.widget.index

    def rotate(self, rotato : int,liste : list) :
        for i in range(rotato) :
            liste.insert(0, liste.pop())
        return liste

    def focus_with_index(self,i : int) :
        self.entry_list[i].focus()
        self.entry_list[i].select_range(0, 'end')

    def write_alert(self,event) :
        event.widget.configure(state='disabled')
        textalert = tk.StringVar(self,value=event.widget.alert)
        alert=tk.Entry(self,textvariable=textalert)
        alert.index=event.widget.index
        alert.grid(row=2+(len(self.entry_list)//4),column=0,columnspan=4)
        alert.focus()
        alert.bind("<Return>",self.return_alert)
        alert.bind("<FocusOut>", self.return_alert)

    def return_alert(self,event) :
        self.entry_list[event.widget.index].configure(state='normal')
        self.entry_list[event.widget.index].set_alert(event.widget.get())
        self.entry_list[self.current_index].focus()
        event.widget.destroy()

class BidUI(tk.Entry) :
    def __init__(self,parent,textvariable,index,alert,width,height) :
        tk.Entry.__init__(self, parent,textvariable = textvariable, justify='center')
        self.place(width=width,height=height)
        self.index=index
        self.alert=alert
        self.set_alert(alert)
        self.refresh_tooltip()
        self.bind("<Tab>", parent.focus_next_widget)
        self.bind("<Shift-Tab>", parent.focus_previous_widget)
        self.bind("<Right>", parent.focus_next_widget)
        self.bind("<Left>", parent.focus_previous_widget)
        self.bind("<Up>",parent.up)
        self.bind("<Down>",parent.down)
        self.bind("<Button-1>",parent.on_click)
        self.bind('a',parent.write_alert)

    def set_alert(self,alert : str) :
        if not alert :
            return
        self.alert=alert
        self.refresh_tooltip()
        self.config({"background": "Yellow"})
    
    def refresh_tooltip(self) :
        if self.alert :
            self.tooltip=ToolTip(self,self.alert)

    

if __name__ == '__main__':
    set_of_boards2 = SetOfBoards()
    fichier = 'test.LIN'
    set_of_boards2.init_from_lin(fichier)
    set_of_boards2.print_as_pbn()
    my_board = set_of_boards2.get_board_by_board_number(1)
    seq = Sequence()
    seq.append_multiple_from_string('P,P,P,1C,X,2C,X,XX,3C')
    seq.print_as_pbn()
    seq.sequence[0].description="test"
    root = tk.Tk()
    root.title(string='Bridgetrainer')
    # play = SetofBoardsUI(root, set_of_boards2)
    play=BiddingSequenceUI(root,"S","All",seq)
    root.mainloop()


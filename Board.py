from dataclasses import dataclass, field
from Séquence import Sequence,FinalContract,Bid,ErrorBid
from Hand import Diagramm
import os
from Parameters import MAIN_REPERTORY
#from ddstable import ddstable
from Consts import PBN_TO_LIN_VUL,LIN_DEALER_DICT,LIN_TO_PBN_DEALER,LIN_TO_PBN_VUL,BID_SUITS,LEVELS, CONTRACTS
from functions_for_par import pretty_print_dds,ordonner_joueurs,return_if_vul,maximum,calculate_bridge_score
from statistics import mean,median, stdev
from time import time,sleep

class PbnError(Exception):
    def __init__(self, value):
        self.value = value
        print("Pbn Error")
        print(value)
    def __str__(self):
        return repr(self.value)

@dataclass
class Board() :
    """A board contains a diagramm and two sequences : one made by the user and one made by the teacher"""
    """Should board number, vul and dealer be here ?"""
    diag : Diagramm = field(init=False)
    sequence_user : Sequence = field(init=False)
    sequence_correction : Sequence = field(init=False)
    points_scale : dict = field(default_factory=list)
    title : str = ""
    comment : str = ""
    level : str = "" #None, Easy, Inter, Hard, Expert
    board_number : int = 0
    vul : str = "" # "None" "NS" "EW" "All"
    dealer : str = "" # in N,S,W,E
    dds_dic : dict = field(default_factory=list)
    par_contract : FinalContract = field(init=False)


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
            if "OptimumScore" in line :
                par = line.split('"')[1]
                par= int(par.split(";")[1])
                self.set_par_contract(FinalContract(None,"P","",par))
        if self.get_vul()=="" :
            self.set_vul("None")
        return self

    def init_from_lin(self,line) : #return self
        
        self.set_board_number(int(line[line.find('o')+1:line.find(',')]))
        self.set_vul(LIN_TO_PBN_VUL[line[line.find('|sv|')+4:line.find('|sk|')]])
        line = line[line.find('|md|')+4:line.find('|sv|')] # Retourne les 4 jeux
        self.set_dealer(LIN_TO_PBN_DEALER[line[0]])
        line = line[1:]
        diag = Diagramm()
        self.set_diagramm(diag.init_from_lin(line,self.get_dealer()))
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

    def calculatePar(self) -> None :
        """Calculate the Par of the board""" # "None" "NS" "EW" "All"
        dic = {}
        joueurs = ordonner_joueurs(self.get_dealer())
        for joueur in joueurs :
            dic[joueur]={}
            vul = return_if_vul(joueur,self.get_vul())
            table_joueur = self.get_dds_dic()[joueur]
            for suit in BID_SUITS :
                dic[joueur][suit]=[]
                for level in CONTRACTS :
                    dic[joueur][suit].append(calculate_bridge_score(Bid(level,suit),table_joueur[suit],vul,joueur))
        self.set_par_contract(maximum (dic, joueurs, FinalContract(None,'P','',0)))
        #print(self.get_par_contract().get_bid(),self.get_par_contract().get_joueur(),self.get_par_contract().get_valeur())

    def print_as_lin(self) :
        """Print as in a .lin file"""
        string = "qx|o%d|md|" % (self.get_board_number())
        string += LIN_DEALER_DICT[self.get_dealer()]
        string += self.get_diagramm().print_as_lin()
        string += '|rh||ah|Board %d|sv|%s|pg||' %(self.get_board_number(), PBN_TO_LIN_VUL[self.get_vul()])
        return string

    def print_as_pbn(self) :
        """print as in a .pbn file"""
        string =""
        string += '[Title "{}"]\n'.format(self.get_title())
        string += '[Board "{}"]\n'.format(self.get_board_number())
        string += '[Vulnerable "{}"]\n'.format(self.get_vul())
        string += '[Deal "{}"]\n'.format(self.get_diagramm().print_as_pbn())
        string += '[Comment "{}"]\n'.format(self.get_comment())
        string += '[Level "{}"]\n'.format(self.get_level())

        #To do : correction seq etc
        return string+"\n"

    def write_on_pbn(self,file_name : str) :
        os.chdir(MAIN_REPERTORY+'/Board type')
        with open(file_name+".lin",'a', encoding="utf-8") as f :
            f.write(self.print_as_pbn())


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
    def get_par_contract(self) -> FinalContract :
        return self.par_contract
    def set_par_contract(self, final_contract : FinalContract) -> None :
        self.par_contract = final_contract
    def get_sequence_correction(self) -> Sequence :
        return self.sequence_correction
    def get_diagramm(self) -> Diagramm :
        return self.diag
    def get_dds_dic(self) -> dict :
        return self.dds_dic
    def set_dds_dic_with_NT_change(self, dic : dict) :
        for joueur in dic :
            dic[joueur]["N"] = dic[joueur].pop("NT")
        self.dds_dic = dic
    def set_dds_dic(self, dic : dict) -> None :
        self.dds_dic = dic
    def set_comment(self, comment : str) -> None :
        self.comment = comment
    def get_comment(self) -> str :
        return self.comment
    def set_level(self, level : str) -> None :
        self.level = level
    def get_level(self) -> str :
        return self.level
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
                    print(board.get_board_number())
                    self.append(board) #read and add each bords

    def init_from_lin (self,file) -> None :
        """open a file given its name and return the set of boards included"""
        os.chdir(MAIN_REPERTORY+'/New LIN')
        self.title = file
        with open (file,'r') as f :
            lines = f.read().split("\n")
            i=0
            for line in lines :
                if line[0:3]=='qx|' :
                    i+=1
                    board = Board()
                    board.init_from_lin(line)
                    self.append(board)

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
            if board.get_board_number() == board_number :
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
        with open(self.get_title()+".pbn",'w', encoding="utf-8") as f :
            for board in self.get_boards() :
                f.write('[Event "{}"]\n'.format(self.get_title()))
                f.write('[Date "{}"]\n'.format(self.get_date()))
                f.write(board.print_as_pbn()+"\n")
            
    def append(self,board : Board) -> None :
        self.boards.append(board)
    
    def set_dds_tables(self) :
        for i,board in enumerate(self.get_boards()) :
            board.set_dds_dic_with_NT_change(ddstable.get_ddstable(board.print_as_pbn().encode('utf-8')))


    def get_mean_par(self) -> int :
        par_list=[]
        for board in self.get_boards() :
            par_list.append(board.get_par_contract().get_valeur())
        return int(mean(par_list))

    def get_median_par(self) -> int :
        par_list=[]
        for board in self.get_boards() :
            par_list.append(board.get_par_contract().get_valeur())
        return int(median(par_list))

    def get_stddev_par(self) -> int :
        par_list=[]
        for board in self.get_boards() :
            par_list.append(board.get_par_contract().get_valeur())
        return int(stdev(par_list))

    def get_absolute_mean_par(self) : 
        par_list=[]
        for board in self.get_boards() :
            par_list.append(abs(board.get_par_contract().get_valeur()))
        return int(mean(par_list))

    def get_repartition_contrats(self) :
        dic = {"C":0,"D" :0,"H" : 0,"S" : 0, "N" : 0}
        total_len=0
        for board in self.get_boards() :
            dic [board.get_par_contract().get_bid().suit] +=1
            total_len+=1
        for suit in dic :
            print(suit, " : ", 100*dic[suit]/total_len,"%")

    def get_repartition_joueurs(self) :
        dic = {"EW" : 0, "NS" : 0}
        total_len=0
        for board in self.get_boards() :
            if board.get_par_contract().get_joueur() in "NS" :
                dic ["NS"] +=1
            elif board.get_par_contract().get_joueur() in "EW" :
                dic["EW"]+=1
            total_len+=1
        for suit in dic :
            print(suit, " : ", 100*dic[suit]/total_len,"%")


    def print_stats_par(self) -> None :
        print("Statistiques du par du fichier ", self.get_title())
        print("Moyenne du par : ",self.get_mean_par())
        print("Moyenne du par absolu :", self.get_absolute_mean_par())
        print("Médiane du par : ", self.get_median_par())
        print("Ecart type du par : ", self.get_stddev_par())
        print("Répartition des contrats :")
        self.get_repartition_contrats()
        self.get_repartition_joueurs()

    def init_pars(self) -> None :
        for board in self.get_boards() :
            board.calculatePar()


if __name__ == '__main__':
    # start = time()
    for fichier in ['MAIN NUMÉRO 1 BURN.LIN','MAIN NUMÉRO 2 BURN.LIN',"PIQUES ET COEURS INVERSÉS.LIN"] :
    # fichier ='test2.LIN'
        set_of_boards2 = SetOfBoards()
        set_of_boards2.init_from_lin(fichier)
        set_of_boards2.set_dds_tables()
        set_of_boards2.init_pars()
        set_of_boards2.print_stats_par()
    pass


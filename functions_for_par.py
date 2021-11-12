from Séquence import ErrorBid,FinalContract,Bid
from ddstable import ddstable
from Consts import *
from time import sleep

def return_if_vul (pos : str, vul : str) -> bool : # "None" "NS" "EW" "All"
    if pos=="N" or pos=="S" :
        if vul=="None" or vul =="EW" :
            return False
        else :
            return True
    elif pos=="W" or pos=="E" :
        if vul=="None" or vul=="NS":
            return False
        else :
            return True
    else :
        raise ErrorBid("Position invalide")

def ordonner_joueurs(dealer : str) -> list :
    joueurs = ['S','W','N','E']
    while dealer!=joueurs[0] :
        joueurs.insert(0,joueurs.pop())
    return joueurs

def is_better_score(nouveau_score : int,ancien_score : int,joueur : str) -> bool :
    if joueur=="N" or joueur=="S" :
        return nouveau_score>ancien_score
    else :
        return nouveau_score<ancien_score

def maximum (dic : dict, joueurs : list, old_f_contract : FinalContract) -> FinalContract :
    is_change=False
    for joueur in joueurs :
        for i in range(0,7) :
            for suit in BID_SUITS :
                new_f_contract = dic[joueur][suit][i]
                # print(new_f_contract,old_f_contract)
                # print("Ancien contrat :",old_f_contract.get_bid(),old_f_contract.get_valeur(), old_f_contract.get_joueur())
                # print("Nouveau contrat :",Bid(i+1,suit),new_f_contract,joueur)
                # print("C'est un meilleur score pour ",joueur,"?",is_better_score(new_f_contract,old_f_contract.get_valeur(),joueur))
                if is_better_score(new_f_contract.get_valeur(),old_f_contract.get_valeur(),joueur)  :
                    # print("Supérieur")
                    if (old_f_contract.get_bid()==None or new_f_contract.get_bid()>old_f_contract.get_bid() or (new_f_contract.get_bid()==old_f_contract.get_bid() and (joueurs.index(joueur)<joueurs.index(old_f_contract.get_joueur()) or same_line(old_f_contract.get_joueur(),new_f_contract.get_joueur())))) :
                        # print("Changement de contrat !")
                        # print("Ancien contract",old_f_contract)
                        # print("New contrat", new_f_contract)
                        """Si score supérieur et (score=passe ou enchère supérieure ou enchère égale et avant aux enchères"""
                        old_f_contract = new_f_contract
                        is_change = True
    if not is_change : # Après trois passes
        #print("Final contract : ", old_f_contract.get_valeur(), old_f_contract.get_bid(), old_f_contract.get_joueur())
        return old_f_contract
    return maximum (dic, joueurs, old_f_contract)

def pretty_print_dds(all : dict) -> None :
    print("{:>5} {:>5} {:>5} {:>5} {:>5} {:>5}".format("", "C", "D", "H", "S", "N"))
    for each in all.keys():
        print("{:>5}".format(each),end='')
        for suit in BID_SUITS:
            trick=all[each][suit]
            if trick>7:
                print(" {:5}".format(trick - 6),end='')
            else:
                print(" {:>5}".format("-"),end='')
        print("")

def calculate_bridge_score(bid : Bid, tricks : int, vul : bool,joueur : str) -> FinalContract : 
    """Knowing the contract and the number or tricks, return the bridge score (absolute negative = EW scores)"""
    PRIME_PARTIELLE = 50
    PRIME_MANCHE = 300
    PRIME_PETIT_CHELEM = 500
    PRIME_GRAND_CHELEM = 1000
    CHUTE = [100,300,500,800,1100,1400,1700,2000,2300,2600,2900,3200,3500]
    if vul :
        PRIME_MANCHE = 500
        PRIME_PETIT_CHELEM = 750
        PRIME_GRAND_CHELEM = 1500
        CHUTE = [200,500,800,1100,1400,1700,2000,2300,2600,2900,3200,3500,3800]
        
    if tricks >= bid.level + 6  :
        if bid.suit == "N" :
            score = 40 + 30 * (bid.level-1) 
        elif bid.suit == "S" or bid.suit == "H" :
            score = 30 * (bid.level) 
        elif bid.suit == "D" or bid.suit == "C" :
            score = 20 * (bid.level) 
        else :
            raise ErrorBid("Couleur de contrat invalide, il doit être C/D/H/S/N")
        #Ajout des primes
        if score >= 100 :
            score += PRIME_MANCHE
        else :
            score += PRIME_PARTIELLE
        if bid.level == 6 :
            score += PRIME_PETIT_CHELEM
        if bid.level == 7 :
            score += PRIME_GRAND_CHELEM
        #Ajout des surlevées
        if bid.suit == "S" or bid.suit == "H" or bid.suit == "N":
            score += (tricks - (bid.level + 6)) * 30
        elif bid.suit == "D" or bid.suit == "C" :
            score += (tricks - (bid.level + 6)) * 20  
        else :
            raise ErrorBid("Couleur de contrat invalide, il doit être C/D/H/S/N")

        if joueur =="N" or joueur == "S" :
            return FinalContract(bid,'P',joueur,score)
        else :
            return FinalContract(bid,'P',joueur,-score)

    else :
        if joueur =="N" or joueur == "S" :
            return FinalContract(bid,'X',joueur,-CHUTE[bid.level + 6 - tricks - 1]) 
        else :
            return FinalContract(bid,'X',joueur,CHUTE[bid.level + 6 - tricks - 1]) 

def same_line(joueur1 : str, joueur2 : str) :
    if (joueur1 and joueur2 in "NS") or (joueur1 and joueur2 in "EW") :
        return True
    return False
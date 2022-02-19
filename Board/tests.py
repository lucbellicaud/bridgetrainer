from .MP_Board import PairsBoard, SetOfPairsBoard
from common_utils import Direction

def test() :
#     play_record = PairsBoard.from_pbn("""
# [Event "BBO2-2015WBTC-BB"]
# [Site "F1"]
# [Board "8"]
# [West "KLUKOWSKI"]
# [North "UPMARK"]
# [East "GAWRYS"]
# [South "F NYSTROM"]
# [Room "Open"]
# [Scoring "IMP"]
# [Vulnerable "None"]
# [Dealer "W"]
# [Deal "W:AQ85432.3.KQJ.93 T7.QT876.8.QJT74 K9.AKJ9542.T7.62 J6..A965432.AK85"]
# {
#                    Nord
#                    X7
#                    DX876
#                    8
#                    DVX74
#   Ouest                            Est
#   AD85432                          R9
#   3                                ARV9542
#   RDV                              X7
#   93                               62
#                    Sud
#                    V6
#                    -
#                    A965432
#                    AR85
# }
# [Declarer "W"]
# [Contract "4SX"]
# [Result "9"]
# [Score "NS 100"]
# [Auction "W"]
# 1S    Pass  2H    3D
# 3S    Pass  4S    X
# Pass  Pass  Pass
# [Play "N"]
# H8 HA S6 H3
# D8 D7 DA DQ
# CQ C2 CK C9
# CJ C6 C5 C3
# *
# """)
#     print(play_record.print_as_pbn())

# ### Passe général ###

#     play_record_2 = PairsBoard.from_pbn(r"""
# [Event "Open /2 DN1 National Finale directe 21-22 - Séance 5"]
# [Site "Fédération Française de Bridge"]
# [Date "2022.02.06"]
# [Board "28"]
# [West ""]
# [North ""]
# [East ""]
# [South ""]
# [Dealer "W"]
# [Vulnerable "NS"]
# [Deal "W:J86.KJ75.A65.852 K7432.A6.42.QJ64 AT95.94.KT73.K97 Q.QT832.QJ98.AT3"]
# [Scoring "MatchPoints;MP1"]
# [Declarer ""]
# [Contract ""]
# [Result ""]
# [Competition "Pairs"]
# [EventDate "2022.01.22"]
# [Annotator "FFB - Christian BORDONNEAU"]
# [Application "Magic Contest France - Read more at www.brenning.se"]
# [ScoreTable "Table\2R;Round\2R;PairId_NS\2R;PairId_EW\2R;Contract\4L;Declarer\1R;Result\2R;Lead\3L;Score_NS\6R;Score_EW\6R;MP_NS\4R;MP_EW\4R;Percentage_NS\3R;Percentage_EW\3R"]
# 19 14  4 11 2HX  S  8 S6   "670"      - 42.0  0.0 100   0
# 16 14 14  1 2S   E  5 DQ   "150"      - 40.0  2.0  95   5
# 10 14 20 38 2H   S  9 DA   "140"      - 38.0  4.0  90  10
# 15 14 15 43 2H   S  8 S6   "110"      - 33.0  9.0  79  21
#  7 14 23 35 2H   S  8 C5   "110"      - 33.0  9.0  79  21
#  4 14 32 26 2H   S  8 C3   "110"      - 33.0  9.0  79  21
#  6 14 34 24 2H   S  8 C3   "110"      - 33.0  9.0  79  21
# 20 14  5 10 Pass -  - -      "0"      - 20.0 22.0  48  52
# 22 14  8  7 Pass -  - -      "0"      - 20.0 22.0  48  52
# 18 14 12  3 Pass -  - -      "0"      - 20.0 22.0  48  52
# 14 14 16 42 Pass -  - -      "0"      - 20.0 22.0  48  52
# 12 14 18 40 Pass -  - -      "0"      - 20.0 22.0  48  52
#  5 14 25 33 Pass -  - -      "0"      - 20.0 22.0  48  52
#  3 14 31 27 Pass -  - -      "0"      - 20.0 22.0  48  52
# 13 14 41 17 Pass -  - -      "0"      - 20.0 22.0  48  52
#  1 14 44 29 Pass -  - -      "0"      - 20.0 22.0  48  52
# 21 14  6  9 2H   S  7 D2       -  "100"  6.0 36.0  14  86
# 11 14 19 39 3C   N  8 D7       -  "100"  6.0 36.0  14  86
#  2 14 28 30 2H   S  7 C6       -  "100"  6.0 36.0  14  86
#  8 14 36 22 2C   S  7 C2       -  "100"  6.0 36.0  14  86
#  9 14 37 21 2H   S  7 C2       -  "100"  6.0 36.0  14  86
# 17 14 13  2 2N   N  5 S5       -  "300"  0.0 42.0   0 100
# [OptimumScore "NS 110"]
# [OptimumContract "2H N 8"]
# [OptimumResultTable "Declarer;Denomination\2R;Result\2R"]
# W  S  6
# W  H  5
# W  D  6
# W  C  5
# W NT  6
# N  S  7
# N  H  8
# N  D  7
# N  C  8
# N NT  7
# E  S  6
# E  H  5
# E  D  6
# E  C  5
# E NT  6
# S  S  7
# S  H  8
# S  D  7
# S  C  8
# S NT  6
# """)
#     print(play_record_2.print_as_pbn())
    set_1 = SetOfPairsBoard.from_pbn("C:\\Users\\lucbe\\OneDrive\\Documents\\Bridge\\bridgetrainer\\Boards\\Pbns\\open2dn1nationalfinaledirecte21-22-sance5.pbn")
    print(set_1.print_as_pbn())
    print(set_1.print_as_lin())
    # SetOfPairsBoard.from_FFB_pdf("C:/Users/lucbe/OneDrive/Documents/Bridge/bridgetrainer/Boards/Old PDFS/0000000FED2201202266464_donnes.pdf")
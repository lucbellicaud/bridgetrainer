from common_utils.utils import Direction
from .Board import PairsBoard
from common_utils import Direction

def test() :
    play_record = PairsBoard.from_pbn("""
[Event "BBO2-2015WBTC-BB"]
[Site "F1"]
[Board "8"]
[West "KLUKOWSKI"]
[North "UPMARK"]
[East "GAWRYS"]
[South "F NYSTROM"]
[Room "Open"]
[Scoring "IMP"]
[Vulnerable "None"]
[Dealer "W"]
[Deal "W:AQ85432.3.KQJ.93 T7.QT876.8.QJT74 K9.AKJ9542.T7.62 J6..A965432.AK85"]
{
                   Nord
                   X7
                   DX876
                   8
                   DVX74
  Ouest                            Est
  AD85432                          R9
  3                                ARV9542
  RDV                              X7
  93                               62
                   Sud
                   V6
                   -
                   A965432
                   AR85
}
[Declarer "W"]
[Contract "4SX"]
[Result "9"]
[Score "NS 100"]
[Auction "W"]
1S    Pass  2H    3D
3S    Pass  4S    X
Pass  Pass  Pass
[Play "N"]
H8 HA S6 H3
D8 D7 DA DQ
CQ C2 CK C9
CJ C6 C5 C3
*
""")
    print(play_record.print_as_pbn())

### Passe général ###

    play_record_2 = PairsBoard.from_pbn("""
[Event "BBO2-2015WBTC-BB"]
[Site "F1"]
[Board "8"]
[West "KLUKOWSKI"]
[North "UPMARK"]
[East "GAWRYS"]
[South "F NYSTROM"]
[Room "Open"]
[Scoring "IMP"]
[Vulnerable "None"]
[Dealer "W"]
[Deal "W:AQ85432.3.KQJ.93 T7.QT876.8.QJT74 K9.AKJ9542.T7.62 J6..A965432.AK85"]
{
                   Nord
                   X7
                   DX876
                   8
                   DVX74
  Ouest                            Est
  AD85432                          R9
  3                                ARV9542
  RDV                              X7
  93                               62
                   Sud
                   V6
                   -
                   A965432
                   AR85
}
[Contract "Pass"]
[Score "NS 0"]
[Auction "W"]
Pass  Pass  Pass Pass
*
[OtherScores "[Declarer "S"]
[Contract "5CX"]
[Result "8"]
[Score "NS -500"]
,
[Declarer "W"]
[Contract "4SX"]
[Result "8"]
[Score "NS 300"]
"]
""")
    print(play_record_2.print_as_pbn())
from common_utils.utils import Direction
from .Sequence import Sequence
from common_utils import Direction

def test() :
    seq= Sequence.from_pbn("""[Event "BBO2-2015WBTC-BB"]
    [Site "F1"]
    [Board "6"]
    [West "KLUKOWSKI"]
    [North "UPMARK"]
    [East "GAWRYS"]
    [South "F NYSTROM"]
    [Room "Open"]
    [Scoring "IMP"]
    [Vulnerable "EW"]
    [Dealer "E"]
    [Deal "E:Q65.KT765.A875.3 AKT7.Q2.KT3.KQ54 J9.A4.Q942.J8762 8432.J983.J6.AT9"]
    {
                    Nord
                    8432
                    V983
                    V6
                    AX9
    Ouest                            Est
    V9                               D65
    A4                               RX765
    D942                             A875
    V8762                            3
                    Sud
                    ARX7
                    D2
                    RX3
                    RD54
    }
    [Declarer "S"]
    [Contract "3S"]
    [Result "7"]
    [Score "NS -100"]
    [Auction "E"]
    Pass  1C  =1=    Pass  1D  =2=
    1H    X     P  2H
    Pass  2S    Pass  3S
    Pass  Pass  Pass
    [Note "1:16+"]
    [Note "2:0-4 zz (may be FG strength!)"]
    [Play "W"]
    HA H3 H6 H2""")
    print(seq)
    print(seq.is_valid(),seq.is_done())
    print(seq.print_as_lin())
    print(seq.print_as_pbn())
    print(seq.get_declarer(Direction.EAST))
    
from .PlayRecord import PlayRecord, Trick


def test():
    play_record = PlayRecord.from_pbn("""
[Event "BBO2-2015WBTC-BB"]
[Site "F1"]
[Board "3"]
[West "KLUKOWSKI"]
[North "UPMARK"]
[East "GAWRYS"]
[South "F NYSTROM"]
[Room "Open"]
[Scoring "IMP"]
[Vulnerable "EW"]
[Dealer "S"]
[Deal "S:QT8.J97.KQ8.AKJ8 AKJ.A532.AJ32.T3 532.T4.T974.Q754 9764.KQ86.65.962"]
{
                   Nord
                   532
                   X4
                   X974
                   D754
  Ouest                            Est
  ARV                              9764
  A532                             RD86
  AV32                             65
  X3                               962
                   Sud
                   DX8
                   V97
                   RD8
                   ARV8
}
[Declarer "S"]
[Contract "1NT"]
[Result "4"]
[Score "NS -150"]
[Auction "S"]
1NT   Pass  Pass  Pass
[Play "W"]
SA S2 S6 S8
H2 H4 HQ H7
SJ S3 S7 ST
SK S5 S9 SQ
H3 HT HK H9
D2 D4 S4 D8
HA C4 H6 HJ
H5 D7 H8 C8
DA D9 D5 DQ
*
""")
    print(play_record)

from common_utils import Rank, Suit, Direction,Card
from .PlayerHand import PlayerHand
from .Deal import Deal

def test() :
    """Hands tests"""
    """Classic hand"""
    card = Card(Suit.SPADES,Rank.QUEEN)
    player_hand = PlayerHand.from_cards([card, Card(Suit.SPADES,Rank.ACE), Card(Suit.SPADES,Rank.THREE),Card(Suit.SPADES,Rank.TWO),Card(Suit.SPADES,Rank.JACK),Card(Suit.HEARTS,Rank.QUEEN),Card(Suit.DIAMONDS,Rank.QUEEN),Card(Suit.CLUBS,Rank.QUEEN),Card(Suit.HEARTS,Rank.ACE),Card(Suit.DIAMONDS,Rank.ACE),Card(Suit.CLUBS,Rank.ACE),Card(Suit.CLUBS,Rank.EIGHT),Card(Suit.CLUBS,Rank.FOUR)])
    player_hand_string = PlayerHand.from_string_lists(["A","Q","J","2","3"],["A","Q"],["A","Q"],["A","Q","8","4"])
    player_hand_pbn = PlayerHand.from_pbn("AQJ32.AQ.AQ.AQ84")
    player_hand_lin = PlayerHand.from_lin("SAQJ32HAQDAQCAQ84")

    assert player_hand==player_hand_pbn==player_hand_lin==player_hand_string

    """Hand with void"""

    card = Card(Suit.SPADES,Rank.QUEEN)
    player_hand = PlayerHand.from_cards([card, Card(Suit.SPADES,Rank.ACE), Card(Suit.SPADES,Rank.THREE),Card(Suit.SPADES,Rank.TWO),Card(Suit.SPADES,Rank.JACK),Card(Suit.HEARTS,Rank.JACK),Card(Suit.HEARTS,Rank.QUEEN),Card(Suit.CLUBS,Rank.QUEEN),Card(Suit.HEARTS,Rank.FOUR),Card(Suit.HEARTS,Rank.ACE),Card(Suit.CLUBS,Rank.ACE),Card(Suit.CLUBS,Rank.EIGHT),Card(Suit.CLUBS,Rank.FOUR)])
    player_hand_string = PlayerHand.from_string_lists(["A","Q","J","2","3"],["A","Q","J","4"],[],["A","Q","8","4"])
    player_hand_pbn = PlayerHand.from_pbn("AQJ32.AQJ4..AQ84")
    player_hand_lin = PlayerHand.from_lin("SAQJ32HAQJ4DCAQ84")

    assert player_hand==player_hand_pbn
    assert player_hand_lin==player_hand_string

    deal_from_lin = Deal.init_from_lin('qx|o1|pn|chris3108,Clement84,FaresQLJB,rosqueeze|st||md|3S23H3QD236TC36TJQ,S6JH258JKD589C24A,S48TKH46TD7JC789K,|rh||ah|Board 1|sv|o|mb|p|mb|1S|mb|p|mb|1N|mb|p|mb|2N|an|FM|mb|p|mb|3D!|an|texas !h |mb|p|mb|4H|an|intÃ©rÃ©ssÃ©|mb|p|mb|p|mb|p|pc|CQ|pc|CA|pc|C9|pc|C5|pg||pc|SJ|pc|SK|pc|SA|pc|S3|pg||pc|HA|pc|H3|pc|H2|pc|H4|pg||pc|H7|pc|HQ|pc|HK|pc|H6|pg||pc|HJ|pc|HT|pc|H9|pc|C6|pg||pc|S6|pc|S4|pc|SQ|pc|S2|pg||pc|S5|pc|D6|pc|H5|pc|S8|pg||pc|D5|pc|D7|pc|DA|pc|D2|pg||pc|S7|pc|C3|pc|H8|pc|ST|pg||pc|D9|pc|DJ|pc|DK|pc|D3|pg||pc|S9|pc|DT|mc|13|pg||')
    deal_from_pbn = Deal.init_from_pbn("""
    [Event "BBO2-2015WBTC-BB"]
    [Site "F1"]
    [Board "3"]
    [West "SYLVAN"]
    [North "JASSEM"]
    [East "WRANG|"]
    [South "MAZURKIEWI"]
    [Room "Closed"]
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
    [Declarer "E"]
    [Contract "3H"]
    [Result "10"]
    [Score "NS -170"]
    [Auction "S"]
    1NT   X =1=      Pass  Pass
    2C    Pass  Pass  2H
    Pass  3H    Pass  Pass
    Pass
    [Note "1:strong"]
    [Play "S"]
    CA C3 C4 C6
    DK DA D4 D6
    CJ CT C7 C2
    DQ D2 DT D5
    D8 DJ D9 S4
    H7 HA H4 H6
    H9 H2 HT HK
    HJ H3 C5 HQ
    S8 SJ S2 S6
    *
    """)

    print(deal_from_lin)
    print(deal_from_lin.print_as_lin())
    print(deal_from_pbn.print_as_pbn())
    # deal_from_pbn.diag.calculate_DD_table()
from __future__ import annotations
from common_utils import Direction, Suit
from common_utils.parsing_tools import Pbn, Lin
from .Diag import Diag


class Deal:
    """
    A bridge deal consists of the dealer, the vulnerability of the teams, and the hands
    """

    def __init__(self, board_number: int, dealer: Direction, ns_vulnerable: bool, ew_vulnerable: bool, diag: Diag):
        self.dealer = dealer
        self.ns_vulnerable = ns_vulnerable
        self.ew_vulnerable = ew_vulnerable
        self.board_number = board_number
        self.diag = diag

    def __str__(self):
        string = ""
        string += "Dealer : " + self.dealer.name + "\n"
        if self.ns_vulnerable and self.ew_vulnerable:
            string += "Vul : Both\n"
        elif self.ns_vulnerable:
            string += "Vul : NS\n"
        elif self.ew_vulnerable:
            string += "Vul : EW\n"
        else:
            string += "Vul : None\n"

        string += self.diag.__str__()
        return string

    @staticmethod
    def init_from_pbn(data_string: str) -> Deal:
        """ Create a deal by parsing a pbn board'"""
        board_number = int(Pbn.get_tag_content(data_string, "Board"))
        ns_vulnerable, ew_vulnerable = Pbn.vul_from_string(
            Pbn.get_tag_content(data_string, "Vulnerable"))
        dealer = Direction.from_str(Pbn.get_tag_content(data_string, "Dealer"))
        diag_str = Pbn.get_tag_content(data_string, "Deal")
        return Deal(board_number, dealer, ns_vulnerable, ew_vulnerable, Diag.init_from_pbn(diag_str))

    @staticmethod
    def init_from_lin(data_string: str) -> Deal:
        """Create a deal by parsing a lin board : SK7HAQT632DK4CQ62,S82H98DAT632CKT43,S965HKJ5DQJ985CA5"""
        diag_str = Lin.get_tag_content(data_string, "md")
        ns_vulnerable, ew_vulnerable = Lin.vul_from_string(
            Lin.get_tag_content(data_string, "sv"))
        dealer = Lin.dealer_from_string(
            Lin.get_tag_content(data_string, "md")[0])
        board_number = int(Lin.get_tag_content(data_string, 'ah').split()[1])
        return Deal(board_number, dealer, ns_vulnerable, ew_vulnerable, Diag.init_from_lin(diag_str))

    def print_as_lin(self) -> str:
        string = ""
        string += "|md|" + \
            Lin.dealer_to_string(self.dealer) + self.diag.print_as_lin()
        string += "|ah|Board "+str(self.board_number)
        string += "|sv|" + \
            Lin.vul_to_string(self.ns_vulnerable, self.ew_vulnerable)
        return string

    def print_as_pbn(self) -> str:
        string = ""
        string += '[Dealer "'+self.dealer.abbreviation()+'"]\n'
        string += '[Vulnerable "' + \
            Pbn.vul_to_string(self.ns_vulnerable, self.ew_vulnerable)+'"]\n'
        string += '[Board "' + str(self.board_number)+'"]\n'
        string += self.diag.print_as_pbn() + "\n"
        return string


if __name__ == '__main__':
    pass

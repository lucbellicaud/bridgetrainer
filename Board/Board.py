from __future__ import annotations
from dataclasses import dataclass
from statistics import mean
from typing import List, Optional

from common_utils import Direction

from .DealRecord.PlayRecord.PlayRecord import PlayRecord
from .DealRecord.Sequence.SequenceAtom import FinalContract
from common_utils.parsing_tools import Pbn
from .DealRecord.DealRecord import DealRecord
from .Deal import Deal


@dataclass
class OtherResult:

    final_contract: Optional[FinalContract]
    tricks: Optional[int]
    score: int

    @staticmethod
    def from_pbn(string: str) -> Optional[List[OtherResult]]:
        """
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
        """
        text = Pbn.get_other_results(string)
        if not text :
            return None
        split_text = text.split(",")
        list: List[OtherResult] = []
        for board_txt in split_text:
            final_contract = FinalContract.from_pbn(board_txt)
            tricks = Pbn.get_tag_content(board_txt, "Result")
            tricks = int(tricks) if tricks else None
            score = Pbn.get_score(board_txt)
            if final_contract:
                list.append(OtherResult(
                    final_contract=final_contract, tricks=tricks, score=score))
        return list

    def print_as_pbn(self) -> str :
        string : str =""
        if self.final_contract :
            string+=self.final_contract.print_as_pbn()
        if self.tricks :
            string+=Pbn.print_tag("Result",str(self.tricks))
        string+= Pbn.print_tag("Score","NS "+str(self.score))
        return string


@dataclass
class PairsBoard:
    deal: Deal
    main_deal_record: DealRecord
    other_results: Optional[List[OtherResult]]
    percentage : Optional[float]


    @staticmethod
    def from_pbn(string: str) -> PairsBoard:
        deal = Deal.init_from_pbn(string)
        main_deal_reccord = DealRecord.from_pbn(string)
        other_results = OtherResult.from_pbn(string)
        percentage_txt = Pbn.get_tag_content(string,"Percentage")
        percentage = float(percentage_txt) if percentage_txt else None
        return PairsBoard(deal=deal,main_deal_record=main_deal_reccord,other_results=other_results,percentage=percentage)

    def calculate_percentage(self,dir : Direction) -> Optional[float] :
        scores : List[int] = [self.main_deal_record.score]
        if not self.other_results :
            return None
        for res in self.other_results :
            scores.append(res.score)
        percent_per_player = float(100)/len(scores)
        above = len([i for i in scores if i > self.main_deal_record.score])
        equal = len([i for i in scores if i == self.main_deal_record.score])-1
        return ((100 - above*percent_per_player)+((100 - above*percent_per_player)-equal*percent_per_player))/2
            
    def print_as_pbn(self) -> str :
        string : str =""
        string+=self.deal.print_as_pbn()
        string+=self.main_deal_record.print_as_pbn(dealer=self.deal.dealer,ns_vulnerable=self.deal.ns_vulnerable,ew_vulnerable=self.deal.ew_vulnerable)
        if self.other_results :
            string +='[OtherScores"'
            for result in self.other_results :
                string+=result.print_as_pbn()+",\n"
            string = string[:-2]+'\n"]\n'
        if self.percentage :
            string += str(self.percentage)
        return string

@dataclass
class SetOfPairsBoard() :
    date : Optional[str]
    titre : Optional[str]
    boards : List[PairsBoard]

    @staticmethod
    def from_pbn(string : str) -> SetOfPairsBoard :
        date = Pbn.get_tag_content(string,"Date")
        titre = Pbn.get_tag_content(string,"Event")
        raw_boards = string.split("\n\n")
        boards : List[PairsBoard] = [PairsBoard.from_pbn(board) for board in raw_boards]
        return SetOfPairsBoard(date,titre,boards)



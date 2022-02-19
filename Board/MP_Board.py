from __future__ import annotations
from dataclasses import dataclass
import datetime
from statistics import mean
from typing import Dict, List, Optional

import pandas
import re
import logging

from common_utils import Direction, Card

from .DealRecord.PlayRecord.PlayRecord import PlayRecord
from .DealRecord.Sequence.SequenceAtom import Declaration, FinalContract
from common_utils.parsing_tools import FFB_PDF, Pbn
from .DealRecord.DealRecord import DealRecord
from .Deal import Deal, Diag, PlayerHand
import fitz
import camelot


@dataclass
class OtherResult:

    final_contract: Optional[FinalContract]
    tricks: Optional[int]
    lead: Optional[Card]
    NS_Percentage: Optional[float]
    score: int

    @staticmethod
    def from_pbn(string: str) -> Optional[List[OtherResult]]:
        """
        """
        text = Pbn.get_content_under_tag(string, "ScoreTable")
        raw_titles = Pbn.get_tag_content(
            string, "ScoreTable").replace('\\', '/')
        if not text:
            return None
        column_titles = list(filter(None, re.split(
            '/.{1,3};?', raw_titles)))  # \\.{1,3};
        data = [list(filter(None, x.replace('"', '').split(" ")))
                for x in text.split("\n")]
        df = pandas.DataFrame(data, columns=column_titles)
        df.replace(to_replace='-', value='', inplace=True)
        return OtherResult.from_data_frame(df)

    @staticmethod
    def from_ffb_pdf(tables: List[pandas.DataFrame]) -> List[OtherResult]:
        df = pandas.DataFrame(columns=['Contract', 'Declarer', 'Lead',
                                       'Result', "Score_NS",  'Score_EW',  'Percentage_NS', 'Percentage_EW'])
        for table in tables:
            table.drop(index=table.index[0], axis=0, inplace=True)
            # Spaghetti incoming
            if len(table.columns) == 12:
                table.rename(columns={0: 'Contract', 1: 'Declarer', 2: 'Lead',
                                      3: 'Result', 5: "Score_NS", 7: 'Score_EW', 9: 'Percentage_NS', 11: 'Percentage_EW'}, inplace=True)
                table.drop([4, 6, 8, 10], inplace=True, axis=1)
            elif len(table.columns) == 11:
                if table[7].values[0] == '':  # Every score in EW
                    table.rename(columns={0: 'Contract', 1: 'Declarer', 2: 'Lead',
                                          3: 'Result', 5: "Score_NS", 7: 'Score_EW', 8: 'Percentage_NS', 10: 'Percentage_EW'}, inplace=True)
                    table.drop([4, 6, 9], inplace=True, axis=1)
                elif table[5].values[0] == '':  # Every score in NS
                    table.rename(columns={0: 'Contract', 1: 'Declarer', 2: 'Lead',
                                          3: 'Result', 4: "Score_NS", 6: 'Score_EW', 8: 'Percentage_NS', 10: 'Percentage_EW'}, inplace=True)
                    table.drop([5, 7, 9], inplace=True, axis=1)
                else:
                    logging.error('Unkown tab format')
            elif len(table.columns) == 10:
                if table[7].values[0] == '':  # Every score in EW
                    table.rename(columns={0: 'Contract', 1: 'Declarer', 2: 'Lead',
                                          3: 'Result', 5: "Score_NS", 7: 'Score_EW', 8: 'Percentage_NS', 9: 'Percentage_EW'}, inplace=True)
                    table.drop([4, 6], inplace=True, axis=1)
                elif table[5].values[0] == '':  # Every score in NS
                    table.rename(columns={0: 'Contract', 1: 'Declarer', 2: 'Lead',
                                          3: 'Result', 4: "Score_NS", 6: 'Score_EW', 8: 'Percentage_NS', 9: 'Percentage_EW'}, inplace=True)
                    table.drop([5, 7], inplace=True, axis=1)
            table['Lead'] = table['Lead'].apply(FFB_PDF.angliciser)
            table['Declarer'] = table['Declarer'].apply(FFB_PDF.angliciser)
            df = pandas.concat([df, table])
        return OtherResult.from_data_frame(df)

    @staticmethod
    def from_data_frame(df: pandas.DataFrame) -> List[OtherResult]:
        # print(df)
        result_list: List[OtherResult] = []
        for row in df.itertuples():
            if "M" in row.Score_NS or "M" in row.Score_EW or "A" in row.Score_NS or "A" in row.Score_EW:
                continue
            final_contract = FinalContract.from_str(row.Contract+row.Declarer)
            lead = Card.from_str(row.Lead) if row.Lead != '' else None
            tricks = int(0)
            if row.Result == "=" and final_contract.bid:
                tricks = final_contract.bid.level
            elif ("+" in row.Result or "-" in row.Result) and final_contract.bid:
                tricks = final_contract.bid.level+int(row.Result)
            else:
                tricks = int(row.Result) if row.Result != '' else None
            score_NS = int(0) if row.Score_NS == "" else int(row.Score_NS)
            score_EW = int(0) if row.Score_EW == "" else -int(row.Score_EW)
            score = score_NS+score_EW
            NS_Percentage = int(row.Percentage_NS)
            result_list.append(OtherResult(
                final_contract=final_contract, tricks=tricks, score=score, lead=lead, NS_Percentage=NS_Percentage))
        return result_list

    def print_as_pbn(self) -> str:
        string: str = ""
        if self.final_contract:
            string += f'{self.final_contract.print_pbn_abbrevation():>4} '
            string += self.final_contract.declarer.abbreviation()+" " if self.final_contract.declarer else "- "
            string += f'{str(self.tricks):>2} ' if self.tricks else " - "
        string += self.lead.to_pbn()+" " if self.lead else " - "
        string += '{:6s}   -    '.format('"'+str(self.score)+'"') if self.score>0 else '  -    {:6s} '.format('"'+str(self.score)+'"')
        string += f'{str(int(self.NS_Percentage)):>3} ' if self.NS_Percentage else "-   "
        string += f'{str(100-int(self.NS_Percentage)):>3} ' if self.NS_Percentage else "-   "
        return string


@dataclass
class PairsBoard:
    deal: Deal
    main_deal_record: Optional[DealRecord]
    other_results: Optional[List[OtherResult]]
    percentage: Optional[float]

    @staticmethod
    def from_pbn(string: str) -> PairsBoard:
        deal = Deal.init_from_pbn(string)
        main_deal_reccord = DealRecord.from_pbn(string)
        other_results = OtherResult.from_pbn(string)
        percentage_txt = Pbn.get_tag_content(string, "Percentage")
        percentage = float(percentage_txt) if percentage_txt else None
        logging.info(f'Fin du chargement de la donne {str(deal.board_number)}')
        return PairsBoard(deal=deal, main_deal_record=main_deal_reccord, other_results=other_results, percentage=percentage)

    @staticmethod
    def from_ffb_pdf(first_page: fitz.Page, tables: List[pandas.DataFrame]) -> PairsBoard:
        first_page_txt: str = first_page.get_text()
        hands_as_cards = FFB_PDF.get_hands(first_page_txt)
        ns_vul, ew_vul = FFB_PDF.get_vul(first_page_txt)
        dealer = FFB_PDF.get_dealer(first_page_txt)
        board_number = FFB_PDF.get_board_number(first_page_txt)
        other_results = OtherResult.from_ffb_pdf(tables)
        hands: Dict[Direction, PlayerHand] = {
            dir: PlayerHand.from_cards(hands_as_cards[dir]) for dir in Direction}
        
        deal = Deal(board_number=board_number, dealer=dealer,
                    ns_vulnerable=ns_vul, ew_vulnerable=ew_vul, diag=Diag(hands))
        return PairsBoard(deal=deal, main_deal_record=None, other_results=other_results, percentage=None)

    def calculate_percentage(self, dir: Direction) -> Optional[float]:
        if not self.main_deal_record:
            return None
        scores: List[int] = [self.main_deal_record.score]
        if not self.other_results:
            return None
        for res in self.other_results:
            scores.append(res.score)
        percent_per_player = float(100)/len(scores)
        above = len([i for i in scores if i > self.main_deal_record.score])
        equal = len([i for i in scores if i == self.main_deal_record.score])-1
        return ((100 - above*percent_per_player)+((100 - above*percent_per_player)-equal*percent_per_player))/2

    def print_as_pbn(self) -> str:
        string: str = ""
        string += self.deal.print_as_pbn()
        if self.main_deal_record:
            string += self.main_deal_record.print_as_pbn(
                dealer=self.deal.dealer, ns_vulnerable=self.deal.ns_vulnerable, ew_vulnerable=self.deal.ew_vulnerable)
        if self.other_results:
            string += r'[Scoretable "Contract\4L;Declarer\1R;Result\2R;Lead\3L;Score_NS\6R;Score_EW\6R;Percentage_NS\3R;Percentage_EW\3R'+"\n"
            for result in self.other_results:
                string += result.print_as_pbn()+"\n"
        if self.percentage:
            string += str(self.percentage)
        return string

    def print_as_lin(self) -> str :
        return self.deal.print_as_lin()+"|"




@dataclass
class SetOfPairsBoard():
    date: Optional[datetime.datetime]
    title: Optional[str]
    boards: List[PairsBoard]

    @staticmethod
    def from_pbn(path : str) -> SetOfPairsBoard:
        with open(path) as file :
            logging.info(f'Loading board from pbn')
            string = file.read()
            date = None
            try :
                date = datetime.datetime.strptime(Pbn.get_tag_content(string, "Date"),"%Y.%m.%d")
            except : pass
            title = Pbn.get_tag_content(string, "Event")
            raw_boards = string.split("\n\n")
            boards: List[PairsBoard] = [
                PairsBoard.from_pbn(board) for board in raw_boards]
            logging.info(f'Boards loaded from pbn')
            return SetOfPairsBoard(date, title, boards)
            

    @staticmethod
    def from_FFB_pdf(path: str) -> SetOfPairsBoard:
        with fitz.open(path) as doc:
            match_date = re.findall(r'(\d{2}/\d{2}/\d{4})',doc[0].get_text())
            title = re.split(r'/|\\',path)[-1].split(".")[0]
            date = datetime.datetime.strptime(match_date[0],"%d/%m/%Y") if match_date else None
            logging.info('Starting pdf extraction - could be long')
            boards_index = [x[2] for x in doc.get_toc()]
            boards_list : List[PairsBoard] = [] 
            for i, v in enumerate(boards_index):
                table_list: List[pandas.DataFrame] = []
                p = v
                table_list.append(camelot.read_pdf(
                    path, flavor="stream", pages=str(p))[0].df)
                while p+1 not in boards_index and p != len(doc):
                    table_list.append(camelot.read_pdf(
                        path, flavor="stream", pages=str(p))[0].df)
                boards_list.append(PairsBoard.from_ffb_pdf(first_page=doc[v-1], tables=table_list))
                logging.info(f'Board {v} out of {boards_index[-1]} loaded')
        return SetOfPairsBoard(date,title,boards_list)
            
    def print_as_pbn(self) -> str :
        string : str = ""
        if self.title is not None : string += Pbn.print_tag("Event",self.title) 
        if self.date is not None : string += Pbn.print_tag("Date",self.date.__str__())
        for board in self.boards :
            string += board.print_as_pbn()+"\n"
        return string

    def print_as_lin(self) -> str :
        return "\n".join([board.print_as_lin() for board in self.boards])
        
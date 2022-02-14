from __future__ import annotations
from typing import List, Tuple
from common_utils import Direction
import re


class Pbn:
    @staticmethod
    def get_tag_content(string: str, tag: str) -> str:
        tag = "["+tag+" "
        tag_pos = string.find(tag)
        if tag_pos == -1:
            return ""
        end_of_content = string[tag_pos:].find("]")
        return string[tag_pos:end_of_content+tag_pos].split('"')[1]

    @staticmethod
    def get_other_results(string: str) -> str:
        tag = "[OtherScores "
        tag_pos = string.find(tag)
        if tag_pos == -1:
            return ""
        string = string[tag_pos:]
        end_of_content = min(i for i in [string.find(']\n"]'), string.find(']"]')] if i > 0)
        return string[string[:end_of_content].find(""):string[:end_of_content].rfind("")+1]

    @staticmethod
    def get_score(string : str) -> int :
        score_txt = Pbn.get_tag_content(string, "Score")
        score = int(score_txt.split()[1])
        if score_txt.split()[0] == "EW":
            return -score
        return score

    @staticmethod
    def get_all_alerts(string: str) -> List[str]:
        list = []
        for alert in re.finditer("\[Note ", string):
            list.append((Pbn.get_tag_content(
                string[alert.start():], "Note")).split(":")[1])
        return list

    @staticmethod
    def get_sequence(string: str) -> str:
        auction_tag = string.find("[Auction ")
        string = string[auction_tag+1:]
        start = string.find("\n")
        end = min(i for i in [string.find(
            "["), string.find("*"), string.find("\n\n")] if i > 0)
        return string[start:end-1]

    @staticmethod
    def get_play_record(string: str) -> str:
        auction_tag = string.find("[Play ")
        string = string[auction_tag+1:]
        start = string.find("\n")
        end = min(i for i in [string.find(
            "["), string.find("*"), string.find("\n\n")] if i > 0)

        return string[start+1:end-1]

    @staticmethod
    def vul_from_string(string: str) -> Tuple[bool, bool]:
        """Return NS and EW vul from string : NS-> (True,False) """
        if string == "None":
            return (False, False)
        if string == "NS":
            return (True, False)
        if string == "EW":
            return (False, True)
        if string == "All":
            return (True, True)
        raise Exception("Vulnérabilité incorrecte")

    @staticmethod
    def vul_to_string(ns_vulnerable: bool, ew_vulnerable: bool) -> str:
        """Return NS and EW vul from string : NS-> (True,False) """
        if ns_vulnerable and ew_vulnerable:
            return "All"
        if ns_vulnerable:
            return "NS"
        if ew_vulnerable:
            return "EW"
        return "None"

    @staticmethod
    def direction_to_tag(dir: Direction) -> str:
        return dir.name.title()

    @staticmethod
    def print_tag(tag: str, content: str):
        return '['+tag+' "'+content+'"]\n'


class Lin:
    @staticmethod
    def get_tag_content(string: str, tag: str) -> str:
        tag = "|"+tag+"|"
        tag_pos = string.find(tag)+len(tag)
        end_of_content = string[tag_pos:].find("|")
        return string[tag_pos:end_of_content+tag_pos]

    @staticmethod
    def vul_from_string(string: str) -> Tuple[bool, bool]:
        if string == "o":
            return (False, False)
        if string == "n":
            return (True, False)
        if string == "e":
            return (False, True)
        if string == "b":
            return (True, True)
        raise Exception("Vulnérabilité incorrecte")

    @staticmethod
    def vul_to_string(ns_vulnerable: bool, ew_vulnerable: bool) -> str:
        """Return NS and EW vul from string : NS-> (True,False) """
        if ns_vulnerable and ew_vulnerable:
            return "b"
        if ns_vulnerable:
            return "n"
        if ew_vulnerable:
            return "e"
        return "o"

    @staticmethod
    def dealer_from_string(string: str) -> Direction:
        LIN_TO_PBN_DEALER = {"1": "S", "2": "W", "3": "N", "4": "E"}
        return Direction.from_str(LIN_TO_PBN_DEALER[string])

    @staticmethod
    def dealer_to_string(dir: Direction) -> str:
        LIN_TO_PBN_DEALER = {Direction.SOUTH: "1", Direction.WEST: "2",
                             Direction.NORTH: "3", Direction.EAST: "4"}
        return LIN_TO_PBN_DEALER[dir]

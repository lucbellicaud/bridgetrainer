from __future__ import annotations
from enum import Enum
from common_utils import Direction

position_dict = {
    Direction.NORTH : (0,1),
    Direction.SOUTH : (2,1),
    Direction.WEST : (1,0),
    Direction.EAST : (1,2)
}

MAIN_FONT_HUGE = ("Arial", 30)
MAIN_FONT_BIG  = ("Arial", 25)
MAIN_FONT_STD_BOLD = ("Arial", 20,"bold")
MAIN_FONT_STD = ("Arial", 20)
MAIN_FONT_SMALL = ("Arial", 13)

ColorDic = {
    True: "red",
    False: "green"
}

DEFAULT_GREY = '#D3D3D3'
LIGHT_BLUE = '#71BAFF'
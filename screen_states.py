# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:21:11 2019

@author: solar
"""

from enum import Enum, auto

class ScreenStates(Enum):
    MAIN_MENU = auto()
    UPDATE_SCORES = auto()
    ROLLOVER_SEASON = auto()
    FIRST_SETUP = auto()
    ADD_TOURN = auto()
    FIRST_TOURN = auto()
    UPDATE_TOP = auto()
    GOOGLE_SETUP = auto()
    EXIT_PROG = auto()
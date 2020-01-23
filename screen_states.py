# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:21:11 2019

@author: solar
"""

from enum import Enum, auto

class ScreenStates(Enum):
    MAIN_MENU = 0
    UPDATE_SCORES = 1
    ROLLOVER_SEASON = 2
    FIRST_SETUP = 3
    ADD_TOURN = 4
    FIRST_TOURN = 5
    UPDATE_TOP = 6
    GOOGLE_SETUP = 7
    EXIT_PROG = 8
    VALID_INPUT_ADD = 9
    INVALID_INPUT_ADD = 10
    VALID_INPUT_FIRST = 11
    INVALID_INPUT_FIRST = 12
    
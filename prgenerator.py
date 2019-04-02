# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:33:40 2019

@author: Kevin Hart
"""

import challonge

# Stuff for Challonge api access
challonge.set_credentials('solar0012', '45lR8Hsb08tm4F5J5Ps85FOGLtdx72XCnPaxxj8B')
tournament = challonge.tournaments.show('uz7g78vq')
matches = challonge.matches.index(tournament['id'])
participants = challonge.participants.index(tournament['id'])
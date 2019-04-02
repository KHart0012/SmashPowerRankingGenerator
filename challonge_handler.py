# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:46:55 2019

@author: Kevin Hart
"""

import challonge
from access_data import username, api_key

challonge.set_credentials(username, api_key)
tournament = challonge.tournaments.show('uz7g78vq')
matches = challonge.matches.index(tournament['id'])
participants = challonge.participants.index(tournament['id'])
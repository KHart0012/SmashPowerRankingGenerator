# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:33:40 2019

@author: Kevin Hart
"""

# Stuff for Challonge api access
import challonge
from access_data import username, api_key

challonge.set_credentials(username, api_key)
tournament = challonge.tournaments.show('uz7g78vq')
matches = challonge.matches.index(tournament['id'])
participants = challonge.participants.index(tournament['id'])

# Stuff for Google Cloud access

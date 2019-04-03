# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:46:11 2019

@author: Kevin Hart
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(creds)

pr = gc.open('Smash Ultimate Power Rankings').sheet1
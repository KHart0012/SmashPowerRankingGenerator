# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:33:40 2019

@author: Kevin Hart
"""

from challonge_handler import initialize_challonge, grab_scores
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from screen_states import ScreenStates

def first_time_run(tourn_str, top_cells):
    top = [cell.value for cell in top_cells]
    return grab_scores(tourn_str, top)

def updated_scores(tourn_str, cells, top_cells):
    prev_scores = grab_current_scores(cells)
    top = [cell.value for cell in top_cells]
    curr_scores = grab_scores(tourn_str, top)
    
    player_dict = dict()
    
    for i in range(len(prev_scores)):
        player_dict[prev_scores[i][0].lower()] = prev_scores[i][1]
    
    for i in range(len(curr_scores)):
        if curr_scores[i][0].lower() in player_dict.keys():
            player_dict[curr_scores[i][0].lower()] += curr_scores[i][1]
        else:
            player_dict[curr_scores[i][0].lower()] = curr_scores[i][1]
        
    return sorted(player_dict.items(), key=lambda x: x[1], reverse=True)
    

def grab_current_scores(cells):
    prev = []
    for i in range(2, len(cells)):
        prev.append((cells[i][1], int(cells[i][2])))
    return prev


def update_top(pr, top_cells, scores):
    i = 0
    for score in scores[:10]:
        top_cells[i].value = score[0]
        i += 1
    pr.update_cells(top_cells)

def display_options(screen_state):
    

def main():
    # Setting up and authorizing access to Google Spreadsheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gc = gspread.authorize(creds)
    pr = gc.open('Smash Ultimate Power Rankings').sheet1
    
    # Initializes Challonge
    initialize_challonge()
    
    # Variables that User might use
    user_input = ''
    tourn_str = ''
    
    # Spreadsheet cells
    top_cells = pr.range(3, 5, 12, 5)
    
    # Main loop
    while user_input.lower() != 'exit':
        
        user_input = input()



if __name__ == '__main__':
    main()
    
'''
TOURN_STR = 'utn1lyez'
top_cells = pr.range(3, 5, 12, 5)
#scores = first_time_run(TOURN_STR, top_cells)
scores = updated_scores(TOURN_STR, pr.get_all_values(), top_cells)
name_cells = pr.range(3, 2, len(scores), 2)
score_cells = pr.range(3, 3, len(scores), 3)
c = 0
for cell in name_cells:
    cell.value = scores[c][0].capitalize()
    c += 1
pr.update_cells(name_cells)
c = 0
for cell in score_cells:
    cell.value = scores[c][1]
    c += 1
pr.update_cells(score_cells)


initialize_challonge()
TOURN_STR = '2oalxh0'
#top = ['Zekken', 'Cloudhead', 'Siebz', 'Tribli', 'AstroKoolaid' ,'ProtoSoul', 'YDIC', 'Marzz', 'SWVY', 'Ecocide']
scores = grab_scores(TOURN_STR, top)
'''
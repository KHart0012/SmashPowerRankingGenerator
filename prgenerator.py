# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:33:40 2019

@author: Kevin Hart
"""

from challonge_handler import initialize_challonge, grab_scores, grab_tournament
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from screen_states import ScreenStates

def first_time_run(tourn_str, top_cells):
    top = [cell.value for cell in top_cells]
    return grab_scores(tourn_str, top)


def updated_scores(tourn_str, cells, top_cells):
    prev_scores = grab_current_scores(cells)
    top = [str(cell.value) for cell in top_cells]
    curr_scores = grab_scores(tourn_str, top)
    
    player_dict = dict()
    
    for i in range(len(prev_scores)):
        try:
            player_dict[prev_scores[i][0].lower()] = int(prev_scores[i][1])
        except:
            pass
    
    for i in range(len(curr_scores)):
        if curr_scores[i][0].lower() in player_dict.keys():
            player_dict[curr_scores[i][0].lower()] += int(curr_scores[i][1])
        else:
            player_dict[curr_scores[i][0].lower()] = int(curr_scores[i][1])
        
    return sorted(player_dict.items(), key=lambda x: x[1], reverse=True)
    

def update_scores(pr, scores):
    rank_cells = pr.range(3, 1, 2 + len(scores), 1)
    name_cells = pr.range(3, 2, 2 + len(scores), 2)
    score_cells = pr.range(3, 3, 2 + len(scores), 3)
    c = 1
    for cell in rank_cells:
        cell.value = c
        c += 1
    pr.update_cells(rank_cells)
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
    


def grab_current_scores(cells):
    prev = []
    for i in range(len(cells)):
        prev.append((cells[i][1], cells[i][2]))
    return prev


def update_top(pr, top_cells, scores):
    i = 0
    for score in scores[:10]:
        top_cells[i].value = score[0]
        i += 1
    pr.update_cells(top_cells)


def clear_scores(pr):
    prev_scores = grab_current_scores(pr.get_all_values())
    rank_cells = pr.range(3, 1, len(prev_scores), 1)
    name_cells = pr.range(3, 2, len(prev_scores), 2)
    score_cells = pr.range(3, 3, len(prev_scores), 3)
    c = 0
    for cell in rank_cells:
        cell.value = ''
        c += 1
    pr.update_cells(rank_cells)
    c = 0
    for cell in name_cells:
        cell.value = ''
        c += 1
    pr.update_cells(name_cells)
    c = 0
    for cell in score_cells:
        cell.value = ''
        c += 1
    pr.update_cells(score_cells)
    
    
    

'''
def add_completed_tournament(tourn_str):
    scores =
    
    name_cells = pr.range(3, 2, len(scores), 2)
    score_cells = pr.range(3, 3, len(scores), 3)
'''

def display_options(options, screen_state):
    if screen_state in options[len(options) - 1]:
        i = 0
        for option in options[screen_state.value]:
            print('[' + str(i + 1) + '] ' + option)
            i += 1
    
    elif screen_state == ScreenStates.ADD_TOURN or screen_state == ScreenStates.FIRST_TOURN:
        print('Enter the Tournament String: ')
    
    elif screen_state == ScreenStates.VALID_INPUT_ADD or screen_state == ScreenStates.VALID_INPUT_FIRST:
        print('Tournament String is Valid! Power Rankings have been updated!')
    
    elif screen_state == ScreenStates.INVALID_INPUT_ADD or screen_state == ScreenStates.INVALID_INPUT_FIRST:
        print('That tournament string is not valid, please re-enter the tournament string:\n')

def validate_input(tourn_str):
    try:
        grab_tournament(tourn_str)
        return True
    except:
        return False

def handle_input(user_input, screen_state):
    text = False
    number = False
    
    print(screen_state)
    
    if screen_state == ScreenStates.VALID_INPUT_FIRST or screen_state == ScreenStates.VALID_INPUT_ADD:
        return ScreenStates.UPDATE_SCORES

    try:
        user_input = int(user_input)
        number = True
    except ValueError:
        text = True
        pass        

    """
    If value if number, either person is selecting a new screen or inputing specific value
    This will handle all numerical inputs
    """

    if number:
        
        # Options for Main Menu
        if screen_state == ScreenStates.MAIN_MENU:
            if user_input == 1:
                return ScreenStates.UPDATE_SCORES
            elif user_input == 2:
                return ScreenStates.ROLLOVER_SEASON
            elif user_input == 3:
                return ScreenStates.FIRST_SETUP
            elif user_input == 4:
                return ScreenStates.EXIT_PROG
            return ScreenStates.MAIN_MENU

        # Options for Update Scores
        elif screen_state == ScreenStates.UPDATE_SCORES:
            if user_input == 1:
                return ScreenStates.ADD_TOURN
            elif user_input == 2:
                return ScreenStates.FIRST_TOURN
            elif user_input == 3:
                return ScreenStates.MAIN_MENU
            return ScreenStates.UPDATE_SCORES

        # Options for Rollover PR Season
        elif screen_state == ScreenStates.ROLLOVER_SEASON:
            if user_input == 1:
                return ScreenStates.UPDATE_TOP
            elif user_input == 2:
                return ScreenStates.MAIN_MENU
            return ScreenStates.ROLLOVER_SEASON

        # Options for First Time Setup
        elif screen_state == ScreenStates.FIRST_SETUP:
            if user_input == 1:
                return ScreenStates.GOOGLE_SETUP
            elif user_input == 2:
                return ScreenStates.MAIN_MENU
            return ScreenStates.FIRST_SETUP

        # If screen state is invaild, then it will just send us back to main menu
        else:
            return ScreenStates.MAIN_MENU

    # Handles all string inputs
    elif text:
        if user_input.lower() == 'exit' or user_input.lower() == 'quit':
            return screen_state.EXIT_PROG

        # Options for Add completed Tournament
        elif screen_state == ScreenStates.ADD_TOURN:
            try:
                validate_input(user_input)
                return ScreenStates.VALID_INPUT_ADD
            except:
                return ScreenStates.INVALID_INPUT_ADD
        
        elif screen_state == ScreenStates.INVALID_INPUT_ADD:
            return ScreenStates.ADD_TOURN

        elif screen_state == ScreenStates.FIRST_TOURN:
            if validate_input(user_input):
                return ScreenStates.VALID_INPUT_FIRST
            return ScreenStates.INVALID_INPUT_FIRST
        
        elif screen_state == ScreenStates.INVALID_INPUT_FIRST:
            return ScreenStates.FIRST_TOURN
    
    return ScreenStates.EXIT_PROG
            
  
# Setting up and authorizing access to Google Spreadsheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(creds)
pr = gc.open('Smash Ultimate Power Rankings').sheet1
top_cells = pr.range(3, 5, 12, 5)
all_cells = pr.get_all_values()
    
# Initializes Challonge
initialize_challonge()

# Basic Setup for now
print("Type 'exit' to exit the program!")
user_input = input('Is this the first tournament of the season? [y/n]: ')
if str(user_input).lower() == 'y':
    tourn_str = input('Please input the first Tournament String: ')
    if (validate_input(tourn_str)):
        scores = first_time_run(tourn_str, top_cells)
        update_scores(pr, scores)
    else:
        print('invalid tournament string')

while user_input.lower() != 'exit':
    all_cells = pr.get_all_values()
    top_cells = pr.range(3, 5, 12, 5)
    print("Type 'exit' to exit the program!")
    user_input = input('Would you like to enter another tournament? [y/n]: ') 
    if str(user_input).lower() == 'y':
        tourn_str = input('Please input the Tournament String: ')
        if (validate_input(tourn_str)):
            scores = updated_scores(tourn_str, all_cells, top_cells)
            update_scores(pr, scores)
        else:
            print('invalid tournament string')
    
    elif str(user_input).lower() == 'clear':
        clear_scores(pr)
    elif user_input.lower() == 'n':
        user_input = 'exit'

        
'''
def main():
    # Setting up and authorizing access to Google Spreadsheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gc = gspread.authorize(creds)
    pr = gc.open('Smash Ultimate Power Rankings').sheet1
    top_cells = pr.range(3, 5, 12, 5)
    all_cells = pr.get_all_values()
    
    # Initializes Challonge
    initialize_challonge()
    
    user_input = input('Is this the first tournament of the season? [y/n]: ')
    if str(user_input).lower() == 'y':
        tourn_str = input('Please input the first Tournament String: ')
        if (validate_input(tourn_str)):
            scores = first_time_run(tourn_str, top_cells)
            update_scores(pr, scores)
        else:
            print('invalid tournament string')
        
    elif str(user_input).lower() == 'n':
        tourn_str = input('Please input the Tournament String: ')
        if (validate_input(tourn_str)):
            scores = updated_scores(tourn_str, all_cells, top_cells)
            update_scores(pr, scores)
        else:
            print('invalid tournament string')
    
    
    #clear_scores(pr)
    
    
    
    # Constants
    screen_state = ScreenStates.MAIN_MENU
    mm_options = ['Update Scores', 'Rollover PR Season', 'First Time Setup', 'Exit']
    us_options = ['Add Completed Tournament', 'First Completed Tournament', 'Back']
    rs_options = ['Update Top 10', 'Back']
    fs_options = ['Google Stuff', 'Back']
    list_options = [
            ScreenStates.MAIN_MENU, 
            ScreenStates.UPDATE_SCORES, 
            ScreenStates.FIRST_SETUP,
            ScreenStates.ROLLOVER_SEASON
    ]
    options = [mm_options, us_options, rs_options, fs_options, list_options]
    
    # Variables
    user_input = ''
    
    # Spreadsheet cells
    top_cells = pr.range(3, 5, 12, 5)
    
    # Main loop
    while screen_state != ScreenStates.EXIT_PROG:
        display_options(options, screen_state)
        if screen_state != ScreenStates.VALID_INPUT_ADD or screen_state != ScreenStates.VALID_INPUT_FIRST: 
            user_input = input()
        screen_state = handle_input(user_input, screen_state)
    
    #quit()
    '''



#if __name__ == '__main__':
    #main()
    
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
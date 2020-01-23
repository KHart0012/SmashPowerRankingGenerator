# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:46:55 2019

@author: Kevin Hart
"""

import challonge
from access_data import username, api_key

TOP2_WIN_POINT = 3
TOP35_WIN_POINT = 2
TOP610_WIN_POINT = 1

def initialize_challonge():
    challonge.set_credentials(username, api_key)

def grab_tournament(tourn_str):
    return challonge.tournaments.show(tourn_str)

def grab_matches(tourn_str):
    return challonge.matches.index(grab_tournament(tourn_str)['id'])

def grab_participants(tourn_str):
    return challonge.participants.index(grab_tournament(tourn_str)['id'])
    
def list_participants(participants):
    parti_list = []
    for parti in participants:
        parti_list.append(parti['name'])
    return parti_list

def participant_name(participants, p_id):
    for parti in participants:
        if parti['id'] == p_id:
            return str(parti['name'])
    return None

def determine_matchups(participants, matches, top):
    point_changes = dict()
    #print(top[5:10])
    for parti in participants:
        point_changes[parti['name']] = 0
    for match in matches:
        score = grab_winloss(match)
        p1 = participant_name(participants, score[0])
        p2 = participant_name(participants, score[2])
        if p1 != None and p2 != None:
            print(p1, p2)
            # Checks if someone in top 2 lost to someone outside of top 2
            if p1 in top[:2] or p2 in top[:2]:
                if (p1 in top[:2] and p2 not in top[:2]) and score[3] > 0:
                    #point_changes[p1] -= (3 + score[3])
                    point_changes[p2] += (TOP2_WIN_POINT + score[3])
                    print(p2, TOP2_WIN_POINT + score[3])
                elif (p2 in top[:2] and p1 not in top[:2]) and score[1] > 0:
                    #point_changes[p2] -= (3 + score[1])
                    point_changes[p1] += (TOP2_WIN_POINT + score[1])
                    print(p1, TOP2_WIN_POINT + score[1])
            # Checks if someone in top 3-5 lost to someone outside of top 3-5
            elif p1 in top[2:5] or p2 in top[2:5]:
                if (p1 in top[2:5] and p2 not in top[:5]) and score[3] > 0:
                    #point_changes[p1] -= (2 + score[3])
                    point_changes[p2] += (TOP35_WIN_POINT + score[3])
                    print(p2, TOP35_WIN_POINT + score[3])
                elif (p2 in top[2:5] and p1 not in top[:5]) and score[1] > 0:
                    #point_changes[p2] -= (2 + score[1])
                    point_changes[p1] += (TOP35_WIN_POINT + score[1])
                    print(p1, TOP35_WIN_POINT + score[1])
            # Checks if someone beats someone in top 10 if top 10
            elif p1 in top[5:10] or p2 in top[5:10]:
                if (p1 in top[5:10] and p2 not in top[:10]) and score[3] > 0:
                    point_changes[p2] += (TOP610_WIN_POINT + score[3])
                    print(p2, TOP610_WIN_POINT + score[3])
                elif (p2 in top[5:10] and p1 not in top[:10]) and score[1] > 0:
                    point_changes[p1] += (TOP610_WIN_POINT + score[1])
                    print(p1, TOP35_WIN_POINT + score[1])
    print(point_changes)
    return sorted(point_changes.items(), key=lambda x: x[1], reverse=True)
    
def grab_winloss(match):
    score = match['scores-csv']
    return (match['player1-id'], int(score[0]), match['player2-id'], int(score[2]))
    
def calculate_rank_points(participants):
    point_dict = dict()
    entrants = len(participants)
    for parti in participants:
        # Top 8 calculation
        if parti['final-rank'] <= 8:
            point_dict[parti['name']] = calc_top_pts(entrants, tourn_level(entrants), parti['final-rank'])
        # Everyone else
        else:
            point_dict[parti['name']] = calc_player_pts(entrants, parti['final-rank'])
        # Adds bonus pts for winning, Helps winning players partially compensate for points lost to others
        if parti['final-rank'] <= 4:
            point_dict[parti['name']] += bonus_pts(tourn_level(entrants), parti['final-rank'])
    print(point_dict)
    return sorted(point_dict.items(), key=lambda x: x[1], reverse=True)
    
def adjust_for_matchups(rank_points, point_changes):
    final_scores = dict()
    for p in rank_points:
        final_scores[p[0]] = p[1]
    for c in point_changes:
        final_scores[c[0]] += c[1]
    return final_scores

def max_pts(tourn_level):
    if tourn_level == 1:
        return 25
    elif tourn_level == 2:
        return 50
    elif tourn_level == 3:
        return 100
    elif tourn_level == 4:
        return 250
    else:
        return 500

def tourn_level(num_people):
    if num_people < 10:
        return 1
    elif num_people < 20:
        return 2
    elif num_people < 30:
        return 3
    elif num_people < 60:
        return 4
    elif num_people < 100:
        return 5

def bonus_pts(tourn_level, rank):
    if rank == 1:
        return 20 * tourn_level
    elif rank == 2:
        return 15 * tourn_level
    elif rank == 3:
        return 12 * tourn_level
    elif rank == 4:
        return 10 * tourn_level
    else:
        return 0

def calc_diff(num_people, tourn_level):
    return round((max_pts(tourn_level) / (1.15 * num_people)) * (tourn_level // 2))

def calc_top_pts(num_people, tourn_level, rank):
    return max_pts(tourn_level) - ((rank - 1) * calc_diff(num_people, tourn_level))

def calc_player_pts(num_people, rank):
    return num_people - rank + 1

def calculate_scores(participants, matches, top):
    scores = adjust_for_matchups(calculate_rank_points(participants), determine_matchups(participants, matches, top))
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def grab_scores(tourn_str, top):
    matches = grab_matches(tourn_str)
    partics = grab_participants(tourn_str)
    return calculate_scores(partics, matches, top)
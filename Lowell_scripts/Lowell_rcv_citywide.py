# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:56:03 2019

@author: darac
"""

"""

This tool runs simple instances of rank-choice voting. It models
the Cincinnati method of tabulating votes in a Single Transverable Vote
(STV) process for a city-wide vote.
When a candidate is elected their excess votes are transferred
to the next preferred candidate on the excess ballots.

"""

import math
import random
import pandas as pd

############## Count ballots using Cincinnati method ###############

def remove_cand(cand, ballot_list):
    for n, ballot in enumerate(ballot_list):
        new_ballot = []
        for c in ballot:
            if c!= cand:
                new_ballot.append(c)
        ballot_list[n]= new_ballot
        
def transfer_surplus(cand, ballot_list, win_lose, cutoff):
    if win_lose == 'lose':
        remove_cand(cand, ballot_list)
    else:           
        cand_ballots_index = []
        for n, ballot in enumerate(ballot_list):
            if ballot[0] == cand:
                cand_ballots_index.append(n)
        rand_winners = random.sample(cand_ballots_index, int(cutoff))
        #remove winning ballots from simulation
        for index in sorted(rand_winners, reverse = True):
            del ballot_list[index]  
        #remove candidate from rest of ballots
        remove_cand(cand, ballot_list)

def recompute_count(candidates, ballot_list):
    cand_totals = {}
    for cand in candidates:
        cand_totals[cand] = len([ballot for ballot in ballot_list if ballot[0] == cand])
    return cand_totals  
        

def rcv_run(ballot_list, num_seats, num_votes, verbose_bool): 
    winners = []
    cutoff = int(num_votes/(num_seats+1) +1)
    candidates = candidate_dict.keys()
    cand_totals = recompute_count(candidates, ballot_list)
    while len(winners) < num_seats:
        remaining_cands = list(set(x for l in ballot_list for x in l))
        if len(remaining_cands) == num_seats - len(winners):
            winners = winners + remaining_cands
            break       
        cand_totals = recompute_count(candidates, ballot_list)
        
        new_winners = []
        for cand in list(candidates):
            if len(winners) == num_seats:
                    break 
            if cand_totals[cand] >= cutoff:
                winners.append(cand)
                new_winners.append(cand)
                transfer_surplus(cand, ballot_list, "win", cutoff)  
                del cand_totals[cand]
                ballot_list = [x for x in ballot_list if x != []]                
                cand_totals = recompute_count(candidates, ballot_list)
                
                if verbose_bool:
                    print("candidate", cand, "elected")           
        candidates = [x for x in candidates if x not in new_winners]                                                         
        min_cand = min(cand_totals, key=cand_totals.get)
        transfer_surplus(min_cand, ballot_list, "lose",cutoff)
        del cand_totals[min_cand]
        ballot_list = [x for x in ballot_list if x != []]
        candidates = [x for x in candidates if x != min_cand]
        cand_totals= recompute_count(candidates, ballot_list)
        
        if verbose_bool:
            print("candidate", min_cand, "eliminated")

    return winners


############## build ballot generation scenarios ###############

def polarized_generator(num_seats, i, perm_white, perm_coalition):
    if i in {1,2,3}:
        if perm_coalition and perm_white:
            return random.sample(coal_cands[:num_seats],num_seats) + random.sample(white_cands[:num_seats],num_seats)
        if perm_coalition and not perm_white:
            return random.sample(coal_cands[:num_seats],num_seats) + white_cands[:num_seats]
        if not perm_coalition and  perm_white:
            return coal_cands[:num_seats] + random.sample(white_cands[:num_seats],num_seats)
        if not perm_coalition and not perm_white:
            return coal_cands[:num_seats] + white_cands[:num_seats] 
    elif i == 0:
        if perm_coalition and perm_white:
            return random.sample(white_cands[:num_seats],num_seats) + random.sample(coal_cands[:num_seats],num_seats)
        if perm_coalition and not perm_white:
            return white_cands[:num_seats] + random.sample(coal_cands[:num_seats],num_seats)
        if not perm_coalition and  perm_white:
            return random.sample(white_cands[:num_seats],num_seats) + coal_cands[:num_seats]
        if not perm_coalition and not perm_white:
            return white_cands[:num_seats] + coal_cands[:num_seats] 


def interweave(listA, listB):
    assert(len(listA) == len(listB))
    new_list = []
    for i in range(len(listA)):
        new_list.append(listA[i])
        new_list.append(listB[i])
    return new_list

def crossover_generator(num_seats, i, perm_white, perm_coalition):
    if i in {1,2,3}:
        if perm_coalition and perm_white:
            return interweave(random.sample(white_cands[:num_seats],num_seats), random.sample(coal_cands[:num_seats],num_seats))
        if perm_coalition and not perm_white:
            return interweave(white_cands[:num_seats], random.sample(coal_cands[:num_seats],num_seats))
        if not perm_coalition and  perm_white:
            return interweave(random.sample(white_cands[:num_seats],num_seats), coal_cands[:num_seats])
        if not perm_coalition and not perm_white:
            return interweave(white_cands[:num_seats], coal_cands[:num_seats])
    elif i == 0:
        if perm_coalition and perm_white:
            return interweave(random.sample(coal_cands[:num_seats],num_seats), random.sample(white_cands[:num_seats],num_seats))
        if perm_coalition and not perm_white:
            return interweave(random.sample(coal_cands[:num_seats],num_seats), white_cands[:num_seats])
        if not perm_coalition and  perm_white:
            return interweave(coal_cands[:num_seats], random.sample(white_cands[:num_seats],num_seats))
        if not perm_coalition and not perm_white:
            return interweave(coal_cands[:num_seats], white_cands[:num_seats])


def scenario_generator(num_seats, votes, vote_vec, perm_white_vec, perm_coal_vec, pct_crossover_vec):
    vote_list = []
    for i in range(len(vote_vec)):
        # polarized votes
        for vote in range(math.ceil(votes*vote_vec[i]*(1.0-pct_crossover_vec[i]))): #ex. make all non-cross over white voter ballots
            vote_list.append(polarized_generator(num_seats, i, perm_white_vec[i], perm_coal_vec[i]))
        # crossover votes
        for vote in range(math.ceil(votes*vote_vec[i]*(pct_crossover_vec[i]))):
            vote_list.append(crossover_generator(num_seats, i, perm_white_vec[i], perm_coal_vec[i]))
    return vote_list
    


candidate_dict = {'w1':0,'w2':0,'w3':0,'w4':0,'w5':0,'w6':0,'w7':0,'w8':0,'w9':0,'c1':1,'c2':1,'c3':1,'c4':1,'c5':1,'c6':1,'c7':1,'c8':1,'c9':1}
candidates = list(candidate_dict.keys())

white_cands = ['w1','w2','w3','w4','w5','w6','w7','w8','w9']
coal_cands = ['c1','c2','c3','c4','c5','c6','c7','c8','c9']

#vector order: white, hispanic, asian, other
cvap_vec = [.59, .17, .17, .07]
turnout_list= [[1,1,1,1], 
               [1,.5,.5,1],
               [1,.25, .75, 1],
               [1, .75, .25, 1],
               [1,1/3, 1/3,1],
               [1,.1,.9,1], 
               [1,.9,.1,1], 
               [1,.8,.8,1]]
crossover_list = [[.1, .3, .3, .3],
                  [.3, .3, .3, .3], 
                  [.1, .5, .5, .1], 
                  [.1, .1, .1, .1], 
                  [.1, .1, .5, .1], 
                  [.1,.5,.1,.1]]

den_list = [sum(x * y for x, y in zip(cvap_vec, turnout_list[i])) for i in range(len(turnout_list)) ]
vote_list = [[x * y/den_list[i] for x, y in zip(cvap_vec, turnout_list[i])] for i in range(len(turnout_list))]

rcv_output = pd.DataFrame(columns = ["Turnout", "Crossover", "num_seats", \
                                     'total pol., unam vote', 'total pol., minority permute min_i', \
                                     'total pol., all permute all', 'total pol., white permute all', \
                                     'crossover, unam vote', 'crossover, minority permute min_i', \
                                     'crossover, all permute all', 'crossover, white permute all'])

for vec in vote_list:    
    for vec2 in crossover_list:
        crossover_vec = vec2
        vote_vec = vec 
        index = vote_list.index(vec)
          
        scen1 = [[False, False, False, False],
                [False, False, False, False],
                [0,0,0,0], 'total pol., unam vote']
    
        scen2a = [[False, False, False, False],
                [False, True, True, True],
                [0,0,0,0], 'total pol., minority permute min_i']
    
        scen2b = [[True, True, True, True],
                [True, True, True, True],
                [0,0,0,0], 'total pol., all permute all']
    
        scen2c = [[True, False, False, False],
                [True, False, False, False],
                [0,0,0,0], 'total pol., white permute all']
    
        scen3 = [[False, False, False, False],
                [False, False, False, False],
                crossover_vec, 'crossover, unam vote']
    
        scen4a = [[False, False, False, False],
                [False, True, True, True],
                crossover_vec, 'crossover, minority permute min_i']
    
        scen4b = [[True, True, True, True],
                [True, True, True, True],
                crossover_vec, 'crossover, all permute all']
    
        scen4c = [[True, False, False, False],
                [True, False, False, False],
                crossover_vec, 'crossover, white permute all']
    
        
        scen_list = [scen1, scen2a, scen2b, scen2c, scen3, scen4a, scen4b, scen4c]
        
###################### Edit Inputs Below ######################  
        
        num_votes = 5000
        num_runs = 200
        num_seats = 3 #elected via RCV city-wide
        
###############################################################
        
        for i in [num_seats]:        
            scen_output = {}
            for scen in scen_list:
                num_coal_seats = []
                for j in range(num_runs):
                    winners = rcv_run(scenario_generator(i, num_votes, vote_vec, scen[0], scen[1], scen[2]), i, num_votes, False)
                    num_coal_seats.append(sum(candidate_dict[x] for x in winners))
                scen_output[scen_list.index(scen)] = sum(num_coal_seats)/len(num_coal_seats)
             
            rcv_output.loc[len(rcv_output)] = [turnout_list[index], crossover_vec, i] + list(scen_output.values())

rcv_output.to_csv("Lowell_rcv_output_citywide.csv")


# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:56:03 2019

@author: darac
"""

"""

this tool runs simple instances of rank-choice voting.
votes that exceed the threshold are transfered proportionally to 
their remaining share among votes with same first choice.

takes as input a list of rankings (first choice to last) 
and percent of voters with that ranking:

[['candidate_1', 'candidate 2', ....], percent with this rank choice], 
    ['candidate_2', 'candidate 1', ....], percent with this rank choice],
    ...]

e.g.:
    ballot_list = [['w1','w2','h1'],
                ['w1','h1','w2'],
                ['h1','w1']]


percentages need not sum to one and can optionally be rescaled

rankings need not be complete

"""

import math
import random
import pandas as pd

#output_sample = open('C:\\Users\\darac\\Desktop\\Lowell\\sample3', 'a')
#output_sample.close()

def remove_cand(cand, ballot_list):#just removes a candidate from each ballot in list, keeps %s the same
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
        
#ballot_list = [['c1', 'c2', 'c4'], ['c3', 'c2', 'c5'] , ['c1', 'c3', 'c2'], ['c1','c4', 'w4'], ['c1', 'c3', 'w2'], ['c1', 'c5', 'w5'], ['c1', 'c4', 'c6'], ['c1', 'c2', 'w5']]   

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
                transfer_surplus(cand, ballot_list, "win", cutoff) #and edit ballot list   
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

#rcv_run(ballot_list, 3, len(ballot_list),1)  


############## build scenarios ###############

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
            #note- polarized means WWWHHH structure, but perm_white/perm_hisp decides ordering within WWW or HHH etc.
        # crossover votes
        for vote in range(math.ceil(votes*vote_vec[i]*(pct_crossover_vec[i]))):
            vote_list.append(crossover_generator(num_seats, i, perm_white_vec[i], perm_coal_vec[i]))
    return vote_list
    


candidate_dict = {'w1':0,'w2':0,'w3':0,'w4':0,'w5':0,'w6':0,'w7':0,'w8':0,'w9':0,'c1':1,'c2':1,'c3':1,'c4':1,'c5':1,'c6':1,'c7':1,'c8':1,'c9':1}
candidates = list(candidate_dict.keys())

white_cands = ['w1','w2','w3','w4','w5','w6','w7','w8','w9']
#hispanic_cands = ['h1','h2','h3','h4','h5','h6','h7','h8','h9']
#asian_cands = ['a1','a2','a3','a4','a5','a6','a7','a8','a9']
coal_cands = ['c1','c2','c3','c4','c5','c6','c7','c8','c9']

#white, hispanic, asian, other
cvap_vec = [.59, .17, .17, .07]
turnout_list= [[1,1,1,1], [1,.5,.5,1], [1,.25, .75, 1], [1, .75, .25, 1], [1,1/3, 1/3,1], [1,.1,.9,1], [1,.9,.1,1], [1,.8,.8,1]]
crossover_list = [[.1, .3, .3, .3], [.3, .3, .3, .3], [.1, .5, .5, .1], [.1, .1, .1, .1], [.1, .1, .5, .1], [.1,.5,.1,.1]]
den_list = [sum(x * y for x, y in zip(cvap_vec, turnout_list[i])) for i in range(len(turnout_list)) ]
vote_list = [[x * y/den_list[i] for x, y in zip(cvap_vec, turnout_list[i])] for i in range(len(turnout_list))]

#white, hisp, asian, other
#crossover_vec = [0.1, .3, 0.3, .3]
#crossover_list=[[.02,.77,.58,.4],
#                [.01,.8,.61,.34],
#                [.07,.53,.38,.01],
#                [.07,.76,.73,.01],
#                [.07,.99,.51,.24],
#                [.1,.69,.76,.27],
#                [.02,.56,.17,.03],
#                [.6,.55,.01,.34],
#                [.45,.68,.07,.04],
#                [.02,.59,.9,.46],
#                [.65,.32,.27,.05],
#                [.2,.17,.48,.07]]
#crossover_list = [[.1, .1, .1, .2], [.3,.5,.4,.7]]
rcv_output = pd.DataFrame(columns = ["Turnout", "Crossover", "CVAP", "Vote vector", "num_seats", \
                                                       'total pol., unam vote', 'total pol., minority permute min_i', \
                                                       'total pol., all permute all', 'total pol., white permute all', \
                                                        'crossover, unam vote', 'crossover, minority permute min_i', \
                                                        'crossover, all permute all', 'crossover, white permute all'])

turnout = []
crossover = []
vote_vec = []
cvap = []
#output_sample = open('C:\\Users\\darac\\Desktop\\Lowell\\sensitivity_analysis_cvap_crossover_change', 'a')
for vec in vote_list:    
    for vec2 in crossover_list:
        crossover_vec = vec2
        vote_vec = vec 
        #for output
    #    output_sample.write("vote_vec: %s\n" % (vote_vec))
    #    output_sample.write("crossover_vec: %s\n" % (crossover_vec))
    #    output_sample.write("cvap_vec: %s\n" % (cvap_vec))
        index = vote_list.index(vec)
    #    output_sample.write("turnout_vec: %s\n" %(turnout_list[index]))
       
    
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
        
        num_votes = 5000 #00#change to 25k
        num_runs = 200 #0#100 runs, only rerun if scen
        

          #seats
        for i in [6]:        
            scen_output = {}
            for scen in scen_list:
                num_coal_seats = []
                for j in range(num_runs):
                    winners = rcv_run(scenario_generator(i, num_votes, vote_vec, scen[0], scen[1], scen[2]), i, num_votes, False)
                    num_coal_seats.append(sum(candidate_dict[x] for x in winners))
                scen_output[scen_list.index(scen)] = sum(num_coal_seats)/len(num_coal_seats)
              #  if 'unam' in scen[3]:
                   # output_sample.write("%s %s seats, coalition seats: %s\n" % (scen[3], i, num_coal_seats[0]))
                 #   print(scen[3], i, 'seats', 'coalition seats:', num_coal_seats[0] )     
                  
                    
             #   else:
                    #output_sample.write("%s %s seats, min: %s, max: %s, avg: %s \n" % (scen[3], i, min(num_coal_seats), max(num_coal_seats), sum(num_coal_seats)/len(num_coal_seats)))
                  #  print(scen[3], i, 'seats', 'min:', min(num_coal_seats), 'max:', max(num_coal_seats), 'avg:', sum(num_coal_seats)/len(num_coal_seats))     
        
            rcv_output.loc[len(rcv_output)] = [turnout_list[index], crossover_vec, cvap_vec, vote_vec, i] + list(scen_output.values())
rcv_output.to_csv("sensitivity_turnout_crossover_6_seat.csv")
#output_sample.close()

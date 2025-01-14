import random
import numpy as np

def prob_all_SaE(N,p,q,max_iter):
    shortest_sl = [(i,i+1) for i in range(N)]
    truth_vals = {(i,i+1):False for i in range(N)}
    truth_vals[(0,N)] = False
    counter = 0

    while True:
        counter += 1

        existing_links = np.sort([link for link in truth_vals if truth_vals[link]])
        for link in shortest_sl:
            big_link_exists = False
            if not truth_vals[link]:
                for big_link in existing_links:
                    if big_link[0]<=link[0] and link[-1]<=big_link[-1]:
                        big_link_exists = True
                        break
                if big_link_exists:
                    continue   
                
                if random.random() < p:
                    truth_vals[link] = True
        
        existing_links = np.sort([link for link in truth_vals if truth_vals[link]])

        temp_rep = 0
        all_linked = False
        while temp_rep != N:
            valid_links = [link for link in existing_links if link[0]==temp_rep]
            if len(valid_links) > 0:
                temp_rep = valid_links[0][-1]
            elif len(valid_links) == 0:
                all_linked = False
                break
        if temp_rep == N:
            all_linked = True

        if all_linked:
            for rep in range(1,N):
                sl_L = None
                sl_R = None
                for link in truth_vals:
                    if truth_vals[link]:
                        if rep == link[-1]:
                            sl_L = link
                        if rep == link[0]:
                            sl_R = link

                if sl_L != None and sl_R != None:
                    if random.random() < q: # succeed -> entanglement 
                        truth_vals[(sl_L[0],sl_R[-1])] = True
                        truth_vals[sl_L] = False
                        truth_vals[sl_R] = False
                    else: # fail
                        truth_vals[sl_L] = False
                        truth_vals[sl_R] = False
                else:
                    pass
        
        if truth_vals[(0,N)]:
            return counter
        
        # stop if iter > ...
        elif counter >= max_iter:
            return counter
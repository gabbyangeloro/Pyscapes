#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 16:47:02 2020

@author: gabrielleangeloro
"""

dgm = [[2,6], [4, 10]]

len_dgm = len(dgm)
# Calculate m 
m = int(max([x for pair in dgm for x in pair])/2)

# initialze W to a list of 2m + 1 empty lists
W = [[] for i in range(2*m +1)]

# for each birth death pair
for bd in dgm:
    b, d = bd
    # for j=1 to j=height of (b_i, d_i) from rank function
    for j in range(1, int((bd[1]- bd[0])/2 +1)) :
        W[b + j].append(j)
    
    # for j=1 to j=height of (b_i, d_i) +1 from rank function
    for j in range(1, int(((bd[1]- bd[0])/2))):
        W[d - j].append(j)

# sort each list in W
for i in range(len(W)):
    W[i] = sorted(W[i], reverse = True)
    
# calculate k: max length of lists in W
K = max([len(_) for _ in W ])

# initialize V
V = []


    
    
            
        
        
        
        
    
    
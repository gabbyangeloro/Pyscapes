#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:33:52 2020

@author: gabrielleangeloro
"""
from PersistenceLandscapeGrid import PersistenceLandscapeGrid
import numpy as np

dgm = [np.array([[2,6],[4,10]])]
 
P = PersistenceLandscapeGrid(0, 10, 11, dgm, 0)
P.compute_landscape()

print(f'P is {P.funct_values} ')

#%%

Q = PersistenceLandscapeGrid(0, 10, 6, dgm, 0)
Q.compute_landscape()
print(f'Q is {Q.funct_values} ')

#%%

R = PersistenceLandscapeGrid(0, 10, 21, dgm, 0)
R.compute_landscape()
print(f'R is {R.funct_values} ')

#%%

S = PersistenceLandscapeGrid(0, 10, 4, dgm, 0)
S.compute_landscape()
print(f'S is {S.funct_values} ')
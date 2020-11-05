#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:33:52 2020

@author: gabrielleangeloro
"""
from PersistenceLandscapeGrid import PersistenceLandscapeGrid
import numpy as np

dgm = [np.array([[2,6],[4,10]])]
 
P1 = PersistenceLandscapeGrid(0, 10, 11, dgm, 0)
P1.compute_landscape(verbose= True)

#print(f'P is {P.funct_pairs} ')
#P.funct_pairs
#%%

from PersistenceLandscapeGrid import PersistenceLandscapeGrid
import numpy as np

dgm = [np.array([[2,6],[4,10]])]

Q = PersistenceLandscapeGrid(0, 10, 6, dgm, 0)
Q.compute_landscape()
print(f'Q is {Q.funct_pairs} ')

#%%

from PersistenceLandscapeGrid import PersistenceLandscapeGrid
import numpy as np

dgm = [np.array([[2,6],[4,10]])]

R = PersistenceLandscapeGrid(0, 10, 21, dgm, 0)

print(f'R is {R.compute_landscape()} ')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Time different versions of PersistenceLandscape
"""
import timeit
 
SETUP_CODE1 = ''' 
from __main__ import PersistenceLanscape1
import numpy as np'''

TEST_CODE1 = ''' 
A = np.array([[1,2]])
for _ in range(10000):
    x = np.random.randint(low=0,high=15)
    y = np.random.randint(low=x+1,high=25)
    np.append(A, np.array([x, y]) )
#A = np.array([ [1.0, 5.0], [2.0, 8.0], [3.0, 4.0], [5.0, 9.0], [6.0, 7.0] ]) 
PersistenceLanscape1(A) 
    '''

times1 = timeit.timeit(setup = SETUP_CODE1, 
                          stmt = TEST_CODE1,  
                      number = 10) # time it takes to execute the snippet 10,000 times
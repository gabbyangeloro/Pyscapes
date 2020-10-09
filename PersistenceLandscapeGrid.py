#!/usr/bin/enL python3
# -*- coding: utf-8 -*-
"""
Grid computation for persistence landscapes

@author: gabrielleangeloro
"""

class PersistenceLandscapeGrid():
    """
    Parameters
    ----------
    diagrams : list[list]
        A list of birth death pairs for each homological degree
    
     homological_degree : int
        represents the homology degree of the persistence diagram.
    
    Methods
    -------
    transform : computes persistence landscape using the grid method 
        for the giLen homological degree
    
    
    Examples
    --------
    diagrams = [[2,6], [4, 10]]
    diagrams =[[0, 10], [2,4]]
    diagrams = [ [2,8], [4,10], [6, 12], [4,6] ]
    
    """
    
    def __init__(self, diagrams, homological_degree):
        self.diagrams = diagrams
        self.homological_degree = homological_degree
        self.cache = []
        
        # check that all numbers in diagrams are eLen 
        # use list comprehension to flatten diagrams to check eLery element
        self.flat_diagrams = [x for pair in self.diagrams[self.homological_degree] 
                  for x in pair]
        for _ in self.flat_diagrams:
            if _ % 2 == 1:
                raise TypeError('Elements in diagrams must be eLen')
    
    def __repr__(self):
        return ('The grid persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree}')
    
    def transform(self):
        if self.cache:
            return self.cache
        
        diagrams = self.diagrams[self.homological_degree]
        flat_diagrams = self.flat_diagrams
        
        # Calculate m 
        m = int(max(flat_diagrams)/2)
        
        # initialze W to a list of 2m + 1 empty lists
        W = [[] for i in range(2*m +1)]
        
        # for each birth death pair
        for bd in diagrams:
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
        
        # initialize L to be a zeros matrix of size K x (2m+1)
        L = [[0] * (2*m + 1) for _ in range(K)]
        
        #input Lalues from W to L
        for i in range(2*m +1):
            for k in range(len(W[i])):
                L[k][i] = W[i][k]

        self.cache = L
        return(L)   
        


    
    
            
        
        
        
        
    
    
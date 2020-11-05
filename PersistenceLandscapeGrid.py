#!/usr/bin/enL python3
# -*- coding: utf-8 -*-
"""
Grid computation for persistence landscapes

@author: gabrielleangeloro
"""
import numpy as np
from auxiliary import ndsnap

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

    
    """
    def __init__(
        self, start: float, stop: float, num_dims: int, 
        diagrams: list = [], homological_degree: int = 0, 
        funct_values: list = [], funct_pairs: list = []):
        
        self.diagrams = diagrams
        self.homological_degree = homological_degree
        self.start = start
        self.stop = stop
        self.num_dims = num_dims
        self.funct_values = funct_values
        self.funct_pairs = funct_pairs

    
    def __repr__(self):
        
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree} on grid from {self.start} to {self.stop}'
        f' with step size {self.num_dims}')
        
    
    def compute_landscape(self, verbose: bool = False):
        
        verboseprint = print if verbose else lambda *a, **k: None
         
        if self.funct_values:
            verboseprint('funct_pairs was entered, value is stored')
            return 
        
        verboseprint('funct_values and funct_pairs were empty, computing values')
        # make grid
        grid_values, step = np.linspace(self.start, self.stop, self.num_dims, 
                                        retstep = True)[:]
        grid_values = list(grid_values)
        grid = np.array([[x,y] for x in grid_values for y in grid_values])
        points = self.diagrams[self.homological_degree]
        diagram_grid = ndsnap(points, grid)
        
        # make grid dictionary 
        
        values = list(range(self.num_dims))
        dict_grid = dict(zip( grid_values, values))
        
        # initialze W to a list of 2m + 1 empty lists
        #W = [[] for i in range(self.stop +1)]
        W = [[] for _ in range(self.num_dims)]
    
        
        # for each birth death pair
        for  bd in diagram_grid:
            b,d = bd
            j = 0
            # step through by x value
            for _ in np.arange(b+step, (b+d)/2 +1, step):
                j += 1
                # dict_grid[b]: index in W that b corresponds to
                # j*step: adding points from a line with slope 1
                W[dict_grid[b]+j].append(j* step) 
            
    
            
            j = 0
            # step through x backwards from d-step to b+d/2 by step
            # arange doesn't include right endpoint, i.e. b+d/2
            for _ in np.arange(d- step, (b+d)/2, -step):
                j += 1
                W[dict_grid[d] - j].append(j* step)
        
        # sort each list in W
        for i in range(len(W)):
            W[i] = sorted(W[i], reverse = True)
            
        # calculate k: max length of lists in W
        K = max([len(_) for _ in W ])
        
        # initialize L to be a zeros matrix of size K x (2m+1)
        L = [[0] * (self.num_dims) for _ in range(K)]
        
        #input Lalues from W to L
        for i in range(self.num_dims):
            for k in range(len(W[i])):
                L[k][i] = W[i][k]

        self.funct_values = L
        return
    
    
    def funct_values_to_pairs(self):
        """
        Converts function values to ordered pairs and stores in `self.funct_pairs`

        Returns
        -------
        None.

        """
        self.compute_landscape()
        
        grid_values = list(np.linspace(self.start, self.stop, self.num_dims, ))
        
        for l in self.funct_values:
            pairs = list(zip(grid_values, l))
            self.funct_pairs.append( pairs )
        return
          
        


    
    
            
        
        
        
        
    
    
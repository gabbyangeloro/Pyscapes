#!/usr/bin/enL python3
# -*- coding: utf-8 -*-
"""
Grid computation for persistence landscapes

@author: gabrielleangeloro
"""
import numpy as np

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
        self, start_gridx:float, end_gridx: float, grid_num: int, 
        diagrams: list = [], homological_degree: int = 0, 
        PL_funct_values: list = []):
        
        self.diagrams = diagrams
        self.homological_degree = homological_degree
        self.start_gridx = start_gridx
        self.end_gridx = end_gridx
        self.grid_num = grid_num
        self.PL_funct_values = PL_funct_values
        self.step_size = (self.end_gridx-self.start_gridx) / self.grid_num
        
        ndsnap = self.ndsnap
    
    def __repr__(self):
        
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree} on grid from {self.start_gridx} to {self.end_gridx}'
        f' with step size {self.step_size}')
    
    def ndsnap(self, points, grid):
        """
        Snap an 2D-array of points to values along an 2D-array grid.
        Each point will be snapped to the grid value with the smallest
        city-block distance.
    
        Parameters
        ---------
        points: 2D-array. Must have same number of columns as grid
        grid: 2D-array. Must have same number of columns as points
    
        Returns
        -------
        A 2D-array with one row per row of points. Each i-th row will
        correspond to row of grid to which the i-th row of points is closest.
        In case of ties, it will be snapped to the row of grid with the
        smaller index.
        """      
        # transpose grid 
        grid_3d = np.transpose(grid[:,:,np.newaxis], [2,1,0])
        # axis 1 is x-values of points
        diffs = np.sum(np.abs(grid_3d - points[:,:,np.newaxis]), axis=1)
        # argmin returns the indices of the minimum values along an axis
        best = np.argmin(diffs, axis=1)
        return grid[best,:]
    
    def create_grid(self):
        homological_degree = self.homological_degree
        start_gridx = self.start_gridx
        end_gridx = self.end_gridx
        diagrams = self.diagrams
        grid_num = self.grid_num
        
        
        # make grid
        # calculate max y -value for grid (always start at y=0)
        end_gridy = np.ceil(max(diagrams[homological_degree][:,1]))
        x, step = np.linspace(start_gridx, end_gridx, grid_num, retstep = True)[:]
        self.step = step
        
        y = np.arange(0, end_gridy+ step, step)
        
        grid = np.array([[itemx, itemy] for itemx in x for itemy in y])
        diagrams = diagrams[homological_degree]
        
        diagrams_grid = self.ndsnap(diagrams, grid)
        self.diagrams_grid = diagrams_grid
        
    
    def transform(self):
        if self.PL_funct_values:
            return self.PL_funct_values
        
        diagrams_grid = self.diagrams_grid 
        homological_degree = self.homological_degree
        start_gridx = self.start_gridx
        end_gridx = self.end_gridx
        diagrams = self.diagrams
        grid_num = self.grid_num
        
        
        # initialze W to a list of 2m + 1 empty lists
        W = [[] for i in range(end_gridx +1)]
        
        # for each birth death pair
        for ind, bd in enumerate(diagrams_grid):
            b = bd[0]
            d = bd[1]
            # for j=1 to j=height of (b_i, d_i) from rank function
            for j in range(1, int((bd[1]- bd[0])/2 +1)) :
                W[ind + j].append(j*self.step)
            
            # for j=1 to j=height of (b_i, d_i) +1 from rank function
            for j in range(1, int(((bd[1]- bd[0])/2))):
                W[ind - j].append(j*self.step)
        
        # sort each list in W
        for i in range(len(W)):
            W[i] = sorted(W[i], reverse = True)
            
        # calculate k: max length of lists in W
        K = max([len(_) for _ in W ])
        
        # initialize L to be a zeros matrix of size K x (2m+1)
        L = [[0] * (end_gridx + 1) for _ in range(K)]
        
        #input Lalues from W to L
        for i in range(end_gridx +1):
            for k in range(len(W[i])):
                L[k][i] = W[i][k]

        self.PL_funct_values = L
        return(L)   
        


    
    
            
        
        
        
        
    
    
""" 
Define Grid Persistence Landscape class.
"""
import numpy as np
from auxiliary import ndsnap
from PersistenceLandscape import PersistenceLandscape


class PersistenceLandscapeGrid(PersistenceLandscape):
    """
    Persistence Landscape Grid class.

    This class implements an approximate version of Persistence Landscape,
    given by sampling the landscape functions on a user-defined grid. 
    This version is only an approximation to the true landscape, but given
    a fine enough grid, this should suffice for most applications. If an exact
    calculation with no approximation is desired, consider `PersistenceLandscapeExact`.

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
        
        super().__init__(diagrams=diagrams, homological_degree=homological_degree)
        # self.diagrams = diagrams
        # self.homological_degree = homological_degree
        self.start_gridx = start_gridx
        self.end_gridx = end_gridx
        self.grid_num = grid_num
        self.PL_funct_values = PL_funct_values
        self.step_size = (self.end_gridx-self.start_gridx) / self.grid_num
        
        # ndsnap = self.ndsnap
    
    def __repr__(self):
        
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree} on grid from {self.start_gridx} to {self.end_gridx}'
        f' with step size {self.step_size}')
    
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
        


    
    
            
        
        
        
        
    
    
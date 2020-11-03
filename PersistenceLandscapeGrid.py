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
        self, start: float, stop: float, num_dims: int, 
        diagrams: list = [], homological_degree: int = 0, 
        funct_values: list = []):
        
        super().__init__(diagrams=diagrams, homological_degree=homological_degree)
        # self.diagrams = diagrams
        # self.homological_degree = homological_degree
        self.start_gridx = start_gridx
        self.end_gridx = end_gridx
        self.grid_num = grid_num
        self.PL_funct_values = PL_funct_values
        self.step_size = (self.end_gridx-self.start_gridx) / self.grid_num
        self.diagrams = diagrams
        self.homological_degree = homological_degree
        self.start = start
        self.stop = stop
        self.num_dims = num_dims
        self.funct_values = funct_values
        
        # ndsnap = self.ndsnap
    
    def __repr__(self):
        
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree} on grid from {self.start_gridx} to {self.end_gridx}'
        f' with step size {self.step_size}')
        
    
    def compute_landscape(self, verbose: bool = False):
        
        verboseprint = print if verbose else lambda *a, **k: None
        
        if self.funct_values:
            return self.funct_values
        
    
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
        
        verboseprint(f'diagram_grid is {diagram_grid}')
        verboseprint(f'step is {step}')
        # initialze W to a list of 2m + 1 empty lists
        #W = [[] for i in range(self.stop +1)]
        W = [[] for _ in range(self.num_dims)]
        
        verboseprint(f'W is {W}')
        
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
            
        verboseprint(f'W is {W}')
            
        # calculate k: max length of lists in W
        K = max([len(_) for _ in W ])
        
        # initialize L to be a zeros matrix of size K x (2m+1)
        L = [[0] * (self.num_dims) for _ in range(K)]
        
        #input Lalues from W to L
        for i in range(self.num_dims):
            for k in range(len(W[i])):
                L[k][i] = W[i][k]

        self.funct_values = L
        return(L)   
        


    
    
            
        
        
        
        
    
    

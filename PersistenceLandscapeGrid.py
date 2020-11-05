""" 
Define Grid Persistence Landscape class.
"""
from __future__ import annotations
import numpy as np
import itertools
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
        funct_values: list = [], funct_pairs: list = []) -> None:
        
        super().__init__(diagrams=diagrams, homological_degree=homological_degree)
        # self.diagrams = diagrams
        # self.homological_degree = homological_degree
        self.start = start
        self.stop = stop
        self.num_dims = num_dims
        self.funct_values = funct_values
        self.funct_pairs = funct_pairs
    
    def __repr__(self) -> str:
        
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree} on grid from {self.start} to {self.stop}'
        f' with step size {self.num_dims}')
        
    
    def compute_landscape(self, verbose: bool = False) -> list:
        
        verboseprint = print if verbose else lambda *a, **k: None
         
        if self.funct_values:
            verboseprint('funct_pairs was entered, value is stored')
            return 
        
        verboseprint('funct_values was empty, computing values')
        # make grid
        grid_values, step = np.linspace(self.start, self.stop, self.num_dims, 
                                        retstep = True)[:]
        grid_values = list(grid_values)
        grid = np.array([[x,y] for x in grid_values for y in grid_values])
        
        # create list of triangle top for each birth death pair
        bd_pairs = self.diagrams[self.homological_degree]
        birth: 'np.ndarray' = bd_pairs[:, 0]
        death: 'np.ndarray' = bd_pairs[:, 1]
        triangle_top_ycoord = (death - birth)/ 2
        triangle_top = np.array(list(zip((birth + death)/2, (death - birth)/2)))
        
        # snap birth-death pairs and triangle tops to grid 
        bd_pairs_grid = ndsnap(bd_pairs, grid)
        triangle_top_grid = ndsnap(triangle_top, grid)
        
        # make grid dictionary 
        
        values = list(range(self.num_dims))
        dict_grid = dict(zip( grid_values, values))
        
        # initialze W to a list of 2m + 1 empty lists
        # W = [[] for i in range(self.stop +1)]
        W = [[] for _ in range(self.num_dims)]
    
        # for each birth death pair
        for ind_in_bd_pairs, bd in enumerate(bd_pairs_grid):
            b, d = bd
            ind_in_Wb = dict_grid[b] # index in W
            ind_in_Wd = dict_grid[d] # index in W
            
            # step through by x value
            j = 0
            # j in (b, b+d/2]
            for _ in np.arange(triangle_top_grid[ind_in_bd_pairs, 0], b, -step):
                j += 1
                # j*step: adding points from a line with slope 1
                W[ind_in_Wb +j].append(j* step) 
          
            j = 0
            # j in (b+d/2, d)
            for _ in np.arange(triangle_top_grid[ind_in_bd_pairs, 0] + step, d, step):
                j += 1
                W[ind_in_Wd  - j].append(j* step)
    
        '''  
        # for each birth death pair
        for  bd in diagram_grid:
            b,d = bd
            j = 0
            # step through by x value
            for _ in np.arange(b+step, (b+d)/2 , step):
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
        '''
        
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
          
        
    
    def __add__(self, other: PersistenceLandscapeGrid) -> PersistenceLandscapeGrid:
        # This assumes the values are stored in numpy arrays
        if self.homological_degree != other.homological_degree:
            raise ValueError("Persistence landscapes must be of same homological degree")
        if self.start_gridx != other.start_gridx:
            raise ValueError("Start values of grids do not coincide")
        if self.end_gridx != other.end_gridx:
            raise ValueError("Stop values of grids do not coincide")
        if self.grid_num != other.grid_num:
            raise ValueError("Number of steps of grids do not coincide")
        return PersistenceLandscapeGrid(start_gridx=self.start_gridx, end_gridx=self.end_gridx, grid_num=self.grid_num,
                                        homological_degree=self.homological_degree, values=self.values+other.values)
    
    def __neg__(self) -> PersistenceLandscapeGrid:
        return PersistenceLandscapeGrid(
            start_gridx=self.start_gridx, 
            end_gridx=self.end_gridx, 
            grid_num=self.grid_num,
            homological_degree=self.homological_degree,
            values = np.array([np.array([-b for b in depth_array]) for depth_array in self.values]))
        pass
    
    def __sub__(self, other):
        return self + -other
    
    def __mul__(self, other: float) -> PersistenceLandscapeGrid:
        if issubclass(other, PersistenceLandscape):
            raise TypeError("Cannot multiply persistence landscapes together")
        pass
    
    def __rmul__(self,other: float) -> PersistenceLandscapeGrid:
        return other*self
    
    def __truediv__(self, other: float) -> PersistenceLandscapeGrid:
        if other == 0.:
            raise ValueError("Cannot divide by zero")
        return (1.0/other)*self
    
    def p_norm(self, p:int = 2) -> float:
        return np.sum([np.linalg.norm(depth,p) for depth in self.values])

    def sup_norm(self) -> float:
        return np.max(np.abs(self.values))

# max and min crit values are given by taking np.max/min on the list of lists.

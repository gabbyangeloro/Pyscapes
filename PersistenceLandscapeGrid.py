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
        for the given homological degree
    
    
    Examples
    --------

    
    """
    def __init__(
        self, start: float, stop: float, num_dims: int, 
        diagrams: list = [], homological_degree: int = 0, 
        values: list = [], pairs: list = []) -> None:
        
        super().__init__(diagrams=diagrams, homological_degree=homological_degree)
        # self.diagrams = diagrams
        # self.homological_degree = homological_degree
        self.start = start
        self.stop = stop
        self.num_dims = num_dims
        self.values = values
        self.pairs = pairs
        # TODO: Do we need self.pairs? NO.
    
    def __repr__(self) -> str:
        
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree} on grid from {self.start} to {self.stop}'
        f' with step size {self.num_dims}')
        
    
    def compute_landscape(self, verbose: bool = False) -> list:
        
        verboseprint = print if verbose else lambda *a, **k: None
         
        # TODO: I don't understand the following check. We check funct_values
        #       but print a message about funct_pairs.
        if self.values:
            verboseprint('values was stored, exiting')
            return 
        
        verboseprint('values was empty, computing values')
        # make grid
        grid_values, step = np.linspace(self.start, self.stop, self.num_dims, 
                                        retstep = True)[:] # TODO Why this [:]? Helps unpack
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
        
        #input Values from W to L
        for i in range(self.num_dims):
            for k in range(len(W[i])):
                L[k][i] = W[i][k]

        self.values = L
        # TODO: Isn't self.values a list now? Shouldn't it be a np.array?
        # Maybe it should be 
        # self.values = np.array([np.array(l) for l in L])?
        # But this seems slow since we have to iterate over everything again.
        # Maybe the right place to do this is on line 150, where L is initialized.
        # There it should be 
        # L = np.array([ np.zeros(self.num_dims) for _ in range(K)])
        # Where numpy arrays are slow is with appending elements, because the entire array
        # has to be copied over in memory (they have to be contiguous I think), but once you
        # know the size of the array, i don't think they're slow anymore.
        return
    
    
    def values_to_pairs(self):
        """
        Converts function values to ordered pairs and stores in `self.pairs`

        Returns
        -------
        None.

        """
        self.compute_landscape()
        
        grid_values = list(np.linspace(self.start, self.stop, self.num_dims, ))
        
        for l in self.values:
            pairs = list(zip(grid_values, l))
            self.pairs.append( pairs )
        return
          
        
    
    def __add__(self, other: PersistenceLandscapeGrid) -> PersistenceLandscapeGrid:
        super().__add__(other)
        if self.start != other.start:
            raise ValueError("Start values of grids do not coincide")
        if self.stop != other.stop:
            raise ValueError("Stop values of grids do not coincide")
        if self.num_dims != other.num_dims:
            raise ValueError("Number of steps of grids do not coincide")
        return PersistenceLandscapeGrid(start=self.start, stop=self.stop, 
                                        num_dims=self.num_dims,
                                        homological_degree=self.homological_degree, 
                                        values=self.values+other.values)
    
    def __neg__(self) -> PersistenceLandscapeGrid:
        return PersistenceLandscapeGrid(
            start=self.start, 
            stop=self.stop, 
            num_dims=self.num_dims,
            homological_degree=self.homological_degree,
            values = np.array([-1*depth_array for depth_array in self.values]))
        pass
    
    def __sub__(self, other):
        return self + -other
    
    def __mul__(self, other: float) -> PersistenceLandscapeGrid:
        super().__mul__(other)
        return PersistenceLandscapeGrid(
            start=self.start, 
            stop=self.stop, 
            num_dims=self.num_dims,
            homological_degree=self.homological_degree,
            values = np.array([other*depth_array for depth_array in self.values]))
    
    def __rmul__(self,other: float) -> PersistenceLandscapeGrid:
        return self.__mul__(other)
    
    def __truediv__(self, other: float) -> PersistenceLandscapeGrid:
        super().__truediv__(other)
        return (1.0/other)*self
    
    def __getitem__(self, key: slice) -> list:
        """
        Returns a list of values corresponding in range specified by 
        depth

        Parameters
        ----------
        key : slice object

        Returns
        -------
        list
            The values of the landscape function corresponding
        to depths given by key
        """
        self.compute_landscape()
        return self.values[key]
    
    def p_norm(self, p:int = 2) -> float:
        return np.sum([np.linalg.norm(depth,p) for depth in self.values])

    def sup_norm(self) -> float:
        return np.max(np.abs(self.values))



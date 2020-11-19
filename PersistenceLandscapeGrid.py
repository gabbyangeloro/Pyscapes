""" 
Define Grid Persistence Landscape class.
"""
from __future__ import annotations
import numpy as np
import itertools
from auxiliary import pairs_snap
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
    
     hom_deg : int
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
        diagrams: list = [], hom_deg: int = 0, 
        values = np.array([])) -> None:
        
        super().__init__(diagrams=diagrams, hom_deg=hom_deg)
        # self.diagrams = diagrams
        #self.hom_deg = hom_deg
        self.start = start
        self.stop = stop
        self.num_dims = num_dims
        self.values = values
    
    def __repr__(self) -> str:
        
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.hom_deg} on grid from {self.start} to {self.stop}'
        f' with step size {self.num_dims}')
        
    
    def compute_landscape(self, verbose: bool = False) -> list:
        
        verboseprint = print if verbose else lambda *a, **k: None
         
       
        if self.values.size :
            verboseprint('values was stored, exiting')
            return 
        
        verboseprint('values was empty, computing values')
        # make grid
        grid_values, step = np.linspace(self.start, self.stop, self.num_dims, 
                                        retstep = True)[:] # TODO Why this [:]? Helps unpack
        grid_values = list(grid_values)
        grid = np.array([[x,y] for x in grid_values for y in grid_values])
        bd_pairs = self.diagrams       
       
        # create list of triangle top for each birth death pair
        birth: 'np.ndarray' = bd_pairs[:, 0]
        death: 'np.ndarray' = bd_pairs[:, 1]
        triangle_top_ycoord = (death - birth)/ 2
        triangle_top = np.array(list(zip((birth + death)/2, (death - birth)/2)))
        
        # snap birth-death pairs and triangle tops to grid 
        bd_pairs_grid = pairs_snap(bd_pairs, grid)
        triangle_top_grid = pairs_snap(triangle_top, grid)
        
        # make grid dictionary 
        index = list(range(self.num_dims))
        dict_grid = dict(zip( grid_values, index))
        
        # initialze W to a list of 2m + 1 empty lists
        W = [[] for _ in range(self.num_dims)]
    
        # for each birth death pair
        for ind_in_bd_pairs, bd in enumerate(bd_pairs_grid):
            [b, d] = bd
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
        
        # sort each list in W
        for i in range(len(W)):
            W[i] = sorted(W[i], reverse = True)
            
        # calculate k: max length of lists in W
        K = max([len(_) for _ in W ])
        
        # initialize L to be a zeros matrix of size K x (2m+1)
        L = np.array([ np.zeros(self.num_dims) for _ in range(K)])
        
        #input Values from W to L
        for i in range(self.num_dims):
            for k in range(len(W[i])):
                L[k][i] = W[i][k]
        
        # check if L is empty 
        if not L.size:
            L = np.array(['empty'])
            print('Bad choice of grid, values is empty')


        self.values = L
        return
    
    
    def values_to_pairs(self):
        """
        Converts function values to ordered pairs and stores in `self.pairs`

        Returns
        -------
        None.

        """
        self.compute_landscape()
        grid_values = np.linspace(self.start, self.stop, self.num_dims, )
        
        for l in self.values:
            pairs = np.array(list(zip(grid_values, l)))
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
                                        hom_deg=self.hom_deg, 
                                        values=self.values+other.values)
    
    def __neg__(self) -> PersistenceLandscapeGrid:
        return PersistenceLandscapeGrid(
            start=self.start, 
            stop=self.stop, 
            num_dims=self.num_dims,
            hom_deg=self.hom_deg,
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
            hom_deg=self.hom_deg,
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
    
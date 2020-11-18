""" 
Define Grid Persistence Landscape class.
"""
from __future__ import annotations
import numpy as np
from operator import attrgetter
# import itertools
from auxiliary import ndsnap, union_vals
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
        values: list = [], pairs: list = [], compute: bool = False) -> None:
        
        super().__init__(diagrams=diagrams, homological_degree=homological_degree)
        # self.diagrams = diagrams
        # self.homological_degree = homological_degree
        self.start = start
        self.stop = stop
        self.num_dims = num_dims
        self.values = values
        if compute:
            self.compute_landscape()
    
    def __repr__(self) -> str:
        
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree} on grid from {self.start} to {self.stop}'
        f' with step size {self.num_dims}')
        
    
    def compute_landscape(self, verbose: bool = False) -> list:
        
        verboseprint = print if verbose else lambda *a, **k: None

        if isinstance(self.values, np.ndarray):
            verboseprint('values was stored, exiting')
            return 
        
        verboseprint('values was empty, computing values')
        # make grid
        grid_values, step = np.linspace(self.start, self.stop, self.num_dims, 
                                        retstep = True)[:] # TODO Why this [:]? Helps unpack
        grid_values = list(grid_values)
        grid = np.array([[x,y] for x in grid_values for y in grid_values])
        bd_pairs = self.diagrams[self.homological_degree]        
        '''
        # check for duplicates of (b,d)
        duplicate = 0
        
        for ind, item in enumerate(list(bd_pairs)):
            if item == [b,d]:
                duplicate += 1
                A.pop(ind)
            else:
                break
        '''
        
        # create list of triangle top for each birth death pair
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
        
        # sort each list in W
        for i in range(len(W)):
            W[i] = sorted(W[i], reverse = True)
            
        # calculate k: max length of lists in W
        K = max([len(_) for _ in W ])
        
        # initialize L to be a zeros matrix of size K x (2m+1)
        #L = [[0] * (self.num_dims) for _ in range(K)]
        L = np.array([ np.zeros(self.num_dims) for _ in range(K)])
        
        #input Values from W to L
        for i in range(self.num_dims):
            for k in range(len(W[i])):
                L[k][i] = W[i][k]


        self.values = L
        return
    
    
    def values_to_pairs(self):
        """
        Converts function values to ordered pairs and returns them.

        Returns
        -------

        """
        self.compute_landscape()
        
        grid_values = list(np.linspace(self.start, self.stop, self.num_dims))
        result = []
        for l in self.values:
            pairs = list(zip(grid_values, l))
            result.append( pairs )
        return np.array(result)
          
        
    
    def __add__(self, other: PersistenceLandscapeGrid) -> PersistenceLandscapeGrid:
        super().__add__(other)
        if self.start != other.start:
            raise ValueError("Start values of grids do not coincide")
        if self.stop != other.stop:
            raise ValueError("Stop values of grids do not coincide")
        if self.num_dims != other.num_dims:
            raise ValueError("Number of steps of grids do not coincide")
        self_pad, other_pad = union_vals(self.values, other.values)
        return PersistenceLandscapeGrid(start=self.start, stop=self.stop, 
                                        num_dims=self.num_dims,
                                        homological_degree=self.homological_degree, 
                                        values=self_pad+other_pad)
    
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

###############################
# End PLG class definition
###############################

def snap_PL(l: list) -> list:
    """
    Given a list `l` of PersistenceLandscapeGrid types, convert them to a list
    where each entry has the same start, stop, and num_dims. This puts each
    entry of `l` on the same grid, so they can be added, averaged, etc.
    
    This assumes they're all of the same homological degree and their values have 
    all been computed.
    """
    _b = min(l,key=attrgetter('start')).start
    _d = max(l,key=attrgetter('stop')).stop
    _dims = max(l,key=attrgetter('num_dims')).num_dims
    # Now use ndsnap somehow?
    grid_values = list(np.linspace(start=_b, stop=_d, num=_dims))
    grid = np.array([[x,y] for x in grid_values for y in grid_values]) # TODO reshape?
    k = [PersistenceLandscapeGrid(start=_b, stop=_d, num_dims=_dims,
                                 values=[ndsnap(depth,grid) for depth in pl.values_to_pairs()],
                                 homological_degree=pl[0].homological_degree) for pl in l]
    return k
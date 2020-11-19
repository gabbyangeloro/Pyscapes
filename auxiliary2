#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import numpy as np
from operator import attrgetter
from auxiliary import values_snap
from PersistenceLandscapeGrid import PersistenceLandscapeGrid

def snap_PL(l: list) -> list:
        """
        Given a list `l` of PersistenceLandscapeGrid types, convert them to a list
        where each entry has the same start, stop, and num_dims. This puts each
        entry of `l` on the same grid, so they can be added, averaged, etc.
        
        This assumes they're all of the same homological degree.
        """
        _b = min(l,key=attrgetter('start')).start
        _d = max(l,key=attrgetter('stop')).stop
        _dims = max(l,key=attrgetter('num_dims')).num_dims
        grid = np.linspace(_b, _d, _dims) 
        #grid_values = list(grid_values)
        #grid = np.array([[x,y] for x in grid_values for y in grid_values])
        '''
        k = [PersistenceLandscapeGrid(start=_b, end=_d, num_dims=_dims,
                                     values=ndsnap(pl.values, grid),
                                     hom_deg= l[0].hom_deg) for pl in l]
        
        '''
        # for each persistence landscape in the list of persitence landscapes
        '''
        k = []
        for pl in l:
            # for each function in the persistence landscape
            snapped_landscape = []
            for funct in pl:
                # snap each function and store 
                snapped_landscape.append(values_snap(funct, grid))
            # store snapped persistence landscape   
            k.append( PersistenceLandscapeGrid(start=_b, stop=_d, num_dims=_dims,
                                     values=snapped_landscape, 
                                     hom_deg = pl.hom_deg))
            '''
        
        k = [ PersistenceLandscapeGrid(start=_b, stop=_d, num_dims=_dims,
                                     values=values_snap(funct, grid), 
                                     hom_deg = pl.hom_deg) for pl in l for funct in pl]
        return k
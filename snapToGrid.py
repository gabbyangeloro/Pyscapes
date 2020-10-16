#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 09:59:11 2020

@author: gabrielleangeloro
"""
import numpy as np

x, step = np.linspace(0, 4, 5, retstep = True)[:]
y = np.arange(0, 5+ step, step)
grid = np.array([[itemx, itemy] for itemx in x for itemy in y])


#%%
        
def ndsnap(points, grid):
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
    # make grid
    x, step = np.linspace(0, 4, 5, retstep = True)[:]
    y = np.arange(0, 5+ step, step)
    grid = np.array([[itemx, itemy] for itemx in x for itemy in y])
    
    # transpose grid 
    grid_3d = np.transpose(grid[:,:,np.newaxis], [2,1,0])
    # axis 1 is x-values of points
    diffs = np.sum(np.abs(grid_3d - points[:,:,np.newaxis]), axis=1)
    # argmin returns the indices of the minimum values along an axis
    best = np.argmin(diffs, axis=1)
    return grid[best,:]

    



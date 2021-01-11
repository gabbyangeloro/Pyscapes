#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 11:17:01 2021

@author: mike
"""

from tadasets import torus
from ripser import ripser
from PersistenceLandscapeGrid import PersLandscapeApprox
from PersistenceLandscapeExact import PersLandscapeExact
from visualization import plot_landscape_simple

t = torus()

tph = ripser(t)['dgms']

tpla = PersLandscapeApprox(dgms=tph,hom_deg=1,num_steps=5000)
tple = PersLandscapeExact(dgms=tph,hom_deg=1)
#%%
plot_landscape_simple(tple)
plot_landscape_simple(tpla)

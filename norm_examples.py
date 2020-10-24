# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 19:44:57 2020

@author: mikec
"""
import numpy as np
from sklearn.datasets import load_wine
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

from ripser import ripser
from persim import plot_diagrams
from PersistenceLandscape import PersistenceLandscape

data = np.random.random_sample((200,2))
diagrams = ripser(data)['dgms']
# rips.plot(diagrams)

# pl = PL(homological_degree=1][]
# landscape = pl.fit_transform(diagrams)

L = PersistenceLandscape(diagrams,homological_degree=1)
L.compute_landscape(verbose=True)
L.p_norm(p=2)
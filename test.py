# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 22:10:00 2020

@author: mikec
"""

import numpy as np
from ripser import Rips
from PersistenceLandscape import PersistenceLandscape
#from pl_transformer import PL

rips = Rips()
data = np.random.random((100,2))
diagrams = rips.fit_transform(data)
rips.plot(diagrams)

#pl = PL(homological_degree=1)
#landscape = pl.fit_transform(diagrams)

pl = PersistenceLandscape(diagrams,homological_degree=1)
L = pl.compute_landscape(verbose=True)
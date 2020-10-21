

import numpy as np
from ripser import Rips
from PersistenceLandscape import PersistenceLandscape
#from pl_transformer import PL

rips = Rips()
data = np.random.random_sample((200,2))
diagrams = rips.fit_transform(data)
rips.plot(diagrams)

# pl = PL(homological_degree=1][]
# landscape = pl.fit_transform(diagrams)

L = PersistenceLandscape(diagrams,homological_degree=1)
L.compute_landscape(verbose=True)

print(L)
print("The number of critical pairs is ", len(L.critical_pairs))
print("The first two are given by ", L[:2])
# M = L + L
"""
Visualization methods for plotting persistence landscapes.

DO NOT USE THIS NOW. USE EXAMPLES.PY INSTEAD.
"""

import matplotlib.pyplot as plt
from PersistenceLandscape import PersistenceLandscape

def plot_landscape(landscape: PersistenceLandscape):
    """
    A plot of the persistence landscape
    """
    pass


#%%
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)


def polygon_under_graph(xlist, ylist):
    """
    Construct the vertex list which defines the polygon filling the space under
    the (xlist, ylist) line graph.  Assumes the xs are in ascending order.
    """
    return [(xlist[0], 0.), *zip(xlist, ylist), (xlist[-1], 0.)]


fig = plt.figure()
ax = fig.gca(projection='3d')

# Make verts a list, verts[i] will be a list of (x,y) pairs defining polygon i
verts = []

# Set up the x sequence
xs = np.linspace(0., 10., 26)

# The ith polygon will appear on the plane y = zs[i]
zs = [0] # range(4)

L = np.array([[0.08088598, 0.        ],
       [0.09222407, 0.01133809],
       [0.10143114, 0.00213103],
       [0.12616551, 0.0268654 ],
       [0.13100001, 0.02203091],
       [0.13280252, 0.02383342],
       [0.14482516, 0.01181078],
       [0.20296358, 0.06994919],
       [0.27291277, 0.        ]])

#for i in L:
   # ys = np.random.rand(len(xs))
 #   verts.append(polygon_under_graph(i[0]))

poly = PolyCollection(L, facecolors=['r', 'g', 'b', 'y'], alpha=.6)
ax.add_collection3d(poly, zs=[0], zdir='y')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(0, 10)
ax.set_ylim(-1, 4)
ax.set_zlim(0, 1)

plt.show()
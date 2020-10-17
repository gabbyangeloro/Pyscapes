# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 19:34:09 2020

@author: mikec
"""

import numpy as np
from ripser import ripser
from persim import plot_diagrams
from PersistenceLandscape import PersistenceLandscape

data = np.random.random((100, 2))
diagrams = ripser(data)['dgms']
#plot_diagrams(diagrams, show=True)

M = PersistenceLandscape(diagrams, homological_degree=1)
M.compute_landscape()
L = M.critical_pairs

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
# verts = [L]


# Set up the x sequence
xs = np.linspace(0., 10., 1000)

# The ith polygon will appear on the plane y = zs[i]
# zs = range(4)

# for i in zs:
#     ys = np.random.rand(len(xs))
#     verts.append(polygon_under_graph(xs, ys))

# poly = PolyCollection(verts, facecolors=['r','g','b','r'], linewidths=3, alpha=.6)
# ax.add_collection3d(poly, zs=zs, zdir='y')
poly = PolyCollection(L,
                      linewidths =[0.5 for _ in range(len(L))],
                      edgecolors=['k' for _ in range(len(L))],
                     # facecolors=plt.cm.jet,
                      facecolors=['r','g','b','r','g','y','b','r','g'],
                      alpha=.7)
ax.add_collection3d(poly, zs=0.2*np.linspace(0.,10.,len(L)), zdir='y')

#ax.plot(L,np.linspace(0.,1.,len(L)))

ax.set_xlabel('X')
#ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(0, 0.3)
ax.set_ylim(-1, 4)
ax.set_zlim(0, 0.06)

ax.view_init(30,90)

#plt.style.context('ggplot')
#plt.show()

#%% line with no fill

fig2 = plt.figure()
ax2 = fig2.gca(projection='3d')
for i, l in enumerate(L):
    xs, ys = zip(*l)
    ax2.plot(xs,ys,zs=i*len(xs),label=i, zdir='y')
#ax2.plot(xs,ys=L, zs=0.2*np.linspace(0.,10.,len(L)))
ax2.set_xlabel('X')
#ax.set_ylabel('Y')
ax2.set_zlabel('Z')
#ax2.set_xlim(0, 0.3)
#ax2.set_ylim(-1, 4)
#ax2.set_zlim(0, 0.06)
ax2.legend()
ax2.view_init(30,90)
plt.gray()

plt.show()

#%% color according to z-value
# https://stackoverflow.com/questions/20165169/change-colour-of-curve-according-to-its-y-value-in-matplotlib
from matplotlib import cm
fig3 = plt.figure()
ax3 = fig3.gca(projection="3d")
xs2, zs2 = zip(*L[0])
ax3.plot(xs=xs2,ys=[1 for _ in xs2],zs=zs2,zdir='y',c=cm.jet(np.abs(zs2)))
plt.show()

#%% fill under
# https://stackoverflow.com/questions/16917919/filling-above-below-matplotlib-line-plot
# More on using colormaps https://stackoverflow.com/questions/8931268/using-colormaps-to-set-color-of-line-in-matplotlib
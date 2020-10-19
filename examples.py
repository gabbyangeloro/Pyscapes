# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 19:34:09 2020

@author: mikec
"""

import numpy as np
from ripser import ripser
from persim import plot_diagrams
from mpl_toolkits.mplot3d import Axes3D
from PersistenceLandscape import PersistenceLandscape

data = np.random.random((100, 2))
diagrams = ripser(data)['dgms']
#plot_diagrams(diagrams, show=True)

M = PersistenceLandscape(diagrams, homological_degree=1)
M.compute_landscape()
L = M.critical_pairs

# # This import registers the 3D projection, but is otherwise unused.
# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

# from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
# from matplotlib import colors as mcolors

# # Fixing random state for reproducibility
# np.random.seed(19680801)


# def polygon_under_graph(xlist, ylist):
#     """
#     Construct the vertex list which defines the polygon filling the space under
#     the (xlist, ylist) line graph.  Assumes the xs are in ascending order.
#     """
#     return [(xlist[0], 0.), *zip(xlist, ylist), (xlist[-1], 0.)]


# fig = plt.figure()
# ax = fig.gca(projection='3d')

# # Make verts a list, verts[i] will be a list of (x,y) pairs defining polygon i
# verts = []
# # verts = [L]


# # Set up the x sequence
# xs = np.linspace(0., 10., 1000)

# # The ith polygon will appear on the plane y = zs[i]
# # zs = range(4)

# # for i in zs:
# #     ys = np.random.rand(len(xs))
# #     verts.append(polygon_under_graph(xs, ys))

# # poly = PolyCollection(verts, facecolors=['r','g','b','r'], linewidths=3, alpha=.6)
# # ax.add_collection3d(poly, zs=zs, zdir='y')
# poly = PolyCollection(L,
#                       linewidths =[0.5 for _ in range(len(L))],
#                       edgecolors=['k' for _ in range(len(L))],
#                      # facecolors=plt.cm.jet,
#                       facecolors=['g','g','b','r','g','y','b','r','g'],
#                       alpha=.7)
# ax.add_collection3d(poly, zs=0.2*np.linspace(0.,10.,len(L)), zdir='y')

# #ax.plot(L,np.linspace(0.,1.,len(L)))

# ax.set_xlabel('X')
# #ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_xlim(0, 0.3)
# ax.set_ylim(-1, 4)
# ax.set_zlim(0, 0.06)

# ax.view_init(30,90)

# #plt.style.context('ggplot')
# #plt.show()

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

#%% test for 2-d plot

fig3 = plt.figure()
#x = np.linspace(0, 2*np.pi, 1000)
#y = np.sin(2*x)
xs2, zs2 = zip(*L[0])
plt.plot(xs2,zs2, c=cm.hot(np.abs(zs2))) # , edgecolor='none')
plt.show()

#%% First good working case
# Ideas:
# If an exact landscape is passed, interpolate it. If a discrete landscape
# is passed, then use the grid it is based on. This one is the exact version

fig4 = plt.figure()
ax = plt.axes()
num_steps = 3000
xs,ys = zip(*L[0])
domain = np.linspace(0, 0.3, num=num_steps)
image = np.interp(domain, xs, ys)
# plt.plot(domain,image)
plt.scatter(domain, image, c=cm.jet(image/max(image)), edgecolor='none', alpha=0.1, marker='.')
#d = np.zeros(len(ys))
#ax.fill_between(xs, ys, where=ys>=d, interpolate=True, color='b')
#ax.fill_between(xs, ys, where=ys<=d, interpolate=True, color='red')
ax.set_xlabel('x')

#%% Plot all of them
# Its hard to see them individually. It's be great if we could put a thin
# black line on them, and set the color of any part of the line with
# value = 0 to 'none'.

from operator import itemgetter
from matplotlib import cm
fig5 = plt.figure()
ax5 = fig5.gca(projection='3d')
num_steps = 1000
max_crit_val = max(L[0],key=itemgetter(1))[1]
domain = np.linspace(0., 0.3, num=num_steps)
for i, l in enumerate(L):
    xs, zs = zip(*l)
    d = np.zeros(len(image))
    image = np.interp(domain, xs, zs)
    ax5.scatter(xs=domain, ys=[i for _ in domain], zs=image,
                c=cm.viridis(image/max_crit_val),
                marker='.', alpha=0.3, linewidth=0)
#ax2.plot(xs,ys=L, zs=0.2*np.linspace(0.,10.,len(L)))
ax5.set_xlabel('X')
#ax.set_ylabel('Y')
ax5.set_zlabel('Z')
#ax2.set_xlim(0, 0.3)
#ax2.set_ylim(-1, 4)
#ax2.set_zlim(0, 0.06)
#ax2.legend()
ax5.view_init(10,90)
#plt.gray()

plt.show()

#%% maybe we should plot vertical lines going straight up to the desired height.
# This works but it is very slow

fig6 = plt.figure()
ax6 = fig6.gca(projection='3d')
num_steps = 1000
min_crit_pt = min(L[0], key=itemgetter(0))[0]
max_crit_pt = max(L[0], key=itemgetter(0))[0]
padding = 0.01
max_crit_val = max(L[0],key=itemgetter(1))[1]
domain = np.linspace(0., 0.3, num=num_steps)
for i, l in enumerate(L):
    xs, zs = zip(*l)
    image = np.interp(domain, xs, zs)
    for x, z in zip(domain,image):
        ax6.plot(
            [x,x],
            [i,i],
            [0,z],
            linewidth=0.5,
            alpha=0.8,
            c=cm.rainbow(z/max_crit_val))

ax6.set_xlabel('X')
ax6.set_ylabel('depth')
ax6.set_zlabel('Z')
ax6.set_xlim(min_crit_pt-padding, max_crit_pt+padding)
ax6.set_ylim(0, 0.4*len(L)+1)
ax6.set_zlim(0, max_crit_val+0.001)
ax6.view_init(15,90)
ax6.view_init(10,90)
plt.show()

#%% I think the following shows that simple masking won't work. The ends get
# cut off so the landscapes look like they're floating.

from operator import itemgetter
from matplotlib import cm
fig7 = plt.figure()
ax7 = fig7.gca(projection='3d')
num_steps = 1000
max_crit_val = max(L[0],key=itemgetter(1))[1]
domain = np.linspace(0., 0.3, num=num_steps)
for i, l in enumerate(L):
    xs, zs = zip(*l)
    # d = np.zeros(len(image))
    image = np.interp(domain, xs, zs)
    domain=domain[image>0.]
    image=image[image>0.]
    ax7.scatter(xs=domain,
                ys=[i for _ in domain],
                zs=image,
                c=cm.rainbow(image/max_crit_val),
                marker='.', alpha=0.3, linewidth=0)
    #ax7.scatter(xs=domain, ys=[i for _ in domain], zs=image,
    #            c=cm.rainbow(image/max_crit_val),
    #            marker='.', alpha=0.3, linewidth=0)
ax7.set_xlabel('X')
#ax.set_ylabel('Y')
ax7.set_zlabel('Z')
#ax2.set_xlim(0, 0.3)
#ax2.set_ylim(-1, 4)
#ax2.set_zlim(0, 0.06)
#ax2.legend()
ax7.view_init(10,90)
#plt.gray()

plt.show()

#%% Try fill between

from operator import itemgetter
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig8 = plt.figure()
ax8 = fig8.gca(projection='3d')
num_steps = 2000
min_crit_pt = min(L[0], key=itemgetter(0))[0]
max_crit_pt = max(L[0], key=itemgetter(0))[0]
max_crit_val = max(L[0], key=itemgetter(1))[1]
padding = 0.01
domain = np.linspace(0., 0.3, num=num_steps)
zees = np.zeros(num_steps)
for i, l in enumerate(L): #i = depth, l = list
    xs, zs = zip(*l) # xs and zs are critical pairs
    image = np.interp(domain,xs,zs) # the {image} of domain under interp of xs/zs
    for j in range(len(domain)-1):
        if image[j] == 0. and image[j+1] == 0.: continue # don't plot trailing zeroes
        verts = [(domain[j], i*0.4, 0), (domain[j+1], i*0.4, 0), # define trapezoid
                 (domain[j],i*0.4, image[j]),
                 (domain[j+1], i*0.4, image[j+1])]
        ax8.add_collection3d(Poly3DCollection( # plot trapezoid
            [verts],
            alpha=1.0,
            linewidths=0.4,
            color=cm.rainbow(image[j]/max_crit_val)))
        ax8.plot( # plot top boundary line
            [domain[j], domain[j+1]],
            [i*0.4, i*0.4],
            [image[j], image[j+1]],
            linewidth=1,
            alpha=0.9,
            color='black'
            )


ax8.set_xlabel('X')
ax8.set_ylabel('depth')
ax8.set_zlabel('Z')
ax8.set_xlim(min_crit_pt-padding, max_crit_pt+padding)
ax8.set_ylim(0, 0.4*len(L)+1)
ax8.set_zlim(0, max_crit_val+0.001)
ax8.view_init(15,90)
plt.show()
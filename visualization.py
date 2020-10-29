"""
Visualization methods for plotting persistence landscapes.

"""

import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PersistenceLandscapeExact import PersistenceLandscapeExact
from operator import itemgetter
from matplotlib import cm

def plot_landscape(landscape: PersistenceLandscapeExact,
                   num_steps: int = 3000,
                   color = cm.viridis,
                   alpha = 0.8,
                   padding: float = 0.1,
                   depth_padding: float = 0.7):
    """
    A plot of the persistence landscape.
    
    Warning: This function is quite slow, especially for large landscapes. 
    
    Parameters
    ----------
    num_steps: int, default 3000
        number of sampled points that are plotted
    
    color, defualt cm.viridis
        color scheme for shading of landscape functions
    
    alpha, default 0.8
        transparency of shading
        
    padding: float, default 0.1
        amount of empty grid shown to left and right of landscape functions
    
    depth_padding: float, default = 0.7
        amount of space between sequential landscape functions
        
    """
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    landscape.compute_landscape()
    # itemgetter index selects which entry to take max/min wrt.
    # the hanging [0] or [1] takes that entry.
    crit_pairs = list(itertools.chain.from_iterable(landscape.critical_pairs))
    min_crit_pt = min(crit_pairs, key=itemgetter(0))[0] # smallest birth time
    max_crit_pt = max(crit_pairs, key=itemgetter(0))[0] # largest death time
    max_crit_val = max(crit_pairs,key=itemgetter(1))[1] # largest peak of landscape
    min_crit_val = min(crit_pairs, key=itemgetter(1))[1] # smallest peak of landscape
    norm = mpl.colors.Normalize(vmin=min_crit_val, vmax=max_crit_val)
    # x-axis for grid
    domain = np.linspace(min_crit_pt-padding*0.1, max_crit_pt+padding*0.1, num=num_steps)
    # for each landscape function
    for depth, l in enumerate(landscape):
        # sequential pairs in landscape
        xs, zs = zip(*l)
        image = np.interp(domain, xs, zs) 
        for x, z in zip(domain,image):
            if z == 0.:
                # plot a single point here?
                continue # moves to the next iterable in for loop
            if z > 0.:
                ztuple = [0, z] 
            elif z < 0.:
                ztuple = [z,0] 
            # for coloring https://matplotlib.org/3.1.0/tutorials/colors/colormapnorms.html
            ax.plot(
                [x,x], # plotting a line to get shaded function
                [depth_padding*depth,depth_padding*depth],
                ztuple,
                linewidth=0.5,
                alpha=alpha,
                c=color(norm(z)))
            ax.plot([x], [depth_padding*depth], [z], 'k.', markersize=0.1)
    
    #ax.set_xlabel('X')
    ax.set_ylabel('depth')
    #ax.set_zlabel('Z')
    #ax.set_xlim(max_crit_pt+padding, min_crit_pt-padding) # reversed
    #ax.set_ylim(0, depth_padding*landscape.max_depth+1)
    # ax.set_zlim(0, max_crit_val+padding)
    # for line in ax.xaxis.get_ticklines():
    #     line.set_visible(False)
    # for line in ax.yaxis.get_ticklines():
    #     line.set_visible(False)
    # for line in ax.zaxis.get_ticklines():
    #     line.set_visible(False)
    #ax.set_xticklabels(np.arange(min_crit_pt,max_crit_pt, 0.2))
    #ax.set_yticklabels(np.arange(0, landscape.max_depth, 3))
    #plt.axis(False)
    ax.view_init(10,90)
    plt.show()

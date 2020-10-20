"""
Visualization methods for plotting persistence landscapes.

"""

import matplotlib.pyplot as plt
import numpy as np
from PersistenceLandscape import PersistenceLandscape
from operator import itemgetter
from matplotlib import cm

def plot_landscape(landscape: PersistenceLandscape,
                   num_steps: int = 3000,
                   color=cm.viridis,
                   alpha=0.8,
                   padding: float = 0.1,
                   depth_padding: float = 0.5):
    """
    A plot of the persistence landscape.
    
    Warning: This function is quite slow, especially for large landscapes.
    """
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    landscape.compute_landscape()
    min_crit_pt = min(landscape[0], key=itemgetter(0))[0]
    max_crit_pt = max(landscape[0], key=itemgetter(0))[0]
    max_crit_val = max(landscape[0],key=itemgetter(1))[1]
    domain = np.linspace(min_crit_pt-padding*0.1, max_crit_pt+padding*0.1, num=num_steps)
    for depth, l in enumerate(landscape):
        xs, zs = zip(*l)
        image = np.interp(domain, xs, zs)
        for x, z in zip(domain,image):
            if z == 0.: continue
            ax.plot(
                [x,x],
                [depth_padding*depth,depth_padding*depth],
                [0,z],
                linewidth=0.5,
                alpha=alpha,
                c=color(z/max_crit_val))
    
    #ax.set_xlabel('X')
    #ax.set_ylabel('depth')
    #ax.set_zlabel('Z')
    #ax.set_xlim(min_crit_pt-padding, max_crit_pt+padding)
    #ax.set_ylim(0, depth_padding*landscape.max_depth+1)
    # ax.set_zlim(0, max_crit_val+padding)
    ax.view_init(10,90)
    plt.show()

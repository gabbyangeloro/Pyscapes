"""
A bunch of examples for timing the different methods. 
"""

# import tadasets ## the proper way of doing this
import numpy as np
from timeit import default_timer as timer


#%% Helper functions
""" 
The following code is copied from the tadasets repo. Do a proper import of
the package once installed.
"""
    

def sphere(n=100, r=1, noise=None, ambient=None):
    """
        Sample `n` data points on a sphere.
    Parameters
    -----------
    n : int
        Number of data points in shape.
    r : float
        Radius of sphere.
    ambient : int, default=None
        Embed the sphere into a space with ambient dimension equal to `ambient`. The sphere is randomly rotated in this high dimensional space.
    """

    theta = np.random.random((n,)) * 2.0 * np.pi
    phi = np.random.random((n,)) * np.pi
    rad = np.ones((n,)) * r

    data = np.zeros((n, 3))

    data[:, 0] = rad * np.cos(theta) * np.cos(phi)
    data[:, 1] = rad * np.cos(theta) * np.sin(phi)
    data[:, 2] = rad * np.sin(theta)


    if noise: 
        data += noise * np.random.randn(*data.shape)

    #if ambient:
    #    data = embed(data, ambient)

    return data


def torus(n=100, c=2, a=1, noise=None, ambient=None):
    """
    Sample `n` data points on a torus.
    Parameters
    -----------
    n : int
        Number of data points in shape.
    c : float
        Distance from center to center of tube.
    a : float
        Radius of tube.
    ambient : int, default=None
        Embed the torus into a space with ambient dimension equal to `ambient`. The torus is randomly rotated in this high dimensional space.
    """

    assert a <= c, "That's not a torus"

    theta = np.random.random((n,)) * 2.0 * np.pi
    phi = np.random.random((n,)) * 2.0 * np.pi

    data = np.zeros((n, 3))
    data[:, 0] = (c + a * np.cos(theta)) * np.cos(phi)
    data[:, 1] = (c + a * np.cos(theta)) * np.sin(phi)
    data[:, 2] = a * np.sin(theta)

    if noise: 
        data += noise * np.random.randn(*data.shape)

    #if ambient:
    #    data = embed(data, ambient)

    return data


def swiss_roll(n=100, r=10, noise=None, ambient=None):
    """Swiss roll implementation
    Parameters
    ----------
    n : int 
        Number of data points in shape.
    r : float
        Length of roll
    ambient : int, default=None
        Embed the swiss roll into a space with ambient dimension equal to `ambient`. The swiss roll is randomly rotated in this high dimensional space.
    References
    ----------
    Equations mimic [Swiss Roll and SNE by jlmelville](https://jlmelville.github.io/smallvis/swisssne.html)
    """

    phi = (np.random.random((n,)) * 3 + 1.5) * np.pi
    psi = np.random.random((n,)) * r

    data = np.zeros((n, 3))
    data[:, 0] = phi * np.cos(phi)
    data[:, 1] = phi * np.sin(phi)
    data[:, 2] = psi

    if noise: 
        data += noise * np.random.randn(*data.shape)

    #if ambient:
    #    data = embed(data, ambient)

    return data


def infty_sign(n=100, noise=None):
    """Construct a figure 8 or infinity sign with :code:`n` points and noise level with :code:`noise` standard deviation.
    Parameters
    ============
    n: int
        number of points in returned data set.
    noise: float
        standard deviation of normally distributed noise added to data.
    
    """


    t = np.linspace(0, 2*np.pi, n+1)[0:n]
    X = np.zeros((n, 2))
    X[:, 0] = np.cos(t)
    X[:, 1] = np.sin(2*t)

    if noise:
        X += noise * np.random.randn(n, 2)
    
    return X


#%% Generate the data sets

infty_sgn = infty_sign()
sphere = sphere(n=500, r=10)
swiss_roll = swiss_roll(n=500, r=10)
torus = torus(n=200)

#%% Compute persistent homology

from ripser import Rips

rips = Rips()
start_infty = timer()
diag_infty = rips.fit_transform(infty_sgn)
end_infty = timer()
print("Computing persistent homology of infinty symbol "
      f"took {end_infty - start_infty}.")
start_sphere = timer()
diag_sphere = rips.fit_transform(sphere)
end_sphere = timer()
print("Computing persistent homology of sphere "
      f"took {end_sphere - start_sphere}.")
start_swiss = timer()
diag_swiss = rips.fit_transform(swiss_roll)
end_swiss = timer()
print("Computing persistent homology of swiss roll "
      f"took {end_swiss - start_swiss}.")
start_torus = timer()
diag_torus = rips.fit_transform(torus)
end_torus = timer()
print("Computing persistent homology of torus "
      f"took {end_torus - start_torus}.")

# Let's see what they look like

rips.plot(diag_infty)
rips.plot(diag_sphere)
rips.plot(diag_swiss)
rips.plot(diag_torus)

#%% Compute landscapes


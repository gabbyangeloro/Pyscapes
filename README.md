## PyLandscapes: Persistence landscapes in python

This packages implements persistence landscapes in a user-friendly
fashion in python. Persistence landscapes are a vectorization scheme for
persistent homology, providing a robust set of feature maps. 

Persistence Landscapes were introduced in 
[Bubenik](https://jmlr.org/papers/volume16/bubenik15a/bubenik15a.pdf).
These provide a functional representation of persistence diagrams amenable
to statistical analysis. They have been proven to be very useful in a variety
of empirical and theoretical applications. See the examples provided 
in [Bubenik](https://arxiv.org/abs/1810.04963).

Our implementation follows the algorithms provided in 
[Bubenik, Dlotko](https://www.sciencedirect.com/science/article/abs/pii/S0747717116300104).
Dlotko has also implemented many of these algorithms in C++ directly in the
Persistence Landscape Toolbox, available 
[here](https://www.math.upenn.edu/~dlotko/persistenceLandscape.html).


### Why persistence landscapes?
- They were one of the first vectorization schemes introduced for persistent
homology, yet there aren't any implementations in python TDA libraries, 
e.g., scikit-tda.
- They are (essentially) non-parametric feature maps. Hence they do not
require any hyperparameter tuning.
- They have already been shown to be quite successful in a variety of 
applications.

### Goals of this implementation
- To interface cleanly with existing libraries for computing persistent
homology (e.g., [ripser.py](https://github.com/scikit-tda/ripser.py)).
- To interface cleanly with existing libraries for machine learning
(e.g., [scikit-learn](https://scikit-learn.org/stable/index.html)).


### Example
While the code is not yet ready for public consumption, here we give a 
brief overview of how it can be used.

#### Exact vs Grid
We provide two different implementations of Persistence Landscapes:

- `PersistenceLandscapeExact` provides an exact implementation. All methods 
and computations done in this class are as accurate as the floating point
arithmetic of Python. In particular, there are **no approximations** in
our calculations. Instantiating these are fast but arithmetic operations,
such as summing and averaging can be quite slow because of this. 

- `PersistenceLandscapeGrid` provides an approximate implementation. These
require the user to specify the parameters of an equally spaced grid
(`start`, `stop`, and `num_steps`) at which each landscape will be sampled at.
This approximation allows us to easily embed the landscape in a `num_steps`-dimensional
real vector space. Instantiating these can be slower than their exact counterparts due
to this sampling. However, arithmetic operations tend to be much faster because
of this approximation, together with Numpy's vectorized operations.

Examples of both are provided below.

#### Sample code

```python
import numpy as np
from ripser import ripser
from PersistenceLandscapeGrid import PersistenceLandscapeGrid

data = np.random.random_sample((200,2)) # generate random points
diagrams = ripser(data)['dgms'] # compute persistent homology
M = PersistenceLandscapeGrid(diagrams=diagrams, homological_degree=1)
M.compute_landscape() # Compute the landscape
```
Computing the actual functions that comprise a persistence landscape can 
be computationally intensive, so we
don't compute them upon instantiation. Instead they're only computed 
after the `compute_landscape` method is called, serving as an initialization 
method. The set of critical pairs is stored in the `critical_pairs` attribute.

Basic arithmetic operations are implemented. This allows for
arbitrary linear combinations of persistence landscapes, including
averages. Norms are implemented for quantifying differences and to
ease the use of permutation tests.
```python
L = 2*M
J = M + M
K = M/5
L.p_norm(p=2)
L.infinity_norm() # 0.0311
```


Persistence Landscapes can also be plotted.
```python
from auxiliary import plot_landscape

plot_landscape(M)
```
<p float="left">
<img src="docs/PL_rand_sample.png" width = 45% />
<img src="docs/PL_bc_pl.png" width=45%>
</p>

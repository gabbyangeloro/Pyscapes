## Persistence landscapes in python

This repository aims to implement persistence landscapes in a user-friendly
fashion in python. Persistence landscapes are a vectorization scheme for
persistent homology, providing a robust set of feature maps. 

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

```python
import numpy as np
from ripser import ripser
from PersistenceLandscape import PersistenceLandscape

data = np.random.random_sample((200,2)) # generate random points
diagrams = ripser(data)['dgms'] # compute persistent homology
M = PersistenceLandscape(diagrams=diagrams, homological_degree=1)
M.compute_landscape() # Compute the landscape
```
Computing persistence landscapes can be computationally intensive, so we
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
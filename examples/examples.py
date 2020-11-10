
#%%
import numpy as np
from sklearn.datasets import load_wine
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

from visualization import plot_landscape
from ripser import ripser
from persim import plot_diagrams
from PersistenceLandscapeExact import PersistenceLandscapeExact
#%%

wine_data, wine_target = load_wine(return_X_y=True)
bc_data, bc_target = load_breast_cancer(return_X_y=True)

scaler = StandardScaler()
wine_data_scl = scaler.fit_transform(wine_data)
bc_data_scl = scaler.fit_transform(bc_data)

wine_dgms = ripser(wine_data_scl)['dgms']
bc_dgms = ripser(bc_data_scl)['dgms']
plot_diagrams(wine_dgms, show=True)
plot_diagrams(bc_dgms, show=True)
#%%

wine_pl = PersistenceLandscapeExact(wine_dgms, homological_degree=1)
bc_pl = PersistenceLandscapeExact(bc_dgms, homological_degree=1)

wine_pl.compute_landscape()
bc_pl.compute_landscape()

#%% 
plot_landscape(wine_pl, title='Wine persistence landscape')
plot_landscape(bc_pl, title='Breast cancer landscape')
#%%
data = np.random.random_sample((200,2))
diagrams = ripser(data)['dgms']
# rips.plot(diagrams)

# pl = PL(homological_degree=1][]
# landscape = pl.fit_transform(diagrams)

L = PersistenceLandscapeExact(diagrams,homological_degree=1)
L.compute_landscape(verbose=True)
L.p_norm(p=2)
#%%
random_data = np.random.random((100, 2))
diagrams = ripser(data)['dgms']
#plot_diagrams(diagrams, show=True)

M = PersistenceLandscapeExact(diagrams, homological_degree=1)
M.compute_landscape()
"""
Script to re-create results from Bubenik/Dlotko sphere experiment.
We will sample 100 points from the 2-sphere and the 3-sphere, construct and
compute VR PH (in degrees 1 and 2), construct landscapes. 
This entire process is repeated 1000 times. In each homological degree, we will
average over these 1000 runs to get a total of 4 average persistence landscapes,
indexed on the dimension of the sphere and degree of homology. 

Fix the degree of homology for a moment (e.g., homological_degree = 1).
We take the supremum norm of the difference of 
the avg PL in dim-1 for S^2 and the avg PL in dim-1 for S^3.
This sup norm is the true difference. We then shuffle the labels of `S^2` versus `S^3`
among these 2000 landscapes, recompute averages with respect to the new labelling,
and take the sup norm of the difference of these averages. If the sup norm of the 
modified shuffling is larger than the sup norm of the true difference, we consider
this shuffling significant and add one to `significant`. The p-value is then 
`significant` divided by the number of times we do the shuffling, which is 10,000 times.
"""

#%% Imports
import numpy as np
import random

from ripser import ripser
from PersistenceLandscape import PersistenceLandscape
from visualization import plot_landscape

from tadasets import dsphere

#%% Construct the list of 1000 landscapes from randomly sampled points.
sph2_pl1_list = []
sph2_pl2_list = []
sph3_pl1_list = []
sph3_pl2_list = []

for i in range(99):
    sph2_pts = dsphere(n=100, d=2, r=1)
    sph2_dgm = ripser(sph2_pts, maxdim=2)['dgms']
    
    sph3_pts = dsphere(n=100, d=3, r=1)
    sph3_dgm = ripser(sph3_pts, maxdim=2)['dgms']
    
    sph2_pl1 = PersistenceLandscape(diagrams=sph2_dgm, homological_degree=1)
    sph2_pl1.compute_landscape()
    sph2_pl1_list.append(sph2_pl1)
    sph2_pl2 = PersistenceLandscape(diagrams=sph2_dgm, homological_degree=2)
    sph2_pl2.compute_landscape
    sph2_pl2_list.append(sph2_pl2)
    sph3_pl1 = PersistenceLandscape(diagrams=sph3_dgm, homological_degree=1)
    sph3_pl1.compute_landscape()
    sph3_pl1_list.append(sph3_pl1)
    sph3_pl2 = PersistenceLandscape(diagrams=sph3_dgm, homological_degree=2)
    sph3_pl2.compute_landscape()
    sph3_pl2_list.append(sph3_pl2)
    
#%% Construct the true average landscape
avg_sph2_pl1 = PersistenceLandscape(diagrams=sph2_dgm, homological_degree=1)
avg_sph2_pl1.compute_landscape()
avg_sph3_pl1 = PersistenceLandscape(diagrams=sph3_dgm, homological_degree=1)
avg_sph3_pl1.compute_landscape()

for i in range(99):
    avg_sph2_pl1 += sph2_pl1_list[i]
    avg_sph3_pl1 += sph3_pl1_list[i]

avg_sph2_pl1=avg_sph2_pl1/100.
avg_sph3_pl1=avg_sph3_pl1/100.

true_diff = (avg_sph2_pl1 - avg_sph3_pl1).sup_norm()

#%% Run the permutation test
# We do stratified shuffling, so each new group will still have 1000 entries each. This
# is what is done in the Bubenik/Dlotko paper.
# This could be done with sklearn.model_selection.permutation_test_score, but
# we don't have the transformer implemented yet.

comb_pl_list = sph2_pl1_list + sph3_pl1_list
significant = 0

for run in range(1000):
    A_indices = random.sample(range(200), 100)
    B_indices = [_ for _ in range(200) if _ not in A_indices]
    
    A_pl_list = comb_pl_list[A_indices]
    B_pl_list = comb_pl_list[B_indices]
    
    A_sum = A_pl_list[0]
    B_sum = B_pl_list[0]
    for i in range(99):
        A_sum += A_pl_list[i+1]
        B_sum += B_pl_list[i+1]
    
    A_avg = A_pl_list/100.
    B_avg = B_pl_list/100.
    
    AB_diff = A_avg - B_avg
    if (AB_diff.sup_norm() > true_diff): signficant += 1

#%%
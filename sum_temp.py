"""
Sum two piecewise linear functions. Each is expressed as a list
of their critical pairs.
"""
import numpy as np
from scipy.interpolate import interp1d


def sum_landscapes(A, B):
    """ Sum two landscapes A and B, thought of as lists containing their
    critical pairs.
    """

    # concatenate the lists
    L = [[a, b, 0] for [a, b] in A] + [[a, b, 1] for [a, b] in B]
    # sort the new list according to increasing a
    L.sort()
    idA, idB = -1, -1
    # Main for loop
    for i, (a, b, f) in enumerate(L):
        if f == 0 and idB == -1:
            # The critical pair is in A and list B hasn't started yet.
            # The list L is fine so far: do nothing but increment the index of A.
            idA += 1
            continue
        if f == 1 and idA == -1:
            # Critical pair in B and list A hasn't started yet.
            # The list L is fine so far: do nothing but increment the index of B.
            idB += 1
            continue
        if idA == len(A) - 1 or idB == len(B) - 1:  
            # we've run out of indices and
            # everything else in the list should be fine.
            break
        if a == L[i+1][0]:
            # There is a tie: two critical pairs have the same x-coordinate.
            # Sum their y-values, remove duplicate entry, and
            # increment both list counters.
            b_new = b + L[i+1][1]
            L[i] = [a, b_new]
            del L[i+1]
            idA += 1
            idB += 1
            continue
        if f == 0:  # current critical point lies in A
            # Add the interpolation of B to the critical value in A
            b_new = b + interp1d([B[idB][0], B[idB+1][0]],
                                 [B[idB][1], B[idB+1][1]])(a)
            L[i] = [a, b_new]
            idA += 1
        else:  # f == 1, so current critical point lies in B
            # same as before
            b_new = b + interp1d([A[idA][0], A[idA+1][0]],
                                 [A[idA][1],A[idA+1][1]])(a)
            L[i] = [a, b_new]
            idB += 1
    return L

A = [ [0,0], [4,2], [5,1.5], [7, 2.5], [9, 0] ]
B = [ [1,0], [2,2], [3,3], [6, 1.5], [8,0]]
f = sum_landscapes(A, B)

C = [ [0,0], [5,3], [7,9], [15,1], [20,0]]
D = [ [1,0], [2,10], [3,9], [4,6], [5,1], [7,0]]
g = sum_landscapes(C, D)
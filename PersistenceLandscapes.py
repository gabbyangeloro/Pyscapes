"""
Define Persistence Landscapes function as a class
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class PersistenceLandscapes(BaseEstimator, TransformerMixin):
    ''' Persistence Landscape class. 

    Parameters
    -----------

    diagrams : A nested list of numpy arrays, e.g., [array( array([:]), array([:]) ),..., array()]
        Each entry in the list corresponds to a single homological degree
        Each array represents the birth death pairs for a homology degree.
        Inside each homology degree array are arrays representing birth death pairs.
        Expecting output from ripser: ripser(data_user)['dgms']
        
    homological_degree : int
        represents the homology degree of the persistence diagram.

    Methods
    ------
    landscape : returns persistence landscape associated to persistence diagram
        for given homology degree
    graph : graphs persistence landscapes
    get_kth_landscape : returns the kth landscape for a given homology degree

    '''

    # example = [np.array([ [1.0, 5.0], [2.0, 8.0], [3.0, 4.0], [5.0, 9.0], [6.0, 7.0] ])]

    def __init__(self, diagrams: list, homological_degree: int = -1):
        if isinstance(homological_degree, int) == False:
            raise TypeError(f'homological_degree must be an integer, not '
                    '{type(homological_degree)}.')
        # if homological_degree < 0:
            # raise ValueError('homological_degree must be positive')
        if isinstance(diagrams,list) == False:
            raise TypeError('diagrams must be a list')
        self.diagrams = diagrams
        self.homological_degree = homological_degree
        self.cache = {}
        
        
    def fit(self):
        return self

    def transform(self)
        pass


    ### Turn this into the transform class
    def construct_landscapes_exact(self, verbose: bool = False) -> dict:
        '''
        Parameters
        -----------
        verbose: bool
            prints what landscape is being computed

        Returns
        --------
        L_dict : dict
            Keys are L1,..., Lk and values are respective function in
            persistence landscape represented as arrays.

        '''
        # check if landscapes were already computed
        verboseprint = print if verbose else lambda *a, **k: None

        if self.cache:

            verboseprint('cache was full and stored value was returned')
            return self.cache

        A = self.data[self.homology_degree]
        k = 0
        size_landscapes= np.array([])
        L_dict = {}


        # Sort A: read from right to left inside ()
        ind =  np.lexsort((-A[:,1], A[:,0]))
        A = A[ind]

        while len(A) != 0:
            verboseprint(f'computing landscape {k+1}...')

            L = np.array([])

            # add a 0 element to begin count of lamda_k
            size_landscapes = np.append(size_landscapes, [0])

            # pop first term
            bd, A = A[0], A[1:len(A)]
            b, d = bd

            # outer brackets for start of L_k
            L = np.insert(L, len(L), np.array([-np.inf, 0]) , axis = 0)
            L = np.insert(L, len(L), np.array([b, 0]) , axis = 0)
            L = np.insert(L, len(L), np.array([(b+d)/2, (d-b)/2]) , axis = 0)

            # increase size of landscape k by 3
            size_landscapes[k] += 3

            while (L[-1] != [np.inf, 0]).all():


                # Check if d is greater than all remaining pairs
                if (d  > A[:,1]).all(): # check dont need vector

                    # add to end of L_k
                    L = np.insert(L, len(L), np.array( [d,0] ), axis = 0)
                    L = np.insert(L, len(L), np.array( [np.inf, 0] ), axis = 0)
                    size_landscapes[k] += 2


                else:
                    # set (b', d')  to be the first term so that d' > d
                    for i in range(len(A)):
                        if A[i][1] > d:
                            # pop (b', d')

                            ind1 = [k for k in range(len(A) ) if k != i]

                            bd_prime, A = A[i], A[ind1]

                            b_prime, d_prime = bd_prime
                            break


                    # Case I
                    if b_prime > d:
                        L = np.insert(L, len(L), np.array([d, 0] ), axis = 0)
                        size_landscapes[k] += 1


                    # Case II
                    if b_prime >= d:
                        L = np.insert(L, len(L), np.array( [b_prime, 0] ), axis = 0)
                        size_landscapes[k] += 1


                    # Case III
                    else:
                        L = np.insert(
                            L, len(L), np.array([(b_prime + d)/2,
                                                 (d-b_prime)/2]), axis = 0 )
                        size_landscapes[k] += 1


                        # Push (b', d) into A in order
                        # find the first b_i in A so that b'<= b_i
                        for i in range(len(A)):
                            if b_prime <= A[i][0]:
                                ind2 = i # index to push (b', d) if b' != b_i
                                break

                        # if b' = b_i
                        # move index to the right one for every d_i so that d < d_i
                        if b_prime == A[ind2][0]:
                            A_i = A[ A[:,0] == b_prime]

                            for j in range(len(A_i)):
                                if d < A_i[j][1]:
                                    ind2 = ind2 + 1


                        A = np.insert(A, ind2 ,np.array([b_prime, d]), axis = 0)


                    L = np.insert(L, len(L), np.array([(b_prime + d_prime)/2,
                                                       (d_prime-b_prime)/2] ), axis = 0 )
                    size_landscapes[k] += 1

                    b,d = b_prime, d_prime # Set (b',d')= (b, d)

            # add L_k to dict
            # reshpae to pairs and leave off infinity terms
            L_dict[f'L{k+1}'] = L.reshape( (int(len(L)/2),2) )[1:-1]
            k += 1

        self.cache = L_dict
        verboseprint('cache was empty and algorthim was executed')
        return L_dict

    '''
    def plot_diagrams(self):
        # check if landscapes were already computed
        if len(self.cache) != 0:
            landscapes = self.cache[0]
            return graph(landscapes)

        else:
            landscapes = self.landscapes()
            return graph(landscapes)
    '''

    def __repr__(self):
        return f'The persistence landscapes of data for the {self.homology_degree}th homology'

    # pick out kth persistence landscape
    def get_kth_landscape(self, k):
        pass
        #return self[k]

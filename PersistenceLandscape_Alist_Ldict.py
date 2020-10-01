"""
Define Persistence Landscapes function as a class
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

### TransformerMixin gives fit_transform for free
### BaseEstimator gives get_params and set_params methods.
### We might not need BaseEstimator...It's useful when the transformer
### has hyperparameters to tune, for gridsearchCV etc.
class PersistenceLandscape_Alist_Larray(BaseEstimator, TransformerMixin):
    ''' Persistence Landscape class.

    Parameters
    ----------
    diagrams : A nested list of numpy arrays, e.g., [array( array([:]), array([:]) ),..., array()]
        Each entry in the list corresponds to a single homological degree
        Each array represents the birth death pairs for a homology degree.
        Inside each homology degree array are arrays representing birth death pairs.
        Expecting output from ripser: ripser(data_user)['dgms']

    homological_degree : int
        represents the homology degree of the persistence diagram.

    Methods
    -------
    landscape : returns persistence landscape associated to persistence diagram
        for given homology degree

    transform : graphs persistence landscapes

    get_kth_landscape : returns the kth landscape for a given homology degree

    '''

    example = [np.array([ [1.0, 5.0], [2.0, 8.0], [3.0, 4.0], [5.0, 9.0], [6.0, 7.0] ])]

    def __init__(self, diagrams: list, homological_degree: int = -1):
        if isinstance(homological_degree, int) == False:
            raise TypeError('homological_degree must be an integer')
        # if homological_degree < 0:
            # raise ValueError('homological_degree must be positive')
        if isinstance(diagrams,list) == False:
            raise TypeError('diagrams must be a list')
        ### Do we need to put additional checks here? Make sure its a list of numpy
        ### arrays? etc?
        self.diagrams = diagrams
        self.homological_degree = homological_degree
        self.cache = {}

    def __repr__(self):
        return ('The persistence landscapes of diagrams in homological '
        f'degree {self.homological_degree}')

    def fit(self):
        return self

    def transform(self, verbose:bool = False, idx:int = 0)-> dict:
        ''' Compute the persistence landscape of self.diagrams.

        Parameters
        ----------
        verbose: bool
            If true, progress messages are printed during computation.

        Returns
        -------
        L_dict : dict
            The keys of L_dict are L1, ..., Lk and the corresponding value is 
            each corresponds to critical values are respective function in
            persistence landscape represented as arrays.

        '''

        verboseprint = print if verbose else lambda *a, **k: None

        # check if landscapes were already computed
        if self.cache:
            verboseprint('cache was not empty and stored value was returned')
            return self.cache

        A = self.diagrams[self.homological_degree]
        # change A into a list
        A = list(A)
        # change inner nparrays into lists
        for i in range(len(A)):
            A[i] = list(A[i])
        
        landscape_idx = 0
        size_landscapes= np.array([])
        L_dict = {}

        # Sort A: read from right to left inside ()
        A = sorted(A, key = lambda x: [x[0], -x[1]])

        while len(A) != 0:
            verboseprint(f'computing landscape index {landscape_idx+1}...')

            L = np.array([])

            # add a 0 element to begin count of lamda_k
            size_landscapes = np.append(size_landscapes, [0])

            # pop first term
            b, d = A.pop(0)

            # outer brackets for start of L_k
            L = np.insert(L, len(L), np.array([-np.inf, 0]) , axis = 0)
            L = np.insert(L, len(L), np.array([b, 0]) , axis = 0)
            L = np.insert(L, len(L), np.array([(b+d)/2, (d-b)/2]) , axis = 0)

            # increase size of landscape k by 3
            size_landscapes[landscape_idx] += 3

            while (L[-1] != [np.inf, 0]).all():


                # Check if d is greater than all remaining pairs
                # prints list [False, True, ....]
                # if false notin list is true than d > all 2nd coordinates of A
                if False not in [d> item[1] for item in A]:

                    # add to end of L_k
                    L = np.insert(L, len(L), np.array( [d,0] ), axis = 0)
                    L = np.insert(L, len(L), np.array( [np.inf, 0] ), axis = 0)
                    size_landscapes[landscape_idx] += 2


                else:
                    # set (b', d')  to be the first term so that d' > d
                    for i, item in enumerate(A):
                        if item[1] > d:
                            b_prime, d_prime = A.pop(i)
                            break


                    # Case I
                    if b_prime > d:
                        L = np.insert(L, len(L), np.array([d, 0] ), axis = 0)
                        size_landscapes[landscape_idx] += 1


                    # Case II
                    if b_prime >= d:
                        L = np.insert(L, len(L), np.array( [b_prime, 0] ), axis = 0)
                        size_landscapes[landscape_idx] += 1


                    # Case III
                    else:
                        L = np.insert(
                            L, len(L), np.array([(b_prime + d)/2,
                                                 (d-b_prime)/2]), axis = 0 )
                        size_landscapes[landscape_idx] += 1


                        # Push (b', d) into A in order
                        # find the first b_i in A so that b'<= b_i
                        for i in range(len(A)):
                            if b_prime <= A[i][0]:
                                ind = i # index to push (b', d) if b' != b_i
                                break

                        # if b' = b_i
                        # move index to the right one for every d_i such that d < d_i
                        if b_prime == A[ind][0]:
                            A_i = [item for item in A if item[0] == b_prime ]

                            for j in range(len(A_i)):
                                if d < A_i[j][1]:
                                    ind = ind + 1


                        A.insert(ind ,[b_prime, d])


                    L = np.insert(L, len(L), np.array([(b_prime + d_prime)/2,
                                                       (d_prime-b_prime)/2] ), axis = 0 )
                    size_landscapes[landscape_idx] += 1

                    b,d = b_prime, d_prime # Set (b',d')= (b, d)

            # add L_k to dict
            # reshpae to pairs and leave off infinity terms
            L_dict[f'L{landscape_idx+1}'] = L.reshape( (int(len(L)/2),2) )[1:-1]
            landscape_idx += 1

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

    ### If we want landscape by index, then we probably need to
    ### refactor the above code. This could get complicated so maybe
    ### we don't worry about it now. In a perfect world, we'd have the
    ### following setup: the PersistenceLandscapes class itself would
    ### have a boolean flag that tracks whether the landscape computation
    ### has finished yet, since we can't check by the length of a list
    ### or anything. We then factor out one iteration of the transform
    ### code, and all other methods would call a while loop on it. Once
    ### we've computed out to the landscape we need, we return it. Any
    ### other method would first check if the cache has that appropriate
    ### entry, then either return or resume the computation.
    def get_landscape_by_index(self, idx: int) -> list:
        """ Returns the landscape function specified by idx.

        Parameters
        ----------
        idx: int
            The index of the desired landscape function.

        Returns
        --------
        The landscape function of index idx.
        """
        if self.cache:
            return self.cache[f'L{idx}']
        else:
            return self.transform()[f'L{idx}']
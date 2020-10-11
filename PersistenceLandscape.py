"""
Define Persistence Landscape class.
"""
import numpy as np
from auxiliary import union_crit_pairs


class PersistenceLandscape:
    """Persistence Landscape class.

    Parameters
    ----------
    diagrams : list of numpy arrays, optional
        A nested list of numpy arrays, e.g., [array( array([:]), array([:]) ),..., array()]
        Each entry in the list corresponds to a single homological degree.
        Each array represents the birth death pairs for a homology degree.
        Inside each homology degree array are arrays representing birth death pairs.
        Expecting output from ripser: ripser(data_user)['dgms']. Only
        one of diagrams or critical pairs should be specified.

    homological_degree : int
        Represents the homology degree of the persistence diagram.

    critical_pairs: list, optional
        A list of critical pairs (points, values) for specifying a persistence
       landscape. These do not necessarily have to arise from a persistence
       diagram. Only one of diagrams or critical pairs should be specified.


    Methods
    -------
    landscape : returns persistence landscape associated to persistence diagram
        for given homology degree

    transform : graphs persistence landscapes

    get_kth_landscape : returns the kth landscape for a given homology degree

    """

    example = [np.array([[1.0, 5.0], [2.0, 8.0], [3.0, 4.0], [5.0, 9.0], [6.0, 7.0]])]

    def __init__(
        self, diagrams: list = [], homological_degree: int = 0, critical_pairs: list = []
    ):
        if isinstance(homological_degree, int) == False:
            raise TypeError("homological_degree must be an integer")
        # if homological_degree < 0:
        # raise ValueError('homological_degree must be positive')
        if isinstance(diagrams, list) == False:
            raise TypeError("diagrams must be a list")
        ### Do we need to put additional checks here? Make sure its a list of numpy
        ### arrays? etc?
        self.homological_degree = homological_degree
        if critical_pairs:
            self.critical_pairs = critical_pairs
            self.diagrams = []
        else:
            self.critical_pairs = []
            self.diagrams = diagrams

    def __repr__(self):
        return (
            "The persistence landscapes of diagrams in homological "
            f"degree {self.homological_degree}"
        )

    def __neg__(self):
        self.compute_landscape( )
        return PersistenceLandscape(homological_degree=self.homological_degree,
                                    critical_pairs=[ [[a,-b] for a, b in
                                                    self.critical_pairs[i]]
                                                    for i in range(len(self.critical_pairs))])

    def __add__(self, other):
        # This requires a list implementation as written.
        if self.homological_degree != other.homological_degree:
            raise ValueError("homological degrees must match")
        return PersistenceLandscape(
            critical_pairs=union_crit_pairs(self, other),
            homological_degree=self.homological_degree
            )

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other: int):
        self.compute_landscape()
        return PersistenceLandscape(
            critical_pairs=[[(a, other*b) for a, b in self.critical_pairs[i]] 
                            for i in range(len(self.critical_pairs))],
            homological_degree=self.homological_degree)
    
    def __rmul__(self,other: int):
        return self.__mul__(other)

    def __truediv__(self, other: int):
        return self*(1.0/other)

    # Indexing, slicing
    def __getitem__(self, key: slice) -> list:
        """
        Returns a list of critical pairs corresponding in range specified by 
        depth.

        Parameters
        ----------
        key : slice object.

        Returns
        -------
        list
            The critical pairs of the landscape function corresponding
            to depths given by key.
        """
        self.compute_landscape()
        return self.critical_pairs[key]
    
    # TODO: Fix the following.
    # def depth(self, key: slice) -> list:
    #     """
    #    Returns a list of critical pairs of 
    #    """
    #    self.compute_landscape()
    #    return self.critical_pairs[key]

    def compute_landscape(self, verbose: bool = False) -> dict:
        """Compute the persistence landscapes of self.diagrams.

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

        """

        verboseprint = print if verbose else lambda *a, **k: None

        # check if landscapes were already computed
        if self.critical_pairs:
            verboseprint('cache was not empty and stored value was returned')
            return self.critical_pairs

        A = self.diagrams[self.homological_degree]    
        # change A into a list
        A = list(A)
        # change inner nparrays into lists
        for i in range(len(A)):
            A[i] = list(A[i])
        # store infitiy values 
        infty_bar = False
        if A[-1][1] == np.inf:
            A. pop(-1)
            infty_bar = True
            # TODO: Do we need this infty_bar variable?
     
        landscape_idx = 0
        L = []

        # Sort A: read from right to left inside ()
        A = sorted(A, key = lambda x: [x[0], -x[1]])

        while len(A) != 0:
            verboseprint(f'computing landscape index {landscape_idx+1}...')

            # add a 0 element to begin count of lamda_k
            #size_landscapes = np.append(size_landscapes, [0])

            # pop first term
            b, d = A.pop(0)
            verboseprint(f'(b,d) is ({b},{d})')

            # outer brackets for start of L_k
            L.append([ [-np.inf, 0], [b, 0], [(b+d)/2, (d-b)/2] ] ) # outer brackets for start of L_k

           
            while L[landscape_idx][-1] != [np.inf, 0]:
                # Check if d is greater than all remaining pairs
                # prints list [False, True, ....]
                # if false notin list is true than d > all 2nd coordinates of A
                if False not in [d> item[1] for item in A]:

                    # add to end of L_k
                    L[landscape_idx].extend([ [d,0], [np.inf, 0] ])

                else:
                    # set (b', d')  to be the first term so that d' > d
                    for i, item in enumerate(A):
                        if item[1] > d:
                            b_prime, d_prime = A.pop(i)
                            verboseprint(f'(bp,dp) is ({b_prime},{d_prime})')
                            break


                    # Case I
                    if b_prime > d:
                        L[landscape_idx].extend([ [d, 0] ])


                    # Case II
                    if b_prime >= d:
                        L[landscape_idx].extend([ [b_prime, 0] ])


                    # Case III
                    else:
                        L[landscape_idx].extend([ [(b_prime + d)/2, (d-b_prime)/2] ])

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


                    L[landscape_idx].extend([ [(b_prime + d_prime)/2, (d_prime-b_prime)/2] ])
                    #size_landscapes[landscape_idx] += 1

                    b,d = b_prime, d_prime # Set (b',d')= (b, d)

            landscape_idx += 1
        
        # self.critical_pairs = L
        verboseprint('cache was empty and algorthim was executed')
        # gets rid of infinity terms 
        # As written, this function shouldn't return anything, but rather 
        # update self.critical pairs. 
        self.critical_pairs = [item[1:-1] for item in L]
        #return [item[1:-1] for item in L]

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

    # If we want landscape by index, then we probably need to
    # refactor the above code. This could get complicated so maybe
    # we don't worry about it now. In a perfect world, we'd have the
    # following setup: the PersistenceLandscapes class itself would
    # have a boolean flag that tracks whether the landscape computation
    # has finished yet, since we can't check by the length of a list
    # or anything. We then factor out one iteration of the transform
    # code, and all other methods would call a while loop on it. Once
    # we've computed out to the landscape we need, we return it. Any
    # other method would first check if the cache has that appropriate
    # entry, then either return or resume the computation.

    def compute_landscape_by_depth(self, depth: int) -> list:
        """Returns the landscape function specified by idx.
        
        Parameters
        ----------
        idx: int
            The index of the desired landscape function.

        Returns
        --------
        The landscape function of index idx.
        """
        if self.critical_pairs:
            return self.critical_pairs[depth]
        else:
            return self.compute_landscape()[depth]

    def p_norm(self, p: int = 2) -> float:
        """Returns the L_{`p`} norm of self."""
        if p != 2:
            raise NotImplementedError()
        pass

    def infinity_norm(self) -> float:
        return max([critical[1] for critical in self.critical_pairs])

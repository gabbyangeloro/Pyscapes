"""
Auxilary functions for working with persistence diagrams.
"""

def death_vector(diagram:list, homologica_degree:int = 0):
    """ Returns the death vector in degree 0 for the persistence diagram.
    
    """
    if homologica_degree != 0:
        raise NotImplementedError("The death vector is not defined for "
                                  "homological degrees greater than zero.")
    pass

def linear_combination(landscapes: list, coeffs: list = [1.0/len(list) for _ 
                                                         in range(len(list))]):
    """ Compute a linear combination of landscapes.
    
    
    Parameters
    ----------
    landscapes : list of PersistenceLandscape objects.
        
    coeffs : list, optional.

    Returns
    -------
    None.

    """
    pass
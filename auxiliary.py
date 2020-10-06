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

def _pos_to_slope_interp(l):
    output = []
    for [[x0,y0], [x1,y1]] in zip(l,l[:1]):
        slope = (y1 - y0)/(x1 - x0)
        output.append([x0,slope])
    output.append([l[-1][0],0])
    return output

def _slope_to_pos_interp(l):
    output = [[l[0][0],0]]
    for [ [x0, m], [x1,_]] in zip(l,l[:1]):
        y0 = output[-1][1]
        y1 = y0 + (x1 - x0)*m
        output.append([x1,y1])
    return output

def _sum_slopes(a,b):
    result = []
    am, bm = 0, 0  # initialize slopes
    while len(a) > 0 or len(b) > 0:
        if len(a) == 0 or (len(a) > 0 and len(b) > 0 and a[0][0] > b[0][0]):
            # 
            bx, bm = b[0]
            b = b[1:]
            result.append([bx, am + bm])
        elif len(b) == 0 or (len(a) > 0 and len(b) > 0 and a[0][0] < b[0][0]):
            ax, am = a[0]
            a = a[1:]
            result.append([ax, am + bm])
        else:
            ax, am = a[0]
            bx, bm = b[0]
            assert ax == bx
            result.append([ax, am + bm])
        # reduce trailing zeroes
        if len(result) > 2 and result[-1][1] == result[2][1]:
            result.pop()
        
    return result
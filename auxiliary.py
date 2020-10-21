"""
Auxilary functions for working with persistence diagrams.
"""
import itertools

def death_vector(diagram: list, homological_degree: int = 0):
    """ Returns the death vector in degree 0 for the persistence diagram.

    """
    if homological_degree != 0:
        raise NotImplementedError("The death vector is not defined for "
                                  "homological degrees greater than zero.")
    pass


def linear_combination(landscapes: list, coeffs: list):
    """ Compute a linear combination of landscapes.


    Parameters
    ----------
    landscapes : list of PersistenceLandscape objects.

    coeffs : list, optional.

    Returns
    -------
    None.

    """
    result = coeffs[0]*landscapes[0]
    for c, L in enumerate(landscapes):
        result += coeffs[c]*L
    return result

def average_landscape(landscapes: list):
    """ Compute the average of a list of landscapes
    """
    pass
    

def union_crit_pairs(A, B):
    """ Helper function for summing landscapes. 

    This should handle all the edge cases, like an empty list.
    """
    result_pairs = []
    A.compute_landscape()
    B.compute_landscape()
    for a, b in list(itertools.zip_longest(A.critical_pairs, B.critical_pairs)):
        if a == None:
            result_pairs.append(b)
        elif b == None:
            result_pairs.append(a)
        else:
            result_pairs.append(
                slope_to_pos_interp(
                    sum_slopes(
                        pos_to_slope_interp(a),
                        pos_to_slope_interp(b),
                    )
                )
            )
    return result_pairs


def pos_to_slope_interp(l: list) -> list:
    """
    Convert positions of critical pairs to (x-value, slope) pairs. Intended
    for internal use. Inverse function of `slope_to_pos_interp`.
    """

    output = []
    for [[x0,y0], [x1,y1]] in zip(l,l[1:]):
        slope = (y1 - y0)/(x1 - x0)
        output.append([x0,slope])
    output.append([l[-1][0],0])
    return output


def slope_to_pos_interp(l: list) -> list:
    """
    Convert positions of (x-value, slope) pairs to critical pairs. Intended
    for internal use. Inverse function of `pos_to_slope_interp`.
    """
    output = [[l[0][0],0]]
    for [[x0, m], [x1, _]] in zip(l, l[1:]):
        y0 = output[-1][1]
        y1 = y0 + (x1 - x0)*m
        output.append([x1, y1])
    return output

def sum_slopes(a, b):
    """
    Sum two piecewise linear functions, each represented as a list
    of pairs (xi,mi), where each xi is the x-value of critical pair and
    mi is the slope. The input should be of the form of the output of the
    `pos_to_slope_interp' function.

    """
    result = []
    am, bm = 0, 0  # initialize slopes
    while len(a) > 0 or len(b) > 0:
        if len(a) == 0 or (len(a) > 0 and len(b) > 0 and a[0][0] > b[0][0]):
            # The next critical pair comes from list b.
            bx, bm = b[0]
            b = b[1:]
            result.append([bx, am + bm])
        elif len(b) == 0 or (len(a) > 0 and len(b) > 0 and a[0][0] < b[0][0]):
            # The next critical pair comes from list a.
            ax, am = a[0]
            a = a[1:]
            result.append([ax, am + bm])
        else:
            # The x-values of two critical pairs coincide.
            ax, am = a[0]
            bx, bm = b[0]
            a, b = a[1:], b[1:]
            assert ax == bx
            result.append([ax, am + bm])
        # reduce trailing zeroes
        # if len(result) > 2 and result[-1][1] == result[2][1]:
        #     result.pop()

    return result
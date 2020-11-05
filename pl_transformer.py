"""
    Implementation of scikit-learn transformers for persistence
    landscapes.
"""

from sklearn.base import BaseEstimator, TransformerMixin

# To get the following functionality to work, I think we need 
# to split off the compute landscape function from within the 
# PL class.

class PL_exact(BaseEstimator, TransformerMixin):
    """ A scikit-learn transformer class for exact persistence landscapes.
    """
    def __init__(self,homological_degree:int = 0):
        self.homological_degree = homological_degree
        
    def fit(self,X,y=None):
        return self
    
    def transform(self,X,y=None):
        # Add check that X is the output of a PH calculation.
        return X[self.homological_degree].compute_landscape()
    
class PL_grid(BaseEstimator, TransformerMixin):
    pass
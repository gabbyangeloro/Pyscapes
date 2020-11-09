"""
Define a base Persistence Landscape class
"""
from abc import ABC, abstractmethod
import numpy as np


class PersistenceLandscape(ABC):
    """
    The base Persistence Landscape class

    This is the base persistence landscape class and should not be
    called directly. The subclasses `PersistenceLandscapeGrid` or
    `PersistenceLandscapeExact` should instead be called.

    """

    def __init__(self, diagrams: list = [], homological_degree: int = 0) -> None:
        if not isinstance(homological_degree, int):
            raise TypeError("homological_degree must be an integer")
        if homological_degree < 0:
            raise ValueError('homological_degree must be positive')
        if not isinstance(diagrams, (list, tuple, np.array)):
            raise TypeError("diagrams must be a list, tuple, or numpy array")
        self.diagrams = diagrams
        self.homological_degree = homological_degree

    # We enforce landscapes have arithmetic and norms, 
    # this is the whole reason for using them.
    
    @abstractmethod
    def p_norm(self, p: int = 2) -> float:
        pass

    @abstractmethod
    def sup_norm(self) -> float:
        pass
        
    @abstractmethod
    def __add__(self, other):
        pass
    
    @abstractmethod
    def __neg__(self):
        pass
    
    @abstractmethod
    def __sub__(self, other):
        pass
    
    @abstractmethod
    def __mul__(self, other):
        pass
        
        

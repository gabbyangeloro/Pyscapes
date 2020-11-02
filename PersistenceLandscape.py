"""
Define a base Persistence Landscape class
"""
from abc import ABC

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
        if not isinstance(diagrams, list):
            raise TypeError("diagrams must be a list")
        self.diagrams = diagrams
        self.homological_degree = homological_degree

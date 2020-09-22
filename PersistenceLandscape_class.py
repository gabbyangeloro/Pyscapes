"""
Define Persistence Landscapes function as a class

"""

class PersistenceLandscapes:
    """
    doc string here
    """

    example = np.array([ [1.0, 5.0], [2.0, 8.0], [3.0, 4.0], [5.0, 9.0], [6.0, 7.0] ]) 
    
    def __init__(self, data, homologyDegree):
        self.data = data
        self.homologyDegree = homologyDegree


    def __iter__(self):
        

    def __next__(self):

    # pick out kth persistence landscape
    def get_kth_landscape(self, k):
        return self[k]

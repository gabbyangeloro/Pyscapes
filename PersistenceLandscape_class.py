"""
Define Persistence Landscapes function as a class

"""

class PersistenceLandscapes:
    """
    doc string here
    """


    
    def __init__(self, data, homologyDegree):
        self.data = data
        self.homologyDegree = homologyDegree
        self.example = np.array([ [1.0, 5.0], [2.0, 8.0], [3.0, 4.0], [5.0, 9.0], [6.0, 7.0] ]) 

    # code here

    def Landscapes(self):
        A = self.data[self.homologyDegree]
    


    def __repr__(self):

    # pick out kth persistence landscape
    def get_kth_landscape(self, k):
        return self[k]

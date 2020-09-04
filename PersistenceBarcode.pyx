# work.pyx 
# Import the low-level C declarations 
		
cimport cPersistenceBarcode 
# Importing functionalities from Python 
# and the C stdlib 
from cpython.pycapsule cimport *
from libc.stdlib cimport malloc, free 

# Wrappers 
def computeDistanceOfPointsInPlane( std::pair<double,double> p1 , std::pair<double,double> p2 ):
	return cPersistenceBarcode.computeDistanceOfPointsInPlane(p1 , p2 )
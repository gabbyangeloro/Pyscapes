# work.pyx 
# Import the low-level C declarations 

cimport cPersistenceClassifier

# Importing functionalities from Python and the C stdlib 
from cpython.pycapsule cimport *
from libc.stdlib cimport malloc, free

# Wrappers

def comaprePairsAccodringToTheSecondCoord( const std::pair< size_t , double >& f , const std::pair< size_t , double >& s ):
	return cPersistenceClassifier.comaprePairsAccodringToTheSecondCoord (size_t, f, size_t, s)
	
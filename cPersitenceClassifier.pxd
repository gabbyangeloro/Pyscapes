# Declaration of "external" C functions and structures
#extern keyword extends the function’s visibility to the whole program
#can be called anywhere in any of the files of the whole program


cdef extern from "PersitenceClassifier.h":

	bool comaprePairsAccodringToTheSecondCoord( const std::pair< size_t , double >& f , const std::pair< size_t , double >& s )
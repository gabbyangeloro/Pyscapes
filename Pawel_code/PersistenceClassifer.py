# importing libraries 
from distutils.core import setup 
from distutils.extension import Extension 
from Cython.Distutils import build_ext 

ext_modules = [Extension('PersistenceClassifer',
						['PersistenceClassifer.pyx'], 
						libraries=['PersistenceClassifer'],
						library_dirs=['.']
						)]	

setup(name = 'PersistenceClassifer extension module',
	cmdclass = {'build_ext': build_ext}, 
	ext_modules = ext_modules, 
	compiler_directive ={'language_level':3}
	)	
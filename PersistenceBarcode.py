from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension("PersistenceBarcode",
              sources=["PersistenceBarcode.pyx"],
              libraries=["m"]  # Unix-like specific
              )
]

setup(name="PersistenceBarcode",
      ext_modules=cythonize(ext_modules))
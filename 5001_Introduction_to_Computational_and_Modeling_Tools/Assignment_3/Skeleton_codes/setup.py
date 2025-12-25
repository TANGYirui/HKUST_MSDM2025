from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "laplace_solver_cython", 
        ["laplace_solver_cython.pyx"],  
        include_dirs=[np.get_include()],
        extra_compile_args=['-O3'],  
        # extra_link_args=['-fopenmp'], 
    )
]

setup(
    name="laplace_solver_cython",
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
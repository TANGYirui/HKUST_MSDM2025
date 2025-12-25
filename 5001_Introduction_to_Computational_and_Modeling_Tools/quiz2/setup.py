from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "check_percolate",
        ["check_percolate.pyx"],
	    extra_compile_args=["-O3", "-march=native", "-ffast-math"],
	    language="c++"
    )
]

setup(
    name="check_percolate",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
        }
    ),
)

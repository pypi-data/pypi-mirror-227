#!/usr/bin/env python

from distutils.core import setup

setup(name='credints',
      version='0.1',
      description='utility functions for creating credible intervals in pymc and sympy.stats (and possibly others)',
      author='Michael Latowicki',
      url='https://github.com/micklat/credints',
      packages=['credints'],
      license='BSD 3-clause',
      install_requires=['nbag', 'scipy', 'numpy'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
      ],
)

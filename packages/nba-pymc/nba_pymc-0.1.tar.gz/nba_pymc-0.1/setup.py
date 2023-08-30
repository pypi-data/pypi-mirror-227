#!/usr/bin/env python

from distutils.core import setup

setup(name='nba_pymc',
      version='0.1',
      description='wrap pymc with node constructors that magically guess the names of variables',
      author='Michael Latowicki',
      url='https://github.com/micklat/nba_pymc',
      packages=['nba_pymc'],
      license='BSD 3-clause',
      install_requires=['nbag', 'pymc'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
      ],
)

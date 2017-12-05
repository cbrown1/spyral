# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='spyral',
      version='1.0',
      description='Spyral: An implementation of the Spiral vocoder, useful for CI simulations',
      long_description='''\
      Paper: https://doi.org/10.1121/1.5009602
      Based on matlab code written by Jacques Grange, grangeja@cardiff.ac.uk. ''',
      author='Christopher Brown',
      author_email='cbrown1@pitt.edu',
      maintainer='Christopher Brown',
      maintainer_email='cbrown1@pitt.edu',
      packages=['spyral',],
      requires = ['numpy (>=1.2)',
                  'scipy (>=0.12)',
                 ],
      platforms = ['any'],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering',
        ],
     )

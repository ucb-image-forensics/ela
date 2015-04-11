#!/usr/bin/env python
from setuptools import setup, find_packages

__version__ = '0.1'

setup(
    name='ela',
    version=__version__,
    url='https://github.com/ucb-image-forensics/ela',
    packages=find_packages(),
    include_package_data=True,
)

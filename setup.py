#!/usr/bin/env python

import os
import shutil
import sys

from setuptools import setup
from setuptools import find_packages

requirements = [
    'numpy',
    'six',
]

exec(open('hopper/_version_.py').read())

setup(
    name='hopper',
    version=__version__,
    description='Concise DL framework for both research and production',
    author='cicicici',
    author_email='cicicici@gmail.com',
    url='https://github.com/cicicici/hopper',
    download_url='https://github.com/cicicici/hopper/tarball/' + __version__,
    license='MIT',
    keywords=['hopper'],

    packages=find_packages(exclude=('test',)),

    zip_safe=True,
    install_requires=requirements,
)


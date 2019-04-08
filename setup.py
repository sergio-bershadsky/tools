#!/usr/bin/env python
import os

from distutils.core import setup
from setuptools import find_packages


DIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    with open(".version") as h:
        return h.read().strip()


def get_requirements():
    with open(os.path.join(DIR, "requirements.frozen.pip"), 'r') as h:
        return list(filter(bool, map(lambda s: s.strip(), h.readlines())))


setup(
    name='bershadsky-tools',
    version=get_version(),
    description='Bershadsky\'s CLI tools',
    author_email='sergio.bershadsky@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=get_requirements(),
    entry_points='''
        [console_scripts]
        b8y=bershadsky_tools.scripts.cli:main
    '''
)

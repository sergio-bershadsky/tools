#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages


def get_version():
    with open(".version") as h:
        return h.read().strip()


setup(
    name='bershadsky-tools',
    version=get_version(),
    description='Bershadsky\'s CLI tools',
    author_email='sergio.bershadsky@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'click',
        'click-repl',
        'click-spinner',
        'click-log',
        'gitpython',
        'massedit',
        'semver',
        'sh',
    ],
    entry_points='''
        [console_scripts]
        b8y=bershadsky_tools.scripts.cli:main
    '''
)

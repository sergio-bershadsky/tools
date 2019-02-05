#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages


setup(
    name='bershadsky-tools',
    version_format='{tag}',
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

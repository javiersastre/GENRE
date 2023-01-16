# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""
Create genre as a Python package
"""

from __future__ import print_function
import io
import os
import os.path
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

MIN_PYTHON_VERSION = (3, 9)

PKGNAME = 'genre'
DESC = '''
Generative ENtity Retrieval
'''


# --------------------------------------------------------------------

def pkg_version():
    """Read the package version from VERSION.txt"""
    basedir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(basedir, 'VERSION.txt'), 'r') as f:
        return f.readline().strip()


def long_description():
    with open("README.md", "r") as fh:
        return fh.read()


def parse_requirements(filename='requirements.txt'):
    """Read the requirements file"""
    pathname = os.path.join(os.path.dirname(__file__), filename)
    modules = []
    urls = []
    with io.open(pathname, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            else:
                modules.append(line)
    return modules, urls


# --------------------------------------------------------------------

def _post_install():
    pass


class MyInstall(install):
    def run(self):
        install.run(self)
        self.execute(_post_install, [], msg='Running post-install tasks')


class MyDevelop(develop):
    def run(self):
        develop.run(self)
        self.execute(_post_install, [], msg='Running post-install tasks')


# --------------------------------------------------------------------


LONG_DESCRIPTION = long_description()
VERSION = pkg_version()

if sys.version_info < MIN_PYTHON_VERSION:
    sys.exit('**** Sorry, {} {} needs at least Python {}'.format(
        PKGNAME, VERSION, '.'.join(map(str, MIN_PYTHON_VERSION))))

install_requires, dependency_links = parse_requirements()

setuptools.setup(
    # Metadata
    name=PKGNAME,
    version=VERSION,
    description=DESC.split('\n')[0],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license='CC BY-NC 4.0',

    # Locate packages
    packages=find_packages(exclude=['tests']),

    # Requirements
    python_requires='>=' + '.'.join(map(str, MIN_PYTHON_VERSION)),
    install_requires=install_requires,
    # Optional requirements
    extras_require={
        'fairseq': [
            'fairseq==0.12.2'
        ],
        'test': [
            'pytest>=7.2.0',
            'nose',
            'coverage'
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

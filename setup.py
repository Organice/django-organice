#!/usr/bin/env python
#
# Copyright 2014-2016 Peter Bittner <django@bittner.it>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand  # noqa: disable=N812

import organice as package
import sys

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Office/Business :: Groupware',
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def read_file(*pathname):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), *pathname)) as thefile:
        return thefile.read()


def replace_last(s, old, new, maxtimes=1):
    """Replace the last (n) occurence(s) of an expression in a string"""
    tokens = s.rsplit(old, maxtimes)
    return new.join(tokens)


# Parse requirements.txt for both package (PyPI) and source (VCS) dependencies
DEPENDENCY_LINKS = []
INSTALL_REQUIRES = [line for line in read_file('requirements.txt').splitlines()
                    if line and not line.strip().startswith('#')]

for index, line in enumerate(INSTALL_REQUIRES):
    if '#egg=' in line:
        DEPENDENCY_LINKS += [line]
        pkg_name_version = replace_last(line.split('#egg=')[1], '-', '==')
        INSTALL_REQUIRES[index] = pkg_name_version

setup(
    name='django-organice',
    version=package.__version__,
    author=package.__author__,
    author_email=package.__author_email__,
    maintainer=package.__maintainer__,
    maintainer_email=package.__maintainer_email__,
    url=package.__url__,
    license=package.__license__,

    description=package.__doc__.strip(),
    long_description='\n'.join([
        read_file('README.rst'),
        read_file('docs', 'changelog.rst')
    ]),
    keywords='cms, collaboration, blog, newsletter, django, python',

    classifiers=CLASSIFIERS,
    dependency_links=DEPENDENCY_LINKS,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,

    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'organice-setup = organice.bin.organice_setup:startproject',
        ],
    },
)

#!/usr/bin/env python
#
# Copyright 2014-2015 Peter Bittner <django@bittner.it>
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

from os.path import dirname, join
from pip.req import parse_requirements
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import organice
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

NON_PYPI_DEP_LINKS = [
    'git+https://github.com/emencia/emencia-django-newsletter.git#egg=emencia.django.newsletter-0.3.dev',
    'git+https://github.com/samluescher/django-form-designer.git#egg=django-form-designer',
    'git+https://github.com/samluescher/django-media-tree@b69c508#egg=django-media-tree',  # treebeard feature branch
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
    return open(join(dirname(__file__), *pathname)).read()


def read_requirements():
    filepath = join(dirname(__file__), 'requirements.txt')
    generator = parse_requirements(filepath, session=False)
    return [str(requirement.req) for requirement in generator]


setup(
    name='django-organice',
    version=organice.__version__,
    author=organice.__author__,
    author_email=organice.__author_email__,
    maintainer=organice.__maintainer__,
    maintainer_email=organice.__maintainer_email__,
    url=organice.__url__,
    license=organice.__license__,

    description=organice.__doc__.strip(),
    long_description='\n'.join([
        read_file('README.rst'),
        read_file('docs', 'changelog.rst')
    ]),
    keywords='cms, collaboration, blog, newsletter, django, python',

    classifiers=CLASSIFIERS,
    install_requires=read_requirements(),
    dependency_links=NON_PYPI_DEP_LINKS,
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

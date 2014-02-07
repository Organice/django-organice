#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Peter Bittner <django@bittner.it>
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

from setuptools import setup, find_packages
import os
import organice


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Office/Business :: Groupware',
]

DEPENDENCIES = [
    'cmsplugin-contact==1.0.0',
    'cmsplugin-zinnia==0.5.1',
    'django-blog-zinnia==0.13',
    'django-cms<3',
    'django-simple-links==0.1.1',
    #'django-tagging==0.4.dev1',
    'emencia.django.newsletter==0.2',
    'PIL',
]

NON_PYPI_DEP_LINKS = [
    #'svn+http://django-tagging.googlecode.com/svn/trunk#egg=django-tagging-0.4.dev1',
]

ROOT_PATH = os.path.dirname(__file__)

setup(
    name='django-organice',
    version=organice.__version__,
    author='Peter Bittner',
    author_email='django@bittner.it',
    url=organice.__url__,
    license=organice.__license__,

    description='All-in-one collaboration solution providing an intuitive, consistent user experience.',
    long_description='\n'.join([
        open(os.path.join(ROOT_PATH, 'README.rst')).read(),
        open(os.path.join(ROOT_PATH, 'docs', 'changelog.rst')).read()
    ]),
    keywords='cms, collaboration, blog, newsletter, django, python',

    classifiers=CLASSIFIERS,
    install_requires=DEPENDENCIES,
    dependency_links=NON_PYPI_DEP_LINKS,
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    zip_safe=False,
)

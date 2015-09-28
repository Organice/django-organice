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

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
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
    'Programming Language :: Python :: 2.7',
    'Topic :: Office/Business :: Groupware',
]

DEPENDENCIES = [
    'django-apptemplates',
    'django-blog-zinnia',
    'django-cms',
    'djangocms-file',
    'djangocms-flash',
    'djangocms-googlemap',
    'djangocms-grid',
    'djangocms-inherit',
    'djangocms-link',
    'djangocms-oembed',
    'djangocms-picture',
    'djangocms-table',
    'djangocms-teaser',
    'djangocms-video',
    # 'django-form-designer',
    # 'django-media-tree',
    'django-organice-theme',
    'django-simple-links',
    'django-tinymce',
    'django-todo',
    'django-allauth',
    'django-analytical',
    'easy-thumbnails',
    # 'emencia.django.newsletter>=0.3.dev',  # v0.2 depends on tagging (which breaks django-tagging)
    'Pillow',
    'solid_i18n',
    'cmsplugin-zinnia',
]

NON_PYPI_DEP_LINKS = [
    'git+https://github.com/emencia/emencia-django-newsletter.git#egg=emencia.django.newsletter-0.3.dev',
    'git+https://github.com/samluescher/django-form-designer.git#egg=django-form-designer',
    'git+https://github.com/samluescher/django-media-tree@b69c508#egg=django-media-tree',  # treebeard feature branch
]

ROOT_PATH = os.path.dirname(__file__)


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


setup(
    name='django-organice',
    version=organice.__version__,
    author=organice.__author__,
    author_email=organice.__email__,
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
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points="""
        [console_scripts]
        organice-setup=organice.bin.organice_setup:startproject
    """,
)

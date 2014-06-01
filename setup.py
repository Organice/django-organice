#!/usr/bin/env python
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
    'django-apptemplates',
    'django-blog-zinnia==0.13',
    'django-cms==2.4.3-support',  # support branch fixes reversion>=1.8 incompatibility
    'django-mptt==0.5.2',  # necessary due to poor dependency resolution
    'django-media-tree',
    'django-organice-theme',
    'django-reversion==1.8.0',
    'django-simple-links',
    'django-tinymce',
    'django-todo>=1.4.dev',
    'django-allauth',
    'django-analytical',
    'easy-thumbnails',
    'emencia.django.newsletter>=0.3.dev',  # v0.2 depends on tagging (which breaks django-tagging)
    'Pillow',
    'solid_i18n',
    'cmsplugin-contact',
    'cmsplugin-zinnia==0.5.1',
]

NON_PYPI_DEP_LINKS = [
    'git+https://github.com/divio/django-cms.git@1cf3c9a#egg=django-cms-2.4.3-support',
    'git+https://github.com/emencia/emencia-django-newsletter.git#egg=emencia.django.newsletter-0.3.dev',
]

ROOT_PATH = os.path.dirname(__file__)

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

    entry_points="""
        [console_scripts]
        organice-setup=organice.bin.organice_setup:startproject
    """,
)

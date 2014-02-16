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
"""
Setup script for starting a django Organice project.
"""
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH
from subprocess import call
import os
import re
import sys


class DjangoSettingsManager(object):
    """
    Utility class which allows moving and copying variables in-between several
    settings files in the project's ``settings/`` folder.
    """
    __path = ''
    __file = {}
    __data = {}
    NO_MATCH = (0, 0)

    def __init__(self, projectname, *filenames):
        """
        Constructor to add settings files (named without path and extension).
        """
        self.__path = os.path.join(projectname, 'settings')
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        for module in filenames:
            self.add_file(module)

    def add_file(self, module):
        """
        Adds a settings file (identified by its module name).
        If the related .py file doesn't exist an empty file is created.
        """
        file = open(os.path.join(self.__path, module + '.py'), 'a+')
        self.__file[module] = file
        self.__data[module] = file.read()

    def get_file(self, module):
        """Returns the file object for a settings module"""
        return self.__file[module]

    def save_files(self):
        """Writes all changes to disk"""
        for module, file in self.__file.items():
            data = self.__data[module]
            file.seek(0)
            file.truncate()
            file.write(data)

    def find_var(self, src, var, comments=True):
        """
        Returns (start, stop) position of a match, or NO_MATCH i.e. (0, 0).
        A match is a variable including optional leading comment lines.  If
        comments is set to False the match strictly starts with the variable.
        """
        data = self.__data[src]

        # variable incl. leading comments, until after trailing equal sign
        # and optional line continuation mark (backslash)
        re_comments = r'(?<=\n)\s*([ ]*#.*\n)*[ ]*' if comments else ''
        re_variable = r'(\A|\b)' + var + r'\s*=\s*\\?\s*'
        pattern = re.compile(re_comments + re_variable)
        m = pattern.search(data)
        if m is None:
            return self.NO_MATCH

        start, stop = m.span()
        stop = self.__find_endofvalue(data, stop)
        return start, stop

    def __find_endofvalue(self, data, start):
        """
        Identifies value type (str, tuple, list, dict) and returns end index.
        """
        delimiters = {
            '"""': (r'"""', r'"""'),
            '"': (r'"', r'"'),
            "'": (r"'", r"'"),
            '(': (r'\(', r'\)'),
            '[': (r'\[', r'\]'),
            '{': (r'\{', r'\}'),
        }

        delim = data[start:start + 3]
        if delim != '"""':
            delim = delim[0]

        delim_length = len(delim)
        stop = start + delim_length
        try:
            open_delim, close_delim = delimiters[delim]
            # TODO: ignore matches in comments and strings
            open_pattern = re.compile(open_delim)
            close_pattern = re.compile(close_delim + r'[ ]*,?[ ]*\n?')
            open_count = 1
            while open_count > 0:
                close_match = close_pattern.search(data, stop)
                if close_match:
                    open_count -= 1
                    cm_start, stop = close_match.span()
                else:
                    raise SyntaxError('Closing delimiter missing for %s' % delim)
                open_matches = open_pattern.findall(data, start + delim_length, cm_start)
                start = stop + delim_length
                open_count += len(open_matches)
        except KeyError:
            # expression (e.g. variable) found instead of opening delimiter
            pattern = re.compile(r'(\n|\Z)')
            m = pattern.search(data, stop)
            # NOTE: no test on m needed, \Z will always match
            ignore, stop = m.span()
        return stop

    def __append(self, dest, chunk):
        self.__data[dest] += chunk

    def __insert(self, dest, start, stop, chunk):
        data = self.__data[dest]
        self.__data[dest] = data[:start] + chunk + data[stop:]

    def append_lines(self, dest, *lines):
        if len(self.__data[dest]) > 0:
            self.__append(dest, os.linesep)
        for data in lines:
            self.__append(dest, data + os.linesep)

    def insert_lines(self, dest, *lines):
        """Finds position after first comment and inserts the data"""
        pattern = re.compile(r'(\s*#.*\n)*')
        match = pattern.search(self.__data[dest])
        start, stop = self.NO_MATCH if match is None else match.span()
        chunk = ''
        for data in lines:
            chunk += data + os.linesep
        self.__insert(dest, stop, stop, chunk)

    def set_value(self, dest, var, value):
        """Replaces or adds a variable in a settings file"""
        var_value = '%s = %s' % (var, value)
        match = self.find_var(dest, var, False)
        if match == self.NO_MATCH:
            self.append_lines(dest, var_value)
        else:
            start, stop = match
            self.__insert(dest, start, stop, var_value + os.linesep)

    def delete_var(self, dest, var):
        """Deletes a variable from a settings file"""
        data = self.__data[dest]
        start, stop = self.find_var(dest, var)
        self.__data[dest] = data[:start] + data[stop:]

    def copy_var(self, src, destinations, var):
        """
        Copies a variable from one settings file to one or more others.
        """
        start, stop = self.find_var(src, var)
        data = self.__data[src][start:stop]
        for dest in destinations:
            self.__append(dest, data)

    def move_var(self, src, destinations, var):
        """
        Moves a variable from one settings file to one or more others.
        """
        self.copy_var(src, destinations, var)
        self.delete_var(src, var)


def startproject():
    """
    Starts a new django Organice project by use of django-admin.py.
    """
    usage_descr = 'django Organice setup. Start getting organiced!'

    if sys.version_info < (2, 7):
        from optparse import OptionParser  # Deprecated since version 2.7

        parser = OptionParser(description=usage_descr)
        (options, args) = parser.parse_args()
        if len(args) != 1:
            parser.error('Please specify a projectname')
        projectname = args[0]
    else:
        from argparse import ArgumentParser  # New since version 2.7

        parser = ArgumentParser(description=usage_descr)
        parser.add_argument('projectname', help='name of project to create')
        args = parser.parse_args()
        projectname = args.projectname

    mode0755 = S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH
    profiles = ('develop', 'staging', 'production')
    filenames = ('__init__', 'common') + profiles

    print('Generating project %s ...' % projectname)
    call(['django-admin.py', 'startproject', projectname, '.'])

    print('Converting settings to deployment profiles (%s) ...' % ', '.join(profiles))
    os.mkdir(os.path.join(projectname, 'settings'))
    os.rename(os.path.join(projectname, 'settings.py'),
              os.path.join(projectname, 'settings', 'common.py'))
    os.chmod('manage.py', mode0755)

    settings = DjangoSettingsManager(projectname, *filenames)
    settings.append_lines('__init__',
                          '"""',
                          'Modularized settings generated by django Organice setup. http://organice.io',
                          'This solution follows the second recommendation from',
                          'http://www.sparklewise.com/django-settings-for-production-and-development-best-practices/',
                          '"""',
                          'from develop import *')
    for prof in profiles:
        settings.append_lines(prof,
                              '# Django project settings for %s environment' % prof.capitalize(),
                              '',
                              'from common import *')

    # out-of-the-box Django values relevant for deployment
    settings.move_var('common', profiles, 'DEBUG')
    settings.move_var('common', profiles, 'TEMPLATE_DEBUG')
    settings.move_var('common', profiles, 'ALLOWED_HOSTS')
    settings.move_var('common', profiles, 'DATABASES')
    settings.move_var('common', profiles, 'SECRET_KEY')
    settings.move_var('common', profiles, 'WSGI_APPLICATION')
    settings.insert_lines('common',
                          'import os',
                          'PROJECT_PATH = os.sep.join(__file__.split(os.sep)[:-3])')
    settings.set_value('common', 'STATIC_ROOT', "os.path.join(PROJECT_PATH, 'static')")
    settings.set_value('staging', 'DEBUG', False)
    settings.set_value('production', 'DEBUG', False)

    # configuration for included packages
    adding_cfg_for = 'Adding configuration for %s ...'

    print(adding_cfg_for % 'installed apps')
    settings.delete_var('common', 'INSTALLED_APPS')
    settings.append_lines('common',
                          'INSTALLED_APPS = (',
                          "    'django.contrib.auth',",
                          "    'django.contrib.comments',",
                          "    'django.contrib.contenttypes',",
                          "    'django.contrib.sessions',",
                          "    'django.contrib.sites',",
                          "    'django.contrib.messages',",
                          "    'django.contrib.staticfiles',",
                          "    'django.contrib.admin',",
                          "    'cms',",
                          "    'mptt',",
                          "    'menus',",
                          "    'south',",
                          "    'sekizai',",
                          "    'reversion',",
                          "    'cms.plugins.text',",
                          "    'cms.plugins.picture',",
                          "    'cms.plugins.link',",
                          "    'cms.plugins.teaser',",
                          "    'cms.plugins.file',",
                          "    'cms.plugins.video',",
                          "    'cms.plugins.flash',",
                          "    'cms.plugins.googlemap',",
                          "    'cms.plugins.inherit',",
                          "    'cmsplugin_contact',",
                          "    'cmsplugin_zinnia',",
                          "    'tagging',",
                          "    'emencia.django.newsletter',",
                          "    'simple_links',",
                          "    'zinnia',",
                          ')')

    print(adding_cfg_for % 'django CMS')
    settings.append_lines('common',
                          'CMS_TEMPLATES = (',
                          "    ('cms_article.html', 'Template for normal content pages'),",
                          "    ('cms_bookmarks.html', 'Template for the bookmarks page'),",
                          "    ('cms_journal.html', 'Template for Issuu powered pages'),",
                          "    ('cms_welcome.html', 'Template for welcome page'),",
                          ')')
    settings.delete_var('common', 'TEMPLATE_DIRS')
    settings.append_lines('common',
                          'TEMPLATE_DIRS = (',
                          "    # Don't forget to use absolute paths, not relative paths.",
                          "    os.path.join(PROJECT_PATH, 'templates'),",
                          "    os.path.join(PROJECT_PATH, 'templates', 'zinnia'),",
                          ')')
    settings.append_lines('common',
                          'TEMPLATE_CONTEXT_PROCESSORS = (',
                          "    'django.contrib.auth.context_processors.auth',",
                          "    'django.core.context_processors.i18n',",
                          "    'django.core.context_processors.request',",
                          "    'django.core.context_processors.media',",
                          "    'django.core.context_processors.static',",
                          "    'cms.context_processors.media',",
                          "    'sekizai.context_processors.sekizai',",
                          ')')

    print(adding_cfg_for % 'Emencia Newsletter')
    settings.append_lines('common',
                          '# emencia/django/newsletter/media/edn/ directory (alternative)',
                          "NEWSLETTER_MEDIA_URL = '/media/'",
                          "NEWSLETTER_DEFAULT_HEADER_SENDER = 'Your Organization <newsletter@your.domain>'")

    print(adding_cfg_for % 'Zinnia Blog')
    settings.append_lines('common',
                          '# use plugin system of django-cms in blog entries',
                          "ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'")

    suggest_editing = ('ADMINS', 'TIME_ZONE', 'LANGUAGE_CODE')
    suggest_adding = ('LANGUAGES', )
    settings.save_files()
    print('Done. Enjoy your organiced day!' + os.linesep)
    print('Please visit file %s and edit or add the variables: %s' %
          (settings.get_file('common').name, ', '.join(suggest_editing + suggest_adding)))


if __name__ == "__main__":
    startproject()

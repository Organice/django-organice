#!/usr/bin/env python

from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH
from subprocess import call
import os
import re
import sys


class DjangoSettingsManager(object):
    """
    Utility class which allows moving and copying variables inbetween several
    settings files in the project's ``settings/`` folder.
    """
    __path = ''
    __file = {}
    __data = {}
    __match = {}

    def __init__(self, projectname, *filenames):
        """
        Constructor to add settings files (named without path and extension).
        """
        self.__path = os.path.join(projectname, 'settings')
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        for fname in filenames:
            self.add_file(fname)

    def add_file(self, fname):
        """
        Adds a settings file (named without path and extension).
        If the related .py file doesn't exist an empty file is created.
        """
        file = open(os.path.join(self.__path, fname + '.py'), 'a+')
        self.__file[fname] = file
        self.__data[fname] = file.read()
        self.__match[fname] = {}

    def save_files(self):
        """
        Write all changes to disk.
        """
        for fname, file in self.__file.items():
            data = self.__data[fname]
            file.write(data)

    def find_var(self, src, var):
        """
        Returns (start, stop) position of a match, or (0, 0) for no match.
        A match is a variable including a leading comment and blank line.
        """
        # yield cached result if available (from an earlier call)
        if var in self.__match[src]:
            return self.__match[src][var]

        data = self.__data[src]
        m = re.search(r'\n{0,1}(#.*\n)*[ ]*' + var + r'\s*=\s*', data)
        if m == None:
            # not found
            self.__match[src][var] = (0, 0)
            return self.__match[src][var]

        start, stop = m.span()
        # jump over line continuation mark (backslash)
        m = re.match(r'\\{0,1}\s*', data, stop)
        if m:
            ignore, stop = m.span()
        stop = self._find_endofvalue(data, stop + 1)
        # cache match for follow-up access
        self.__match[src][var] = (start, stop)
        return self.__match[src][var]

    def _find_endofvalue(self, data, start):
        """
        Identifies value type (str, tuple, list, dict) and returns end index.
        """
        delimiters = {
            '\"\"\"': '\"\"\"',
            '"': '"',
            "'": "'",
            '(': ')',
            '[': ']',
            '{': '}',
        }

        open_delim = data[start:start + 3]
        if open_delim != '"""':
            open_delim = data[start:start + 1]

        stop = start + len(open_delim)
        try:
            close_delim = delimiters[open_delim]
            m = re.search(close_delim + r'[ ]*\n{0,1}', data, stop)
            if m:
                ignore, stop = m.span()
            else:
                raise SyntaxError('No closing delimiter %s found' % (close_delim, ))
        except:
            # variable found instead of opening delimiter
            m = re.search(r'\n', data, stop)
            if m:
                ignore, stop = m.span()
            else:
                stop = len(data)
        return stop

    def _append(self, dest, data):
        self.__data[dest] += data

    def append_lines(self, dest, *lines):
        if len(self.__data[dest]) > 0:
            self._append(os.linesep)
        for data in lines:
            self._append(dest, data + os.linesep)

    def delete_var(self, src, var):
        """
        Deletes a variable from a settings file.
        """
        data = self.__data[src]
        start, stop = self.find_var(src, var)
        self.__data[src] = data[:start] + data[stop:]

    def copy_var(self, src, destinations, var):
        """
        Copies a variable from one settings file to one or more others.
        """
        start, stop = self.find_var(src, var)
        data = self.__data[src][start:stop]
        for dest in destinations:
            self._append(dest, data)

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
            parser.error("Please specify a projectname")
        projectname = args[0]
    else:
        from argparse import ArgumentParser  # New since version 2.7

        parser = ArgumentParser(description=usage_descr)
        parser.add_argument("projectname", help="name of project to create")
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
                          '\"""',
                          'Modularized settings generated by django Organice setup. http://organice.io',
                          'This solution follows the second recommendation from',
                          'http://www.sparklewise.com/django-settings-for-production-and-development-best-practices/',
                          '\"""',
                          'from develop import *')
    for prof in profiles:
        settings.append_lines(prof,
                              '# Django project settings for %s environment' % prof.capitalize(),
                              '',
                              'from common import *')
    settings.move_var('common', profiles, 'DEBUG')
    settings.move_var('common', profiles, 'TEMPLATE_DEBUG')
    settings.move_var('common', profiles, 'ALLOWED_HOSTS')
    settings.move_var('common', profiles, 'DATABASES')
    settings.move_var('common', profiles, 'SECRET_KEY')
    settings.move_var('common', profiles, '#WSGI_APPLICATION')
    settings.save_files()
    print('Done. Enjoy your organiced day!')


if __name__ == "__main__":
    startproject()

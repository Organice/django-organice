#!/usr/bin/env python

from django.core.management import execute_from_command_line
import os
import re


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
        for fname in filenames:
            self.add_file(fname)

    def add_file(self, fname):
        """
        Adds a settings file (named without path and extension).
        """
        file = open(os.path.join(self.__path, fname + '.py'), 'r+')
        self.__file[fname] = file
        self.__data[fname] = file.read()

    def save_files(self):
        """
        Write all changes to disk.
        """
        for fname, file in self.__file:
            data = self.__data[fname]
            file.write(data)

    def find_var(self, src, var):
        """
        Returns (start, stop) position of a match, or (0, 0) for no match.
        A match is a variable including a leading comment and blank line.
        """
        # yield cached result if available (from an earlier call)
        if var in self.__match:
            return self.__match[var]

        data = self.__data[src]
        m = re.search(r'\n{0,1}(#.*\n)*[ ]*' + var + r'\s*=\s*', data)
        if m == None:
            # not found
            return self.__match[var] = (0, 0)

        start, stop = m.span()
        # jump over line continuation mark (backslash)
        m = re.match(r'\\{0,1}\s*', data, stop)
        if m:
            ignore, stop = m.span()
        stop = _find_endofvalue(data, stop + 1)
        # cache match for follow-up access
        return self.__match[var] = (start, stop)

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
        start, stop = find_var(src, var)
        self.__data[src] = data[:start] + data[stop:]

    def copy_var(self, src, destinations, var):
        """
        Copies a variable from one settings file to one or more others.
        """
        start, stop = find_var(src, var)
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
    usage = 'Usage: %prog projectname'
    if sys.version_info < (2, 7):
        from optparse import OptionParser  # Deprecated since version 2.7

        parser = OptionParser(usage=usage)
        (options, args) = parser.parse_args()
    else:
        from argparse import ArgumentParser  # New in version 2.7

        parser = ArgumentParser(usage=usage)
        args = parser.parse_args()

    if len(args) != 1:
        parser.error("Please specify a projectname")
    projectname = args[0]

    execute_from_command_line('django-admin.py startproject %s .' % projectname)
    execute_from_command_line('chmod 755 manage.py')

    profiles = ('develop', 'staging', 'production')
    filenames = ('common', ) + profiles
    settings = DjangoSettingsManager(projectname, filenames)
    for env in profiles:
        settings.append_lines(env,
                              '# Django project settings for %s environment' % env.capitalize(),
                              '',
                              'from common import *')
    settings.move_var('common', profiles, 'DEBUG')
    settings.move_var('common', profiles, 'TEMPLATE_DEBUG')
    settings.move_var('common', profiles, 'ALLOWED_HOSTS')
    settings.move_var('common', profiles, 'DATABASES')
    settings.move_var('common', profiles, 'SECRET_KEY')
    settings.move_var('common', profiles, '#WSGI_APPLICATION')
    settings.save_files()


if __name__ == "__main__":
    startproject()

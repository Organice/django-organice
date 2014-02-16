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
Generic Django settings manipulation utilities, used by organice-setup script.
"""
import os
import re


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

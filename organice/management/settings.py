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


class DjangoModuleManager(object):
    """
    Utility class to modify and write files in a Python module.
    """
    __path = ''
    __file = {}
    __data = {}

    def __init__(self, projectname, *modulename):
        """Constructor, computes and creates physical base path for module"""
        self.__path = os.path.join(projectname, *modulename)
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)

    def add_file(self, module, data=None, lines=None):
        """
        Adds a Python file (identified by its module name) in the module.
        If the related .py file doesn't exist an empty file is created.
        """
        file = open(os.path.join(self.__path, module + '.py'), 'a+')
        self.__file[module] = file
        self.__data[module] = '' if data or lines else file.read()
        if data:
            self.set_data(module, data)
        if lines:
            self.append_lines(module, *lines)

    def get_file(self, module):
        """Returns the file object for a module file"""
        return self.__file[module]

    def save_files(self):
        """Writes all changes to disk"""
        for module, file in self.__file.items():
            data = self.__data[module]
            file.seek(0)
            file.truncate()
            file.write(data)

    def get_data(self, module):
        """Returns the data contained in the module file"""
        return self.__data[module]

    def set_data(self, module, data):
        """Sets the data contained in the module file"""
        self.__data[module] = data

    def append_data(self, module, chunk):
        """Appends a chunk of data to the module file"""
        self.__data[module] += chunk

    def append_lines(self, module, *lines):
        """Appends lines of text to the module file"""
        if len(self.__data[module]) > 0:
            self.append_data(module, os.linesep)
        for data in lines:
            self.append_data(module, data + os.linesep)


class DjangoSettingsManager(DjangoModuleManager):
    """
    Utility class which allows moving and copying variables in-between several
    settings files in the project's ``settings/`` folder.
    """
    NO_MATCH = (0, 0)

    def __init__(self, projectname, *filenames):
        """Constructor, adds settings files (named without path and extension)"""
        super(DjangoSettingsManager, self).__init__(projectname, 'settings')
        for module in filenames:
            super(DjangoSettingsManager, self).add_file(module)

    def find_var(self, src, var, comments=True):
        """
        Returns (start, stop) position of a match, or NO_MATCH i.e. (0, 0).
        A match is a variable including optional leading comment lines.  If
        comments is set to False the match strictly starts with the variable.
        """
        data = super(DjangoSettingsManager, self).get_data(src)

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

    def __insert(self, dest, start, stop, chunk):
        data = super(DjangoSettingsManager, self).get_data(dest)
        super(DjangoSettingsManager, self).set_data(dest, data[:start] + chunk + data[stop:])

    def insert_lines(self, dest, *lines):
        """Finds position after first comment and inserts the data"""
        pattern = re.compile(r'(\s*#.*\n)*')
        match = pattern.search(super(DjangoSettingsManager, self).get_data(dest))
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

    def set_value_lines(self, dest, var, *lines):
        self.set_value(dest, var, os.linesep.join(lines))

    def delete_var(self, dest, var):
        """Deletes a variable from a settings file"""
        start, stop = self.find_var(dest, var)
        data = super(DjangoSettingsManager, self).get_data(dest)
        super(DjangoSettingsManager, self).set_data(dest, data[:start] + data[stop:])

    def copy_var(self, src, destinations, var):
        """Copies a variable from one settings file to one or more others"""
        start, stop = self.find_var(src, var)
        data = super(DjangoSettingsManager, self).get_data(src)[start:stop]
        for dest in destinations:
            super(DjangoSettingsManager, self).append_data(dest, data)

    def move_var(self, src, destinations, var):
        """Moves a variable from one settings file to one or more others"""
        self.copy_var(src, destinations, var)
        self.delete_var(src, var)

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
"""
Generic Django settings manipulation utilities, used by organice-setup script.
"""
import os
import re


class DjangoModuleManager(object):
    """
    Utility class to modify and write files in a Python module.
    """

    def __init__(self, projectname, *modulename):
        """Constructor, computes and creates physical base path for module"""
        self.__path = os.path.join(projectname, *modulename)
        self.__file = {}
        self.__data = {}

        if not os.path.exists(self.__path):
            os.makedirs(self.__path)

    def add_file(self, module, data=None, lines=None):
        """
        Add a Python file (identified by its module name) in the module.
        If the related .py file doesn't exist an empty file is created.
        """
        thefile = open(os.path.join(self.__path, module + '.py'), 'a+')
        thefile.seek(0)  # needed in `Python 3 <http://bugs.python.org/issue22651>`_
        self.__file[module] = thefile
        self.__data[module] = '' if data or lines else thefile.read()
        if data:
            self.set_data(module, data)
        if lines:
            self.append_lines(module, *lines)

    def get_file(self, module):
        """Return the file object for a module file"""
        return self.__file[module]

    def save_files(self):
        """Write all changes to disk"""
        for module, thefile in self.__file.items():
            data = self.__data[module]
            thefile.seek(0)
            thefile.truncate()
            thefile.write(data)

    def get_data(self, module):
        """Return the data contained in the module file"""
        return self.__data[module]

    def set_data(self, module, data):
        """Set the data contained in the module file"""
        self.__data[module] = data

    def append_data(self, module, chunk):
        """Append a chunk of data to the module file"""
        self.__data[module] += chunk

    def append_lines(self, module, *lines):
        """Append lines of text to the module file"""
        if len(self.__data[module]) > 0:
            self.append_data(module, os.linesep)
        for data in lines:
            self.append_data(module, data + os.linesep)

    def remove_line(self, module, line):
        """Remove a matching line of text from the module file"""
        self.replace_line(module, line, None)

    def replace_line(self, module, old, new):
        """Replace a matching line of text by some new text in the module file"""
        self.__data[module] = \
            self.__data[module].replace(old + os.linesep,
                                        new + os.linesep if new else '')


class DjangoSettingsManager(DjangoModuleManager):
    """
    Utility class which allows moving and copying variables in-between several
    settings files in the project's ``settings/`` folder.
    """
    DELIMITERS = {
        '(': ')',
        '[': ']',
        '{': '}',
    }
    REGEX_DELIMS = {
        '"""': (r'"""', r'"""'),
        "'''": (r"'''", r"'''"),
        '"': (r'"', r'"'),
        "'": (r"'", r"'"),
        '(': (r'\(', r'\)'),
        '[': (r'\[', r'\]'),
        '{': (r'\{', r'\}'),
    }
    NO_MATCH = (0, 0)

    def __init__(self, projectname, *filenames):
        """Constructor, adds settings files (named without path and extension)"""
        super(DjangoSettingsManager, self).__init__(projectname, 'settings')
        for module in filenames:
            self.add_file(module)

    @staticmethod
    def _indentation_by(indent_level):
        return indent_level * 4 * ' '

    def find_block(self, src, settings_path):
        """
        Return (start, stop) position of a match, or NO_MATCH i.e. (0, 0).
        A match is a value block of a certain data type (usually a list or a
        tuple), excluding its opening and closing delimiter.  Assumes clean
        indentation (4 spaces) for each level, starting at level 0.
        """
        data = self.get_data(src)
        return DjangoSettingsManager._find_block(data, settings_path)

    @staticmethod
    def _find_block(data, settings_path):
        start, stop = 0, len(data)

        for indent_level, key in enumerate(settings_path):
            closing_token = DjangoSettingsManager.DELIMITERS[key[len(key) - 1]]
            indentation = DjangoSettingsManager._indentation_by(indent_level)

            needle = "%s%s" % (indentation, key)
            start = data.find(needle, start, stop)
            assert start != -1, "Key not found: %s" % key
            start += len(needle)

            needle = "\n%s%s" % (indentation, closing_token)
            stop = start if data[start] == closing_token \
                else 1 + data.find(needle, start, stop)
            assert stop >= start, "End of block not found: %s" % key
        return (start, stop)

    def find_var(self, src, var, comments=True):
        """
        Return (start, stop) position of a match, or NO_MATCH i.e. (0, 0).
        A match is a variable including optional leading comment lines.  If
        comments is set to False the match strictly starts with the variable.
        """
        data = self.get_data(src)

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
        Identify value type (str, tuple, list, dict) and return end index.
        """
        delim = data[start:start + 3]
        if delim != '"""' and delim != "'''":
            delim = delim[0]

        delim_length = len(delim)
        stop = start + delim_length
        try:
            open_delim, close_delim = self.REGEX_DELIMS[delim]
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
        data = self.get_data(dest)
        self.set_data(dest, data[:start] + chunk + data[stop:])

    def append_to_list(self, dest, settings_path, *items):
        """Append one or more list items to a list identified by a hierarchy"""
        start, stop = self.find_block(dest, settings_path)
        indentation = self._indentation_by(len(settings_path))
        chunk = ''
        if start == stop:
            chunk += os.linesep
        for line in items:
            chunk += indentation + line + ',' + os.linesep
        if start == stop:
            chunk += self._indentation_by(len(settings_path) - 1)
        self.__insert(dest, stop, stop, chunk)

    def delete_from_list(self, dest, settings_path, *items):
        """Remove list items from a list identified by a hierarchy"""
        start, stop = self.find_block(dest, settings_path)
        indentation = self._indentation_by(len(settings_path))
        data = self.get_data(dest)
        block = data[start:stop]
        # TODO: make work for a value being a list/tuple (works for single, self-contained lines only atm)
        for line in items:
            chunk = indentation + line + ',' + os.linesep
            block = block.replace(chunk, '')
        self.set_data(dest, data[:start] + block + data[stop:])

    def insert_lines(self, dest, *lines):
        """Find position after first comment and/or docstring, and insert the data"""
        dest_data = self.get_data(dest)
        re_comments = r'(\s*#.*\n)*'
        pattern = re.compile(re_comments + r'\s*')
        match = pattern.search(dest_data)
        start, stop = self.NO_MATCH if match is None else match.span()
        next3chars = dest_data[stop:stop + 3]
        if next3chars == '"""' or next3chars == "'''":
            stop = self.__find_endofvalue(dest_data, stop)
        chunk = ''
        for data in lines:
            chunk += data + os.linesep
        self.__insert(dest, stop, stop, chunk)

    def set_value(self, dest, var, value):
        """Replace or add a variable in a settings file"""
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
        """Delete a variable from a settings file"""
        start, stop = self.find_var(dest, var)
        data = self.get_data(dest)
        self.set_data(dest, data[:start] + data[stop:])

    def copy_var(self, src, destinations, var):
        """Copy a variable from one settings file to one or more others"""
        start, stop = self.find_var(src, var)
        data = self.get_data(src)[start:stop]
        for dest in destinations:
            self.append_data(dest, data)

    def move_var(self, src, destinations, var):
        """Move a variable from one settings file to one or more others"""
        self.copy_var(src, destinations, var)
        self.delete_var(src, var)

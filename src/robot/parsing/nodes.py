#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from ast import AST
import re

from robot.utils import normalize_whitespace, rstrip


def join_doc_or_meta(lines):
    def lines_with_newlines():
        last_index = len(lines) - 1
        for index, line in enumerate(lines):
            yield line
            if index < last_index:
                match = re.search(r'(\\+)n?$', line)
                escaped_or_has_newline = match and len(match.group(1)) % 2 == 1
                if not escaped_or_has_newline:
                    yield '\n'
    return ''.join(lines_with_newlines())


class Node(AST):
    _fields = ()
    _attributes = ('lineno', 'end_lineno')

    def __init__(self, lineno=0, end_lineno=0):
        self.lineno = lineno
        self.end_lineno = end_lineno


class MultiValue(Node):
    _fields = ('values',)

    def __init__(self, values, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.values = tuple(values)


class SingleValue(Node):
    _fields = ('value',)

    def __init__(self, values, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        if values and values[0].upper() != 'NONE':
            self.value = values[0]
        else:
            self.value = None


class DataFile(Node):
    _fields = ('sections',)

    def __init__(self, sections, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.sections = sections


class SettingSection(Node):
    _fields = ('settings',)

    def __init__(self, settings, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.settings = settings


class VariableSection(Node):
    _fields = ('variables',)

    def __init__(self, variables, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.variables = variables


class TestCaseSection(Node):
    _fields = ('tests',)

    def __init__(self, tests, header, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.tests = tests
        section_name = normalize_whitespace(header[0]).strip('* ')
        self.tasks = section_name.upper() in ('TASKS', 'TASK')


class KeywordSection(Node):
    _fields = ('keywords',)

    def __init__(self, keywords, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.keywords = keywords


class Variable(Node):
    _fields = ('name', 'value')

    def __init__(self, name, value, lineno=0, end_lineno=0):
        # TODO: Should this be done already by the parser?
        # Applies also to 'WITH NAME', 'NONE' and 'TASK(S)' handling
        # as well as joining doc/meta lines and tuple() conversion.
        Node.__init__(self, lineno, end_lineno)
        if name.endswith('='):
            name = rstrip(name[:-1])
        self.name = name
        self.value = value


class KeywordCall(Node):
    # TODO: consider `keyword` -> `name`, as in Fixture
    _fields = ('assign', 'keyword', 'args')

    def __init__(self, assign=None, keyword=None, args=None, lineno=0,
                 end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.assign = tuple(assign or ())
        self.keyword = keyword
        self.args = tuple(args or ())


class ForLoop(Node):
    _fields = ('variables', 'flavor', 'values', 'body')

    # TODO: _header and _end are used for deprecation. Remove in RF 3.3!
    def __init__(self, variables, flavor, values, body=None, lineno=0,
                 end_lineno=0, _header='FOR'):
        Node.__init__(self, lineno, end_lineno)
        self.variables = variables
        self.flavor = normalize_whitespace(flavor)
        self.values = values
        self.body = body or []
        self._header = _header
        self._end = 'END'


class TestCase(Node):
    _fields = ('name', 'body')

    def __init__(self, name, body, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.name = name
        self.body = body


class Keyword(Node):
    _fields = ('name', 'body')

    def __init__(self, name, body, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.name = name
        self.body = body


class TemplateArguments(Node):
    _fields = ('args',)

    def __init__(self, args, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.args = args


class ImportSetting(Node):
    _fields = ('name', 'args')

    def __init__(self, name, args, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.name = name
        self.args = tuple(args)


class LibrarySetting(ImportSetting):

    def __init__(self, name, args, lineno=0, end_lineno=0):
        args, alias = self._split_alias(args)
        ImportSetting.__init__(self, name, args, lineno, end_lineno)
        self.alias = alias

    def _split_alias(self, args):
        if len(args) > 1 and normalize_whitespace(args[-2]) == 'WITH NAME':
            return args[:-2], args[-1]
        return args, None


class ResourceSetting(ImportSetting):
    pass


class VariablesSetting(ImportSetting):
    pass


class MetadataSetting(Node):
    _fields = ('name', 'value')

    def __init__(self, name, values, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        self.name = name
        self.value = join_doc_or_meta(values)


class DocumentationSetting(SingleValue):

    def __init__(self, values, lineno, end_lineno):
        SingleValue.__init__(self, [join_doc_or_meta(values)], lineno, end_lineno)


class Fixture(Node):
    _fields = ('name', 'args')

    def __init__(self, values, lineno=0, end_lineno=0):
        Node.__init__(self, lineno, end_lineno)
        if values and values[0].upper() != 'NONE':
            self.name = values[0]
            self.args = tuple(values[1:])
        else:
            self.name = None
            self.args = ()


class SuiteSetupSetting(Fixture): pass
class SuiteTeardownSetting(Fixture): pass
class TestSetupSetting(Fixture): pass
class TestTeardownSetting(Fixture): pass
class SetupSetting(Fixture): pass
class TeardownSetting(Fixture): pass


class TestTemplateSetting(SingleValue): pass
class TemplateSetting(SingleValue): pass
class TestTimeoutSetting(SingleValue): pass
class TimeoutSetting(SingleValue): pass


class ForceTagsSetting(MultiValue): pass
class DefaultTagsSetting(MultiValue): pass
class TagsSetting(MultiValue): pass
class ArgumentsSetting(MultiValue): pass
class ReturnSetting(MultiValue): pass

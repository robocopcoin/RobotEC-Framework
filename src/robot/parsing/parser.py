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

from .vendor import yacc

from .lexer import Token
from .lexerwrapper import LexerWrapper
from .nodes import (
    DataFile, SettingSection, VariableSection, TestCaseSection,
    KeywordSection, Variable, DocumentationSetting, SuiteSetupSetting,
    SuiteTeardownSetting, MetadataSetting, TestSetupSetting,
    TestTeardownSetting, TestTemplateSetting, TestTimeoutSetting,
    ForceTagsSetting, DefaultTagsSetting, LibrarySetting,
    ResourceSetting, VariablesSetting, SetupSetting, TeardownSetting,
    TimeoutSetting, TagsSetting, TemplateSetting, ArgumentsSetting,
    ReturnSetting, TemplateArguments, TestCase, Keyword, KeywordCall, ForLoop
)


class RobotFrameworkParser(object):
    tokens = Token.DATA_TOKENS

    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self, source):
        parser = yacc.yacc(module=self)
        return parser.parse(lexer=LexerWrapper(self.lexer, source))

    def p_datafile(self, p):
        '''datafile :
                    | sections'''
        sections = p[1] if len(p) == 2 else []
        end = sections[-1].end_lineno if sections else 0
        p[0] = DataFile(sections, lineno=0, end_lineno=end)

    def p_sections(self, p):
        '''sections : section
                    | sections section'''
        p[0] = combine_values(p)

    def p_section(self, p):
        '''section : setting_section
                   | variable_section
                   | testcase_section
                   | keyword_section'''
        p[0] = p[1]

    def p_setting_section(self, p):
        '''setting_section : setting_header EOS
                           | setting_header EOS settings'''
        start = p[1]
        settings = p[3] if len(p) == 4 else []
        end = settings[-1].end_lineno if settings else start
        p[0] = SettingSection(settings, start, end)

    def p_setting_header(self, p):
        '''setting_header : SETTING_HEADER
                           | setting_header SETTING_HEADER'''
        p[0] = p.lineno(1)

    def p_settings(self, p):
        '''settings : setting
                    | settings setting'''
        p[0] = combine_values(p)

    def p_setting(self, p):
        '''setting : documentation_setting
                   | suite_setup_setting EOS
                   | suite_teardown_setting EOS
                   | metadata_setting EOS
                   | test_setup_setting EOS
                   | test_teardown_setting EOS
                   | test_template_setting EOS
                   | test_timeout_setting EOS
                   | force_tags_setting EOS
                   | default_tags_setting EOS
                   | library_setting EOS
                   | resource_setting EOS
                   | variables_setting EOS
                   | setup_setting EOS
                   | teardown_setting EOS
                   | template_setting EOS
                   | timeout_setting EOS
                   | tags_setting EOS
                   | arguments_setting EOS
                   | return_setting EOS'''
        p[0] = p[1]

    def p_documentation(self, p):
        '''documentation_setting : DOCUMENTATION arguments EOS'''
        p[0] = DocumentationSetting(*values_and_linespan(p[2]))

    def p_suite_setup(self, p):
        '''suite_setup_setting : SUITE_SETUP arguments'''
        p[0] = SuiteSetupSetting(*values_and_linespan(p[2]))

    def p_suite_teardown(self, p):
        '''suite_teardown_setting : SUITE_TEARDOWN arguments'''
        p[0] = SuiteTeardownSetting(*values_and_linespan(p[2]))

    def p_metadata(self, p):
        '''metadata_setting : METADATA arguments'''
        name, args, start, end = name_args_and_linespan(p[2])
        p[0] = MetadataSetting(name, args, start, end)

    def p_test_setup(self, p):
        '''test_setup_setting : TEST_SETUP arguments'''
        p[0] = TestSetupSetting(*values_and_linespan(p[2]))

    def p_test_teardown(self, p):
        '''test_teardown_setting : TEST_TEARDOWN arguments'''
        p[0] = TestTeardownSetting(*values_and_linespan(p[2]))

    def p_test_template(self, p):
        '''test_template_setting : TEST_TEMPLATE arguments'''
        p[0] = TestTemplateSetting(*values_and_linespan(p[2]))

    def p_test_timeout(self, p):
        '''test_timeout_setting : TEST_TIMEOUT arguments'''
        p[0] = TestTimeoutSetting(*values_and_linespan(p[2]))

    def p_force_tags(self, p):
        '''force_tags_setting : FORCE_TAGS arguments'''
        p[0] = ForceTagsSetting(*values_and_linespan(p[2]))

    def p_default_tags(self, p):
        '''default_tags_setting : DEFAULT_TAGS arguments'''
        p[0] = DefaultTagsSetting(*values_and_linespan(p[2]))

    def p_library(self, p):
        '''library_setting : LIBRARY arguments'''
        name, args, start, end = name_args_and_linespan(p[2])
        p[0] = LibrarySetting(name, args, start, end)

    def p_resource(self, p):
        '''resource_setting : RESOURCE arguments'''
        name, args, start, end = name_args_and_linespan(p[2])
        p[0] = ResourceSetting(name, args, start, end)

    def p_variables_import(self, p):
        '''variables_setting : VARIABLES arguments'''
        name, args, start, end = name_args_and_linespan(p[2])
        p[0] = VariablesSetting(name, args, start, end)

    def p_setup(self, p):
        '''setup_setting : SETUP arguments'''
        p[0] = SetupSetting(*values_and_linespan(p[2]))

    def p_teardown(self, p):
        '''teardown_setting : TEARDOWN arguments'''
        p[0] = TeardownSetting(*values_and_linespan(p[2]))

    def p_template(self, p):
        '''template_setting : TEMPLATE arguments'''
        p[0] = TemplateSetting(*values_and_linespan(p[2]))

    def p_timeout(self, p):
        '''timeout_setting : TIMEOUT arguments'''
        p[0] = TimeoutSetting(*values_and_linespan(p[2]))

    def p_tags(self, p):
        '''tags_setting : TAGS arguments'''
        p[0] = TagsSetting(*values_and_linespan(p[2]))

    def p_arguments_setting(self, p):
        '''arguments_setting : ARGUMENTS arguments'''
        p[0] = ArgumentsSetting(*values_and_linespan(p[2]))

    def p_return(self, p):
        '''return_setting : RETURN arguments'''
        p[0] = ReturnSetting(*values_and_linespan(p[2]))

    def p_variable_section(self, p):
        '''variable_section : variable_header EOS
                            | variable_header EOS variables'''
        start = p[1]
        variables = p[3] if len(p) == 4 else []
        end = variables[-1].end_lineno if variables else start
        p[0] = VariableSection(variables, start, end)

    def p_variable_header(self, p):
        '''variable_header : VARIABLE_HEADER
                           | variable_header VARIABLE_HEADER'''
        p[0] = p.lineno(1)

    def p_variables(self, p):
        '''variables : variable
                     | variables variable'''
        p[0] = combine_values(p)

    def p_variable(self, p):
        '''variable : VARIABLE arguments EOS'''
        p[0] = Variable(p[1], *values_and_linespan(p[2]))

    def p_testcase_section(self, p):
        '''testcase_section : testcase_header EOS
                            | testcase_header EOS tests'''
        header_values, start, _ = values_and_linespan(p[1])
        tests = p[3] if len(p) == 4 else []
        end = tests[-1].end_lineno if tests else start
        p[0] = TestCaseSection(tests, header_values, start, end)

    def p_testcase_header(self, p):
        '''testcase_header : TESTCASE_HEADER
                           | testcase_header TESTCASE_HEADER'''
        p[0] = combine_values_with_lineno(p)

    def p_keyword_section(self, p):
        '''keyword_section : keyword_header EOS
                           | keyword_header EOS keywords'''
        start = p[1]
        keywords = p[3] if len(p) == 4 else []
        end = keywords[-1].end_lineno if keywords else start
        p[0] = KeywordSection(keywords, start, end)

    def p_keyword_header(self, p):
        '''keyword_header : KEYWORD_HEADER
                          | keyword_header KEYWORD_HEADER'''
        p[0] = p.lineno(1)

    def p_tests(self, p):
        '''tests : test
                 | tests test'''
        p[0] = combine_values(p)

    def p_keywords(self, p):
        '''keywords : keyword
                    | keywords keyword'''
        p[0] = combine_values(p)

    def p_test(self, p):
        '''test : NAME EOS
                | NAME EOS body_items'''
        start = p.lineno(1)
        if len(p) == 3:
            body = []
            end = start
        else:
            body = p[3]
            end = body[-1].end_lineno
        p[0] = TestCase(p[1], body, lineno=start, end_lineno=end)

    def p_keyword(self, p):
        '''keyword : NAME EOS
                   | NAME EOS body_items'''
        start = p.lineno(1)
        if len(p) == 3:
            body = []
            end = start
        else:
            body = p[3]
            end = body[-1].end_lineno
        p[0] = Keyword(p[1], body, lineno=start, end_lineno=end)

    def p_body_items(self, p):
        '''body_items : body_item
                      | body_items body_item'''
        p[0] = combine_values(p)

    def p_body_item(self, p):
        '''body_item : forloop
                     | setting
                     | step
                     | templatearguments
                     | invalid_forloop'''
        p[0] = p[1]

    # TODO: rename -> keyword_call
    def p_step(self, p):
        '''step : KEYWORD arguments EOS'''
        arguments, _, end_lineno = values_and_linespan(p[2])
        p[0] = KeywordCall(None, p[1], arguments, p.lineno(1), end_lineno)

    def p_step_with_assignment(self, p):
        '''step : assignments EOS
                | assignments KEYWORD arguments EOS'''
        assignments, lineno, end_lineno = values_and_linespan(p[1])
        if len(p) == 3:
            p[0] = KeywordCall(assignments, lineno=lineno, end_lineno=end_lineno)
        else:
            arguments, _, end_lineno = values_and_linespan(p[3])
            p[0] = KeywordCall(assignments, p[2], arguments, lineno=lineno, end_lineno=end_lineno)

    def p_forloop(self, p):
        '''forloop : for_header for_body END EOS
                   | for_header END EOS
                   | END EOS'''
        if len(p) == 3: # FIXME: Better way to handle dangling END
            p[0] = KeywordCall(None, p[1])
        elif len(p) == 4:
            p[0] = p[1]
            p[0].end_lineno = p.lineno(3)
            p[0]._end = p[2]    # TODO: Used for deprecation. Remove in RF 3.3!
        else:
            p[0] = p[1]
            p[0].body = p[2]
            p[0].end_lineno = p.lineno(4)
            p[0]._end = p[3]    # TODO: Used for deprecation. Remove in RF 3.3!

    def p_for_header(self, p):
        '''for_header : FOR arguments FOR_SEPARATOR arguments EOS
                      | FOR arguments EOS'''
        # TODO: _header is used for deprecating ':FOR' style. Remove in RF 3.3!
        start = p.lineno(1)
        variables = values_and_linespan(p[2])[0]
        if len(p) == 6:
            values = values_and_linespan(p[4])[0]
            p[0] = ForLoop(variables, p[3], values, lineno=start, _header=p[1])
        else:
            p[0] = ForLoop(variables, 'IN', [], lineno=start, _header=p[1])

    def p_for_body(self, p):
        '''for_body : step
                    | for_body step
                    | templatearguments
                    | for_body templatearguments'''
        p[0] = combine_values(p)

    def p_templatearguments(self, p):
        '''templatearguments : arguments EOS'''
        p[0] = TemplateArguments(*values_and_linespan(p[1]))

    def p_invalid_for_loop(self, p):
        '''invalid_forloop : for_header for_body'''
        p[0] = p[1]

    def p_assignments(self, p):
        '''assignments : ASSIGN
                       | assignments ASSIGN'''
        p[0] = combine_values_with_lineno(p)

    def p_arguments(self, p):
        '''arguments : args
                     | empty_arg'''
        p[0] = p[1]

    def p_args(self, p):
        '''args : ARGUMENT
                | arguments ARGUMENT'''
        p[0] = combine_values_with_lineno(p)

    def p_empty_arg(self, p):
        '''empty_arg : '''
        p[0] = []

    def p_error(self, e):
        if e:
            print(e.type)
        print("Parse error:" + str(e))
        # FIXME not a proper way to handle errors
        #self.parser.errok()


def combine_values(p):
    if len(p) == 1:
        return []
    if len(p) == 2:
        return [p[1]]
    value = p[1]
    value.append(p[2])
    return value


def combine_values_with_lineno(p):
    if len(p) == 1:
        return []
    if len(p) == 2:
        return [(p[1], p.lineno(1))]
    value = p[1]
    value.append((p[2], p.lineno(2)))
    return value


def values_and_linespan(values_with_linenos):
    if values_with_linenos:
        values = [v[0] for v in values_with_linenos]
        start = values_with_linenos[0][1]
        end = values_with_linenos[-1][1]
        return values, start, end
    return [], 0, 0


def name_args_and_linespan(values_with_linenos):
    if values_with_linenos:
        value, start, end = values_and_linespan(values_with_linenos)
        return value[0], value[1:], start, end
    return '', [], 0, 0

"""
Adapters for the cheat sheets from the Learn X in Y project
"""
from __future__ import print_function

import os
import re
from globals import PATH_LEARNXINY

class LearnXYAdapter(object):

    """
    Parent class of all languages adapters
    """

    _learn_xy_path = PATH_LEARNXINY
    _replace_with = {}
    _filename = ''
    prefix = ''
    _replace_with = {}
    _splitted = True
    _block_cut_start = 2
    _block_cut_end = 0

    def __init__(self):

        self._whole_cheatsheet = self._read_cheatsheet()
        self._blocks = self._extract_blocks()

        self._topics_list = [x for x, _ in self._blocks]
        if "Comments" in self._topics_list:
            self._topics_list = [x for x in self._topics_list if x != "Comments"] + ["Comments"]
        self._topics_list += [":learn"]
        print(self.prefix, self._topics_list)

    def _is_block_separator(self, before, now, after):
        if (re.match(r'////////*', before)
                and re.match(r'// ', now)
                and re.match(r'////////*', after)):
            block_name = re.sub(r'//\s*', '', now).replace('(', '').replace(')', '')
            block_name = '_'.join(block_name.strip(", ").split())
            for character in '/,':
                block_name = block_name.replace(character, '')
            for k in self._replace_with:
                if k in block_name:
                    block_name = self._replace_with[k]
            return block_name
        return None

    def _cut_block(self, block, start_block=False):
        if not start_block:
            answer = block[self._block_cut_start:-self._block_cut_end]
        if answer == []:
            return answer
        if answer[0].strip() == '':
            answer = answer[1:]
        if answer[-1].strip() == '':
            answer = answer[:1]
        return answer

    def _read_cheatsheet(self):
        filename = os.path.join(self._learn_xy_path, self._filename)

        with open(filename) as f_cheat_sheet:
            code_mode = False
            answer = []
            for line in f_cheat_sheet.readlines():
                if line.startswith('```'):
                    if not code_mode:
                        code_mode = True
                        continue
                    else:
                        code_mode = False
                if code_mode:
                    answer.append(line.rstrip('\n'))
            return answer

    def _extract_blocks(self):

        if not self._splitted:
            return []

        lines = self._whole_cheatsheet
        answer = []

        block = []
        block_name = "Comments"
        for before, now, after in zip([""]+lines, lines, lines[1:]):
            new_block_name = self._is_block_separator(before, now, after)
            if new_block_name:
                if block_name:
                    block_text = self._cut_block(block)
                    if block_text != []:
                        answer.append((block_name, block_text))
                block_name = new_block_name
                block = []
                continue
            else:
                block.append(before)

        answer.append((block_name, self._cut_block(block)))
        return answer

    def is_valid(self, name):
        """
        Check whether topic `name` is valid.
        """

        for topic_list in self._topics_list:
            if topic_list == name:
                return True
        return False

    def get_list(self, prefix=False):
        """
        Get list of topics for `prefix`
        """
        if prefix:
            return ["%s/%s" % (self.prefix, x) for x in self._topics_list]
        return self._topics_list

    def get_cheat_sheet(self, name, partial=False):
        """
        Return specified cheat sheet `name` for the language.
        If `partial`, cheat sheet name may be shortened
        """

        if name == ":list":
            return "\n".join(self.get_list()) + "\n"

        if name == ":learn":
            return "\n".join(self._whole_cheatsheet) + "\n"

        if partial:
            possible_names = []
            for block_name, _ in self._blocks:
                if block_name.startswith(name):
                    possible_names.append(block_name)
            if possible_names == [] or len(possible_names) > 1:
                return None
            name = possible_names[0]

        for block_name, block_contents in self._blocks:
            if block_name == name:

                print("\n".join(block_contents))
                print(name)
                return "\n".join(block_contents)

        return None

#
# Specific programming languages LearnXY cheat sheets configurations
# Contains much code for the moment; should contain data only
# ideally should be replaced with YAML
#

class LearnAwkAdapter(LearnXYAdapter):
    "Learn AWK in Y Minutes"
    prefix = "awk"
    _filename = "awk.html.markdown"
    _splitted = False

class LearnBashAdapter(LearnXYAdapter):
    "Learn Bash in Y Minutes"
    prefix = "bash"
    _filename = "bash.html.markdown"
    _splitted = False

class LearnBfAdapter(LearnXYAdapter):
    "Learn Brainfuck in Y Minutes"
    prefix = "bf"
    _filename = "bf.html.markdown"
    _splitted = False

class LearnCAdapter(LearnXYAdapter):
    "Learn C in Y Minutes"
    prefix = "c"
    _filename = "c.html.markdown"
    _splitted = False

class LearnChapelAdapter(LearnXYAdapter):
    "Learn Chapel in Y Minutes"
    prefix = "chapel"
    _filename = "chapel.html.markdown"
    _splitted = False

class LearnClojureAdapter(LearnXYAdapter):
    """
    Learn Clojure in Y Minutes
    """

    prefix = "clojure"
    _filename = "clojure.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match(r'\s*$', before)
                and re.match(r';\s*', now)
                and re.match(r';;;;;;+', after)):
            block_name = re.sub(r';\s*', '', now)
            block_name = '_'.join([x.strip(",&:") for x in  block_name.strip(", ").split()])
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        if not start_block:
            answer = block[2:]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnCoffeeScriptAdapter(LearnXYAdapter):
    "Learn coffeescript in Y Minutes"
    prefix = "coffee"
    _filename = "coffeescript.html.markdown"
    _splitted = False

class LearnCppAdapter(LearnXYAdapter):
    """
    Learn C++ in Y Minutes
    """

    prefix = "cpp"
    _filename = "c++.html.markdown"
    _replace_with = {
        'More_about_Objects': 'Prototypes',
    }

    def _is_block_separator(self, before, now, after):
        if (re.match(r'////////*', before)
                and re.match(r'// ', now)
                and re.match(r'////////*', after)):
            block_name = re.sub(r'//\s*', '', now).replace('(', '').replace(')', '')
            block_name = '_'.join(block_name.strip(", ").split())
            for character in '/,':
                block_name = block_name.replace(character, '')
            for k in self._replace_with:
                if k in block_name:
                    block_name = self._replace_with[k]
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer == []:
            return answer
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnCsharpAdapter(LearnXYAdapter):
    "Learn C# in Y Minutes"
    prefix = "csharp"
    _filename = "csharp.html.markdown"
    _splitted = False

class LearnDAdapter(LearnXYAdapter):
    "Learn D in Y Minutes"
    prefix = "d"
    _filename = "d.html.markdown"
    _splitted = False

class LearnDartAdapter(LearnXYAdapter):
    "Learn Dart in Y Minutes"
    prefix = "dart"
    _filename = "dart.html.markdown"
    _splitted = False

class LearnFactorAdapter(LearnXYAdapter):
    "Learn Factor in Y Minutes"
    prefix = "factor"
    _filename = "factor.html.markdown"
    _splitted = False

class LearnForthAdapter(LearnXYAdapter):
    "Learn Forth in Y Minutes"
    prefix = "forth"
    _filename = "forth.html.markdown"
    _splitted = False

class LearnFsharpAdapter(LearnXYAdapter):
    "Learn F# in Y Minutes"
    prefix = "fsharp"
    _filename = "fsharp.html.markdown"
    _splitted = False

class LearnElispAdapter(LearnXYAdapter):
    "Learn Elisp in Y Minutes"
    prefix = "elisp"
    _filename = "elisp.html.markdown"
    _splitted = False

class LearnElixirAdapter(LearnXYAdapter):
    """
    Learn Elixir in Y Minutes
    """

    prefix = "elixir"
    _filename = "elixir.html.markdown"
    _replace_with = {
        'More_about_Objects': 'Prototypes',
    }

    def _is_block_separator(self, before, now, after):
        if (re.match(r'## ---*', before)
                and re.match(r'## --', now)
                and re.match(r'## ---*', after)):
            block_name = re.sub(r'## --\s*', '', now)
            block_name = '_'.join(block_name.strip(", ").split())
            for character in '/,':
                block_name = block_name.replace(character, '')
            for k in self._replace_with:
                if k in block_name:
                    block_name = self._replace_with[k]
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnElmAdapter(LearnXYAdapter):
    """
    Learn Elm in Y Minutes
    """

    prefix = "elm"
    _filename = "elm.html.markdown"
    _replace_with = {
        'More_about_Objects': 'Prototypes',
    }

    def _is_block_separator(self, before, now, after):
        if (re.match(r'\s*', before)
                and re.match(r'\{--.*--\}', now)
                and re.match(r'\s*', after)):
            block_name = re.sub(r'\{--+\s*', '', now)
            block_name = re.sub(r'--\}', '', block_name)
            block_name = '_'.join(block_name.strip(", ").split())
            for character in '/,':
                block_name = block_name.replace(character, '')
            for k in self._replace_with:
                if k in block_name:
                    block_name = self._replace_with[k]
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnErlangAdapter(LearnXYAdapter):
    """
    Learn Erlang in Y Minutes
    """

    prefix = "erlang"
    _filename = "erlang.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('%%%%%%+', before)
                and re.match(r'%%\s+[0-9]+\.', now)
                and re.match('%%%%%%+', after)):
            block_name = re.sub(r'%%+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip('.').strip().split())
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnFortranAdapter(LearnXYAdapter):
    "Learn Fortran in Y Minutes"
    prefix = "fortran"
    _filename = "fortran95.html.markdown"
    _splitted = False

class LearnGoAdapter(LearnXYAdapter):
    "Learn Go in Y Minutes"
    prefix = "go"
    _filename = "go.html.markdown"
    _splitted = False

class LearnGroovyAdapter(LearnXYAdapter):
    "Learn Groovy in Y Minutes"
    prefix = "groovy"
    _filename = "groovy.html.markdown"
    _splitted = False

class LearnJavaAdapter(LearnXYAdapter):
    "Learn Java in Y Minutes"
    prefix = "java"
    _filename = "java.html.markdown"
    _splitted = False

class LearnJavaScriptAdapter(LearnXYAdapter):
    """
    Learn JavaScript in Y Minutes
    """
    prefix = "js"
    _filename = "javascript.html.markdown"
    _replace_with = {
        'More_about_Objects': 'Prototypes',
    }

    def _is_block_separator(self, before, now, after):
        if (re.match('//////+', before)
                and re.match(r'//+\s+[0-9]+\.', now)
                and re.match(r'\s*', after)):
            block_name = re.sub(r'//+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip(", ").split())
            for k in self._replace_with:
                if k in block_name:
                    block_name = self._replace_with[k]
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnJuliaAdapter(LearnXYAdapter):
    """
    Learn Julia in Y Minutes
    """
    prefix = "julia"
    _filename = "julia.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('####+', before)
                and re.match(r'##\s*', now)
                and re.match('####+', after)):
            block_name = re.sub(r'##\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip(", ").split())
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnHaskellAdapter(LearnXYAdapter):
    """
    Learn Haskell in Y Minutes
    """
    prefix = "haskell"
    _filename = "haskell.html.markdown"
    _replace_with = {
        'More_about_Objects': 'Prototypes',
    }

    def _is_block_separator(self, before, now, after):
        if (re.match('------+', before)
                and re.match(r'--+\s+[0-9]+\.', now)
                and re.match('------+', after)):
            block_name = re.sub(r'--+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip(", ").split())
            for k in self._replace_with:
                if k in block_name:
                    block_name = self._replace_with[k]
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnLispAdapter(LearnXYAdapter):
    "Learn Lisp in Y Minutes"
    prefix = "lisp"
    _filename = "common-lisp.html.markdown"
    _splitted = False

class LearnLuaAdapter(LearnXYAdapter):
    """
    Learn Lua in Y Minutes
    """
    prefix = "lua"
    _filename = "lua.html.markdown"
    _replace_with = {
        '1_Metatables_and_metamethods': 'Metatables',
        '2_Class-like_tables_and_inheritance': 'Class-like_tables',
        'Variables_and_flow_control': 'Flow_control',
    }

    def _is_block_separator(self, before, now, after):
        if (re.match('-----+', before)
                and re.match('-------+', after)
                and re.match(r'--\s+[0-9]+\.', now)):
            block_name = re.sub(r'--+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip('.').strip().split())
            if block_name in self._replace_with:
                block_name = self._replace_with[block_name]
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnMathematicaAdapter(LearnXYAdapter):
    "Learn Mathematica in Y Minutes"
    prefix = "mathematica"
    _filename = "wolfram.html.markdown"
    _splitted = False

class LearnMatlabAdapter(LearnXYAdapter):
    "Learn Matlab in Y Minutes"
    prefix = "matlab"
    _filename = "matlab.html.markdown"
    _splitted = False

class LearnKotlinAdapter(LearnXYAdapter):
    """
    Learn Kotlin in Y Minutes
    """
    prefix = "kotlin"
    _filename = "kotlin.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('#######+', before)
                and re.match('#######+', after)
                and re.match(r'#+\s+[0-9]+\.', now)):
            block_name = re.sub(r'#+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip().split())
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnObjectiveCAdapter(LearnXYAdapter):
    "Learn Objective C in Y Minutes"
    prefix = "objective-c"
    _filename = "objective-c.html.markdown"
    _splitted = False

class LearnOCamlAdapter(LearnXYAdapter):
    """
    Learn OCaml in Y Minutes
    """
    prefix = "ocaml"
    _filename = "ocaml.html.markdown"
    _replace_with = {
        'More_about_Objects': 'Prototypes',
    }

    def _is_block_separator(self, before, now, after):
        if (re.match(r'\s*', before)
                and re.match(r'\(\*\*\*+', now)
                and re.match(r'\s*', after)):
            block_name = re.sub(r'\(\*\*\*+\s*', '', now)
            block_name = re.sub(r'\s*\*\*\*\)', '', block_name)
            block_name = '_'.join(block_name.strip(", ").split())
            for k in self._replace_with:
                if k in block_name:
                    block_name = self._replace_with[k]
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnPerlAdapter(LearnXYAdapter):
    """
    Learn Perl in Y Minutes
    """
    prefix = "perl"
    _filename = "perl.html.markdown"
    _replace_with = {
        'Conditional_and_looping_constructs': 'Control_Flow',
        'Perl_variable_types': 'Types',
        'Files_and_I/O': 'Files',
        'Writing_subroutines': 'Subroutines',
    }

    def _is_block_separator(self, before, now, after):
        if re.match(r'####+\s+', now):
            block_name = re.sub(r'#+\s', '', now)
            block_name = '_'.join(block_name.strip().split())
            if block_name in self._replace_with:
                block_name = self._replace_with[block_name]
            return block_name
        else:
            return None

    @staticmethod
    def _cut_block(block, start_block=False):
        if not start_block:
            answer = block[2:]
        if answer == []:
            return answer
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnPerl6Adapter(LearnXYAdapter):
    "Learn Perl 6 in Y Minutes"
    prefix = "perl6"
    _filename = "perl6.html.markdown"
    _splitted = False

class LearnPHPAdapter(LearnXYAdapter):
    """
    Learn PHP in Y Minutes
    """
    prefix = "php"
    _filename = "php.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match(r'/\*\*\*\*\*+', before)
                and re.match(r'\s*\*/', after)
                and re.match(r'\s*\*\s*', now)):
            block_name = re.sub(r'\s*\*\s*', '', now)
            block_name = re.sub(r'&', '', block_name)
            block_name = '_'.join(block_name.strip().split())
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        return block[2:]

class LearnPythonAdapter(LearnXYAdapter):
    """
    Learn Python in Y Minutes
    """
    prefix = "python"
    _filename = "python.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('#######+', before)
                and re.match('#######+', after)
                and re.match(r'#+\s+[0-9]+\.', now)):
            block_name = re.sub(r'#+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip().split())
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnPython3Adapter(LearnXYAdapter):
    "Learn Python 3 in Y Minutes"
    prefix = "python3"
    _filename = "python3.html.markdown"
    _splitted = False

class LearnRAdapter(LearnXYAdapter):
    "Learn R in Y Minutes"
    prefix = "r"
    _filename = "r.html.markdown"
    _splitted = False

class LearnRacketAdapter(LearnXYAdapter):
    "Learn Racket in Y Minutes"
    prefix = "racket"
    _filename = "racket.html.markdown"
    _splitted = False

class LearnRubyAdapter(LearnXYAdapter):
    """
    Learn Ruby in Y Minutes

    Format of the file was changed, so we have to fix the function too.
    This case is a good case for health check:
    if number of extracted cheat sheets is suddenly became 1,
    one should check the markup
    """
    prefix = "ruby"
    _filename = "ruby.html.markdown"

    def _is_block_separator(self, before, now, after):
        if (re.match('#######+', before)
                and re.match('#######+', after)
                and re.match(r'#+\s+[0-9]+\.', now)):
            block_name = re.sub(r'#+\s+[0-9]+\.\s*', '', now)
            block_name = '_'.join(block_name.strip().split())
            return block_name
        return None

    @staticmethod
    def _cut_block(block, start_block=False):
        answer = block[2:-1]
        if answer[0].split() == '':
            answer = answer[1:]
        if answer[-1].split() == '':
            answer = answer[:1]
        return answer

class LearnRustAdapter(LearnXYAdapter):
    "Learn Rust in Y Minutes"
    prefix = "rust"
    _filename = "rust.html.markdown"
    _splitted = False

class LearnSolidityAdapter(LearnXYAdapter):
    "Learn Solidity in Y Minutes"
    prefix = "solidity"
    _filename = "solidity.html.markdown"
    _splitted = False

class LearnSwiftAdapter(LearnXYAdapter):
    "Learn Swift in Y Minutes"
    prefix = "swift"
    _filename = "swift.html.markdown"
    _splitted = False

class LearnTclAdapter(LearnXYAdapter):
    "Learn Tcl in Y Minutes"
    prefix = "tcl"
    _filename = "tcl.html.markdown"
    _splitted = False

class LearnTcshAdapter(LearnXYAdapter):
    "Learn Tcsh in Y Minutes"
    prefix = "tcsh"
    _filename = "tcsh.html.markdown"
    _splitted = False

class LearnVisualBasicAdapter(LearnXYAdapter):
    "Learn Visual Basic in Y Minutes"
    prefix = "vb"
    _filename = "visualbasic.html.markdown"
    _splitted = False

ADAPTERS = {cls.prefix: cls() for cls in vars()['LearnXYAdapter'].__subclasses__()}

def get_learnxiny(topic, request_options=None):
    """
    Return cheat sheet for `topic`
    or empty string if nothing found
    """
    lang, topic = topic.split('/', 1)
    if lang not in ADAPTERS:
        return ''
    return ADAPTERS[lang].get_cheat_sheet(topic)

def get_learnxiny_list():
    """
    Return list of all learnxiny topics
    """
    answer = []
    for language_adapter in ADAPTERS.values():
        answer += language_adapter.get_list(prefix=True)
    return answer

def is_valid_learnxy(topic):
    """
    Return whether `topic` is a valid learnxiny topic
    """

    lang, topic = topic.split('/', 1)
    if lang not in ADAPTERS:
        return False

    return ADAPTERS[lang].is_valid(topic)

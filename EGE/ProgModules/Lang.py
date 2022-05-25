import re
from dataclasses import dataclass
from EGE import Html as html

class ops:

    power = [ '**' ]
    mult = [ '*', '/', '%', '//' ]
    add = [ '+', '-' ]
    comp = [ '>', '<', '==', '!=', '>=', '<=' ]
    logic = [ '&&', '||', '^', '=>', 'eq' ]
    bitwise = [ '&', '|' ]
    unary = [ '++{}', '--{}', '{}++', '{}--', '!', '+', '-' ]
    prio_unary = [ f"`{op}" for op in unary ]

    between = { 'between': [ '&&', [ '<=', 1, 0 ], [ '<=', 0, 2 ] ] }

class Lang:
    def __init__(self, params):
        # my $self = { %init };
        self.html = params.get('html') if params else 0
        self.unindent = params.get('unindent') if params else 0
        self.body_is_block = params.get('body_is_block') if params else 0
        self.prio = {}
        self.make_priorities()

    def to_html(self, s: str):
        return html.escape(s)

    def op_fmt(self, op):
        fmt = self.translate_op().get(op, op)
        regexp = re.compile(r'\{\d*\}')
        return (
            not isinstance(fmt, str) and fmt or
            isinstance(fmt, str) and regexp.search(fmt) and fmt or
            f"{{}} {fmt} {{}}")

    def un_op_fmt(self, op):
        fmt = self.translate_un_op().get(op, op)
        return '{}' in fmt and fmt or fmt + ' {}'

    #def name {
    #    ref($_[0]) =~ /::(\w+)$/;
    #    $1;
    #}

    @dataclass
    class G:
        left: str = ""
        inner: str = ""
        right: str = ""
        tag: str = ""
        alt: str = ""

    def print_tag(self, t: G):
        return (self.html and
            t.left + html.tag(t.tag, t.inner) + t.right or
            t.left + t.alt + t.inner + t.right)

    def get_fmt(self, name_fmt, args=None):
        args = f'"{args}"' if isinstance(args, str) else args
        fmt = eval(f"self.{name_fmt}" + (f"({args})" if args is not None else "()"))
        return (
            isinstance(fmt, dict) and self.print_tag(self.G(**fmt)) or
            isinstance(fmt, str) and self.html and self.to_html(fmt) or
            fmt)

    def var_fmt(self): return '{}'

    def make_priorities(self):
        raw = self.prio_list()
        for prio in range(len(raw)):
            for op in raw[prio]:
                self.prio[op] = prio + 1

    def prio_list(self):
        return [
            ops.prio_unary, ops.power, ops.mult, ops.add,
            ops.comp, [ '^', '=>' ] + ops.bitwise, [ '&&' ], [ '||' ], [ 'between' ],
        ]

    def translate_un_op(self): return {}

    def block_stmt_separator(self): return "\n"

    def args_separator(self): return ', '
    def args_fmt(self): return '{}'

    def call_func_fmt(self): return '{}({})'

    def expr_fmt(self): return '{}'

    def p_func_start_fmt(self, multiline: bool): return self.c_func_start_fmt(multiline)
    def p_func_end_fmt(self, multiline: bool): return self.c_func_end_fmt(multiline)

    def p_return_fmt(self): return self.c_return_fmt()


class Basic(Lang):

    def assign_fmt(self): return '{} = {}'
    def index_fmt(self): return '{}({})'
    def translate_op(self):
        return {
            '**': '^',
            '%': 'MOD', '//': '\\',
            '==': '=', '!=': '<>',
            '&&': 'AND', '||': 'OR', '^': 'XOR', '=>': 'IMP', 'eq': 'EQV',
            **ops.between
        }

    def translate_un_op(self): return { '!': 'NOT' }

    def for_start_fmt(self, multiline: bool): return "FOR {} = {} TO {}\n"
    def for_end_fmt(self, multiline: bool): return "\nNEXT {}"

    def if_start_fmt(self, multiline: bool):
        return 'IF {} THEN' + (multiline and "\n" or ' ')

    def if_end_fmt(self, multiline: bool):
        return multiline and "\nEND IF" or ''

    def while_start_fmt(self, multiline: bool): return "DO WHILE {}\n"
    def while_end_fmt(self, multiline: bool): return "\nEND DO"

    def until_start_fmt(self, multiline: bool): return "DO UNTIL {}\n"
    def until_end_fmt(self, multiline: bool): return "\nEND DO"

    def c_func_start_fmt(self, multiline: bool): return "FUNCTION {}({})\n"
    def c_func_end_fmt(self, multiline: bool): return "\nEND FUNCTION\n"

    def print_fmt(self): return 'PRINT {}'
    def print_str_fmt(self): return 'PRINT "{}"'

    def input_int_fmt(self): return 'INPUT {}'

    def c_return_fmt(self): return 'RETURN {}'


class C(Lang):

    def assign_fmt(self): return '{} = {};'
    def index_fmt(self): return '{}[{}]'
    def translate_op(self):
        return {
            '**': 'pow({}, {})', '//': 'int({} / {})', '=>': '<=', 'eq': '==',
            **ops.between
        }

    def for_start_fmt(self, multiline: bool):
    # !!!!
        return 'for ({0} = {1}; {0} <= {2}; ++{0})' + (multiline and '{{' or '') + "\n"

    def for_end_fmt(self, multiline: bool):
        return multiline and "\n}}" or ''

    def if_start_fmt(self, multiline: bool):
        return 'if ({})' + (multiline and " {{\n" or "\n")
    def if_end_fmt(self, multiline: bool):
        return multiline and "\n}}" or ''

    def while_start_fmt(self, multiline: bool):
        return 'while ({})' + (multiline and " {{\n" or "\n")
    def while_end_fmt(self, multiline: bool):
        return multiline and "\n}}" or ''

    def until_start_fmt(self, multiline: bool):
        return 'while (!({}))' + (multiline and " {{\n" or "\n")
    def until_end_fmt(self, multiline: bool):
        return multiline and "\n}}" or ''

    def c_func_start_fmt(self, multiline: bool): return "int {}({}) {{\n"
    def c_func_end_fmt(self, multiline: bool): return "\n}}\n"

    def p_func_start_fmt(self, multiline: bool): return "int {0}({1}) {{\n  int {0};\n"
    def p_func_end_fmt(self, multiline: bool): return "\n  return {};\n}}\n"

    def print_fmt(self): return 'print({})'
    def print_str_fmt(self): return 'printf("{}")'

    def input_int_fmt(self): return 'scanf("%d", &{})'

    def expr_fmt(self): return '{};'

    def args_fmt(self): return 'int {}'

    def c_return_fmt(self): return 'return {};'


class Pascal(Lang):

    def prio_list(self):
        return [
            ops.prio_unary, ops.power, ops.mult + [ '&&' ],
            ops.add + [ '||', '^' ], ops.comp + [ '=>', 'eq' ], [ 'between' ]
        ]

    def assign_fmt(self): return '{} := {};'
    def index_fmt(self): return '{}[{}]'
    def translate_op(self):
        return {
            '%': 'mod', '//': 'div',
            '==': '=', '!=': '<>',
            '&&': 'and', '||': 'or', '^': 'xor', '=>': '<=', 'eq': '=',
            'between': 'InRange({}, {}, {})',
        }

    def translate_un_op(self): return { '!': 'not' }

    def for_start_fmt(self, multiline: bool):
        return 'for {} := {} to {} do' + (multiline and ' begin' or '') + "\n"
    def for_end_fmt(self, multiline: bool):
        return multiline and "\nend;" or ''

    def if_start_fmt(self, multiline: bool):
        return 'if {} then' + (multiline and " begin\n" or "\n")
    def if_end_fmt(self, multiline: bool):
        return multiline and "\nend;" or ''

    def while_start_fmt(self, multiline: bool):
        return 'while {} do' + (multiline and " begin\n" or "\n")
    def while_end_fmt(self, multiline: bool):
        return multiline and "\nend;" or ''

    def until_start_fmt(self, multiline: bool):
        return 'while not ({}) do' + (multiline and " begin\n" or "\n")
    def until_end_fmt(self, multiline: bool):
        return multiline and "\nend;" or ''

    def c_func_start_fmt(self, multiline: bool): return "function {}({}: integer): integer;\nbegin\n"
    def c_func_end_fmt(self, multiline: bool): return "\nend;\n"

    def print_fmt(self): return 'write({})'
    def print_str_fmt(self): return "write('{}')"

    def input_int_fmt(self): return 'readln({})'

    def expr_fmt(self): return '{};'

    def c_return_fmt(self): return 'exit({});'
    def p_return_fmt(self): return 'exit;'


class Alg(Lang):

    def assign_fmt(self): return '{} := {}'
    def index_fmt(self): return '{}[{}]'
    def translate_op(self):
        return {
            '==': '=', '!=': '≠',
            '%': 'mod({}, {})', '//': 'div({}, {})',
            '&&': 'и', '||': 'или', '=>': '→', 'eq': '≡',
            **ops.between,
        }
    def translate_un_op(self): return { '!': 'не' }

    def for_start_fmt(self, multiline: bool): return "нц для {} от {} до {}\n"
    def for_end_fmt(self, multiline: bool): return "\nкц"

    def if_start_fmt(self, multiline: bool): return "если {} то\n"
    def if_end_fmt(self, multiline: bool): return "\nвсе"

    def while_start_fmt(self, multiline: bool): return "пока {} нц\n"
    def while_end_fmt(self, multiline: bool): return "\nкц"

    def until_start_fmt(self, multiline: bool): return "пока не ({}) нц\n"
    def until_end_fmt(self, multiline: bool): return "\nкц"

    def c_func_start_fmt(self, multiline: bool): return "алг цел {}(цел {})\nнач\n"
    def c_func_end_fmt(self, multiline: bool): return "\nкон\n"

    def print_fmt(self): return 'вывод {}'
    def print_str_fmt(self): return 'вывод "{}"'

    def input_int_fmt(self): return 'ввод {}'

    def c_return_fmt(self):
        return 'выход_алг {} | выход_алг выраж - оператор выхода из алгоритма, с возвращением результата выраж'
    def p_return_fmt(self):
        return 'выход_алг | выход_алг - оператор выхода из алгоритма'


class Perl(Lang):

    def var_fmt(self): return '${}'
    def assign_fmt(self): return '{} = {};'
    def index_fmt(self): return '${}[{}]'
    def translate_op(self):
        return { '//': 'int({} / {})', '=>': '<=', 'eq': '==', **ops.between }

    def for_start_fmt(self, multiline: bool): return 'for ({0} = {1}; {0} <= {2}; ++{0}) {{' + "\n"
    def for_end_fmt(self, multiline: bool): return "\n}}"

    def if_start_fmt(self, multiline: bool): return "if ({}) {{\n"
    def if_end_fmt(self, multiline: bool): return "\n}}"

    def while_start_fmt(self, multiline: bool): return "while ({}) {{\n"
    def while_end_fmt(self, multiline: bool): return "\n}}"

    def until_start_fmt(self, multiline: bool): return "until ({}) {{\n"
    def until_end_fmt(self, multiline: bool): return "\n}}"

    def c_func_start_fmt(self, multiline: bool): return "sub {} {{\n  my ({}) = @_;\n"
    def c_func_end_fmt(self, multiline: bool): return "\n}}\n"

    def p_func_start_fmt(self, multiline: bool): return "sub {0} {{\n  my ${0};\n  my ({1}) = @_;\n"
    def p_func_end_fmt(self, multiline: bool): return "\n  return ${};\n}}\n"

    def print_fmt(self): return 'print({})'
    def print_str_fmt(self): return "print('{}')"

    def input_int_fmt(self): return '{} = <STDIN>'

    def expr_fmt(self): return '{};'

    def args_fmt(self): return '${}'

    def c_return_fmt(self): return 'return {};'


class Logic(Lang):

    def prio_list(self):
        return [
            ops.prio_unary, ops.power, ops.mult, ops.add,
            ops.comp, [ '&&' ], [ '||', '^' ], [ '=>', 'eq' ],
        ]

    def index_fmt(self): return { 'left': '{}', 'inner': '{}', 'tag': 'sub', 'alt': '_' }

    def translate_op(self):
        return {
            '**': { 'left': '{}', 'inner': '{}', 'tag': 'sup', 'alt': ' ^ ' },
            '-': '−', '*': '⋅',
            '==': '=', '!=': '≠', '>=': '≥', '<=': '≤',
            '&&': '∧', '||': '∨', '^': '⊕', '=>': '→', 'eq': '≡',
        }

    def var_fmt(self): return { 'inner': '{}', 'tag': 'i' }

    def call_func_fmt(self): return { 'inner': '{}', 'tag': 'i', 'right': '({})' }

    def translate_un_op(self): return { '!': '¬' }


class SQL(Lang):

    def translate_op(self):
        return {
            '**': 'POWER({}, {})',
            '==': '=', '!=': '<>','&&': 'AND', '||': 'OR',
            'between': '{} BETWEEN {} AND {}',
        }

    def translate_un_op(self): return { '!': 'NOT' }

    def assign_fmt(self): return '{} = {}'
    def block_stmt_separator(self): return ', '

class Python(Lang):
    def var_fmt(self): return '{}'
    def assign_fmt(self): return '{} = {}'
    def index_fmt(self): return '{}[{}]'

    def translate_op(self):
        return {
            '=>': '<=', 'eq': '==',
            '&&': '&', '||': '|',
            'between': '{1} <= {0} <= {2}'
        }

    def un_op_fmt(self, op):
        fmt = self.translate_un_op().get(op, op)
        fmt = 'not ' if fmt == '!' else fmt
        return '{}' in fmt and fmt or fmt + '{}'

    def for_start_fmt(self, multiline: bool): return 'for {} in range({}; {}; {}):' + "\n"
    def for_end_fmt(self, multiline: bool): return "\n"

    def if_start_fmt(self, multiline: bool): return "if ({}): \n"
    def if_end_fmt(self, multiline: bool): return "\n"

    def while_start_fmt(self, multiline: bool): return "while ({}): \n"
    def while_end_fmt(self, multiline: bool): return "\n"

    def until_start_fmt(self, multiline: bool): return "until ({}):\n"
    def until_end_fmt(self, multiline: bool): return "\n"

    def c_func_start_fmt(self, multiline: bool): return "def {}({}):\n"
    def c_func_end_fmt(self, multiline: bool): return "\n\n"

    def p_func_start_fmt(self, multiline: bool): return "def {}({}):\n"
    def p_func_end_fmt(self, multiline: bool): return "\n  return {}\n"

    def print_fmt(self): return 'print({})'
    def print_str_fmt(self): return "print('{}')"

    def input_int_fmt(self): return '{} = int(input())'

    def expr_fmt(self): return '{}'

    def args_fmt(self): return '{}'

    def c_return_fmt(self): return 'return {}'

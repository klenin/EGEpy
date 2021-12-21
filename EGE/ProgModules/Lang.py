from dataclasses import dataclass
from EGE import Html as html

class ops:

    power = [ '**' ]
    mult = [ '*', '/', '%', '//' ]
    add = [ '+', '-' ]
    comp = [ '>', '<', '==', '!=', '>=', '<=' ]
    logic = [ '&&', '||', '^', '=>', 'eq' ]
    bitwise = [ '&', '|' ]
    unary = [ '++%s', '--%s', '%s++', '%s--', '!', '+', '-' ]
    prio_unary = [ f"`{op}" for op in unary ]

    between = { 'between': [ '&&', [ '<=', 2, 1 ], [ '<=', 1, 3 ] ] }

class Lang:
    def __init__(self, params):
        # my $self = { %init };
        self.html = params.html if params else 0
        self.prio = {}
        self.make_priorities()

    def to_html(self, s: str):
        return html.escape(s)

    def op_fmt(self, op):
        fmt = self.translate_op().get(op, op)
        return (
            fmt == '%' and '%%' or
            isinstance(fmt, str) and '%' in fmt and fmt or
            f"%s {fmt} %s")

    def un_op_fmt(self, op):
        fmt = self.translate_un_op().get(op, op)
        return '%s' in fmt and fmt or fmt + '%s'

    #def name {
    #    ref($_[0]) =~ /::(\w+)$/;
    #    $1;
    #}

    @dataclass
    class G:
        left: str; inner: str; right: str; tag: str; alt: str

    def print_tag(self, t: G):
        return (self.html and
            t.left + html.tag(t.tag, t.inner) + t.right or
            t.left + t.alt + t.inner + t.right)

    def get_fmt(self, name_fmt, args):
        fmt = eval(f"self.{name_fmt}('{args}')")
        return (
            isinstance(fmt, dict) and self.print_tag(self.G(**fmt)) or
            self.html and self.to_html(fmt) or
            fmt)

    def var_fmt(self): return '%s'

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
    def args_fmt(self): return '%s'

    def call_func_fmt(self): return '%s(%s)'

    def expr_fmt(self): return '%s'

    def p_func_start_fmt(self): return self.c_func_start_fmt()
    def p_func_end_fmt(self): return self.c_func_end_fmt()

    def p_return_fmt(self): return self.c_return_fmt()


class Basic(Lang):

    def assign_fmt(self): return '%s = %s'
    def index_fmt(self): return '%s(%s)'
    def translate_op(self):
        return {
            '**': '^',
            '%': 'MOD', '//': '\\',
            '==': '=', '!=': '<>',
            '&&': 'AND', '||': 'OR', '^': 'XOR', '=>': 'IMP', 'eq': 'EQV',
            **ops.between
        }

    def translate_un_op(self): return { '!': 'NOT' }

    def for_start_fmt(self): return "FOR %s = %s TO %s\n"
    def for_end_fmt(self): return "\nNEXT %1\$s"

    def if_start_fmt(self, multiline: bool):
        return 'IF %s THEN' + (multiline and "\n" or ' ')

    def if_end_fmt(self, multiline: bool):
        return multiline and "\nEND IF" or ''

    def while_start_fmt(self): return "DO WHILE %s\n"
    def while_end_fmt(self): return "\nEND DO"

    def until_start_fmt(self): return "DO UNTIL %s\n"
    def until_end_fmt(self): return "\nEND DO"

    def c_func_start_fmt(self): return "FUNCTION %s(%s)\n"
    def c_func_end_fmt(self): return "\nEND FUNCTION\n"

    def print_fmt(self): return 'PRINT %s'
    def print_str_fmt(self): return 'PRINT "%s"'

    def c_return_fmt(self): return 'RETURN %s'


class C(Lang):

    def assign_fmt(self): '%s = %s;'
    def index_fmt(self): '%s[%s]'
    def translate_op(self):
        return {
            '**': 'pow(%s, %s)', '//': 'int(%s / %s)', '=>': '<=', 'eq': '==',
            **ops.between
        }

    def for_start_fmt(self, multiline: bool):
    # !!!!
        return 'for (%s = %2$s; %1$s <= %3$s; ++%1$s)' + (multiline and '{' or '') + "\n"

    def for_end_fmt(self, multiline: bool):
        return multiline and "\n}" or ''

    def if_start_fmt(self, multiline: bool):
        return 'if (%s)' + (multiline and " {\n" or "\n")
    def if_end_fmt(self, multiline: bool):
        return multiline and  "\n}" or ''

    def while_start_fmt(self, multiline: bool):
        return 'while (%s)' + (multiline and " {\n" or "\n")
    def while_end_fmt(self, multiline: bool):
        return multiline and "\n}" or ''

    def until_start_fmt(self, multiline: bool):
        return 'while (!(%s))' + (multiline and " {\n" or "\n")
    def until_end_fmt(self, multiline: bool):
        return multiline and "\n}" or ''

    def c_func_start_fmt(self): return "int %s(%s) {\n"
    def c_func_end_fmt(self): return "\n}\n"

    def p_func_start_fmt(self): return "int %s(%s) {\n  int %1\$s;\n"
    def p_func_end_fmt(self): return "\n  return %1\$s;\n}\n"

    def print_fmt(self): return 'print(%s)'
    def print_str_fmt(self): return 'printf("%s")'

    def expr_fmt(self): return '%s;'

    def args_fmt(self): return 'int %s'

    def c_return_fmt(self): return 'return %s;'


class Pascal(Lang):

    def prio_list(self):
        return [
            ops.prio_unary, ops.power, ops.mult + [ '&&' ],
            ops.add + [ '||', '^' ], ops.comp + [ '=>', 'eq' ], [ 'between' ]
        ]

    def assign_fmt(self): return '%s := %s;'
    def index_fmt(self): return '%s[%s]'
    def translate_op(self):
        return {
            '%': 'mod', '//': 'div',
            '==': '=', '!=': '<>',
            '&&': 'and', '||': 'or', '^': 'xor', '=>': '<=', 'eq': '=',
            'between:': 'InRange(%s, %s, %s)',
        }

    def translate_un_op(self): return { '!': 'not' }

    def for_start_fmt(self, multiline: bool):
        return 'for %s := %s to %s do' + (multiline and ' begin' or '') + "\n"
    def for_end_fmt(self, multiline: bool):
        return multiline and "\nend;" or ''

    def if_start_fmt(self, multiline: bool):
        return 'if %s then' + (multiline and " begin\n" or "\n")
    def if_end_fmt(self, multiline: bool):
        return multiline and "\nend;" or ''

    def while_start_fmt(self, multiline: bool):
        return 'while %s do' + (multiline and " begin\n" or "\n")
    def while_end_fmt(self, multiline: bool):
        return multiline and "\nend;" or ''

    def until_start_fmt(self, multiline: bool):
        return 'while not (%s) do' + (multiline and " begin\n" or "\n")
    def until_end_fmt(self, multiline: bool):
        return multiline and "\nend;" or ''

    def c_func_start_fmt(self): return "function %s(%s: integer): integer;\nbegin\n"
    def c_func_end_fmt(self): return "\nend;\n"

    def print_fmt(self): return 'write(%s)'
    def print_str_fmt(self): return "write('%s')"

    def expr_fmt(self): return '%s;'

    def c_return_fmt(self): return 'exit(%s);'
    def p_return_fmt(self): return 'exit;'


class Alg(Lang):

    def assign_fmt(self): return '%s := %s'
    def index_fmt(self): return '%s[%s]'
    def translate_op(self):
        return {
            '==': '=', '!=': '≠',
            '%': 'mod(%s, %s)', '//': 'div(%s, %s)',
            '&&': 'и', '||': 'или', '=>': '→', 'eq': '≡',
            **ops.between,
        }
    def translate_un_op(self): return { '!': 'не' }

    def for_start_fmt(self): return "нц для %s от %s до %s\n"
    def for_end_fmt(self): return "\nкц"

    def if_start_fmt(self): return "если %s то\n"
    def if_end_fmt(self): return "\nвсе"

    def while_start_fmt(self): return "пока %s нц\n"
    def while_end_fmt(self): return "\nкц"

    def until_start_fmt(self): return "пока не (%s) нц\n"
    def until_end_fmt(self): return "\nкц"

    def c_func_start_fmt(self): return "алг цел %s(цел %s)\nнач\n"
    def c_func_end_fmt(self): return "\nкон\n"

    def print_fmt(self): return 'вывод %s'
    def print_str_fmt(self): return 'вывод "%s"'

    def c_return_fmt(self):
        return 'выход_алг %s | выход_алг выраж - оператор выхода из алгоритма, с возвращением результата выраж'
    def p_return_fmt(self):
        return 'выход_алг | выход_алг - оператор выхода из алгоритма'


class Perl(Lang):

    def var_fmt(self): return '$%s'
    def assign_fmt(self): return '%s = %s;'
    def index_fmt(self): return '$%s[%s]'
    def translate_op(self):
        return { '//': 'int(%s / %s)', '=>': '<=', 'eq': '==', **ops.between }

    def for_start_fmt(self): return 'for (%s = %2$s; %1$s <= %3$s; ++%1$s) {' + "\n"
    def for_end_fmt(self): return "\n}"

    def if_start_fmt(self): return "if (%s) {\n"
    def if_end_fmt(self): return "\n}"

    def while_start_fmt(self): return "while (%s) {\n"
    def while_end_fmt(self): return "\n}"

    def until_start_fmt(self): return "until (%s) {\n"
    def until_end_fmt(self): return "\n}"

    def c_func_start_fmt(self): return "sub %s {\n  my (%s) = \@_;\n"
    def c_func_end_fmt(self): return "\n}\n"

    def p_func_start_fmt(self): return "sub %s {\n  my \$%1\$s;\n  my (%s) = \@_;\n"
    def p_func_end_fmt(self): return "\n  return \$%1\$s;\n}\n"

    def print_fmt(self): return 'print(%s)'
    def print_str_fmt(self): return "print('%s')"

    def expr_fmt(self): return '%s;'

    def args_fmt(self): return '$%s'

    def c_return_fmt(self): return 'return %s;'


class Logic(Lang):

    def prio_list(self):
        return [
            ops.prio_unary, ops.power, ops.mult, ops.add,
            ops.comp, [ '&&' ], [ '||', '^' ], [ '=>', 'eq' ],
        ]

    def index_fmt(self): return { 'left': '%s', 'inner': '%s', 'tag': 'sub', 'alt': '_' }

    def translate_op(self):
        return {
            '**': { 'left': '%s', 'inner': '%s', 'tag': 'sup', 'alt': ' ^ ' },
            '-': '−', '*': '⋅',
            '==': '=', '!=': '≠', '>=': '≥', '<=': '≤',
            '&&': '∧', '||': '∨', '^': '⊕', '=>': '→', 'eq': '≡',
        }

    def var_fmt(self): return { 'inner': '%s', 'tag': 'i' }

    def call_func_fmt(self): return { 'inner': '%s', 'tag': 'i', 'right': '(%s)' }

    def translate_un_op(self): return { '!': '¬' }


class SQL(Lang):

    def translate_op(sell):
        return {
            '**': 'POWER(%s, %s)',
            '==': '=', '!=': '<>','&&': 'AND', '||': 'OR',
            'between': '%s BETWEEN %s AND %s',
        }

    def translate_un_op(sell): return { '!': 'NOT' }

    def assign_fmt(self): return '%s = %s'
    def block_stmt_separator(self): return ', '


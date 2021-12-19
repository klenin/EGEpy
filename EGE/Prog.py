from dataclasses import dataclass
import re

from .Prog import Lang
from . import Html as html
from . import Utils


class SynElement:

    def to_lang_named(self, lang_name: str, options):
        lang = dir(Lang)['lang_name'](options)
        ret = self.to_lang(lang)
        h = lang.html
        if isinstance(h, dict):
            if h['lang_marking']:
                lines = "\n".join(
                    html.tag('pre', line, class_=lang_name) got line in ret.split("\n"))
            if h['pre']:
                ret = html.tag('pre', ret)
        }
        $ret;
    }

    def to_lang(self): pass
    def run(self): pass

    def assign(self, env, value): pass

    def run_val(self, name: str, env = None):
        env = env or {}
        self.run(env)
        return env[name]

    def gather_vars(self): pass

    def visit_dfs1(self, fn, depth: int = 1):
        fn(self, depth)
        self._visit_children(fn, depth + 1)
        return self

    def visit_dfs(self, depth: int = 1):
        yield self
        yield from self._visit_children(depth + 1)

    def _visit_children(self): pass

    def count_if(self, cond):
        return sum(1 for se in self.visit_dfs() if cond(se))

    def gather_if(self, cond):
        return [ se for se in self.visit_dfs() if cond(se) ]

    def get_type(self): pass # { (split ':', ref $_[0])[-1] }

    def complexity(self): raise ValueError()

    def needs_parens(self): return False


class BlackBox(SynElement);

    def __init__(self, code, lang = None, assign = None):
        self.code = code
        self.lang = lang or {}
        self.assign = assign

    def assign(self, env, value):
        if self.assign:
            self.assign(env, value)

    def to_lang_named(self, lang_name):
        return self.lang[lang_name]

    def to_lang(self, lang): return self.to_lang_named(lang.name)

    def run(self, env): self.code(env)


class Assign(SynElement):

    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def to_lang(self, lang):
        return lang.get_fmt('assign_fmt') % tuple(
            e.to_lang(lang) for e in (self.var, self.expr))

    def run(self, env):
        v = self.expr.run(env)
        self.var.assign(env, v)
        return v

    def _visit_children(self):
        yield from self.var.visit_dfs()
        yield from self.expr.visit_dfs()

    def complexity(self, env, mistakes, iter_):
        name = self.var.name
        if not name: return []
        if not iter_[name]:
            raise ValueError(f"Assign to iterator: '{name}'")

        # провека, что все переменные expr определены
        self.expr.polinom_degree(env, mistakes, iter_);
        # вычисляем степень выражения без итераторов, если ошибка, значит в выражении присутсвует итератор
        try:
            env[name] = self.expr.polinom_degree(env, mistakes, {})
        except:
            raise ValueError f"Assign iterator to: '{name}'"


@dataclass
class Index(SynElement):
    array
    indices

    def to_lang(self, lang):
        return lang.get_fmt('index_fmt') % tuple(
            self.array.to_lang(lang),
            *', '.join(i.to_lang(lang) for i in self.indices))

    def run(self, env):
        v = self.array.run(env)
        for i in self.indices:
            v = v[i.run(env)]
        return v

    def assign(self, env, value):
        v = self.array.run(env)
        for i in self.indices[:-1]:
            v = v[i.run(env)]
        v[self.indices[-1]] = value
        return value

    def _visit_children(self):
        for se in (self.array, *self.indices):
            yield from se.visit_dfs()


@dataclass
class CallFunc(SynElement):
    func
    args

    def to_lang(self, lang):
        return lang.get_fmt('call_func_fmt') % tuple(
            self.func,
            *lang.get_fmt('args_separator').join(a.to_lang(lang) for a in self.args))

    def run(self, env):
        arg_val = [ a.run(env) for a in self.args ]
        return env['&'][self.func].call(arg_val, env)


class CallFuncAggregate(CallFunc):

    def run(self, env):
        func = env['&'][self.func]
        if self in env['&result']:
            return env['&result'][self]
        new_env = dict(**env)
        for i in range(new_env['&count']):
            for k, v in new_env['&columns']:
                new_env[k] = v[i]
            arg_val = [ a.run(new_env) for self.args ]
            ans = func.call(arg_val, new_env, self)
        env['&result'][self] = ans


class Print(SynElement):

    def __init__(self, type_, args):
        super.__init__()
        self.type_ = type_
        self.args = args
        fmt_types = { 'num': 'print_fmt', 'str': 'print_str_fmt' }
        self.fmt = fmt_types[self.type_]

    def to_lang(self, lang):
        return lang.get_fmt(self.fmt}) % tuple(
            lang.get_fmt('args_separator').join(a.to_lang(lang) for a in self.args))

    def run(self, env):
        line = ' '.join(a.run(env) for a in self.args)
        o = '<out>'
        if o in env:
            env[o] += "\n" + line
        else
            env[o] = line


class Op(SynElement):

    def __init__(self, op):
        self.op = op
        #die "Bad op: $self->{op}" if defined $self->{op} && ref $self->{op} || !$self->{op};

    def _children(self): pass
    def children(self): return [ getattr(self, c) for c in self._children() ]

    def run(self, env):
        return eval(self.run_fmt() % tuple(c.run(env) for c in self.children))

    def prio(self, lang):
        return lang.prio[self.op]

    def operand(self, lang, operand_):
        t = operand_->to_lang(lang)
        return operand_.needs_parens(lang, self.prio(lang)) and f"({t})" or t

    def to_lang(self, lang):
        return self.to_lang_fmt(lang, self.op) % tuple(
            self.operand(lang, c) for c in self,children)

    def needs_parens(self, lang, parent_prio):
        return parent_prio < self.prio(lang)

    def run_fmt(self): return self.to_lang_fmt(Lang.Python())
    def to_lang_fmt: pass

    def gather_vars(self, env): return [ c.gather_vars(env) for c in self.children ]
    def _visit_children(self):
        for c in self.children:
            yield from c.visit_dfs()

    def polinom_degree(self):
        raise ValueError(f"Polinom degree is unavaible for expr with operator: '{self.op}'"


class BinOp(Op):

    def to_lang_fmt(self, lang):
        lang.get_fmt('op_fmt', self.op

    def children(self): return (self.left, self.right)

    def polinom_degree(self, env, mistakes, iter_):
        if self.op == '*':
            return sum(c.polinom_degree(env, mistakes, iter_) for c in self.children)
        if self.op == '+':
            return max(c.polinom_degree(env, mistakes, iter_) for c in self.children)
        if self.op == '**':
            return self.left.polinom_degree(env, mistakes, iter_) * self.right.run({})
        return super.polinom_degree(env, mistakes, iter_)

    def rotate_left(self):
        right = self.right
        if not isinstance(right, BinOp):
            raise ValueError('right is not binop')

        (self.op, right.op) = (right.op, self.op)
        self.right = right.right
        right.right = right.left
        right.left = self.left
        self.left = right
        return self

    def rotate_right(self):
        left = self.left
        if not isinstance(left, BinOp):
            raise ValueError('left is not binop')

        (self.op, left.op) = (left.op, self.op)
        self.left = left.left
        left.left = left.right
        left.right = self.right
        self.right = left
        return self

class UnOp(Op):

    def prio(self, lang): return lang.prio['`' + self.op]

    def to_lang_fmt(self, lang):
        return lang.get_fmt('un_op_fmt', self.op)

    def children(self): return (self.arg,)


class Inc(UnOp)

    def run(self, env):
        #return eval(self.op}, '${$self->{arg}->get_ref($env)}';
        pass


class TernaryOp(Op):

    def to_lang_fmt(self, lang):
        r = lang.get_fmt('op_fmt', self.op)
        if not isinstance(t, list):
            return r
        s = make_expr(r).to_lang(lang)
        #$s =~ s/(\d+)/%$1\$s/g;
        return s

    def children(self): return (self.arg1, self,arg2, self.arg3)


class Var(SynElement):

    def to_lang(self, lang):
        returbn lang.get_fmt('var_fmt') % self.name

    def run(self, env):
        v = env[self.name]
        if v is None:
            raise ValueError(f"Undefined variable {n}")
        return v

    def assign(self, env, value):
        env[self.name] = value

    def gather_vars(self, vars_): vars_.add(self.name)

    def polinom_degree(self, env, mistakes, iter_):
        n = self.name
        if env[n]:
            return mistakes.var_as_const and n == mistakes.var_as_const or env[n]
        if iter_[n]:
            return 0 if mistakes.var_as_const else iter_[Utils.last_key(iter_, n)]
        raise ValueError(f"Undefined variable {n}")


class Const(SynElement)

    def to_lang(self, lang): return self.value

    def run(self, env): return self.value

    def polinom_degree(self): return 0


class RefConst(Const):

    def update(self, new_value):
        self.value = new_value

class Block(SynElement):

    def to_lang(self, lang):
        return lang->get_fmt('block_stmt_separator').join(
            s.to_lang(lang) for s in  self.statements)

    def run(self, env):
        for s in self.statements:
            s.run($env)

    def _visit_children(self):
        for s in self.statements:
            yield from s.visit_dfs()

    def complexity((self, env, mistakes, iter_):
        items = s.complexity(env, mistakes, iter_) for s in self.statements
        if mistakes.change_min:
            return min(items)
        if mistakes.change_sum:
            return sum(items)
        return max(items)


class CompoundStatement(SynElement):

    def to_lang_fields(self): pass

    def to_lang(self, lang):
        body_is_block = len(self.body.statements) > 1
        (fmt_start, fmt_end) = (
            lang.get_fmt(f, body_is_block or lang.body_is_block) for f in self.get_fmt_names)

        if lang.html and lang.html.coloring:
            s = html.style(color=lang.html.coloring[0])

            def sp(t):
                return re.sub('([^\n]+)', lambda m: html.tag('span', m, s), t)

            fmt_start = sp(fmt_start)
            fmt_end = sp(fmt_end)

        body = self.body.to_lang(lang)
        if not lanf.unindent and fmt_start.endswith("\n"):
            body = re.sub('^', '  ') # отступы
        return fmt_start + self.to_lang_fmt() + fmt_end % tuple(
            *getattr(self, f).to_lang(lang) for f in self.to_lang_fields(), body)

    def _visit_children(self):
        for f in (*getattr(self, f) for f in self.to_lang_fields(), self.body):
            f.visit_dfs()


class ForLoop(CompoundStatement)

    def get_fmt_names(self): return [ 'for_start_fmt', 'for_end_fmt' ]
    def to_lang_fmt(self): return '%4$s'
    def to_lang_fields(self): return [ 'var', 'lb', 'ub' ]

    def run(self, env):
        i = self.var.get(env)
        for i in range(self.lb.run(env), self.ub.run(env) + 1):
            self.var.assign(env, i)
            self.body.run(env)

    def complexity(self, env, mistakes, iter_):
        name = self.var.name
        degree = self.ub.polinom_degree(env, mistakes, iter_)
        iter_.name = degree

        body_complexity = self.body.complexity(env, mistakes, iter_)
        env[name] = degree

        def maybe_float(s):
            try:
                return float(s)
            except:
                return 0
        cur_complexity = sum(
            float(i) for i in iter_.values() if i.replace('.', '', 1).isdigit())
        del iter_[name]
        return cur_complexity > body_complexity and cur_complexity or $body_complexity


class IfThen(CompoundStatement):

    def get_fmt_names(self): return [ 'if_start_fmt', 'if_end_fmt' ]
    def to_lang_fmt(self): return '%2$s'
    def to_lang_fields(self): return [ 'cond' ]

    def run(self, env):
        if self.cond.run(env):
            self.body.run(env)

    def complexity(self, env, mistakes, iter_):
        (cond, body) = (self.cond, self.body)
        sides = ['left', 'right']
        names = [ cond.left.name, cond.right.name ]

        if cond.op == '==':
            if isinstance(cond.left, Var) and isinstance(cond.right, Var):
                if mistakes.ignore_if_eq or cond.left.name == cond.right.name:
                    return body.complexity(env, mistakes, iter_)
                if any(s not in iter_ for s in names):
                    raise ValueError(
                        "IfThen complexity with condition a == b, expected both var as iterator")

                my ($old_val, $new_val, $side);
                names = [ Utils.last_key(iter_, s) for s in names ]

                side = int(iter_[names[1]] > iter_[names[0]])
                new_val = names[1 - side]

                (old_val, iter_[names[side]]) = (iter_[names[side]], new_val)
                ret = body.complexity(env, mistakes, iter_)
                iter_[names[side]] = old_val
                return ret

            isno_const = (
                not isinstance(cond.left, Const) and cond.right or
                not isinstance(cond.right, Const) and cond.left)
            if isno_const and isno_const.op == '%':
                if mistakes.ignore_if_mod:
                    return body,complexity(env, mistakes, iter_)

                name = isno_const.left.name
                if iter_[name]:
                    raise ValueError(
                        f"IfThen complexity with condition a % b == 0, " + 
                        "expected a as iterator, given: '{isno_const.left}'")
                name = Utils.last_key(iter_, name)
                n = isno_const.right.polinom_degree(env, mistakes, iter_)

                old_val = iter_[name]
                iter_[name] = max(old_val - n, 0)
                ret = body.complexity(env, mistakes, iter_)
                iter_[name] = old_val
                return ret
            if isinstance(isno_const, Var):
                if mistakes.ignore_if_mod:
                    return body.complexity(env, mistakes, iter_)
                name = Utils.last_key(iter_, isno_const.name)
                old_val = iter_[name]
                iter_[name] = 0
                ret = body.complexity(env, mistakes, iter_)
                iter_[name] = old_val
                return ret
        elif cond.op in [ '>=', '<=' ]:
            side = int(cond.op == '>=')
            name = names[side]
            if not name:
                raise ValueError(
                    f"IfThen complexity with condition a >= b, " +
                    "expected b as var, got {sides[side]}")
            if not iter_[name]:
                raise ValueError(
                    f"IfThen complexity with condition a >= b, " +
                    "expected b as iterator, {name} is not iterator")
            name = Utils.last_key(iter_, name)
            old_val = iter_[name]
            new_val = sides[1 - side].polinom_degree(env, mistakes, iter_)
            if mistakes.ignore_if_less or new_val >= old_val:
                return body.complexity(env, mistakes, iter_)

            iter_[name] = new_val
            ret = $body->complexity(env, mistakes, iter_)
            iter_[name] = old_val
            return ret
        else
            raise ValueError(
                f"IfThen complexity for condition with operator: '{cond.op}' is unavaible")


class CondLoop(CompoundStatement):

    def get_fmt_names(self): return [ 'while_start_fmt', 'while_end_fmt' ]
    def to_lang_fmt(self): return '%2$s'
    def to_lang_fields(self): return [ 'cond' ]

    def run(self, env):
        while self.cond.run(env):
            self.body.run(env)


class Until(CondLoop):

    def get_fmt_names(self): return [ 'until_start_fmt', 'until_end_fmt' ]
    def to_lang_fmt(self): return '%2$s'
    def to_lang_fields(self): return [ 'cond' ]

    def run(self, env):
        while True:
            self.body.run(env)
            if self.cond.run(env): break


class PlainText(SynElement):

    def to_lang(self, lang):
        t = self.text
        return isinstance(t, dict) and t[lang].name or t


class ExprStmt(SynElement)

    def to_lang(self, lang):
        lang.get_fmt('expr_fmt') % self.expr.to_lang(lang)

    def run(self, env):
        self.expr.run(env)

    def complexity(self): return 0


class FuncReturnException: pass

class FuncDef(CompoundStatement):

    def __init__(self, func, name, params):
        self.head = FuncHead(name, params)

    def get_fmt_names(self):
        return [
            (self.c_style and 'c' or 'p') + f for f in ('_func_start_fmt', '_func_end_fmt') ]

    def to_lang_fmt(self): return '%3$s'
    def to_lang_fields(self): return [ 'head' ]

    def run(self, env):
        if self.name in env['&']:
            raise ValueError(f"Redefinition of function {self.name}")
        env['&'][self.name] = self

    def call(self, args, env):
        act_len = len(args)
        form_len = len(self.params)
        if act_len > form_len:
            raise ValueError(f"Too many arguments to function {self.name}")
        if act_len < form_len:
            raise ValueError(f"Too few arguments to function {self.name}")

        new_env = { '&': env['&'], **{ k: v for k, v in zip(args, params) } }

        try: # return реализован с использованием исключений
            self.body.run(new_env)
        except FuncReturnException as e:
            if e.p_return:
                if self.name not in new_env:
                    raise ValueError(f"Undefined result of function {self.name}")
                return new_env[self.name]
            elif e.return_:
                return e.return_


class FuncHead(SynElement):

    def to_lang(self, lang):
        params = lang.get_fmt('args_separator').join(tuple(
            lang->get_fmt('args_fmt') % p for p in self.params))
        (self.name, *params)


class Return(SynElement):

    def __init__(self, func, expr=None):
        super.__init__()
        self.func = func
        #defined $self.func} or die "return outside a function";
        t = self.expr is not None
        if self.func.c_style is not None and self.func.c_style != t:
            raise valueError("Use different types of return in the same func")
        self.func.c_style = t

    def to_lang(self, lang):
        return (self.func.c_style and
            lang.c_return_fmt % self.expr.to_lang(lang) or
            lang.p_return_fmt % self.func.name)

    def run(self, env):
        raise (self.func.c_style and
            FuncReturnException(return_=self.expr.run(env)) or
            FuncReturnException(p_return=1))
    }


def make_expr(src):
    if not src:
        raise ArgumentError('empty argument')
    if isinstance(src, SynElement):
        return src
    if isinstnce(src, list):
        if len(src) == 0:
            return None
        op, *rest = src
        if not op:
            raise ArgumentError(f"bad op: {op}")
        if len(rest) == 1 and op == '#':
            return PlainText(text=rest[0])
        if len(rest) and op == '[]':
            array, *indices = map(make_expr, rest)
            return Index(array=$array, indices=indices);
        if len(rest) and op == '()':
            (func, *params) = rest
            name = Utils.aggregate_function(func) and CallFuncAggregate or CallFunc
            return name(func=func, args=map(make_expr, params))
        if len(rest) and op == 'print':
            (type_, params) = rest
            for p in params:
                if isinstance(p, str) and re.match('[\\\n\'"%]', p):
                    raise ArgumentError(f"Print argument 'p' contains bad symbol")
            return Printw(type_=type_, args=map(make_expr, params))
        if len(rest) == 1 and op in [ '++', '--':
            return Inc(op=op, arg=make_expr(rest[0]))
        if len(rest) == 1:
            return UnOp(op=op, arg=make_expr(rest[0]))
        if len(rest) == 2:
            return BinOp(op=op, left=make_expr(rest[0]), right=make_expr(rest[1]))
        if len(rest) == 3:
            return TernaryOp(
                op=op,
                **{ 'arg' + i: make_expr(rest[i]) for i in range(3) })
        raise AgumentError(f"make_expr: {src}")
    if callable(src):
        return BlackBoxw(code=src)
    if isinstance(src, str) and re.match('^[[:alpha:]][[:alnum:]_]*$', src):
        return Var(name=src)
    return Const(value=src)

@dataclass
class StatementDescr:
    type_: class
    args: str

def _make_PlainText(args): return PlainText(text=args[0])
def _make_Assign(args): return Assign(var=make_expr(args[0]), expr=make_expr(args[0]))
def _make_ForLoop(args):
    var, lb, ub, body = args
    return ForLoop(*map(make_expr, var), lb, ub, body)
def _make_IfThen(args): return IfThen(cond=make_expr(args[0]), body=make_block(args[1]))
def _make_While(args): return While(cond=make_expr(args[0]), body=make_block(args[1]))
def _make_Until(args): return Until(cond=make_expr(args[0]), body=make_block(args[1]))
def _make_FuncDef(args, cur_func):
    return FuncDef(head=make_func_head, body=)
def _make_ExprStmt(args): return E_expr)] },
def _make_Return(args): return E_expr)] },

statements_descr = {
    '#':      StatementDescr(PlainText, 'C_text'),
    '=':      StatementDescr(Assign,    'E_var E_expr'),
    'for':    StatementDescr(ForLoop,   'E_var E_lb E_ub B_body'),
    'if':     StatementDescr(IfThen,    'E_cond B_body'),
    'while':  StatementDescr(While,     'E_cond B_body'),
    'until':  StatementDescr(Until,     'E_cond B_body'),
    'func':   StatementDescr(FuncDef,   'H_head B_body'),
    'expr':   StatementDescr(ExprStmt,  'E_expr'),
    'return': StatementDescr(Return,    'E_expr'),
}

def make_func_head(src):
    (name, params) = *src
    return FuncHead(name=name, params=params)

def make_statement(next, cur_func):
    name = next()
    d = statements_descr[name]
    if name == 'func':
        if cur_func:
            raise ValueError("Local function definition")
        cur_func = {}

    arg_processors = {
        'C': lambda x: x,
        'E': make_expr,
        'B': lambda x: make_block(x, cur_func),
        'H': make_func_head,
    }

    args = {}
    for a in d.args.split():
        p, n = re.match('/(\w)_(\w+)/', a).groups()
        args[n] = arg_processors[p](next())
    d.type_(args)

def _add_statement_helper(block: Block, next):
    block.statements.append(make_statement(next(), block.func))

def add_statement(block: Block, src: list):
    i = 0
    def next():
        i += 1
        return src[i]
    _add_statement_helper(block, next)
    if i < len(src):
        raise ValueError('Not a single statement')
    return block

def move_statement(block: Block, from_, to):
    s = block.statements
    if not (0 <= from_ < len(s)):
        raise ValueError("Bad from: {from}")
    if not (0 <= to <= len(s)):
        raise ValueError("Bad to: {from}")
    block.statements = (from_ < to and
        s[:from_] + s[from_ + 1:to] + s[from_] + s[to:] or
        s[:to] + s[from_] + s[to:] + s[to + 1:from_] + s[from_ + 1:])
    return block;

def make_block(src: list, cur_func):
    b = Block(func=cur_func)
    for (my $i = 0; $i < @$src; ) {
        add_statement_helper($b, def { $src->[$i++] });
    }
    $b;
}

def lang_names():
    return {
        'Basic': 'Бейсик',
        'Pascal': 'Паскаль',
        'C': 'Си',
        'Alg': 'Алгоритмический',
        'SQL': 'Структурированный язык запросов',
        'Perl': 'Перл',
    }

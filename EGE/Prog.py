from dataclasses import dataclass
import re

import EGE.Svg as svg
from .ProgModules import Lang
from . import Html as html
from . import Utils
from EGE.Utils import Box
from .ProgModules.Flowchart import Flowchart, Jump

class SynElement:

    def to_lang_named(self, lang_name: str, options=None) -> str:
        lang = getattr(Lang, lang_name)(options)
        ret = self.to_lang(lang)
        h = lang.html
        if isinstance(h, dict):
            if h.get('lang_marking'):
                ret = "\n".join(
                    html.tag('pre', line, class_=lang_name) for line in ret.split("\n"))
            if h.get('pre'):
                ret = html.tag('pre', ret)
        return ret

    def to_lang(self, attr): pass
    def run(self, attr): pass

    def assign(self, env: dict[str, Box], value): pass

    def run_val(self, name: str, env: dict[str, Box] = None):
        env = env or {}
        self.run(env)
        return env.get(name).value if env.get(name) else env.get(name)

    def gather_vars(self, *args): pass

    def visit_dfs(self, fn=None, *args):
        if fn:
            self = fn(self, *args)
        self._visit_children(fn, *args)
        return self

    def get_children_dfs(self):
        yield self
        yield from self._get_children()

    def _visit_children(self, *attr): pass
    def _get_children(self, *attr): return []

    def count_if(self, cond):
        return sum(1 if cond(se) else 0 for se in self.get_children_dfs())

    def gather_if(self, cond):
        res = []
        for se in self.get_children_dfs():
            if cond(se):
                res.append(se)
        return res

    def get_type(self, x): return x.split(':')[-1]

    def complexity(self, *attr): raise ValueError()

    def needs_parens(self, *args): return False


class BlackBox(SynElement):

    def __init__(self, code=None, lang=None, assign=None):
        self.code = code
        self.lang = lang or {}
        self.assign = assign

    def assign(self, env: dict[str, Box], value):
        if self.assign:
            self.assign(env, value)

    def to_lang_named(self, lang_name, options=None):
        return self.lang[lang_name]

    def to_lang(self, lang): return self.to_lang_named(lang.name)

    def run(self, env: dict[str, Box]): return self.code(env)


class Assign(SynElement):

    def __init__(self, params, *args):
        self.var = params['var']
        self.expr = params['expr']

    def to_lang(self, lang):
        return lang.get_fmt('assign_fmt').format(*[
            e.to_lang(lang) for e in (self.var, self.expr)
        ])

    def run(self, env: dict[str, Box]):
        v = self.expr.run(env)
        self.var.assign(env, v)
        return v

    def _visit_children(self, fn, *args):
        self.var = self.var.visit_dfs(fn, *args)
        self.expr = self.expr.visit_dfs(fn, *args)

    def _get_children(self):
        yield from self.var.get_children_dfs()
        yield from self.expr.get_children_dfs()

    def complexity(self, env: dict[str, Box], mistakes, iter_):
        name = self.var.name
        if not name:
            return []
        if not iter_[name]:
            raise ValueError(f"Assign to iterator: '{name}'")

        # провека, что все переменные expr определены
        self.expr.polinom_degree(env, mistakes, iter_)
        # вычисляем степень выражения без итераторов, если ошибка, значит в выражении присутсвует итератор
        try:
            env[name] = self.expr.polinom_degree(env, mistakes, {})
        except:
            raise ValueError(f"Assign iterator to: '{name}'")


@dataclass
class Index(SynElement):

    def __init__(self, array, indices):
        self.array = array
        self.indices = indices

    def to_lang(self, lang):
        return lang.get_fmt('index_fmt').format(*[self.array.to_lang(lang),
                                                  ', '.join(str(i.to_lang(lang)) for i in self.indices)])

    def run(self, env: dict[str, Box]):
        v = self.array.run(env)
        for i in self.indices:
            v = v[i.run(env)]
        return v

    def assign(self, env: dict[str, Box], value):
        v = self.array.get_ref(env)
        if v.value is None:
            v.value = []
        for step, i in enumerate(self.indices[:]):
            index = i.run(env)
            if index >= len(v.value):
                for j in range(len(v.value), index + 1):
                    if step + 1 == len(self.indices):
                        v.value.append(None)
                    else:
                        v.value.append(Box([]))
            if step + 1 < len(self.indices):
                tmp = v[index]
                v = None
                v = tmp
        v[self.indices[-1].run(env)] = value
        return value

    def _visit_children(self, fn, *args):
        for se in (self.array, *self.indices):
            se.visit_dfs(fn, *args)

    def _get_children(self):
        for se in (self.array, *self.indices):
            yield from se.get_children_dfs()


@dataclass
class CallFunc(SynElement):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def to_lang(self, lang):
        return lang.get_fmt('call_func_fmt').format(*[
            self.func,
            lang.get_fmt('args_separator').join(a.to_lang(lang) for a in self.args)
        ])

    def run(self, env):
        arg_val = [ a.run(env) for a in self.args ]
        return env['&'][self.func].call(arg_val, env)


class CallFuncAggregate(CallFunc):

    def run(self, env: dict[str, Box]):
        func = env['&'][self.func]
        if self in env['&result']:
            return env['&result'][self]
        new_env = dict(**env)
        for i in range(new_env['&count']):
            for k, v in new_env['&columns']:
                new_env[k] = v[i]
            arg_val = [ a.run(new_env) for a in self.args ]
            ans = func.call(arg_val, new_env, self)
        env['&result'][self] = ans

class Print(SynElement):

    def __init__(self, type_, args):
        self.type_ = type_
        self.args = args
        fmt_types = { 'num': 'print_fmt', 'str': 'print_str_fmt' }
        self.fmt = fmt_types[self.type_]

    def to_lang(self, lang):
        return lang.get_fmt(self.fmt).format(
            lang.get_fmt('args_separator').join(a.to_lang(lang) for a in self.args))

    def run(self, env: dict[str, Box]):
        line = ' '.join(str(a.run(env)) for a in self.args)
        o = '<out>'
        if o in env:
            env[o] += "\n" + line
        else:
            env[o] = Box(line)

class Input(SynElement):
    def __init__(self, args):
        self.args = args
        self.fmt = 'input_int_fmt'

    def to_lang(self, lang):
        return lang.get_fmt(self.fmt).format(
            lang.get_fmt('args_separator').join(a.to_lang(lang) for a in self.args)
        )

    def run(self, env: dict[str, Box]):
        pass

class Op(SynElement):

    def __init__(self, op):
        self.op = op

    def _children(self): pass
    def children(self): return [ self._children() ]

    def rename_vars(self, dct: dict):
        for child in self.children():
            if isinstance(child, Const):
                child.value = dct[child.value]
            else:
                child.rename_vars(dct)

    def run(self, env: dict[str, Box]):
        return eval(self.run_fmt().format(*[c.run(env) for c in self.children()]))

    def prio(self, lang):
        return lang.prio[self.op]

    def operand(self, lang, operand_):
        t = operand_.to_lang(lang)
        return operand_.needs_parens(lang, self.prio(lang)) and f"({t})" or t

    def to_lang(self, lang):
        return self.to_lang_fmt(lang).format(*[
            self.operand(lang, c) for c in self.children()
        ])

    def needs_parens(self, lang, parent_prio):
        return parent_prio < self.prio(lang)

    def run_fmt(self): return self.to_lang_fmt(Lang.Python(params=None))
    def to_lang_fmt(self, *args) -> str: pass

    def gather_vars(self, env: dict[str, Box]):
        for c in self.children():
            c.gather_vars(env)

    def _visit_children(self, fn, *args):
        for c in self.children():
            c.visit_dfs(fn, *args)

    def _get_children(self):
        for c in self.children():
            yield from c.get_children_dfs()

    def polinom_degree(self, *args):
        raise ValueError(f"Polinom degree is unavaible for expr with operator: '{self.op}'")


class BinOp(Op):

    def __init__(self, op, left=None, right=None):
        super().__init__(op)
        self.right = right
        self.left = left

    def to_lang_fmt(self, lang):
        return lang.get_fmt('op_fmt', self.op)

    def children(self): return self.left, self.right

    def polinom_degree(self, env, mistakes, iter_):
        if self.op == '*':
            return sum(c.polinom_degree(env, mistakes, iter_) for c in self.children())
        if self.op == '+':
            return max(c.polinom_degree(env, mistakes, iter_) for c in self.children())
        if self.op == '**':
            return self.left.polinom_degree(env, mistakes, iter_) * self.right.run({})
        return super().polinom_degree(env, mistakes, iter_)

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

    def __init__(self, op, arg):
        super().__init__(op)
        self.arg = arg

    def prio(self, lang): return lang.prio['`' + self.op]

    def to_lang_fmt(self, lang):
        return lang.get_fmt('un_op_fmt', self.op)

    def _children(self): return self.arg

class Inc(UnOp):

    def run(self, env: dict[str, Box]):
        if self.op[:2] == '++':
            env[self.arg.name] += 1
        elif self.op[:2] == '--':
            env[self.arg.name] -= 1
        return env[self.arg.name].value


class TernaryOp(Op):
    def __init__(self, op, arg1, arg2, arg3):
        super().__init__(op)
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def to_lang_fmt(self, lang):
        r = lang.get_fmt('op_fmt', self.op)
        if not isinstance(r, list):
            return r
        s = re.sub(r'(\d+)', r'{\g<1>}', make_expr(r).to_lang(lang))
        return s

    def children(self): return self.arg1, self.arg2, self.arg3


class Var(SynElement):
    def __init__(self, name):
        self.name = name

    def to_lang(self, lang):
        return lang.get_fmt('var_fmt').format(self.name)

    def run(self, env: dict[str, Box]):
        if env.get(self.name) is None:
            raise ValueError(f"Undefined variable {self.name}")
        return env.get(self.name).value

    def assign(self, env: dict[str, Box], value) -> Box:
        if self.name not in env:
            env[self.name] = Box(value)
        else:
            env[self.name].value = value
        return env[self.name]

    def get_ref(self, env: dict[str, Box]) -> Box:
        if self.name not in env:
            self.assign(env, None)
        return env[self.name]

    def gather_vars(self, vars_): vars_[self.name] = Box(1)

    def polinom_degree(self, env: dict[str, Box], mistakes, iter_):
        n = self.name
        if env[n].value:
            return mistakes.var_as_const and n == mistakes.var_as_const or env[n]
        if iter_[n]:
            return 0 if mistakes.var_as_const else iter_[Utils.last_key(iter_, n)]
        raise ValueError(f"Undefined variable {n}")


class Const(SynElement):
    def __init__(self, value):
        self.value = value

    def to_lang(self, lang): return str(self.value)

    def run(self, env: dict[str, Box]):
        return self.value

    def polinom_degree(self): return 0


class RefConst(Const):

    def update(self, new_value):
        self.value = new_value

class Block(SynElement):
    def __init__(self, statements, func):
        self.statements = statements
        self.func = func

    def to_lang(self, lang):
        return lang.get_fmt('block_stmt_separator').join(
            s.to_lang(lang) for s in self.statements)

    def run(self, env: dict[str, Box]):
        for s in self.statements:
            s.run(env)

    def _visit_children(self, fn, *args):
        for idx, s in enumerate(self.statements):
            self.statements[idx] = s.visit_dfs(fn, *args)

    def _get_children(self):
        for s in self.statements:
            yield from s.get_children_dfs()

    def complexity(self, env: dict[str, Box], mistakes, iter_):
        items = [s.complexity(env, mistakes, iter_) for s in self.statements]
        if mistakes.change_min:
            return min(items)
        if mistakes.change_sum:
            return sum(items)
        return max(items)

    def to_svg(self, f: Flowchart, enter: Jump, exit_: Jump):
        r = ''
        elements = []
        linear = []
        for st in self.statements + [ None ]:
            if st and isinstance(st, Assign):
                linear.append(st.to_lang_named('Alg'))
            else:
                if linear:
                    elements.append(linear)
                linear = []
                if st:
                    elements.append(st)
        j = None
        for el in elements:
            j = exit_ if el == elements[-1] else f.make_jump()
            if isinstance(el, list):
                r += f.add_box(el, enter, j)
                f.down()
            else:
                r += el.to_svg(f, enter, j)
            enter = j
        return r

    def to_svg_main(self):
        f = Flowchart(x=0, y=0)
        exit_ = f.make_jump()
        r = self.to_svg(f, None, exit_)
        exit_.dest = f.point()
        r = svg.g(f"\n{r}" + f.jumps(),
                  stroke='black',
                  fill='none') + f.texts()
        f.y2 += 1
        f.x2 += 1
        wh = [ f.x2 - f.x1, f.y2 - f.y1 ]
        return html.div_xy(
            "\n" + svg.start(list(map(str, [ f.x1, f.y1, *wh ]))) + r + svg.end(), *wh
        )

class CompoundStatement(SynElement):
    def __init__(self, body):
        self.body = body

    def to_lang_fields(self): pass

    def to_lang(self, lang):
        body_is_block = len(self.body.statements) > 1
        (fmt_start, fmt_end) = (
            lang.get_fmt(f, body_is_block or lang.body_is_block) for f in self.get_fmt_names())

        if lang.html and lang.html.get('coloring'):
            s = html.style(color=lang.html['coloring'][0])

            def sp(t):
                return re.sub('([^\n]+)', lambda m: html.tag('span', m[0], **s), t)

            fmt_start = sp(fmt_start)
            fmt_end = sp(fmt_end)
            if len(lang.html['coloring']) > 1:
                lang.html['coloring'].pop(0)

        body = self.body.to_lang(lang)
        if fmt_start.endswith("\n"):
            if not lang.unindent:
                body = re.sub('^', '  ', body)  # отступы
                body = re.sub('\n', '\n  ', body)
        t = [getattr(self, f).to_lang(lang) for f in self.to_lang_fields()]
        if isinstance(t[0], tuple):
            t = [x for i in t for x in i]
        ret = []
        if (isinstance(self, ForLoop) and isinstance(lang, Lang.Basic)) or (
                isinstance(self, FuncDef) and not self.c_style and (
                isinstance(lang, Lang.C) or isinstance(lang, Lang.Perl) or isinstance(lang, Lang.Python))):
            ret.append(t[0])
        return fmt_start.format(*t) + self.to_lang_fmt().format(body) + fmt_end.format(*ret)

    def _visit_children(self, fn, *args):
        for f in [*(getattr(self, f) for f in self.to_lang_fields()), self.body]:
            f.visit_dfs(fn, *args)

    def _get_children(self):
        for f in [*(getattr(self, f) for f in self.to_lang_fields()), self.body]:
            yield from f.get_children_dfs()


class ForLoop(CompoundStatement):
    def __init__(self, param, *args):
        super().__init__(param['body'])
        self.var = param['var']
        self.lb = param['lb']
        self.ub = param['ub']

    def get_fmt_names(self): return [ 'for_start_fmt', 'for_end_fmt' ]
    def to_lang_fmt(self): return '{}'
    def to_lang_fields(self): return [ 'var', 'lb', 'ub' ]

    def run(self, env: dict[str, Box]):
        for i in range(self.lb.run(env), self.ub.run(env) + 1):
            self.var.assign(env, i)
            self.body.run(env)

    def complexity(self, env: dict[str, Box], mistakes, iter_):
        name = self.var.name
        degree = self.ub.polinom_degree(env, mistakes, iter_)
        iter_.name = degree

        body_complexity = self.body.complexity(env, mistakes, iter_)
        env[name].value = degree

        cur_complexity = sum(
            float(i) for i in iter_.values() if i.replace('.', '', 1).isdigit())
        del iter_[name]
        return cur_complexity > body_complexity and cur_complexity or body_complexity


class IfThen(CompoundStatement):
    def __init__(self, param, *args):
        super().__init__(param['body'])
        self.cond = param['cond']

    def get_fmt_names(self): return [ 'if_start_fmt', 'if_end_fmt' ]
    def to_lang_fmt(self): return '{}'
    def to_lang_fields(self): return [ 'cond' ]

    def run(self, env: dict[str, Box]):
        if self.cond.run(env):
            self.body.run(env)

    def complexity(self, env: dict[str, Box], mistakes, iter_):
        (cond, body) = (self.cond, self.body)
        names = [ cond.left.name, cond.right.name ]

        if cond.op == '==':
            if isinstance(cond.left, Var) and isinstance(cond.right, Var):
                if mistakes.ignore_if_eq or cond.left.name == cond.right.name:
                    return body.complexity(env, mistakes, iter_)
                if any(s not in iter_ for s in names):
                    raise ValueError(
                        "IfThen complexity with condition a == b, expected both var as iterator")

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
                    return body, body.complexity(env, mistakes, iter_)

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
            new_val = cond[1 - side].polinom_degree(env, mistakes, iter_)
            if mistakes.ignore_if_less or new_val >= old_val:
                return body.complexity(env, mistakes, iter_)

            iter_[name] = new_val
            ret = body.complexity(env, mistakes, iter_)
            iter_[name] = old_val
            return ret
        else:
            raise ValueError(
                f"IfThen complexity for condition with operator: '{cond.op}' is unavaible")


class CondLoop(CompoundStatement):
    def __init__(self, cond, body):
        super().__init__(body)
        self.cond = cond

    def get_fmt_names(self): return [ 'while_start_fmt', 'while_end_fmt' ]
    def to_lang_fmt(self): return '{}'
    def to_lang_fields(self): return [ 'cond' ]

    def run(self, env):
        while self.cond.run(env):
            self.body.run(env)

    def to_svg(self, f: Flowchart, enter: Jump, exit_: Jump):
        top = f.make_jump(Jump(dest=f.point(), dir='left'))
        f.down(20)
        middle = f.make_jump(Jump(label=self.continue_label()))
        exit_.label = self.exit_label()
        r = f.add_rhomb(self.cond.to_lang_named('Alg'),
                        enter,
                        { 'right': exit_, 'middle': middle })
        f.down()
        r += self.body.to_svg(f, middle, top)
        f.down(10)
        return r

    @staticmethod
    def continue_label():
        return 'Да'

    @staticmethod
    def exit_label():
        return 'Нет'

class While(CondLoop):
    def __init__(self, param, *args):
        super().__init__(param['cond'], param['body'])

    def get_fmt_names(self): return [ 'while_start_fmt', 'while_end_fmt' ]
    def to_lang_fmt(self): return '{}'
    def to_lang_fields(self): return [ 'cond' ]

    def run(self, env: dict[str, Box]):
        while True:
            self.body.run(env)
            if not self.cond.run(env):
                break

    @staticmethod
    def continue_label():
        return 'Да'

    @staticmethod
    def exit_label():
        return 'Нет'

class Until(CondLoop):
    def __init__(self, param, *args):
        super().__init__(param['cond'], param['body'])

    def get_fmt_names(self): return [ 'until_start_fmt', 'until_end_fmt' ]
    def to_lang_fmt(self): return '{}'
    def to_lang_fields(self): return [ 'cond' ]

    def run(self, env: dict[str, Box]):
        while True:
            self.body.run(env)
            if self.cond.run(env):
                break

    @staticmethod
    def continue_label():
        return 'Нет'

    @staticmethod
    def exit_label():
        return 'Да'

class PlainText(SynElement):
    def __init__(self, text, *args):
        self.text = text['text']

    def to_lang(self, lang):
        t = self.text
        return isinstance(t, dict) and t.get(type(lang).__name__) or isinstance(t, str) and t or ''


class ExprStmt(SynElement):
    def __init__(self, param, *args):
        self.expr = param['expr']

    def to_lang(self, lang):
        return lang.get_fmt('expr_fmt').format(self.expr.to_lang(lang))

    def run(self, env: dict[str, Box]):
        return self.expr.run(env)

    def complexity(self): return 0


class FuncReturnException(BaseException):
    def __init__(self, p_return=None, return_=None):
        self.p_return = p_return
        self.return_ = return_

class FuncDef(CompoundStatement):
    def __init__(self, param, cur_func):
        self.head = param['head']
        self.body = param['body']
        self.c_style = cur_func.c_style if cur_func is not None and hasattr(cur_func, 'c_style') else False

    def get_fmt_names(self):
        return [
            (self.c_style and 'c' or 'p') + f for f in ('_func_start_fmt', '_func_end_fmt') ]

    def to_lang_fmt(self): return '{}'
    def to_lang_fields(self): return [ 'head' ]

    def run(self, env: dict[str, Box]):
        if env.get('&') and self.head.name in env.get('&'):
            raise ValueError(f"Redefinition of function {self.head.name}")
        env['&'] = Box({})
        env['&'][self.head.name] = self

    def call(self, args, env: dict[str, Box]):
        act_len = len(args)
        form_len = len(self.head.params)
        if act_len > form_len:
            raise ValueError(f"Too many arguments to function {self.head.name}")
        if act_len < form_len:
            raise ValueError(f"Too few arguments to function {self.head.name}")

        new_env = { '&': env['&'], **{k: Box(v) for v, k in zip(args, self.head.params) }}

        try: # return реализован с использованием исключений
            self.body.run(new_env)
            return new_env.get(self.head.name)
        except FuncReturnException as e:
            if e.p_return is not None:
                if self.head.name not in new_env:
                    raise ValueError(f"Undefined result of function {self.head.name}")
                return new_env[self.head.name]
            elif e.return_ is not None:
                return e.return_


class FuncHead(SynElement):
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def to_lang(self, lang):
        params = lang.get_fmt('args_separator').join(
            lang.get_fmt('args_fmt').format(p) for p in self.params)
        return self.name, params


class Return(SynElement):

    def __init__(self, param, cur_func):
        self.func = cur_func
        self.expr = param.get('expr')
        t = self.expr is not None
        if hasattr(self.func, 'c_style') and self.func.c_style is not None and self.func.c_style != t:
            raise ValueError("Use different types of return in the same func")
        self.func.c_style = t

    def to_lang(self, lang):
        return (self.func.c_style and
            lang.c_return_fmt().format(self.expr.to_lang(lang)) or
            lang.p_return_fmt().format(self.func.head.name))

    def run(self, env: dict[str, Box]):
        raise (self.func.c_style and
            FuncReturnException(return_=self.expr.run(env)) or
            FuncReturnException(p_return=1))


def make_expr(src):
    if src is None:
        raise ValueError('empty argument')
    if isinstance(src, SynElement):
        return src
    if isinstance(src, list):
        if len(src) == 0:
            return None
        op, *rest = src
        rest = list(filter(lambda v: v is not None, rest))
        if not op:
            raise ValueError(f"bad op: {op}")
        if len(rest) == 1 and op == '#':
            return PlainText({'text': rest[0]})
        if len(rest) and op == '[]':
            array, *indices = map(make_expr, rest)
            return Index(array=array, indices=indices)
        if len(rest) and op == '()':
            (func, *params) = rest
            name = Utils.aggregate_function(func) and CallFuncAggregate or CallFunc
            return name(func=func, args=[ make_expr(i) for i in params ])
        if len(rest) and op == 'print':
            type_, *params = rest
            for p in params:
                if isinstance(p, str) and re.match('[\\\n\'"%]', p):
                    raise ValueError(f"Print argument 'p' contains bad symbol")
            return Print(type_=type_, args=[ make_expr(param) for param in params ])
        if len(rest) and op == 'input':
            if len(rest) > 1:
                raise ValueError(f"Input argument contains bad symbol")
            return Input(args=[ make_expr(param) for param in rest ])
        if len(rest) == 1 and ('++' in op or '--' in op):
            return Inc(op=op, arg=make_expr(rest[0]))
        if len(rest) == 1:
            return UnOp(op=op, arg=make_expr(rest[0]))
        if len(rest) == 2:
            return BinOp(op=op, left=make_expr(rest[0]), right=make_expr(rest[1]))
        if len(rest) == 3:
            return TernaryOp(
                op=op,
                **{ 'arg' + str(i+1): make_expr(rest[i]) for i in range(3) })
        raise ValueError(f"make_expr: {src}")
    if callable(src):
        return BlackBox(code=src)
    if isinstance(src, str) and re.match('^[a-zA-Z][a-zA-Z0-9_]*$', src):
        return Var(name=src)
    return Const(value=src)

@dataclass
class StatementDescr:
    type_: type
    args: str

def _make_PlainText(args): return PlainText(text=args[0])
def _make_Assign(args): return Assign(var=make_expr(args[0]), expr=make_expr(args[0]))
def _make_ForLoop(args):
    var, lb, ub, body = args
    return ForLoop(*map(make_expr, var), lb, ub, body)
def _make_IfThen(args): return IfThen(cond=make_expr(args[0]), body=make_block(args[1]))
def _make_While(args): return While(cond=make_expr(args[0]), body=make_block(args[1]))
def _make_Until(args): return Until(cond=make_expr(args[0]), body=make_block(args[1]))
def _make_FuncDef(args): return FuncDef(head=make_func_head(args[0]), body=make_block(args[1]))
def _make_ExprStmt(args): return ExprStmt(expr=make_expr(args[0]))
def _make_Return(args): return Return(func=args[0], expr=make_expr(args[1]))

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
    name, *params = src
    return FuncHead(name=name, params=params)

def make_statement(next, cur_func):
    name = next[0]
    next.pop(0)
    d = statements_descr[name]
    if name == 'func':
        if cur_func:
            raise ValueError("Local function definition")

    arg_processors = {
        'C': lambda x: x,
        'E': make_expr,
        'B': lambda x: make_block(x, cur_func),
        'H': make_func_head,
    }

    args = {}
    for a in d.args.split():
        p, n = re.match('(\w)_(\w+)', a).groups()
        args[n] = arg_processors[p](next[0])
        if name == 'func':
            cur_func = args[n]
            name = ''
        next.pop(0)
    return d.type_(args, cur_func), next

def _add_statement_helper(block: Block, next):
    statement, next = make_statement(next, block.func)
    block.statements.append(statement)
    return next

def add_statement(block: Block, src: list):
    _add_statement_helper(block, src)
    return block

def move_statement(block: Block, from_, to):
    s = block.statements
    if not (0 <= from_ < len(s)):
        raise ValueError("Bad from: {from}")
    if not (0 <= to <= len(s)):
        raise ValueError("Bad to: {from}")

    s.insert(to, s[from_])
    s.pop(from_ + 1 if from_ > to else 0)
    return block

def make_block(src: list, cur_func=None):
    b = Block(func=cur_func, statements=[])
    while len(src):
        src = _add_statement_helper(b, src)
    return b

def lang_names():
    return {
        'Basic': 'Бейсик',
        'Pascal': 'Паскаль',
        'C': 'Си',
        'Alg': 'Алгоритмический',
        'SQL': 'Структурированный язык запросов',
        'Perl': 'Перл',
    }

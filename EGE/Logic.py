from .Prog import make_expr
from .Bits import Bits
from .GenBase import EGEError
from .Prog import UnOp, BinOp

def maybe_not(rnd, arr: list):
    return rnd.pick([ arr, arr, [ '!', arr ] ])

def random_op(rnd):
    common = ('&&', '||')
    rare = ('=>', '^')

    return rnd.pick(common + common + common + rare)

def random_logic(rnd, arr: list):
    if len(arr) == 0:
        return rnd.coin()
    if len(arr) == 1:
        return maybe_not(rnd, arr[0])

    p = rnd.in_range(1, len(arr) - 1)
    return maybe_not(rnd, [
        random_op(rnd),
        random_logic(rnd, arr[:p]),
        random_logic(rnd, arr[p:])
    ])

def random_logic_expr(rnd, arr: list):
    return make_expr(random_logic(rnd, arr))

def bits_to_vars(bits, names: list):
    return { name: bits.get_bit(i) for i, name in enumerate(names) }

def truth_table_string(expr):
    expr_vars = {}
    expr.gather_vars(expr_vars)
    if expr_vars is None:
        return expr.run({})
    names = sorted(expr_vars.keys())
    bits = Bits().set_size(len(names))
    r = str(int(expr.run(bits_to_vars(bits, names))))
    bits.inc()
    while not bits.is_empty():
        r += str(int(expr.run(bits_to_vars(bits, names))))
        bits.inc()
    return r

def is_unop(obj):
    return isinstance(obj, UnOp)

def is_binop(obj):
    return isinstance(obj, BinOp)

def equiv_not1(expr):
    nel = [ '!', expr.left ]
    ner = [ '!', expr.right ]

    if expr.op == '&&':
        src = [ '||', nel, ner ]
    elif expr.op == '||':
        src = [ '&&', nel, ner ]
    elif expr.op == '^':
        src = [ '^' , nel, expr.right ]
    elif expr.op == '=>':
        src = [ '&&', expr.left, ner ]
    else:
        raise EGEError(expr.op)

    return make_expr(src)

def equiv_not(e):
    if is_unop(e) and is_binop(e.arg):
        return equiv_not1(e.arg)
    elif is_binop(e):
        return make_expr([ '!', equiv_not1(e) ])
    else:
        return make_expr([ '!', [ '!', e ] ])

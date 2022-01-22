import math

def aggregate_function(name):
    # TODO
    return None

def last_key(d, key):
    while key in d[key]:
        key = d[key]
    return key

def char_range(c1, c2):
    """Generates the characters from c1 to c2, inclusive."""
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)

def product(*args):
    return math.prod(args)

def minmax(*args):
    a = sorted(args)
    return a[0], a[-1]

def nrange(f, t):
    return list(range(f, t + 1))

def ucfirst(s: str) -> str:
    return s[0].upper() + s[1:]

def unique(l: list) -> list:
    # From python 3.7 plain dict is insertion-ordered
    # So dict.fromkeys does not lose ordering
    return list(dict.fromkeys(l))

def sign(a, b) -> int:
    return bool(a > b) - bool(a < b)

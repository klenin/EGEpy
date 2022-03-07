import math


class Box:
    def __init__(self, value=None):
        self._value = [ value ]

    @property
    def value(self):
        if isinstance(self._value[0], Box):
            return self._value[0].value
        return self._value[0]

    @value.setter
    def value(self, new):
        if isinstance(self._value[0], Box):
            self._value[0].value = new
        else:
            self._value[0] = new

    @value.deleter
    def value(self):
        del self._value
        self._value = [ None ]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Box({self.value})"

    # Binary Operators
    def __add__(self, other):
        return self._value[0] + other

    def __sub__(self, other):
        return self._value[0] - other

    def __mul__(self, other):
        return self._value[0] * other

    def __truediv__(self, other):
        return self._value[0] / other

    # Assignment operators
    def __iadd__(self, other):
        self._value[0] += other
        return self

    def __isub__(self, other):
        self._value[0] -= other
        return self

    def __imul__(self, other):
        self._value[0] *= other
        return self

    def __idiv__(self, other):
        self._value[0] /= other
        return self

    # Comparison operators
    def __lt__(self, other):
        return self.value < (other.value if isinstance(other, Box) else other)

    def __gt__(self, other):
        return self.value > (other.value if isinstance(other, Box) else other)

    def __le__(self, other):
        return self.value <= (other.value if isinstance(other, Box) else other)

    def __ge__(self, other):
        return self.value >= (other.value if isinstance(other, Box) else other)

    def __eq__(self, other):
        return self.value == (other.value if isinstance(other, Box) else other)

    def __ne__(self, other):
        return self.value != (other.value if isinstance(other, Box) else other)

    # Unary operators
    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    # Indexer operators
    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __delitem__(self, key):
        del self.value[key]

    def __index__(self):
        return self.value

    # Magic operators

    def __bool__(self):
        return bool(self.value)

    def __hash__(self):
        return hash(self.value)

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

def gcd(n: int, m: int):
    return math.gcd(n, m)

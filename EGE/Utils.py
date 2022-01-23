import math
from EGE.SQL.Aggregate import Aggregate

def aggregate_function(name:str = None):
    '''name: Union[str, None]'''
    aggr = Aggregate.__subclasses__()
    if name is not None:
        for sub in aggr:
            if name == sub.__name__:
                return sub
    return [ sub for sub in aggr ]

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


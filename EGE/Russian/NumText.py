# Copyright © 2021 Alexander S. Klenin
# Licensed under GPL version 2 or later.
# http://github.com/klenin/EGE2

from dataclasses import dataclass

def _split_plus(suffix, words):
    return [ w + suffix for w in words.split() ]

@dataclass
class CaseDef:
    zeroes: str
    one_two: list
    three_nine: list
    teens: list
    tens: list
    hundreds: list

case_defs = {
    # именительный
    'nominative': CaseDef(
        'ноль',
        [ w.split() for w in [ 'один два', 'одна две', 'одно два' ] ],
        'три четыре пять шесть семь восемь девять'.split(),
        [ 'десять' ] + _split_plus('надцать', 'один две три четыр пят шест сем восем девят'),
        'двадцать тридцать сорок пятьдесят шестьдесят семьдесят восемьдесят девяносто'.split(),
        'сто двести триста четыреста пятьсот шестьсот семьсот восемьсот девятьсот'.split(),
    ),
    #родительный
    'genitive': CaseDef(
        'ноля',
        [ w.split() for w in [ 'одного двух', 'одной двух', 'одного двух' ] ],
        'трёх четырёх пяти шести семи восьми девяти'.split(),
        [ 'десяти' ] + _split_plus('надцати', 'один две три четыр пят шест сем восем девят'),
        'двадцати тридцати сорока пятидесяти шестидесяти семидесяти восьмидесяти девяноста'.split(),
        'ста двухсот трёхсот четырёхсот пятисот шестисот семисот восьмисот девятисот'.split(),
    ),
    #дательный
    'dative': CaseDef(
        'нолю',
        [ w.split() for w in [ 'одному двум', 'одной двум', 'одному двум' ] ],
        'трём четырём пяти шести семи восьми девяти'.split(),
        [ 'десяти' ] + _split_plus('надцати', 'один две три четыр пят шест сем восем девят'),
        'двадцати тридцати сорока пятидесяти шестидесяти семидесяти восьмидесяти девяноста'.split(),
        'ста двумстам трёмстам четырёмстам пятистам шестистам семистам восьмистам девятистам'.split(),
    ),
    #винительный, одушевлённый
    'accusative_animate': CaseDef(
        'ноль',
        [ w.split() for w in ['одного двух', 'одну двух', 'одно двух' ] ],
        [ 'трёх четырёх пять шесть семь восемь девять'.split() ],
        [ 'десять' ] + _split_plus('надцать', 'один две три четыр пят шест сем восем девят'),
        'двадцать тридцать сорок пятьдесять шестьдесять семьдесять восемьдесять девяносто'.split(),
        'сто двести триста четыреста пятьсот шестьсот семьсот восемьсот девятьсот'.split(),
    ),
    #творительный
    'instrumental': CaseDef(
        'нолем',
        [ w.split() for w in [ 'одним двумя', 'одной двумя', 'одним двумя' ] ],
        'тремя четырьмя пятью шестью семью восемью девятью'.split(),
        [ 'десятью' ] + _split_plus('надцатью', 'один две три четыр пят шест сем восем девят'),
        'двадцатью тридцатью сорока пятьюдесятью шестьюдесятью семьюдесятью восемьюдесятью девяноста'.split(),
        'ста двумястами тремястами четырьмястами пятьюстами шестьюстами семьюстами восемьюстами девятьюстами'.split(),
    ),
    #предложный
    'prepositional': CaseDef(
        'ноле',
        [ w.split() for w in [ 'одном двух', 'одной двух', 'одном двух' ] ],
        'трёх четырёх пяти шести семи восьми девяти'.split(),
        [ 'десяти' ] + _split_plus('надцати', 'один две три четыр пят шест сем восем девят'),
        'двадцати тридцати сорока пятидесяти шестидесяти семидесяти восьмидесяти девяноста'.split(),
        'ста двухстах трехстах четырёхстах пятистах шестистах семистах восьмистах девятистах'.split(),
    ),
}

def num_by_words(num: int, gender: int, case: str = 'nominative'):
    if not (0 <= num < 1000):
        raise ValueError()
    case = case_defs[case]
    if num == 0:
        return case.zeroes
    hundreds = num >= 100 and case.hundreds[num // 100 - 1]
    num %= 100
    tens = (
        num >= 20 and case.tens[num // 10 - 2] or
        num >= 10 and case.teens[num - 10])
    num = 0 if 10 <= num < 20 else num % 10
    units = (
        num >= 3 and case.three_nine[num - 3] or
        num >= 1 and case.one_two[gender][num - 1])
    return ' '.join(w for w in (hundreds, tens, units) if w)

def num_text(n: int, forms: list, text_only: bool = False):
    d = n % 10
    t = (
        10 <= n <= 20 and 3 or
        d == 1 and 1 or
        d in (2, 3, 4) and 2 or
        3)
    return ('' if text_only else str(n) + ' ') + forms[t - 1]

num_by_words_text = lambda n, gender, case, forms: \
    num_by_words(n, gender, case) + ' ' + num_text(n, forms, True);

num_bits = lambda n: num_text(n, [ 'бит', 'бита', 'бит' ])

num_bytes = lambda n: num_text(n, [ 'байт', 'байта', 'байтов' ])

bits_and_bytes = lambda n: (num_bytes(n), num_bits(n * 8))

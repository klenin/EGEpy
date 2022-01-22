from functools import reduce

from EGE.ProgModules.RandomAlg import big_o, monomial, to_logic, _log
from ...GenBase import SingleChoice
from ...Utils  import transpose

class OPoly(SingleChoice):
    def generate(self):
        powers = sorted(self.rnd.pick_n(4, [ i for i in range(7) ]), reverse=True)
        coeffs = [ self.rnd.in_range(1, 9) for _ in range(4) ]
        
        elems = [ monomial('n', a[0], a[1]) for a in transpose(coeffs, powers) ]
        func = to_logic(reduce(lambda a, b: [ '+', a, b ], elems))

        self.text = f"Функция {func} является"
        variants = list(filter(lambda x: x > 0, self.rnd.shuffle(powers)))
        self.correct = variants.index(max(powers))
        variants = [ monomial('n', 1, v) for v in variants ] + [ max(coeffs) ]
        variants = [ big_o(v) for v in variants ]
        self.set_variants(variants)

        return self

class OPolyCmp(SingleChoice):
    def generate(self):
        power = self.rnd.in_range(3, 6)
        func = big_o(monomial('n', 1, power))
        blocks = [
            power - self.rnd.in_range(1, 3),
            [ '/', 1, power],
            -power,
        ]
        variants = [ big_o(monomial('n', 1, block)) for block in blocks ]
        additional_variants = [
            monomial('n', _log('n'), power - self.rnd.in_range(1, 2)),
            _log(monomial('n', 1, power)),
            [ '+', _log('n'), monomial('n', 1, power - self.rnd.in_range(1,3)) ],
        ] 
        for v in additional_variants:
            variants.append(big_o(v))

        correct_variants = [
            monomial('n', 1, power + self.rnd.in_range(1, 3)),
            monomial(power, 1, 'n'),
            monomial(power - 1, 1, 'n'),
            monomial('n', _log('n'), power + self.rnd.in_range(0, 2)),
        ]

        correct = self.rnd.pick([ big_o(v) for v in correct_variants ])

        self.text = f"Всякая функция, являющаяся {func}, является также и"
        self.set_variants([ correct ] + self.rnd.pick_n(3, variants))

        return self

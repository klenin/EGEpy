from functools import reduce

from EGE.ProgModules.RandomAlg import big_o, monomial, to_logic
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


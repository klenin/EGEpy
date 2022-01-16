"""Генератор B04"""
import math

import EGE.Random
import EGE.Russian
import EGE.Prog
import EGE.ProgModules.Lang
import EGE.Html as html
import EGE.RussianModules.Animals
from EGE.RussianModules.NumText import num_by_words
from EGE.GenBase import DirectInput
from EGE.Utils import product, minmax, nrange

class ImplBorder(DirectInput):
    """
    Генерация заданий B04 типа "граничное значение в импликации"
    """
    def __make_xx(self):
        xx = self.rnd.pick_n(2, [ 'X', [ '+', 'X', 1 ], [ '-', 'X', 1 ] ])
        return [ '*', *xx ]

    def __make_side(self):
        a = self.__make_xx()
        return [
            self.rnd.pick("> < >= <=".split()),
            self.__make_xx(),
            self.rnd.in_range(30, 99)
        ]

    @staticmethod
    def __find_first(v, q: list):
        try:
            return q.index(v)
        except ValueError:
            return None

    @staticmethod
    def __find_last(v, q: list):
        try:
            return len(q) - q[:-1].index(v) - 1
        except ValueError:
            return None

    def generate(self):
        n = 15
        e = None
        values = []
        while not (1 <= sum(values) <= n) or e is None:
            e = EGE.Prog.make_expr([ '=>', self.__make_side(), self.__make_side() ])
            values = [ e.run({'X': i}) for i in range(n + 1) ]

        et = html.cdata(e.to_lang_named('Logic'))
        shfls = self.rnd.shuffle([ dict(
            t1='наименьшее наибольшее'.split()[i // 2],
            t2='ложно истинно'.split()[i % 2],
            v=(lambda i, v, q: self.__find_first(v, q) if i < 2 else self.__find_last(v, q))(i, i % 2, values)
        ) for i in range(4) ])
        facet = next(( el for el in shfls if 1 <= el['v'] <= n - 1 ))
        self.text = f"""
Каково {facet['t1']} целое число X, при котором {facet['t2']} высказывание {et}?"""
        self.correct = facet['v']
        self.accept_number()
        return self

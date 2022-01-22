from ...GenBase import DirectInput
from ...Prog import make_expr

class LogicVarSet(DirectInput):
    def _connect(self, args: list):
        return make_expr([ '==', [ '&&',
            [ '||', [ 'eq', args[0], args[1] ], [ 'eq', args[2], args[3] ] ],
            [ '||', [ '!', [ 'eq', args[0], args[1] ] ], [ '!', [ 'eq', args[2], args[3] ] ] ],
        ], 1 ]).to_lang_named('Logic', { 'html': 1 })

    def generate(self):
        n_2 = self.rnd.in_range(4, 8)
        self.correct = 2 ** (n_2 + 1)
        self.accept_number()
        x = [[ '[]', 'x', i ] for i in range(1, 2 * n_2 + 1)]
        conds = '<br/>'.join(self._connect(x[2*i:2*i+4]) for i in range(n_2 - 1))
        vars = ', '.join(make_expr(i).to_lang_named('Logic', { 'html': 1 }) for i in x)
        self.text = f"""Сколько существует различных наборов значений логических переменных {vars} которые
удовлетворяют всем перечисленным ниже условиям? <p>{conds}</p> В ответе
<strong><u>не нужно</u></strong>
перечислять все различные наборы значений {vars}, при которых выполнена данная
система равенств. В качестве ответа вам нужно указать количество таких наборов.
"""
        return self

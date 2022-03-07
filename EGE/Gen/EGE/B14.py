from ...GenBase import DirectInput
from ...Prog import make_block
import EGE.LangTable

class FindFuncMin(DirectInput):
    def generate(self):
        bord = 20
        beg = self.rnd.in_range(-bord - 10, -bord)
        end = self.rnd.in_range(bord, bord + 10)
        x1 = self.rnd.in_range(-bord, -bord + 10)
        x2 = self.rnd.in_range(bord - 10, bord)
        param = self.rnd.index_var()[0]

        b = make_block([
            'func', [ 'F', param ],
            [ '=', 'F', [ '*', [ '+', param, -x1 ], [ '-', param, x2 ] ] ],

            '=', 'A', beg,
            '=', 'B', end,
            '=', 'M', 'A',
            '=', 'R', [ '()', 'F', 'A' ],

            'for', 'i', 'A', 'B',
            [
                'if', [ '<', [ '()', 'F', 'i' ], 'R' ],
                [
                    '=', 'M', 'i',
                    '=', 'R', [ '()', 'F', 'i' ]
                ]
            ]
        ])
        self.text = f'''
Определите значение переменной M после выполнения следующего алгоритма: 
{EGE.LangTable.table(b, [ [ 'Basic', 'Alg' ], [ 'Pascal', 'C' ] ])}'''
        self.correct = b.run_val('M')
        self.accept = r'^-?\d+$'
        return self


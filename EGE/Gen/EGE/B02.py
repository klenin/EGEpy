"""Генератор B02"""

from ...GenBase import DirectInput
from ...Random import Random
from ...RussianModules.NumText import num_bits, num_bytes, num_by_words, num_by_words_text
import EGE.Prog
import EGE.LangTable

class Flowchart(DirectInput):
    def generate(self):
        va, vb = self.rnd.shuffle([ 'a', 'b' ])
        loop = self.rnd.pick([ 'while', 'until' ])
        va_init, va_end, va_op, va_arg, va_cmp = self.rnd.pick([
            lambda: [ 0, self.rnd.in_range(5, 7), '+', 1, '<' ],
            lambda: [ self.rnd.in_range(5, 7), 0, '-', 1, '>' ],
            lambda: [ 1, 2 ** self.rnd.in_range(3, 5), '*', 2, '<' ],
            lambda: [ 2 ** self.rnd.in_range(3, 5), 1, '/', 2, '>' ],
        ])()
        vb_init, vb_op, vb_arg = self.rnd.pick([
            lambda: [ self.rnd.in_range(0, 3), '+', self.rnd.in_range(1, 3) ],
            lambda: [ self.rnd.in_range(15, 20), '-', self.rnd.in_range(1, 3) ],
            lambda: [ self.rnd.in_range(1, 4), '*', self.rnd.in_range(2, 4) ],
            lambda: [ 2 ** self.rnd.in_range(8, 10), '/', 2 ]
        ])()
        b = EGE.Prog.make_block([
            '=', va, va_init,
            '=', vb, vb_init,
            loop, [ va_cmp if loop == 'while' else '==', va, va_end ],
            [ '=', va, [ va_op, va, va_arg ], '=', vb, [ vb_op, vb, vb_arg ], ]
        ])
        self.text = f"""
Запишите значение переменной {vb} после выполнения фрагмента алгоритма:
{b.to_svg_main()}
<i>Примечание: знаком “:=” обозначена операция присваивания</i>
"""
        vars = { va: 0, vb: 0 }
        b.run(vars)
        self.correct = vars[vb]
        self.accept = r"^\-?\d+"
        return self

class SimpleWhile(DirectInput):
    def generate(self):
        lo = self.rnd.in_range(0, 5)
        hi = lo + self.rnd.in_range(3, 5)
        p = self.rnd.pick([
            { 'op': '+', 'start': lo, 'end': hi, 'comp': [ '<', '<=' ] },
            { 'op': '-', 'start': hi, 'end': lo, 'comp': [ '>', '>=' ] },
        ])
        block = EGE.Prog.make_block([
            '=', 's', self.rnd.in_range(1, 10),
            '=', 'k', p['start'],
            'while', [ self.rnd.pick(p['comp']), 'k', p['end'] ], [
                '=', 's', [ '+', 's', 'k' ],
                '=', 'k', [ p['op'] , 'k', 1 ]
            ]
        ])
        self.text = f"""
Напишите, чему равно значение переменной <tt>s</tt> после выполнения следующего блока программы. 
Для вашего удобства алгоритм представлен на четырех языках. 
{EGE.LangTable.table(block, [ [ 'Basic', 'Alg' ], [ 'Pascal', 'C' ] ])}
"""
        self.correct = block.run_val('s')
        self.accept_number()
        return self

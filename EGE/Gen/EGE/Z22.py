from dataclasses import dataclass

from EGE.GenBase import DirectInput
from ... import Html as html
from ...RussianModules.NumText import num_by_words
from ...Utils import nrange

@dataclass
class Plus:
    arg: int = 0

    def text(self):
        return f'прибавить {self.arg}'

    def rev(self, x: int):
        return x - self.arg

@dataclass
class Mult:
    arg: int = 0

    def text(self):
        return f'умножить на {self.arg}'

    def rev(self, x: int):
        return 0 if x % self.arg else int(x / self.arg)

class CalculatorFindPrgmCount(DirectInput):
    def generate(self):
        iteration = 0
        while True:
            self.start_num = self.rnd.in_range(1, 5)
            self.end_num = self.rnd.in_range(14, 25 + self.start_num)
            self.din = [ 1 ] + [ 0 ] * (self.end_num - self.start_num + 1)
            self.curr_comms =  [ Plus(arg=2 if self.start_num % 2 == self.end_num % 2 else 1) ]
            mult_count = self.rnd.coin() + 1
            self.curr_comms += [ Mult(arg=i) for i in self.rnd.pick_n(mult_count, nrange(mult_count + 1, 5)) ]
            answer = self._solve(self.end_num)
            if 10 < answer < 100 or iteration > 20:
                break
            iteration += 1

        self.correct = answer
        self.accept_number()
        self.text = f'''
У исполнителя Калькулятор {num_by_words(len(self.curr_comms), 1)} команды, которым присвоены номера: 
{html.ol_li([ c.text() for c in self.curr_comms ])} 
Сколько есть программ, которые число {self.start_num} преобразуют в число {self.end_num}?'''
        return self

    def _solve(self, n: int):
        if n < self.start_num:
            return 0
        if not self.din[n - self.start_num]:
            for c in self.curr_comms:
                self.din[n - self.start_num] += self._solve(c.rev(n))
        return self.din[n - self.start_num]


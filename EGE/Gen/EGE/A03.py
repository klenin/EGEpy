from ...GenBase import SingleChoice

class Ones(SingleChoice):

    cases = [
        { 'd': 0, 'a': 0 }, { 'd': 1, 'a': 1 }, { 'd': -1, 'a': 3 },
    ]

    def generate(self):
        npower = self.rnd.in_range(5, 10)
        case = self.rnd.pick(Ones.cases)
        n = 2 ** npower + case['d']
        self.text = f"Сколько единиц в двоичной записи числа {n}?"
        self.set_variants([1, 2, npower - 1, npower ])
        self.correct = case['a']
        return self

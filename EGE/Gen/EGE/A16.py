from ...GenBase import SingleChoice
from ...Utils import char_range

class Spreadsheet(SingleChoice):
    def generate(self):
        len_ = [ 0 for _ in range(3) ]
        len_[2] = self.rnd.pick([5, 6])
        len_[0] = self.rnd.in_range(1, len_[2] - 1)
        len_[1] = len_[2] - len_[0]
        ofs = [ 0, len_[0], 0 ]
        cells = [ self.rnd.in_range(1, 8) for _ in range(len_[2]) ]
        start = self.rnd.in_range(1, 3)
        cell_name = self.rnd.pick([ lambda x: list(char_range('A', 'Z'))[x] + str(start),
                                    lambda x: list(char_range('A', 'Z'))[start - 1] + str(x + 1) ])
        cn = [ cell_name(i) for i in range(len_[2]) ]

        values = [ 0 for _ in range(len(len_)) ]
        descr = [ 0 for _ in range(len(len_)) ]
        for i in range(len(len_)):
            if len_[i] == 1:
                values[i] = cells[ofs[i]]
                descr[i] = f'значение ячейки {cn[ofs[i]]}'
            else:
                r = ofs[i] + len_[i] - 1
                values[i] = sum(cells[ofs[i]:r+1])
                f = 'СУММ'
                if not values[i] % len_[i]:
                    f = 'СРЗНАЧ'
                    values[i] /= len_[i]
                descr[i] = f'значение формулы {f}({cn[ofs[i]]}:{cn[r]})'

        order = self.rnd.shuffle([i for i in range(3)])
        bad = []
        seen = [ values[order[1]] ]
        for i in range(len_[2]):
            for j in range(i, len_[2]):
                s = sum(cells[i:j+1])
                if s not in seen:
                    bad.append(s)
                    seen.append(s)
                if j == i or s % (j - i + 1):
                    s /= j - i + 1
                    if s not in seen:
                        bad.append(s)
                        seen.append(s)

        text_args = [ [ descr[order[i]], values[order[i]] ] for i in range(3) ]
        self.text = ('В электронной таблице {0} равно {1}. ' +
        'Чему равно {2}, если {4} равно {5}?').format(*[ item for sub in text_args for item in sub ])
        self.set_variants([ values[order[1]], *self.rnd.pick_n(3, bad) ])
        return self

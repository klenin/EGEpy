from ...GenBase import SingleChoice
from ...Prog import make_block
from ...LangTable import table
import string


class Beads(SingleChoice):
    @staticmethod
    def excepts(array: list, excepts: list):
        r = array
        for e in excepts:
            r.remove(e)
        return r

    def ucfirst(self, s: str):
        return s[0].upper() + s[1:]

    def generate(self):
        all_letters = self.rnd.pick_n(5, list(string.ascii_uppercase))
        length = 3
        order = self.rnd.shuffle(list(range(length)))
        subsets = [ self.rnd.pick_n(self.rnd.pick([3, 4]), all_letters) for _ in range(length) ]

        one_of_beads = [ 'одна из бусин ' + ', '.join(s) for s in subsets ]
        pos_names = [
            ['в начале цепочки', 'на первом месте', ],
            ['в середине цепочки', 'на втором месте', ],
            ['в конце цепочки', 'на последнем месте', 'на третьем месте', ],
        ]

        def gen(bad_stage: int):
            letter = ''
            if bad_stage == 0:
                letter = self.rnd.pick(Beads.excepts(all_letters, subsets[0]))
            r = ['' for _ in range(length)]
            for i in range(length):
                if bad_stage != i:
                    letter = self.rnd.pick(list(filter(lambda x: x != letter, subsets[i])))
                r[order[i]] = letter
            return ''.join(r)

        def pos_name(x: int):
            return self.rnd.pick(pos_names[order[x]])

        rule = self.ucfirst(pos_name(0)) + f' стоит {one_of_beads[0]}. '

        for i in range(1, length):
            f = '{} — {}, {} {}. '.format(
                self.ucfirst(pos_name(i)), one_of_beads[i],
                self.rnd.pick(['которой нет', 'не стоящая']), pos_name(i - 1)
            )
            rule = rule + f

        self.text = f'''Цепочка из трёх бусин, помеченных латинскими буквами, 
                    формируется по следующему правилу. {rule}
                    Какая из перечисленных цепочек создана по этому правилу?'''
        self.set_variants([ gen(i - 1) for i in range(length + 1) ])
        return self


class ArrayFlip(SingleChoice):
    def generate(self):
        n = self.rnd.in_range(8, 12)
        i, k = self.rnd.index_var(2)
        init_op = self.rnd.pick([
            [ '=', [ '[]', 'A', i ], [ '-', n - 1, i ] ],
            [ '=', [ '[]', 'A', i ], i ]
        ])
        A_i = [ '[]', 'A', i ]
        A_ni = [ '[]', 'A', [ '-', (n - 1), i ] ]
        if self.rnd.coin():
            A_i, A_ni = A_ni, A_i
        b = make_block([
            'for', i, 0, n - 1, init_op,
            'for', i, 0, (n - 1) // 2, [ '=', k, A_i, '=', A_i, A_ni, '=', A_ni, k ]
        ])
        lt = table(b, [ [ 'Basic', 'Alg' ], [ 'Pascal', 'C' ] ])
        ar_val = b.run_val('A')
        bad1 = list(range((n - 1) // 2 + 1)) + list(range(n // 2))[::-1]
        bad2 = list(range((n - 1) // 2 + 1))[::-1] + list(range(n % 2, (n - 1) // 2 + 1))

        ar_val = list(ar_val)
        self.set_variants([ ' '.join(str(x) for x in v) for v in [ ar_val, ar_val[::-1], bad1, bad2 ] ])
        self.text = f'''В программе используется одномерный целочисленный массив A с индексами
                    от 0 до {n - 1}. Ниже представлен фрагмент программы, записанный на 
                    разных языках программирования, в котором значения элементов сначала 
                    задаются, а затем меняются. {lt} Чему будут равны элементы этого массива
                    после выполнения фрагмента программы?'''
        return self


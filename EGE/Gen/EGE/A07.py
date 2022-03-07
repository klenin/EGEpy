from ...GenBase import SingleChoice
from ...Logic import random_logic_expr
from ...Bits import Bits
from ...RussianModules.NumText import num_text, num_by_words
from ...RussianModules import Names as RussianNames
from ...RussianModules import Animals as RussianAnimals
from ...Prog import SynElement
from ...Utils import char_range
import copy
import re

class Condition:
    n: int; type: int; vc: int

    def __init__(self, rnd):
        self.n = rnd.in_range(1, 5)
        self.type = 1 if rnd.in_range(1, 6) > 1 else 2
        self.vc = rnd.coin()

    def __eq__(self, other):
        if self.n == other.n and self.type == other.type and self.vc == other.vc:
            return True
        return False

    def __str__(self):
        pos_names = [ 'Первая', 'Вторая', 'Третья', 'Четвёртая', 'Пятая', 'Шестая' ]
        letters = [ 'гласная буква', 'гласных буквы', 'гласных букв' ]

        vc = 'со' if self.vc else ''
        if self.type == 1:
            return pos_names[self.n - 1] + f' буква {vc}гласная'
        else:
            return 'В слове ' + num_text(self.n, [ vc + i for i in letters ])

class CondGroup:
    size: int; vars: list; expr: SynElement; cond: list; text: str; min_len: int

    def __init__(self, rnd):
        self.size = rnd.pick([ 2, 3 ])
        self.cond = [Condition(rnd)]
        for i in range(2, self.size + 1):
            new_cond = Condition(rnd)
            while any([ i == new_cond for i in self.cond ]):
                new_cond = Condition(rnd)
            self.cond.append(new_cond)

        self.vars = [ str(self.cond[i]) for i in range(self.size) ]
        self.expr = random_logic_expr(rnd, self.vars)
        self.text = self.expr.to_lang_named('Logic')
        self.min_len = max(self.cond, key=lambda x: x.n).n

class Strings(SingleChoice):

    def letter_vc(self, char):
        return 0 if char.lower() in [ 'а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я' ] else 1

    def count_vc(self, s, vc):
        return sum([ self.letter_vc(s[i]) == vc for i in range(len(s)) ])

    def check_cond(self, cond, s):
        vc = cond.vc
        if cond.type == 1:
            return self.letter_vc(s[cond.n - 1]) == vc
        else:
            return cond.n == self.count_vc(s, vc)

    def check_good(self, tf):
        for i in self.rnd.shuffle([0, 1]):
            if len(tf[1 - i]) != 0 and len(tf[i]) >= 3:
                return i
        return -1

    def check_cond_group(self, g, s):
        g1 = copy.deepcopy(g)
        var_bool = {}
        for i in range(g1.size):
            b = self.check_cond(g1.cond[i], s)
            var_bool[g1.vars[i]] = b
            g1.vars[i] = b
        g1.expr.rename_vars(var_bool)
        return g1.expr.run({})

    def strings(self, strings, list_text):
        good = -1
        while good < 0:
            g = CondGroup(self.rnd)
            true_false = [ [], [] ]
            for s in strings:
                if len(s) < g.min_len:
                    continue
                true_false[self.check_cond_group(g, s)].append(s)
                good = self.check_good(true_false)

        tf = 'истинно' if good != 0 else 'ложно'

        self.text = f'Для какого {list_text} {tf} высказывание:<br/>{g.text}?'
        return self.set_variants([true_false[good][0]] + true_false[1 - good][:3])

class Names(Strings):

    def generate(self):
        return self.strings(self.rnd.shuffle(RussianNames.all_names), 'имени')

class Animals(Strings):

    def generate(self):
        return self.strings(self.rnd.shuffle(RussianAnimals.animals), 'из названий животных')

class RandomSequences(Strings):

    def generate(self):
        seen = set()
        while len(seen) < 100:
            r = ''
            while r == '' or r in seen:
                r = ''.join(self.rnd.pretty_russian_letter().upper() for _ in range(1, 7))
            seen.add(r)
        return self.strings(list(seen), 'символьного набора')

class RestorePassword(SingleChoice):

    def delete_nums(self, string):
        good_variants = []
        bad_variants = []
        for l in range(1, len(string)):
            pos = []
            for match in re.finditer(r'(?:\D|^)\d{%d}(?!\d)' % l, string):
                pos.append(match.start())
            if not len(pos):
                continue

            subset = Bits().set_size(len(pos))
            # генерация всех подмножеств множества перечислением двоичных векторов
            for _ in range(2, 2**len(pos) + 1):
                subset.inc()
                s = string
                for i in range(len(pos) - 1, -1, -1):
                    if subset.get_bit(i):
                        s = s[:pos[i]] + s[pos[i] + l:]
                bad_variants.append(s)
            good_variants.append([ bad_variants.pop(), l ])
        bad_variants.append(string)
        return good_variants, bad_variants

    def generate(self):
        init_str = ''.join(self.rnd.pick(list(char_range('A', 'F')) + list(map(str, range(10)))) for _ in range(5))
        l = self.rnd.pick_n(2, list(char_range('A', 'Z')))
        d = self.rnd.pick_n(2, list(range(10)))
        sub_init = l[0] + str(d[0])
        sub_good = l[1] + str(d[1])

        # Вставим в разные копии одной строки в 2 позиции маленькие строки.
        pos = sorted(self.rnd.pick_n(2, list(range(len(init_str)))))
        string = init_str[:pos[0]] + sub_good + init_str[pos[0]:pos[1]] + sub_good + init_str[pos[1]:]
        init_str = init_str[:pos[0]] + sub_init + init_str[pos[0]:pos[1]] + sub_init + init_str[pos[1]:]

        # Удалив полностью и частично цифры из строк получим варианты ответов
        good_variants, bad_variants = self.delete_nums(string)
        bad_variants2, bad_variants3 = self.delete_nums(init_str)

        good_variants = self.rnd.shuffle(good_variants)
        ans = good_variants.pop(0)

        self.set_variants([ans[0]] +
                          self.rnd.pick_n(3,
                                          bad_variants +
                                          [ i[0] for i in good_variants ] +
                                          bad_variants3 +
                                          [ i[0] for i in bad_variants2 ]))

        os = self.rnd.pick([ 'Windows', 'GNU/Linux', 'операционную систему', 'почтовый аккаунт' ])
        self.text = (
                self.rnd.pick(RussianNames.male) +
                f''' забыл пароль для входа в {os}, но помнил алгоритм его 
                получения из символов «{init_str}» в строке подсказки. 
                Если последовательность символов «{sub_init}» заменить на «{sub_good}» 
                и из получившейся строки удалить все ''' +
                ('одно' if ans[1] == 1 else num_by_words(ans[1], 1, 'genitive')) +
                'значные числа, то полученная последовательность и будет паролем:')

        return self

class SpreadsheetShift(SingleChoice):

    def _move(self, ceil, hold_x, hold_y, dx, dy):
        x = ceil['x']
        y = ceil['y']
        if not hold_x:
            x += dx
        if not hold_y:
            y += dy
        return { 'x': x, 'y': y }

    def _all_moves(self, ceil, hold_x, hold_y, dx, dy):
        res = [ self._move(ceil, hold_x, hold_y, dx, dy) ]
        if dx:
            res.append(self._move(ceil, not hold_x, hold_y, dx, dy))
        if dy:
            res.append(self._move(ceil, hold_x, not hold_y, dx, dy))
        if dx and dy:
            res.append(self._move(ceil, not hold_x, not hold_y, dx, dy))
        return res

    def _print_ceil(self, ceil, hold_x=None, hold_y=None, suffix=None):
        return ''.join([('$' if hold_y else ''), chr(ceil['y'] + ord('a')),
                        ('$' if hold_x else ''), str(ceil['x']),
                        (suffix if suffix else '')])

    def _rnd_ceil(self):
        return { 'x': self.rnd.in_range(4, 10), 'y': self.rnd.in_range(4, 10) }

    def _ceil_eq(self, ceil1, ceil2):
        return ceil1['x'] == ceil2['x'] and ceil1['y'] == ceil2['y']

    def _gen_params(self, c):
        d = self.rnd.in_range(1, 3)

        c['moves'] = self.rnd.shuffle([ [d, d], [-d, d], [d, -d], [-d, -d], [d, 0], [-d, 0], [0, d], [0, -d] ])

        hold_x = False
        hold_y = False
        while not hold_x and not hold_y:
            hold_x = self.rnd.coin()
            hold_y = self.rnd.coin()

        c['ceil'] = self._rnd_ceil()
        c['hold_x'] = hold_x
        c['hold_y'] = hold_y

        while True:
            c['from_ceil'] = self._rnd_ceil()
            c['to_ceil'] = self._move(c['from_ceil'], 0, 0, *c['moves'][0])
            if not self._ceil_eq(c['ceil'], c['from_ceil']) and not self._ceil_eq(c['ceil'], c['to_ceil']):
                break

        c['suffix'] = self.rnd.pick([' + ', ' - ', ' * ', ' / ']) + str(self.rnd.in_range(1, 9))
        return c

    def _gen_task(self, c):
        res = []
        i = 0
        while len(res) < 4:
            for p in self._all_moves(c['ceil'], c['hold_x'], c['hold_y'], *c['moves'][i]):
                if not sum([self._ceil_eq(p, i) for i in res]):
                    res.append(p)
            i += 1
        c['result'] = res[0: 4]
        return c

    def generate(self):
        context = {}
        self._gen_params(context)
        self._gen_task(context)

        self.set_variants([self._print_ceil(i, context['hold_x'], context['hold_y'], context['suffix']) for i in context['result']])

        self.text = '''В ячейке {} электронной таблицы записана формула = {}. Какой вид 
            приобретет формула, после того как ячейку {} скопируют в ячейку {}? 
            Примечание: знак $ используется для обозначения абсолютной адресации.'''.format(
            self._print_ceil(context['from_ceil']),
            self._print_ceil(context['ceil'], context['hold_x'], context['hold_y'], context['suffix']),
            self._print_ceil(context['from_ceil']),
            self._print_ceil(context['to_ceil']))

        return self

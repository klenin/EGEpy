from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text
from ...Utils import char_range
from ... import Html as html
from .A17 import pie_chart
import re

class Calculator(DirectInput):
    def _make_cmd(self, args: list):
        cmd = {}
        for i, key in enumerate(['t1', 't2', 't3', 'run']):
            cmd[key] = args[i]
        return cmd

    def _apply(self, cmd: list, prg: list, value: int):
        for item in prg:
            value = cmd[item]['run'](value)
        return value

    def _next_prg(self, cmd: list, prg: list):
        for i in range(len(prg)):
            prg[i] += 1
            if prg[i] < len(cmd):
                return 1
            prg[i] = 0
        return 0

    def _code(self, d: list):
        return ''.join(str(i + 1) for i in d)

    def _same_digit(self, x: str):
        return re.match(r"^(\d)\1+$", x)

    def _get_commands(self):
        v1 = self.rnd.in_range(1, 9)
        v2 = self.rnd.in_range(2, 5)

        return [
            [
                f"прибавь {v1}",
                f"прибавляет к числу на экране {v1}",
                f"прибавляет к нему {v1}",
                lambda x: x + v1
            ],
            [
                f"умножь на {v2}",
                f"умножает число на экране на {v2}",
                f"умножает его на {v2}",
                lambda x: x * v2
            ],
            [
                'возведи в квадрат',
                'возводит число на экране в квадрат',
                'возводит его в квадрат',
                lambda x: x ** 2
            ],
        ]

    def generate(self):
        num = self.rnd.in_range(4, 6)

        while True:
            cmd = [ self._make_cmd(i) for i in self.rnd.pick_n(2, self._get_commands()) ]
            arg = self.rnd.in_range(2, 10)
            prg = [ 0 for _ in range(num) ]
            results = {}
            while True:
                idx = self._apply(cmd, prg, arg)
                if idx not in results.keys():
                    results[idx] = 1
                else:
                    results[idx] += 1
                if not self._next_prg(cmd, prg):
                    break
            r = []
            for key in results.keys():
                if 50 < key and key < 1000 and results[key] == 1:
                    r.append(key)
            result = r and self.rnd.pick(r)
            if result:
                break
        prg = [ 0 for i in range(num) ]
        while True:
            self._next_prg(cmd, prg)
            if self._apply(cmd, prg, arg) == result:
                break
        code_prg = self._code(prg)

        while True:
            sample_prg = [ self.rnd.in_range(0, len(cmd)-1) for _ in range(num) ]
            sample_code = self._code(sample_prg)
            sample_result = self._apply(cmd, sample_prg, 1)
            if sample_code != code_prg and sample_result != result and not self._same_digit(sample_code):
                break

        sample_prg_list = [ cmd[i]['t1'] for i in sample_prg ]
        sample_prg_list[-1] += ','

        bold = html.style(**{ 'font-weight': 'bold' })
        self.text = f'''У исполнителя Калькулятор две команды, которым присвоены номера:
{html.ol_li([(i['t1']).title() for i in cmd], bold)}
Выполняя первую из них, Калькулятор {cmd[0]['t2']}, 
а выполняя вторую, {cmd[1]['t3']}.
Запишите порядок команд в программе получения из числа {arg}
числа {result}, содержащей не более {num} команд, указывая лишь номера команд
(Например, программа {sample_code} — это программма
{html.ul_li(sample_prg_list, bold)}
которая преобразует число 1 в число {sample_result}).'''
        self.correct = code_prg
        self.accept_number()
        return self


class ComleteSpreadsheet(DirectInput):
    def _char_to_int(self, c: str):
        return ord(c[1:len(c)]) - ord('A')

    def _to_formula(self, str: str, perm_alph: list):
        return re.sub(r"\%\w+", lambda x: perm_alph[self._char_to_int(x.string[x.start():x.end()])] + '1', str)

    def _apply_perm(self, array: list, perm: list):
        return [array[i] for i in perm]

    def _back_perm(self, perm: list):
        h = {}
        for i in range(len(perm)):
            h[perm[i]] = i
        return [h[i] for i in sorted(h.keys())]

    def generate(self):
        table = self.rnd.pick([
            {
                1: [ 3, 2, 3, 2 ],
                2: [ '(%C+%A)/2', '%C-%D', '%A-%D', '%B/2' ],
                'ans': [ 3, 1, 1, 1 ],
                'find': 1
            },
            {
                1: [ 1, 2, 3 ],
                2: [ '(%A+%B+%C)/2', '%C', '3*%B-%C' ],
                'ans': [ 3, 3, 3 ],
                'find': 0
            },
            {
                1: [ 2, 3, 0, 3 ],
                2: [ '%A', '(%B+%D)/3', '2*%C', '2*(%B-%A)' ],
                'ans': [ 2, 2, 0, 2 ],
                'find': 2
            }
        ])

        n = len(table[1])
        perm_1 = self.rnd.shuffle([ i for i in range(n) ])
        perm_1_back = self._back_perm(perm_1)
        perm_2 = self.rnd.shuffle([ i for i in range(n) ])
        perm_alph = self._apply_perm(list(char_range('A', 'Z')), perm_1_back)

        new_table = {
            1: self._apply_perm(table[1], perm_1),
            2: self._apply_perm(table[2], perm_2),
            'ans': self._apply_perm(table['ans'], perm_2),
            'find': perm_1_back[table['find']]
        }
        self.correct = new_table[1][new_table['find']]
        new_table[1][new_table['find']] = ''
        empty_cell = list(char_range('A', 'Z'))[new_table['find']] + '1'

        last_letter = list(char_range('A', 'Z'))[n - 1]
        table_text = html.table([
            html.row('th', [ html.nbsp, *list(char_range('A', last_letter)) ]),
            html.row('td', [ '<strong>1</strong>', *[ str(i) for i in new_table[1] ] ]),
            html.row('td', [ '<strong>2</strong>', *[ self._to_formula(i, perm_alph) for i in new_table[2] ] ]),
            ], **{ 'border': 1, **html.style(text_align='center') }
        )
        colors = [ 'red', 'green', 'blue', 'orange', 'gray', 'yellow', 'brown' ]
        chart = pie_chart(new_table['ans'], { 'size': 100, 'colors': colors })
        self.text = f'''Дан фрагмент электронной таблицы: {table_text}
Какое число  должно быть записано в ячейке {empty_cell}, чтобы 
построенная после выполнения вычислений диаграмма по значениям
диапазона ячеек A2:{last_letter}2 соответствовала рисунку? {chart}'''
        return self

class AdslSpeed(DirectInput):
    def generate(self):
        speed = (1 << self.rnd.in_range(5, 9)) * 1000
        word_forms = {
            1: [ 'секунду', 'секунды', 'секунд' ],
            60: [ 'минуту', 'минуты', 'минут' ],
            3600: [ 'час', 'часа', 'часов' ],
        }
        time_unit_multiplier = self.rnd.pick(list(word_forms.keys()))
        time_in_units = self.rnd.in_range(1, 7)
        while True:
            c = self.correct = time_in_units * time_unit_multiplier * speed / 8 / 1024
            if c == int(c):
                break
            time_in_units *= 2
        self.text = f'''Скорость передачи данных через ADSL-соединение равна {speed} бит/c.
Передача файла через данное соединение заняла {num_text(time_in_units, word_forms[time_unit_multiplier])}.
Определите размер файла в килобайтах.'''
        return self

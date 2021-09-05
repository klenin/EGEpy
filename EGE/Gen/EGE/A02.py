from collections import Counter
from dataclasses import dataclass
from math import ceil, log

from ...GenBase import EGEError, SingleChoice
from ...Random import Random
from ...Russian.NumText import bits_and_bytes, num_bits, num_bytes, num_text
from ... import Html as html

def bits_or_bytes(rnd: Random, n: int):
    return num_bytes(n) if rnd.coin() else num_bits(n * 8)

@dataclass
class Sport:
    name: str; forms: list

class SportsmanNumbers(SingleChoice):

    def generate(self):
        flavour = self.rnd.pick([
            Sport('велокроссе', [ 'велосипедист', 'велосипедиста', 'велосипедистов' ]),
            Sport('забеге', [ 'бегун', 'бегуна', 'бегунов' ]),
            Sport('марафоне', [ 'атлет', 'атлета', 'атлетов' ]),
            Sport('заплыве', [ 'пловец', 'пловца', 'пловцов' ]),
        ])
        bits = self.rnd.in_range(5, 7)
        total = 2 ** bits - self.rnd.in_range(2, 5)
        passed = total // 2 + self.rnd.in_range(-5, 5)
        passed_text = num_text(passed, flavour.forms)
        total_text = num_text(total, [ 'спортсмен', 'спортсмена', 'спортсменов' ])
        self.text = f"""
В {flavour.name} участвуют {total_text}. Специальное устройство регистрирует
прохождение каждым из участников промежуточнго финиша, записывая его номер
с использованием минимального количества бит, одинакового для каждого спортсмена.
Каков информационный объем сообщения, записанного устройством,
после того как промежуточный финиш прошли {passed_text}?
"""
        return self.set_variants(
            [ num_bits(bits * passed) ] +
            self.rnd.pick_n(3, [
                *bits_and_bytes(total),
                *bits_and_bytes(passed),
                num_bits(bits * total)
            ])
        )


@dataclass
class NumberType:
    long_: str; short: str; forms: list

class CarNumbers(SingleChoice):

    def _make_alphabet(self):
        char_cnt = self.rnd.in_range(2, 33)
        base, base_name = self.rnd.pick([
            [ 2, 'двоичные' ],
            [ 8, 'восьмеричные' ],
            [ 10, 'десятичные' ],
            [ 16, 'шестнадцатиричные' ],
        ])
        letters = num_text(char_cnt, [ 'различную букву', 'различные буквы', 'различных букв' ])
        self.alph_text = (self.case_sensitive and
            f"{base_name} цифры и {letters} " +
            'местного алфавита, причём все буквы используются в двух начертаниях: ' +
            'как строчные, так и заглавные (регистр буквы имеет значение!)'
            or
            f"{letters} и {base_name} цифры")
        self.alph_length = char_cnt * (self.case_sensitive and 2 or 1) + base

    def _gen_task(self):
        bits_per_item = ceil(log(self.alph_length) / log(2)) * self.sym_cnt
        answer = (bits_per_item + 7) // 8
        variants = { answer, answer - 1, bits_per_item }
        len_ = self.alph_length
        while len_ in variants:
            len += 1
        self.result = [ num_bytes(v * self.items_cnt) for v in variants | { len_ } ]

    def _gen_text(self):
        number = dict(short='номер', forms=[ 'номерa', 'номеров', 'номеров' ])
        obj_name = self.rnd.pick([
            NumberType(long_='автомобильный номер', **number),
            NumberType(long_='телефонный номер', **number),
            NumberType(long_='почтовый индекс', short='индекс', forms=[ 'индекса', 'индексов', 'индексов' ]),
            NumberType(long_='почтовый адрес', short='адрес', forms=[ 'адреса', 'адресов', 'адресов' ]),
            NumberType(long_='номер медицинской страховки', **number),
        ])
        items_cnt_text = num_text(self.items_cnt, obj_name.forms)
        sym_cnt_text = num_text(self.sym_cnt, [ 'символа', 'символов', 'символов' ])
        return f"""
В некоторой стране {obj_name.long_} состоит из {sym_cnt_text}. В качестве символов
используют {self.alph_text}. Каждый такой {obj_name.short} в компьютерной программе
записывается минимально возможным и одинаковым целым количеством байтов, при этом
используют посимвольное кодирование и все символы кодируются одинаковым и минимально
возможным количеством битов. Определите объём памяти, отводимый этой программой для
записи {items_cnt_text}.
"""

    def generate(self):
        self.case_sensitive = bool(self.rnd.coin())
        self.sym_cnt = self.rnd.in_range(4, 20)
        self.items_cnt = self.rnd.in_range(2, 20)
        self._make_alphabet()
        self._gen_task()

        self.text = self._gen_text()
        return self.set_variants(self.result)


class Units(SingleChoice):

    @dataclass
    class P:
        name: str; power2: int; power10: int

    def generate(self):
        npower = self.rnd.in_range(1, 4)
        n = 2 ** npower
        self.correct = self.rnd.coin()
        small_unit_name = ['байт', 'бит'][self.correct]
        large_unit = self.rnd.pick([
            Units.P('Кбайт', 10, 3),
            Units.P('Мбайт', 20, 6),
            Units.P('Гбайт', 30, 9),
        ])
        self.text = f"Сколько {small_unit_name} содержит {n} {large_unit.name}?"
        return self.set_variants([
            '2<sup>%d</sup>' % (npower + large_unit.power2),
            '2<sup>%d</sup>' % (npower + large_unit.power2 + 3),
            '%d × 10<sup>%d</sup>' % (n, large_unit.power10),
            '%d × 10<sup>%d</sup>' % (8 * n, large_unit.power10),
        ])


class MinRoutes(SingleChoice):
    """
    Источник

    Демонстрационные варианты ЕГЭ по информатике 2012, официальный информационный
    портал ЕГЭ. Задание A2.

    Выбираются количество городов и количество дорог.

    Генерируется матрица смежности для неориентированного графа без петель (возможно)
    с циклами.

    Использоуется алгоритм Флойда-Уоршолла для поиска расстояний между вершинами.
    Причем во время работы алгоритма при улучшшении существующих значений в таблице
    маршрутов запоминаются предыдущие значения(будут использованы в качестве
    дистракторов).

    Выбираются 2 вершины между которыми существует маршрут с наибольшим числом
    дистракторов. В качестве недостающих вариантов ответов берутся длины маршрутов
    из других вершин в конечную и случайные числа.
    """

    def _gen_params(self):
        self.n: int = 6
        self.edges_cnt = self.rnd.in_range(5, 10)
        self.weights_range = [1, 10]

    def _init_tables(self):
        self.towns = [ chr(ord('A') + i) for i in range(self.n) ]
        self.alt_routes = [ [ set() ] * self.n for _ in range(self.n) ]
        self.routes = [ [ None ] * self.n for _ in range(self.n) ]

    def _gen_init_routes(self):
        self._init_tables()

        edges = [ [ i, j ] for i in range(self.n) for j in range(self.n) if j != i ]
        for e in self.rnd.pick_n(self.edges_cnt, edges):
            i, j = e
            weight = self.rnd.in_range(*self.weights_range)
            self.routes[i][j] = self.routes[j][i] = weight

        self.init_routes = [ row[:] for row in self.routes ]

    def _find_all_dists(self):
        r = self.routes

        def relax(i, j, k):
            a, b, c = r[i][k], r[k][j], r[i][j]
            if a is not None and b is not None:
                if c is None or c > a + b:
                    r[i][j] = a + b
                self.alt_routes[i][j].add(a)

        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        relax(i, j, k)

    def _choose_from_to(self):
        first, mi, mj = True, 0, 0
        for i in range(self.n):
            for j in range(self.n):
                if (
                    i != j and not self.init_routes[i][j] and (
                    self.routes[i][j] is not None if first else
                    len(self.alt_routes[i][j]) > len(self.alt_routes[mi][mj]))
                ):
                    first, mi, mj = False, i, j
        self.ans_from, self.ans_to = mi, mj

    def add_ans(self, ans):
        if ans not in self.ans:
            self.ans.append(ans)

    def _gen_task_and_answers(self):
        self._choose_from_to()
        i, j = self.ans_from, self.ans_to
        r = self.routes[i][j]
        self.ans = [ r ] + [ a for a in self.alt_routes[i][j] if a != r ]
        for k in range(self.n):
            r = self.routes[k][j]
            if r:
                self.add_ans(r)

        while len(self.ans) < 4:
            self.add_ans(self.rnd.in_range(
                self.weights_range[0],
                self.weights_range[1] * self.towns_cnt))

    def _gen_text(self):
        towns = ', '.join(self.towns)
        from_ = self.towns[self.ans_from]
        to = self.towns[self.ans_to]
        r = (
            f"Между населёнными пунктами {towns} построены дороги, протяжённость " +
            'которых приведена в таблице. (Отсутствие числа в таблице означает, ' +
            'что прямой дороги между пунктами нет.) ')

        t = html.row_n('th', [ html.nbsp ] + self.towns)
        for i in range(len(self.init_routes)):
            t += html.row_n('td',
                [ html.tag('strong', self.towns[i]) ] +
                [ v or html.nbsp for v in self.init_routes[i] ])

        r += (html.table(t, border=1) +
            f"Определите длину кратчайшего пути между пунктами {from_} и {to} " +
            '(при условии, что передвигаться можно только по построенным дорогам)')
        self.text = r

    def _dijkstra(self, from_, to):
        d = [ None ] * self.n
        d[from_] = 0
        fin = [ i == from_ for i in range(self.n) ]
        for step in range(self.n):
            v: int = 0
            for i in range(self.n):
                if d[i] is not None and (d[v] is None or d[i] < d[v]):
                    v = i
            fin[v] = True
            if v == to:
                break
            updated = False
            for i in range(self.n):
                x = self.routes[v][i]
                if (x is not None and (d[i] is None or d[i] > d[v] + x)):
                    d[i] = d[v] + x
                    updated = True
            if not updated:
                break
        return d[to]

    def _validate(self):
        if self.ans_from == self.ans_to:
            raise EGEError(f"{self.ans_from} == {self.ans_to}")
        d = self._dijkstra(self.ans_from, self.ans_to)
        if d is None or d != self.ans[0]:
            raise EGEError(f"{d} != {self.ans[0]}")
        if len(self.ans) < 3:
            raise EGEError(f"{self.ans}")
        cnt = Counter(self.ans)
        m, c = cnt.most_common()[0]
        if c > 1:
            raise EGEError(f"count({m}) = {c}")

    def generate(self):
        self._gen_params()
        self._gen_init_routes()
        self._find_all_dists()
        self._gen_task_and_answers()
        self._gen_text()
        self._validate()
        return self.set_variants(self.ans[:4])


class SportAthleteNumbers(SingleChoice):

    def generate(self):
      athletes = self.rnd.in_range(9, 255)
      bits = ceil(log(athletes) / log(2))
      self.text = (
          f"В соревновании участвуют {athletes} атлетов. " +
          'Какое минимальное количество бит необходимо, чтобы кодировать номер каждого атлета?')
      return self.set_variants(
          [ num_bits(bits) ] +
          self.rnd.pick_n(3, [
              num_bits(bits * 3 // 2),
              num_bits(bits + 1),
              num_bits(bits - 1)
          ])
       )

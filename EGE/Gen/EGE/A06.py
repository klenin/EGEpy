import imp
from statistics import variance
from EGE.Bits import Bits
from ...GenBase import SingleChoice
from ...LangTable import unpre, table
from ...Prog import make_block
from ...Utils import sign

class CountBySign(SingleChoice):
    def generate(self):
        array_length = self.rnd.in_range(50, 100)
        iteration_variable = self.rnd.index_var()[0]
        c_language_comment = unpre(f'''
/* В программе на языке Си следует считать, что массивы A и B
индексируются начиная с 1 и состоят из элементов
A[1], … A[{array_length}], B[1], … B[{array_length}] */'''
        )
        first_loop_body = [
            '=', ['[]', 'A', iteration_variable], [ '*', iteration_variable, iteration_variable ],
        ]
        second_loop_body = [
            '=', [ '[]', 'B', iteration_variable ], [ '-', [ '[]', 'A', iteration_variable ], array_length ],
        ]
        code_block_parts = [
            'for', iteration_variable, 1, array_length, first_loop_body,
            'for', iteration_variable, 1, array_length, second_loop_body,
            '#', { 'C': c_language_comment },
        ]
        code_block = make_block(code_block_parts)
        lang_table = table(code_block, [ [ 'Basic', 'Alg' ], [ 'Pascal', 'C' ] ])
        case = self.rnd.pick([
            { 'name': 'положительные',   'test': lambda x: x > 0  },
            { 'name': 'отрицательные',   'test': lambda x: x < 0  },
            { 'name': 'неотрицательные', 'test': lambda x: x >= 0 },            
        ])
        self.text = f'''
Значения двух массивов A и B с индексами от 1 до {array_length}
задаются при помощи следующего фрагмента программы: {lang_table}
Какое количество элементов массива B[1..{array_length}] будет принимать
{case['name']} значения после выполнения данной программы?'''

        array_B = code_block.run_val('B')
        correct = len(list(filter(lambda x: case['test'](x), array_B.values())))
        errors = [
            correct + 1, correct - 1, array_length - correct, array_length - correct + 1, array_length - correct - 1
        ]
        self.set_variants([ correct ] + self.rnd.pick_n(3, errors))
        return self

class FindMinMax(SingleChoice):
    def generate(self):
        array_length = self.rnd.in_range(50, 100)
        # Нужно гарантировать единственные максимум и минимум.
        value = self.rnd.in_range(array_length // 2 + 1, array_length - 1)
        iteration_variable = self.rnd.index_var()[0]
        factor = [ '-' ] + self.rnd.shuffle([ iteration_variable, value ])
        indexB, indexA = self.rnd.shuffle([
            iteration_variable, [ '-', array_length + 1, iteration_variable ]
        ])
        first_loop_body = [
            '=', [ '[]', 'A', iteration_variable ], [ '*', factor, factor ],
        ]
        second_loop_body = [
            '=', [ '[]', 'B', indexB ], [ '[]', 'A', indexA ],
        ]
        code_block_parts = [
            'for', iteration_variable, 1, array_length, first_loop_body,
            'for', iteration_variable, 1, array_length, second_loop_body,
        ]
        code_block = make_block(code_block_parts)
        lang_table = table(code_block, [ [ 'Basic', 'Pascal', 'Alg' ] ])
        case = self.rnd.pick([
            { 'name': 'наибольшим', 'test': 1 },
            { 'name': 'наименьшим', 'test': -1 },
        ])
        self.text = f'''
Значения двух массивов A[1..{array_length}] и B[1..{array_length}]
задаются с помощью следующего фрагмента программы: {lang_table}
Какой элемент массива B будет {case['name']}?'''

        array_B = code_block.run_val('B')
        correct = 1
        wrong = 1
        for i in range(2, array_length + 1):
            sn = sign(array_B[i], array_B[correct]) * case['test']
            if sn > 0:
                correct = i
            elif sn < 0:
                wrong = i
        
        seen = { correct: True }

        def filter_function(value: int) -> bool:
            if not (1 <= value <= array_length) or (value in seen and seen[value]):
                return False
            seen[value] = True
            return True

        errors = list(filter(filter_function, [
            correct + 1, correct - 1, array_length - correct, array_length - correct  - 1, wrong, array_length - wrong
        ]))
        self.set_variants([f"B[{variant}]" for variant in [ correct ] + self.rnd.pick_n(3, errors)])
        return self

class CountOddEven(SingleChoice):
    def generate(self):
        array_length = self.rnd.in_range(7, 10)
        outer_iteration_variable, inner_iteration_variable = self.rnd.index_var(2)
        get_by_index_operation = [
            '[]', 'A', outer_iteration_variable, inner_iteration_variable
        ]
        add_operation = [
            '+', outer_iteration_variable, [
                self.rnd.pick([ '+', '-' ])[0], inner_iteration_variable, 1
            ]
        ]
        assignment_operation = [ '=', get_by_index_operation, add_operation ]
        inner_loop_block = [
            'for', inner_iteration_variable, 1, array_length, assignment_operation
        ]
        outer_loop_block = [
            'for', outer_iteration_variable, 1, array_length, inner_loop_block
        ]
        
        code_block = make_block(outer_loop_block)
        lang_table = table(code_block, [ [ 'Basic', 'Pascal', 'Alg' ] ])
        case = self.rnd.pick([
            { 'name': 'чётное', 'test': 0 },
            { 'name': 'нечётное', 'test': 1 },
        ])
        self.text = f'''
Значения двумерного массива A размера {array_length} × {array_length}
задаются с помощью вложенного оператора цикла
в представленном фрагменте программы: {lang_table}
Сколько элементов массива A будут принимать {case['name']} значение?'''
        
        array_A = code_block.run_val('A')
        correct = 0
        for i in range(1, array_length + 1):
            for j in range(1, array_length + 1):
                if (array_A[i][j] % 2 == case['test']):
                    correct += 1
        
        errors = [ _ for _ in range(-5, 0) ] + [ _ for _ in range(1, 6) ]
        errors = [ correct + error for error in errors ]
        seen = { correct: True }

        def filter_function(value: int) -> bool:
            if (value in seen and seen[value]):
                return False
            seen[value] = True
            return True

        errors = list(filter(filter_function, errors))
        self.set_variants([ correct ] + self.rnd.pick_n(3, errors))
        return self 

class AlgMinMax(SingleChoice):
    def generate(self):
        i, j = self.rnd.pick_n(2, [ 'i', 'j', 'k', 'm' ])
        minmax = self.rnd.pick([
            { 'text': 'максимальн', 'comp': '>' },
            { 'text': 'минимальн', 'comp': '<' },
        ])
        eq = self.rnd.pick([
            { 'answer': 1, 'comp': '' },
            { 'answer': 2, 'comp': '=' },
        ])
        idx = self.rnd.pick([
            { 'answer': 0, 'res': [ '[]', 'A', j ] },
            { 'answer': eq['answer'], 'res': j },
        ])
        minmax_statement = [
            f"{minmax['comp']}{eq['comp']}",
            [ '[]', 'A', i ],
            [ '[]', 'A', j ],
        ]
        condition_statement = [ 'if', minmax_statement, [ '=', j, i ], ]
        loop_block = [ 'for', i, 1, 'N', condition_statement ]
        code_block = make_block(
            [ '=', j, 1, ] + loop_block + [ '=', 's', idx['res'] ]
        )
        lang_table = table(code_block, [ [ 'Basic', 'Pascal', 'Alg' ] ])
        self.text = f'''
Дан фрагмент программы, обрабатывающей массив A из N элементов: {lang_table}
Чему будет равно значение переменной s после выполнения
данного алгоритма, при любых значениях элементов массива A?'''
        if_many = f" из них, если {minmax['text']}ых элементов несколько)"
        variants = [
            f"{minmax['text'].capitalize()}ому эдементу в массиве A",
            f"Индексу {minmax['text']}ого элемента в массиве A (первому{if_many}",
            f"Индексу {minmax['text']}ого элемента в массиве A (последнему{if_many}",
            f"Количеству элементов, равных {minmax['text']}ому в массиве A",
        ]
        self.set_variants(variants)
        self.correct = idx['answer']
        return self

class AlgAvg(SingleChoice):
    def generate(self):
        i, j = self.rnd.pick_n(2, [ 'i', 'j', 'k', 'm' ])
        case = self.rnd.pick([
            { 'text': 'положительн', 'comp': '>' },
            { 'text': 'отрицательн', 'comp': '<' },
        ])
        correct = self.correct = self.rnd.in_range(1, 3)
        index_statement = [ '[]', 'A', i, ]
        condition_body = [
            '=', 's', index_statement if correct == 3 else [ '+', 's', index_statement ],
            '=', j, [ '+', j, 1 ],
        ]
        condition_block = [
            'if', [ case['comp'], index_statement, 0 ], condition_body,
        ]
        loop_block = [ 'for', i, 1, 'N', condition_block, ]
        after_loop_block = [] if correct == 3 else [
            '=', 's', [ '/', 's', j ] if correct == 1 else j
        ]
        code_block_parts = [ '=', 's', 0, '=', j, 0, ] + loop_block + after_loop_block
        code_block = make_block(code_block_parts)
        lang_table = table(code_block, [ [ 'Basic', 'Pascal' ], [ 'C', 'Alg' ], ])
        self.text = f'''
Дан фрагмент программы, обрабатывающей массив A из N элементов
(известно, что в массиве имеются {case['text']}ые элементы): {lang_table}
Чему будет равно значение переменной s после выполнения
данного алгоритма, при любых значениях элементов массива A?'''

        variants = [
            "Среднему арифметическому всех элементов массива A",
            f"Среднему арифметическому всех {case['text']}ых элементов массива A",
            f"Количеству {case['text']}ых элементов массива A",
            f"Значению последнего {case['text']}ого элемента массива A",
        ]
        self.set_variants(variants)
        return self

class BusStation(SingleChoice):
    def generate(self):
        towns_count = 4
        towns = self.rnd.pick_n(towns_count, [
            "ЛИСЬЕ", "СОБОЛЕВО", "ЕЖОВО", "ЗАЙЦЕВО", "МЕДВЕЖЬЕ", "ПЧЕЛИННОЕ",
        ])
        init_vertices = self._random_routes(self.rnd.in_range(6, 10), towns_count)
        graph = [ [ None for _ in range(towns_count + 1) ] for _ in range(towns_count + 1) ]
        for vertex in init_vertices:
            graph[vertex['from']][vertex['to']] = vertex
        
        graph = self._find_all_routes(graph, towns_count)

        can_go = []
        for row in graph:
            for vertex in row:
                if vertex is None:
                    continue
                if 'fin' in vertex:
                    can_go.append(vertex)
        
        way = self.rnd.pick(can_go)

        # Добавляется верный ответ. Затем, если такой существует, предыдущий, затёртый алгоритмом
        # нахождения кратчайших путей вариант. Далее выбираются маршруты, которые ведут в пункт назначения.
        # Если не набралось 4 варианта выбираются случайные ответы.
        # При добавлении проверяется уникальность ответов.
        answer = [ way['fin'] ]
        if 'last_time' in way:
            answer.append(way['pred_res'])
        for i in range(len(answer), towns_count):
            elem = graph[i][way['to']]
            if elem is None:
                continue
            if 'fin' in elem:
                if len(list(filter(lambda a: a == elem['fin'], answer))) == 0:
                    answer.append(elem['fin'])
        for i in range(len(answer), towns_count):
            elem = None
            while (True):
                elem = self.rnd.pick(can_go)
                if len(list(filter(lambda a: a == elem['fin'], answer))) == 0:
                    break
            answer.append(elem['fin'])

        self.text = self._gen_schedule_text(way, towns, init_vertices)
        self.set_variants([ self._stime(v) for v in answer ])
        return self

    def _gen_schedule_text(self, way: dict, towns: dict, init_vertices: list) -> str:
        start_time = self._stime(5 * self.rnd.in_range(0, int(way['start'] / 5)))
        text = f'''
<p>
    Путешественник пришел в {start_time} на автостанцию населенного пункта
    <strong>{towns[way['from']]}</strong> и обнаружил следующее расписание автобусов для всей районной
    сети маршрутов:
</p>
<table border="1">
    <tr>
        <th>Пункт отправления</th>
        <th>Пункт прибытия</th>
        <th>Время отправления</th>
        <th>Время прибытия</th>
    </tr>'''
        for vertex in init_vertices:
            text += "<tr>"
            text += f"<td>{towns[vertex['from']]}</td>"
            text += f"<td>{towns[vertex['to']]}</td>"
            text += f"<td>{self._stime(vertex['start'])}</td>"
            text += f"<td>{self._stime(vertex['fin'])}</td>"
            text += "</tr>\n"
        text += "</table>\n"
        text += f'''
<p>Определите самое раннее время, когда путешественник сможет оказаться в
пункте <strong>{towns[way['to']]}</strong> согласно этому расписанию.</p>'''
        return text

    def _random_routes(self, path_count: int, n: int) -> list:
        # Генерация случайных маршрутов без петель
        # |~|1|2|3| каждому целому числу от 0 до $n * ($n - 1) можно
        # |4|~|5|6| однозначно сопоставить позицию в матрице смежности
        # |7|8|~|9|
        # ...
        positions = self.rnd.pick_n(path_count, [ x for x in range(n * (n - 1)) ])
        vertices = []
        for pos in positions:
            x = pos % (n - 1)
            y = int(pos / (n - 1))
            if (x >= y):
                x += 1
            vertices.append({ 'from': x, 'to': y })
        
        time = 0
        for vertex in vertices:
            time += 5 * self.rnd.in_range(2, 20)
            vertex['start'] = time
            vertex['fin'] = time + 5 * self.rnd.in_range(1, 10)

        return vertices

    def _find_all_routes(self, graph: dict, towns_count: int) -> dict:
        # Для нахождения кратчайших расстояний используется Алгоритм Флойда — Уоршелла
        for k in range(towns_count + 1):
            for i in range(towns_count + 1):
                for j in range(towns_count + 1):
                    v, u, w = graph[i][j], graph[i][k], graph[k][j]
                    if v is None or u is None or w is None:
                        continue
                    if (not 'fin' in u) or (not 'start' in w) or (u['fin'] > w['start']):
                        continue
                    if (not 'start' in v) or ('fin' in v and 'fin' in w and v['fin'] > w['fin']):
                        if ('fin' in v):
                            v['pred_res'] = v['fin']
                        v['fin'] = w['fin']
                        v['start'] = u['start']
                        v['from'] = u['from']
                        v['to'] = w['to']
        return graph

    def _stime(self, value: int) -> str:
        return str(int(value / 60 + 7)) + ":" + "{:02d}".format(value % 60)

class CrcMessage(SingleChoice):
    def generate(self):
        lenght = 6
        words = 3
        
        def create_bits():
            new_bin = [ self.rnd.coin() for _ in range(1, lenght + 1) ]
            new_bin.append(0)
            bits = Bits().set_bin(new_bin, True)
            bits.set_bit(0, bits.xor_bits())
            return bits

        original_msg = [ create_bits() for _ in range(1, words + 1) ]
        
        def modificate_bit(bit: Bits) -> Bits:
            new_bit = bit.dup()
            flipped_bits = new_bit.flip(self.rnd.pick_n(self.rnd.in_range(1, 4), [ _ for _ in range(lenght + 1) ]))
            return flipped_bits.set_bit(self.rnd.in_range(lenght - 1), 1)
        
        received_msg = [ modificate_bit(bit) for bit in original_msg ]
        correct_idx = Bits().set_bin([ bit.xor_bits() for bit in received_msg ], True).get_dec()
        wrong_idx = self.rnd.pick_n(3, list(filter(lambda x: x != correct_idx, [ x for x in range(2 ** (words - 1) + 1) ])))
        
        original_text = [ ' '.join([ bit.get_bin() for bit in original_msg ]) ]
        received_text = [ ' '.join([ bit.get_bin() for bit in received_msg ]) ]

        zeroes = '0' * (lenght + 1)

        def idx_to_msg(arg: int) -> str:
            bits = Bits().set_size(words).set_dec(arg).get_bits()
            return ' '.join([ zeroes if bits[x] else received_msg[x].get_bin() for x in range(words) ])

        self.text = f'''
В некоторой информационной системе информация кодируется двоичными шестиразрядными словами.
При передаче данных возможны их искажения, поэтому в конец каждого слова добавляется седьмой
(контрольный) разряд таким образом, чтобы сумма разрядов нового слова, считая контрольный,
была чётной. Например, к слову 110011 справа будет добавлен 0, а к слову 101100 – 1.
После приёма слова производится его обработка. При этом проверяется сумма его разрядов,
включая контрольный. Если она нечётна, это означает, что при передаче этого слова произошёл сбой,
и оно автоматически заменяется на зарезервированное слово {zeroes}. Если она чётна, это означает,
что сбоя не было или сбоев было больше одного. В этом случае принятое слово не изменяется.
Исходное сообщение: <b>{original_text}</b> было принято в виде: <b>{received_text}</b>.
Как будет выглядеть принятое сообщение после обработки?'''

        variants = wrong_idx
        variants.insert(0, correct_idx)

        self.set_variants([ idx_to_msg(v) for v in variants ])
        return self

class InfSize(SingleChoice):
    def generate(self):
        pow = self.rnd.in_range(4, 7)
        value = 2 ** pow
        time = self.rnd.in_range(2, 11)
        self.text = f'''
Известно, что длительность непрерывного подключения к сети Интернет с помощью модема
для некоторых АТС не превышает {time} минут.
Определите максимальный размер файла (в Килобайтах),
который может быть передан за время такого подключения,
если модем передает информацию в среднем со скоростью {value} Килобит/с?'''
        time *= 60
        self.set_variants([
            2 ** (pow - 3) * time,
            2 ** pow * time,
            2 ** (pow - 3) * time / 60,
            2 ** (pow + 3) * time,
        ])
        return self

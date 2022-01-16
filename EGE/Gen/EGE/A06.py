import math
from ...GenBase import SingleChoice
from ...LangTable import unpre, table
from ...Prog import make_block

class CountBySign(SingleChoice):
    def generate(self):
        array_length = self.rnd.in_range(50, 100)
        iteration_variable = self.rnd.index_var()[0]
        c_language_comment = unpre(
            f'''/* В программе на языке Си следует считать, что массивы A и B
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
            { 'name': 'положительные', 'test': lambda x: x > 0 },
            { 'name': 'отрицательные', 'test': lambda x: x < 0 },
            { 'name': 'неотрицательные', 'test': lambda x: x >= 0 },            
        ])
        self.text = f'''Значения двух массивов A и B с индексами от 1 до {array_length}
            задаются при помощи следующего фрагмента программы: {lang_table}
            Какое количество элементов массива B[1..{array_length}] будет принимать
            {case['name']} значения после выполнения данной программы?'''

        array_B = code_block.run_val('B')
        correct = len(list(filter(lambda x: case['test'](x), array_B.values())))
        errors = [
            correct + 1, correct - 1, array_length - correct, array_length - correct + 1, array_length - correct - 1
        ]
        self.set_variants([correct] + self.rnd.pick_n(3, errors))
        return self

class FindMinMax(SingleChoice):
    def generate(self):
        array_length = self.rnd.in_range(50, 100)
        # Нужно гарантировать единственные максимум и минимум.
        value = self.rnd.in_range(array_length // 2 + 1, array_length - 1)
        iteration_variable = self.rnd.index_var()[0]
        d1 = [ '-' ] + self.rnd.shuffle([ iteration_variable, value ])
        d2, d3 = self.rnd.shuffle([
            iteration_variable, [ '-', array_length + 1, iteration_variable]
        ])
        first_loop_body = [
            '=', [ '[]', 'A', iteration_variable ], [ '*', d1, d1 ],
        ]
        second_loop_body = [
            '=', [ '[]', 'B', d2 ], [ '[]', 'A', d3 ],
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
        self.text = f'''Значения двух массивов A[1..{array_length}] и B[1..{array_length}]
            задаются с помощью следующего фрагмента программы: {lang_table}
            Какой элемент массива B будет {case['name']}?'''

        # Analoge of '<=>' operator in Perl.
        def sign(x, y):
            if x < y:
                return -1
            elif x == y:
                return 0
            else:
                return 1

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

        def filter_function(value):
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
        self.text = f'''Значения двумерного массива A размера {array_length} × {array_length} "
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

        def filter_function(value):
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
        self.text = f'''Дан фрагмент программы, обрабатывающей массив A из N элементов: {lang_table}
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
            '=', 's', index_statement if correct == 3 else [ '+', 's', index_statement],
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
        self.text = f'''Дан фрагмент программы, обрабатывающей массив A из N элементов
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
        return super().generate()

    def _gen_schedule_text(self):
        pass

    def _random_routes(self):
        pass

    def _stime(self):
        pass

class CrcMessage(SingleChoice):
    def generate(self):
        return super().generate()

class InfSize(SingleChoice):
    def generate(self):
        return super().generate()

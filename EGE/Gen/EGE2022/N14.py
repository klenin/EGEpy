from typing import List, Tuple
from ...GenBase import DirectInput, EGEError
from ... Utils import nrange
from dataclasses import dataclass
from enum import Enum


class TaskTypes(Enum):
    SumOfDigits = 0
    HowMuchDigits = 1
    HowMuchZeros = 2
    HowMuchOnes = 3
    DifferentDigits = 4

@dataclass
class TaskAttributes:
    task_type: int
    descr: list

    def split_descr(self):
        descr_s = self.descr.strip().split('<placeh>')
        return descr_s

class DirectSumDigits(DirectInput):
    # Прямое сложение в СС
    def get_random_task(self) -> TaskAttributes:
        tasks = [
            TaskAttributes(
                task_type=TaskTypes.SumOfDigits,
                descr='''Значение арифметического выражения <placeh> записали 
                в системе счисления с основанием <placeh>. 
                Найдите сумму цифр получившегося числа и запишите её в ответе в десятичной системе счисления.
                ''',
            ),
            TaskAttributes(
                task_type=TaskTypes.HowMuchDigits,
                descr='''Значение арифметического выражения: <placeh>
                –  записали в системе счисления с основанием <placeh>. 
                Сколько цифр «<placeh>» содержится в этой записи?
                ''',
            ),
            TaskAttributes(
                task_type=TaskTypes.HowMuchZeros,
                descr='''Значение арифметического выражения: <placeh>
                – записали в системе счисления с основанием <placeh>. 
                Сколько значащих нулей содержит эта запись?
                ''',
            ),
            TaskAttributes(
                task_type=TaskTypes.HowMuchOnes,
                descr='''Сколько единиц содержится в двоичной записи значения выражения <placeh>?''',
            ),
            TaskAttributes(
                task_type=TaskTypes.DifferentDigits,
                descr='''Значение выражения <placeh> записали 
                в системе счисления с основанием <placeh>. Cколько различных цифр содержит эта запись?
                ''',
            ),
        ]
        task = self.rnd.pick(tasks)
        return task

    @staticmethod
    def _pow_to_str(pow: int):
        return f'<sup>{pow}</sup>'

    @staticmethod
    def _get_sum_digits(example: int, base: int) -> int:
        s = 0
        while example > 0:
            s += example % base
            example = example // base
        return s

    @staticmethod
    def _get_count_given_digit(example: int, base: int, digit: int) -> int:
        s = 0
        while example > 0:
            if example % base == digit:
                s += 1
            example = example // base
        return s

    @staticmethod
    def _get_different_digits(example: int, base: int) -> int:
        s = set()
        while example > 0: 
            s.update(example % base)
            example = example // base
        return len(s)

    def _transform_power_term_to_str(self, base:int, pow_i:int) -> str:
        if pow_i == 1:
            term_str = f"{base}"
        elif pow_i == 0:
            term_str = "1"
        else:
            shift = self.rnd.in_range(2, min(4, pow_i))
            if pow_i - shift <= 1:
                term_str = f'{base}{self._pow_to_str(pow_i)}'
            else:
                if pow_i % shift == 0:
                    term_str = f'{base**shift}{self._pow_to_str(pow_i // shift)}'
                else:
                    term_str = f'{base**shift}*{base}{self._pow_to_str(pow_i - shift)}'
            
        return term_str

    def _create_expression(self, base: int, n_terms: int, pows: List[int]) -> Tuple[int, str]:

        expr_str = self._transform_power_term_to_str(base, pows[0])
        expr = base**pows[0]

        for i in range(1, n_terms):
            sign = self.rnd.pick(['+', '-'])
            expr_str += sign
            expr_str += self._transform_power_term_to_str(base, pows[i])
                
            if sign == '+':
                expr += base**pows[i]
            else:
                expr -= base**pows[i]

        return expr, expr_str

    def generate(self):

        task = self.get_random_task()
        n_terms = self.rnd.pick([3, 4, 5, 6])
        base = self.rnd.in_range(2, 8)
        pows = sorted(self.rnd.pick_n(n_terms, nrange(6, 32)), reverse=True)
        pows[-1] = self.rnd.pick([0, 1, 2, 3])

        if task.task_type == TaskTypes.SumOfDigits:
            expr, expr_str = self._create_expression(base, n_terms, pows)
            answer = self._get_sum_digits(expr, base)
            descr = task.split_descr()
            full_descr = descr[0] + expr_str + descr[1] + str(base) + descr[2]

        elif task.task_type == TaskTypes.HowMuchDigits:
            digit = self.rnd.in_range(0, base)
            expr, expr_str = self._create_expression(base, n_terms, pows)
            answer = self._get_count_given_digit(expr, base, digit)
            descr = task.split_descr()
            full_descr = descr[0] + expr_str + descr[1] + str(base) + descr[2]
            full_descr += str(digit) + descr[3]

        elif task.task_type == TaskTypes.HowMuchZeros:
            expr, expr_str = self._create_expression(base, n_terms, pows)
            answer = self._get_count_given_digit(expr, base, digit=0)
            descr = task.split_descr()
            full_descr = descr[0] + expr_str + descr[1] + str(base) + descr[2]

        elif task.task_type == TaskTypes.HowMuchOnes:
            expr, expr_str = self._create_expression(2, n_terms, pows)
            answer = self._get_count_given_digit(expr, base=2, digit=1)
            descr = task.split_descr()
            full_descr = descr[0] + expr_str + descr[1]

        elif task.task_type == TaskTypes.DifferentDigits:
            expr, expr_str = self._create_expression(base, n_terms, pows)
            answer = self._get_different_digits(expr, base)
            descr = task.split_descr()
            full_descr = descr[0] + expr_str + descr[1] + str(base) + descr[2]
        else:
            raise EGEError("`task_type` is not valid")

        self.text = full_descr
        self.correct = answer
        self.accept_number()
        return self


# class BaseDetermination(DirectInput):
#     """Определение основания"""

#     def get_random_task(self):
#         pass

#     def generate(self):
#         pass
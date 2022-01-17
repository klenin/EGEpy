# Copyright © 2010-2015 Alexander S. Klenin
# Copyright © 2011 V. Kevroletin
# Copytight © 2022 Vladimir K. Glushkov, glushkov.vk@students.dvfu.ru
# Licensed under GPL version 2 or later.
import math
import string

import EGE.LangTable
import EGE.Prog
from EGE.GenBase import DirectInput, EGEError
from EGE.RussianModules.NumText import num_text


class IdentifyLetter(DirectInput):
    """
    Генерация задания B8 "Определить n-й символ в строке, созданной по определённым правилам"
    """
    def generate(self):
        n = self.rnd.in_range(6, 10)
        dn = self.rnd.in_range(1, n - 1)
        dx = self.rnd.in_range(1, n - dn)

        self.text = f"""
Строки (цепочки символов латинских букв) создаются по следующему правилу.
Первая строка состоит из одного символа — латинской буквы «A». Каждая из
последующих цепочек создается такими действиями: в очередную строку
сначала записывается буква, чей порядковый номер в алфавите
соответствует номеру строки (на <em>i</em>-м шаге пишется <em>i</em>-я буква алфавита), к ней
слева дважды подряд приписывается предыдущая строка.
Вот первые 4 строки, созданные по этому правилу:
<ol>
<li>A</li>
<li>AAB</li>
<li>AABAABC</li>
<li>AABAABCAABAABCD</li>
</ol>
<p><i><b>Латинский алфавит (для справки)</b></i>: ABCDEFGHIJKLMNOPQRSTUVWXYZ</p>
Имеется задание:
«Определить символ, стоящий в <em>n</em>-й строке на позиции
<strong>2<sup><em>n</em>−{dn}</sup> − {dx}</strong>, считая от
левого края цепочки».
<br/>Выполните это задание для <strong><em>n</em> = {n}</strong>"""
        self.correct = string.ascii_uppercase[n - dn - dx]
        return self

class FindCalcSystem(DirectInput):
    """
    Генератор B08 FindCalcSystem - указать систему счисления, в которую перевели число, по длине результата и последней цифре.
    Кевролетин В.В.
    Выбираются параметры - число(10 .. 100) и основание системы исчисления (2 .. 9)
    Перебором проверяется, есть ли другие системы исчисления, в которых результат имеет столько же цифр
    и такую же последнюю цифру. Если друга система счисления есть - параметры генерируются заново.
    """
    @staticmethod
    def _len_last(num: int, base: int) -> tuple[int, int]:
        if num != 0:
            return math.ceil(math.log(num) / math.log(base)), num % base
        return 0, 0

    def _check_uniq(self, num: int, base: int) -> bool:
        len, last = self._len_last(num, base)
        len2, base2 = len - 1, 1
        while len2 < len:
            base2 += 1
            if base2 == base:
                continue
            len2, last2 = self._len_last(num, base2)
            if len2 == len and last2 == last:
                return False
        return True

    def generate(self):
        num, base = self.rnd.in_range(10, 99), self.rnd.in_range(2, 9)
        while not self._check_uniq(num, base):
            num, base = self.rnd.in_range(10, 99), self.rnd.in_range(2, 9)

        len, last = self._len_last(num, base)
        len_text = num_text(len, [ 'цифру', 'цифры', 'цифр' ])
        self.text = f"""
Запись числа {num}<sub>10</sub> в системе счисления с 
основанием <em>N</em> оканчивается на {last} и содержит {len_text}. 
Чему равно основание этой системы счисления <em>N</em>?'"""
        self.correct = base
        self.accept_number()
        return self

class FirstSumDigits(DirectInput):
    """
    Вариант задания B8  Описание задания: алгоритм, дающий на выход несколько чисел.
    """
    def generate(self):
        a = self.rnd.pick([ 2, 4 ])
        b = self.rnd.in_range(1, a * 9)
        maximal = bool(self.rnd.coin())

        sum_digits = b
        answer = []
        if maximal:
            while sum_digits > 9:
                sum_digits -= 9
                answer.append(9)
            answer.append(sum_digits)
            answer += [ 0 ] * (a - len(answer))
        else:
            while sum_digits > 10:
                sum_digits -= 9
                answer.insert(0, 9)
            if a > len(answer) + 1:
                answer.insert(0, sum_digits - 1)
                answer = [ 0 ] * (a - len(answer) - 1) + answer
                answer.insert(0, 1)
            else:
                answer.insert(0, sum_digits)

        x = int(''.join(list(map(str, answer))))

        block = EGE.Prog.make_block([
            '=', 'a', 0,
            '=', 'b', 0,
            'while', [ '>', 'x', 0 ], [
                '=', 'a', [ '+', 'a', 1 ],
                '=', 'b', [ '+', 'b', [ '%', 'x', 10 ] ],
                '=', 'x', [ '//', 'x', 10 ],
            ],
        ])

        d = { 'x': x }
        block.run(d)
        if d['a'] != a or d['b'] != b:
            raise EGEError(f"wrong {maximal} x={x} a={a}, b={b}")
        d = { 'x': x + (9 if maximal else -9) }
        block.run(d)

        if d['a'] == a and d['b'] == b:
            raise EGEError(f"not last {maximal} x={x} a={a}, b={b}")

        lt = EGE.LangTable.table(block, [ [ 'Basic', 'Alg' ], [ 'Pascal', 'C' ] ])
        self.text = f"""
Ниже на 4-х языках записан алгоритм. Получив на вход число x, этот алгоритм печатает 
два числа a и b.  Укажите {'наибольшее' if maximal else 'наименьшее'} из таких чисел x, при вводе которых алгоритм 
печатает сначала {a}, а потом {b}. {lt}"""
        self.correct = x
        self.accept_number()
        return self

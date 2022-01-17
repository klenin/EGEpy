# Copyright © 2010-2015 Alexander S. Klenin
# Copyright © 2011 V. Kevroletin
# Copytight © 2022 Vladimir K. Glushkov, glushkov.vk@students.dvfu.ru
# Licensed under GPL version 2 or later.
import string
import math

from EGE.GenBase import DirectInput
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
    def __len_last(self, num: int, base: int) -> tuple[int, int]:
        if num != 0:
            return math.ceil(math.log(num) / math.log(base)), num % base
        return 0, 0

    def __check_uniq(self, num: int, base: int) -> bool:
        len, last = self.__len_last(num, base)
        len2, base2 = len - 1, 1
        while len2 < len:
            base2 += 1
            if base2 == base:
                continue
            len2, last2 = self.__len_last(num, base2)
            if len2 == len and last2 == last:
                return False
        return True

    def generate(self):
        num, base = self.rnd.in_range(10, 99), self.rnd.in_range(2, 9)
        while not self.__check_uniq(num, base):
            num, base = self.rnd.in_range(10, 99), self.rnd.in_range(2, 9)

        len, last = self.__len_last(num, base)
        len_text = num_text(len, [ 'цифру', 'цифры', 'цифр' ])
        self.text = f"""
Запись числа {num}<sub>10</sub> в системе счисления с 
основанием <em>N</em> оканчивается на {last} и содержит {len_text}. 
Чему равно основание этой системы счисления <em>N</em>?'"""
        self.correct = base
        self.accept_number()
        return self

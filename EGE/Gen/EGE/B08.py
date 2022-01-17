# Copyright © 2010-2015 Alexander S. Klenin
# Copyright © 2011 V. Kevroletin
# Copytight © 2022 Vladimir K. Glushkov, glushkov.vk@students.dvfu.ru
# Licensed under GPL version 2 or later.
import string

from EGE.GenBase import DirectInput

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

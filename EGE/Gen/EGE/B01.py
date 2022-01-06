import math
from dataclasses import dataclass

from .A01 import Recode, FromTo, bits_or_bytes, recode_get_encodings

from ...GenBase import DirectInput
from ...Random import Random
from ...RussianModules.NumText import num_bits, num_bytes, num_by_words, num_by_words_text

class Recode2(DirectInput):

    def generate(self):
        delta = self.rnd.pick([8, 16, 32] + [i * 10 for i in range(1, 11)])
        dir_ = recode_get_encodings(self.rnd, self.rnd.coin(), ['увеличилось', 'уменьшилось'])
        ans_in_bytes = self.rnd.coin()
        delta_text = bits_or_bytes(self.rnd, delta)
        self.text = f"""
Автоматическое устройство осуществило перекодировку информационного
сообщения на русском языке длиной в $delta символов, первоначально
записанного в {dir_.from_}, в {dir_.to}. На сколько {delta_text}.
{dir_.change} длина сообщения? В ответе запишите только число."""
        self.correct = delta if ans_in_bytes else delta * 8
        self.accept_number()

class Direct(DirectInput):

    def generate(self):
        sig_n = self.rnd.in_range(2, 5)
        sig_text = num_by_words(sig_n, 0, "genitive")
        sec_n = self.rnd.in_range(2, 5)
        sec_text = num_by_words_text(
            sec_n, 1, 'nominative',
            "секунду секунды секунд".split()
        )
        self.text = f"""
Некоторое сигнальное устройство за одну секунду передает один из 
{sig_text} сигналов. Сколько различных сообщений длиной в {sec_text} 
можно передать при помощи этого устройства?"""
        self.correct = math.pow(sig_n, sec_n)
        self.accept_number()


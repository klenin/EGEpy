from dataclasses import dataclass

from ...GenBase import SingleChoice
from ...Random import Random
from ...Russian.NumText import num_bits, num_bytes

def bits_or_bytes(rnd: Random, n: int):
    return num_bytes(n) if rnd.coin() else num_bits(n * 8)

@dataclass
class FromTo:
    from_: str; to: str; change: str = None

class Recode(SingleChoice):

    def _recode_get_encodings(self, change, txts):
        big = self.rnd.pick([
            FromTo('16-битной кодировке UCS-2', '16-битную кодировку UCS-2'),
            FromTo('2-байтном коде Unicode', '2-байтный код Unicode'),
        ]);
        little = self.rnd.pick([
          FromTo('8-битной кодировке КОИ-8', '8-битную кодировке КОИ-8'),
        ])
        return FromTo(
            (big if change else little).from_,
            (little if change else big).to,
            change = txts[change])

    def generate(self):
        delta = self.rnd.pick([ 8, 16, 32 ] + [ i * 10 for i in range (1, 11) ])
        dir_ = self._recode_get_encodings(self.rnd.coin(), [ 'увеличилось', 'уменьшилось' ])
        delta_text = bits_or_bytes(self.rnd, delta)
        self.text = f"""
Автоматическое устройство осуществило перекодировку информационного сообщения,
первоначально записанного в {dir_.from_}, в {dir_.to}.
При этом информационное сообщение {dir_.change} на {delta_text}.
Какова длина сообщения в символах?
"""
        self.set_variants([ delta * 8, delta, delta // 2, delta * 16 ])
        self.correct = 1
        return self

@dataclass
class NameSize:
    name: str; size: str

class Simple(SingleChoice):

    def generate(self):
        enc = self.rnd.pick([
            NameSize('UCS-2', 2),
            NameSize('КОИ-8', 1),
            NameSize('CP1251', 1),
        ])
        size_names = [
            [ '1 байтом', '8 битами' ],
            [ '2 байтами', '16 битами' ],
        ]
        size_name = self.rnd.pick(size_names[enc.size - 1])
        text = self.rnd.pick([
            'Известно, что Слоны в диковинку у нас.',
            'У сильного всегда бессильный виноват.',
            'Попрыгунья Стрекоза лето красное пропела.',
        ])
        self.text = f"""
В кодировке {enc.name} каждый символ кодируется {size_name}.
Определите объём следующего предложения в данном представлении: <b>{text}</b>.
"""
        len_ = len(text)
        len_nosp = len(text.replace(' ', ''));
        self.set_variants([
            bits_or_bytes(self.rnd, i) for i in [ len_, 2 * len_, len_ // 8, len_nosp ] ])
        self.correct = enc.size - 1
        return self

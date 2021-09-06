from dataclasses import dataclass
from math import ceil, log

from ...GenBase import SingleChoice
from ...Random import Random
from ...Russian.NumText import bits_and_bytes, num_bits, num_bytes, num_text
from ...Html import *

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
        passed_text = num_text(passed, flavour.forms);
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
        self.result = [ num_bytes(v * self.items_cnt) for v in variants | { len_ } ];

    def _gen_text(self):
        number = dict(short='номер', forms=[ 'номерa', 'номеров', 'номеров' ])
        obj_name = self.rnd.pick([
            NumberType(long_='автомобильный номер', **number),
            NumberType(long_='телефонный номер', **number),
            NumberType(long_='почтовый индекс', short='индекс', forms=[ 'индекса', 'индексов', 'индексов' ]),
            NumberType(long_='почтовый адрес', short='адрес', forms=[ 'адреса', 'адресов', 'адресов' ]),
            NumberType(long_='номер медицинской страховки', **number),
        ])
        items_cnt_text = num_text(self.items_cnt, obj_name.forms);
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

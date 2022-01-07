from ...GenBase import SingleChoice
from ...Bits import Bits
from ...RussianModules.NumText import num_text
from ...Russian import join_comma_and
from .A02 import CarNumbers


class VariableLength(SingleChoice):
    def generate(self):
        code = {'А': '00', 'Б': '11', 'В': '010', 'Г': '011'}
        letters = list(code.keys())
        symt = join_comma_and(letters)
        codet = ', '.join(f"{letter} - {code.get(letter)}" for letter in letters)

        while True:
            msg = [self.rnd.pick(letters) for _ in range(6)]
            bs = Bits().set_bin(''.join(code[i] for i in msg))
            bad_bs = Bits().set_bin(''.join("{:03d}".format(int(code[i])) for i in msg))
            if bs.get_oct() == bad_bs.get_oct():
                break

        msgt = ''.join(msg)
        c = 'А'
        bad_letters = {}
        for letter in letters:
            bad_letters[letter] = c
            c = chr(ord(c) + 1)
        bads = ''.join(bad_letters[i] for i in msg)

        self.text = f'''Для передачи по каналу связи сообщения, состоящего только из 
символов {symt}, используется неравномерный (по длине) код: {codet}. 
Через канал связи передаётся сообщение: {msgt}. 
Закодируйте сообщение данным кодом. Полученную двоичную последовательность переведите в восьмеричный вид.'''

        self.set_variants([bs.get_oct(), bs.get_hex(), bad_bs.get_oct(), bads])
        return self


class FixedLength(SingleChoice):
    def fixed_hex(self, s: list):
        return Bits().set_bin(''.join(s)).get_hex()

    def generate(self):
        code = {'А': '00', 'Б': '01', 'В': '10', 'Г': '11'}
        letters = list(code.keys())
        symt = join_comma_and(letters)

        msg = self.rnd.shuffle([*self.rnd.pick_n(2, letters), *[self.rnd.pick(letters) for i in range(2)]])
        msgt = ''.join(msg)

        good = self.fixed_hex([code[i] for i in msg])
        bad = [
            self.fixed_hex([f'00{code[i]}' for i in msg]),
            self.fixed_hex([f'{code[i]}00' for i in msg]),
            None
        ]

        while True:
            bad[2] = self.fixed_hex([code[i] for i in self.rnd.shuffle(msg)])
            if bad[2] != good:
                break

        self.text = f'''Для кодирования букв {symt} решили использовать двухразрядные 
последовательные двоичные числа (от 00 до 11, соответственно). 
Если таким способом закодировать последовательность символов {msgt} и 
записать результат в шестнадцатеричной системе счисления, то получится'''

        self.set_variants([good, *bad])
        return self


class PasswordLength(SingleChoice):
    def generate(self):
        car_n = CarNumbers(self.rnd)
        car_n.case_sensitive = 1
        car_n.sym_cnt = self.rnd.in_range(1, 20)
        car_n.items_cnt = self.rnd.in_range(1, 10) * 10
        car_n._make_alphabet()
        car_n._gen_task()

        fmt = '''Для регистрации на сайте некоторой страны пользователю требуется придумать пароль.
Длина пароля – ровно {}. В качестве символов используются {}.
Под хранение каждого такого пароля на компьютере отводится минимально возможное и
одинаковое целое количество байтов, при этом используется посимвольное кодирование
и все символы кодируются одинаковым и минимально возможным количеством битов.
Определите объём памяти, который занимает хранение {}.'''

        self.text = fmt.format(num_text(car_n.sym_cnt, ['символ', 'символа', 'символов']),
                               car_n.alph_text,
                               num_text(car_n.items_cnt, ['пароля', 'паролей', 'паролей']))
        self.set_variants(car_n.result)
        return self

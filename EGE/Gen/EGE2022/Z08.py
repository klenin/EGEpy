from EGE import Random
from ...GenBase import DirectInput
from ...RussianModules.NumText import num_bits, num_text
from math import ceil, log, log2
from string import ascii_uppercase

class CellEncoding(DirectInput):
    def _resolve(self, q):
        return ceil(log(q) / log(2))


class ChessCellEncoding(CellEncoding):
    def generate(self):
        cols = self.rnd.in_range(3, 32)
        rows = cols
        self.correct = self._resolve(rows * cols)
        self.text = f"Шахматная доска состоит из {cols} столбцов и {rows} строк. Какое минимальное количество бит потребуется для кодирования координат одной шахматной клетки?"

        return self


class PositiveInts(CellEncoding):
    def generate(self):
        n = self.rnd.in_range(2, 1024)
        self.correct = self._resolve(n - 1)
        self.text = f"Какое минимальное количество бит потребуется для кодирования целых положительных чисел, меньших {n}?"

        return self


class TicTacToe(CellEncoding):
    def generate(self):
        cols = self.rnd.in_range(3, 32)
        rows = cols
        self.correct = self._resolve(cols * rows)
        self.text = f"Двое играют в «крестики-нолики» на поле {cols} на {rows} клетки. Какое количество информации (в битах) получил второй игрок, узнав ход первого игрока?"

        return self


class BlackWhiteBalls(DirectInput):
    def generate(self):
        prob_inverse = 2 ** self.rnd.in_range(2, 10)
        black = self.rnd.in_range(2, 10)
        white = prob_inverse * black - black

        self.correct = ceil(log2(prob_inverse))
        self.text = f"В корзине лежат {black} черных шаров и {white} белых. Сколько бит информации несет сообщение о том, что достали черный шар?"

        return self


class ShannonProb(DirectInput):
    def _get_condition(self):
        bits = self.rnd.in_range(1, 10)
        num = self.rnd.in_range(bits ** 2, 1024)

        while num % (bits ** 2) != 0:
            print(num)
            num -= 1

        return bits, num, ceil(num / bits ** 2)


class Pencils(ShannonProb):
    def _pencils_to_text(self, n):
        return num_text(n, ['цветной карандаш', 'цветных карандаша', 'цветных карадашей'])

    def generate(self):
        bits, num, self.correct = self._get_condition()
        self.text = f"В коробке лежат {self._pencils_to_text(num)}. Сообщение о том, что достали белый карандаш, несет {num_bits(bits)} информации. Сколько белых карандашей было в коробке?"

        return self


class VasyaMarks(ShannonProb):
    def _marks_to_text(self, n):
        return num_text(n, ['оценку', 'оценки', 'оценок'])

    def generate(self):
        bits, num, self.correct = self._get_condition()
        self.text = f"За четверть Василий Пупкин получил {num} оценок. Сообщение о том, что он вчера получил четверку, несет {num_bits(bits)} информации. Сколько четверок получил Василий за четверть?"

        return self


def is_int(n):
    return int(n) == float(n)


class BlackWhiteBalls2(DirectInput):
    def _balls_to_text(self, n):
        return num_text(n, ['черный шар', 'черных шара', 'черных шаров'])

    def generate(self):
        bits = self.rnd.in_range(2, 5)
        num = self.rnd.in_range(bits ** 2 + 10, 256)

        while not is_int((num * 2 ** bits) / (2 ** bits - 1)):
            num += 1
        self.correct = ceil((num * 2 ** bits) / (2 ** bits - 1))
        self.text = f"В корзине лежат черные и белые шары. Среди них {self._balls_to_text(num)}. Сообщение о том, что достали белый шар, несет {num_bits(bits)} информации. Сколько всего шаров в корзине?"

        return self


class Pencils2(DirectInput):
    def _pencils_to_text(self, n):
        return num_text(n, ['карандаш', 'карандаша', 'карадашей'])

    def generate(self):
        bits = self.rnd.in_range(2, 5)
        num = self.rnd.in_range(bits ** 2 + 10, 256)

        while not is_int((num * 2 ** bits - num) / 2 ** bits):
            num += 1
        self.correct = ceil((num * 2 ** bits - num) / 2 ** bits)
        self.text = f"В закрытом ящике находится {self._pencils_to_text(num)}, некоторые из них синего цвета. Наугад вынимается один карандаш. Сообщение «этот карандаш – НЕ синий» несёт {num_bits(bits)} информации. Сколько синих карандашей в ящике?"

        return self


class WordCount(DirectInput):
    def _word_size_to_text(self, n):
        text = ['трехбуквенных', 'четырехбуквенных', 'пятибуквенных', 'шестибуквенных', 'семибуквенных']

        return text[n - 3]

    def _get_alphabet(self, n):
        return ', '.join(list(ascii_uppercase[0:n]))

    def _get_text(self, n, m):
        v = self.rnd.in_range(1, 2)
        if v == 1:
            return f"Некоторый алфавит содержит {num_text(m, ['', 'различных символа', 'различных символов'])}. Сколько {self._word_size_to_text(n)} слов можно составить из символов этого алфавита, если символы в слове могут повторяться?"
        if v == 2:
            return f"Сколько слов длины {n} можно составить из букв {self._get_alphabet(m)}? Каждая буква может входить в слово несколько раз."

    def generate(self):
        n = self.rnd.in_range(3, 7)
        m = self.rnd.in_range(3, 5)

        self.correct = m ** n
        self.text = self._get_text(n, m)

        return self


class WordCount2(DirectInput):
    def _alphabet_size_to_text(self, n):
        text = [
            'трехбуквенном алфавите {A, B, C}',
            'четырехбуквенном алфавите {A, B, C, D}',
            'пятибуквенном алфавите {A, B, C, D, E}',
        ]

        return text[n - 3]

    def _len_to_text(self, n):
        text = ['одного', 'двух', 'трех', 'четырех', 'пяти']

        return text[n - 1]

    def generate(self):
        len_from = self.rnd.in_range(1, 3)
        len_to = self.rnd.in_range(len_from + 1, 5)
        alphabet_size = self.rnd.in_range(3, 5)

        self.correct = sum([alphabet_size ** n for n in range(len_from, len_to + 1)])
        self.text = f"Сколько есть различных символьных последовательностей длины от {self._len_to_text(len_from)} до {self._len_to_text(len_to)} в {self._alphabet_size_to_text(alphabet_size)}?"

        return self

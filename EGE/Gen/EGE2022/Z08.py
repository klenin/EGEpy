from ...GenBase import DirectInput
from ...RussianModules.NumText import num_bits, num_text
from math import ceil, log, log2


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

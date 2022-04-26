from ...GenBase import DirectInput
from ...RussianModules.NumText import num_bits, num_text
from math import ceil, log, log2


class CellEncoding(DirectInput):
    def _resolve(self, q):
        return ceil(log(q) / log(2))


class ChessCellEncoding(CellEncoding):
    def generate(self):
        cols = self.rnd.in_range(3, 33)
        rows = cols
        self.correct = self._resolve(rows * cols)
        self.text = f"Шахматная доска состоит из {cols} столбцов и {rows} строк. Какое минимальное количество бит потребуется для кодирования координат одной шахматной клетки?"

        return self


class PositiveInts(CellEncoding):
    def generate(self):
        n = self.rnd.in_range(2, 1025)
        self.correct = self._resolve(n - 1)
        self.text = f"Какое минимальное количество бит потребуется для кодирования целых положительных чисел, меньших {n}?"

        return self


class TicTacToe(CellEncoding):
    def generate(self):
        cols = self.rnd.in_range(3, 33)
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
        num = self.rnd.in_range(bits ** 2, 1025)

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

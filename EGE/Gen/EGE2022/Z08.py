from EGE import Random, Russian
from ...GenBase import DirectInput
from ...RussianModules.NumText import num_bits, num_text
from math import ceil, log, log2, factorial
from string import ascii_uppercase
from EGE.Gen.EGE.B04 import LexOrder, Bulbs, SignalRockets, LetterCombinatorics


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
        return num_text(n, [ 'цветной карандаш', 'цветных карандаша', 'цветных карадашей' ])

    def generate(self):
        bits, num, self.correct = self._get_condition()
        self.text = f"В коробке лежат {self._pencils_to_text(num)}. Сообщение о том, что достали белый карандаш, несет {num_bits(bits)} информации. Сколько белых карандашей было в коробке?"

        return self


class VasyaMarks(ShannonProb):
    def _marks_to_text(self, n):
        return num_text(n, [ 'оценку', 'оценки', 'оценок' ])

    def generate(self):
        bits, num, self.correct = self._get_condition()
        self.text = f"За четверть Василий Пупкин получил {num} оценок. Сообщение о том, что он вчера получил четверку, несет {num_bits(bits)} информации. Сколько четверок получил Василий за четверть?"

        return self


def is_int(n):
    return int(n) == float(n)


class BlackWhiteBalls2(DirectInput):
    def _balls_to_text(self, n):
        return num_text(n, [ 'черный шар', 'черных шара', 'черных шаров' ])

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
        return num_text(n, [ 'карандаш', 'карандаша', 'карадашей' ])

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
        text = [ 'трехбуквенных', 'четырехбуквенных', 'пятибуквенных', 'шестибуквенных', 'семибуквенных' ]

        return text[n - 3]

    def _get_alphabet(self, n):
        return ', '.join(list(ascii_uppercase[0:n]))

    def _get_text(self, n, m):
        v = self.rnd.coin()
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
        text = [ 'одного', 'двух', 'трех', 'четырех', 'пяти' ]

        return text[n - 1]

    def generate(self):
        len_from = self.rnd.in_range(1, 3)
        len_to = self.rnd.in_range(len_from + 1, 5)
        alphabet_size = self.rnd.in_range(3, 5)

        self.correct = sum([ alphabet_size ** n for n in range(len_from, len_to + 1) ])
        self.text = f"Сколько есть различных символьных последовательностей длины от {self._len_to_text(len_from)} до {self._len_to_text(len_to)} в {self._alphabet_size_to_text(alphabet_size)}?"

        return self


class LightPanel(DirectInput):
    def generate(self):
        first = self.rnd.in_range(5, 10)
        last = self.rnd.in_range(4, 9)
        n = first + last
        self.text = f'''На световой панели в ряд расположены {n} лампочек.
                    Каждая из первых {first} лампочек может гореть красным, жёлтым или зелёным цветом.
                    Каждая из остальных {last} лампочек может гореть одним из двух цветов — красным или белым.
                    Сколько различных сигналов можно передать с помощью панели
                    все лампочки должны гореть, порядок цветов имеет значение)?'''
        self.correct = 3 ** first * 2 ** last

        return self


class LightPanel2(DirectInput):
    def _len_to_text(self, n):
        text = [ 'одного', 'двух', 'трех', 'четырех', 'пяти' ]

        return text[n - 1]

    def generate(self):
        n = self.rnd.in_range(2, 5)
        m = self.rnd.in_range(2, 5)

        self.correct = m ** n
        self.text = f"""Световое табло состоит из {self._len_to_text(n)} светящихся элементов, каждый из которых может светиться одним 
        из {self._len_to_text(m)} различных цветов. Каждая комбинация из {self._len_to_text(n)} цветов кодирует определённый сигнал. Сколько различных 
        сигналов можно передать при помощи табло при условии, что все элементы должны светиться?"""

        return self


class WordsWithRestrictions(DirectInput):
    def _type_to_text(self, type):
        return [ 'гласной', 'согласной' ][type]

    def generate(self):
        word_length = self.rnd.in_range(3, 6)
        vowels_count = self.rnd.in_range(2, 5)
        consonants_count = self.rnd.in_range(2, 5)
        vowels = self.rnd.pick_n(vowels_count, Russian.vowels)
        consonants = self.rnd.pick_n(consonants_count, Russian.consonants)

        task_type = self.rnd.coin()
        alphabet = self.rnd.shuffle(vowels + consonants)

        if task_type == 1:
            self.correct = vowels_count * (len(alphabet)) ** (word_length - 1)
        else:
            self.correct = consonants_count * (len(alphabet)) ** (word_length - 1)
        self.text = f"""Сколько слов длины {word_length}, начинающихся с {self._type_to_text(task_type)} буквы, можно составить из букв {', '.join(alphabet)}? 
        Каждая буква может входить в слово несколько раз. Слова не обязательно должны быть осмысленными словами русского языка."""

        return self


class WordEncoding(DirectInput):
    def _type_to_text(self, type):
        return [ 'гласную', 'согласную' ][type]

    def generate(self):
        code_len = self.rnd.in_range(3, 6)
        vowels_count = self.rnd.in_range(2, 5)
        consonants_count = self.rnd.in_range(2, 5)
        vowels = self.rnd.pick_n(vowels_count, Russian.vowels)
        consonants = self.rnd.pick_n(consonants_count, Russian.consonants)

        alphabet = self.rnd.shuffle(vowels + consonants)
        banned_first_letter = self.rnd.pick(alphabet)
        type = self.rnd.coin()

        self.text = f"""Андрей составляет {code_len}-буквенные коды из букв {', '.join(alphabet)}. 
        Каждую букву можно использовать любое количество раз, при этом код не может начинаться с буквы {banned_first_letter} и должен 
        содержать хотя бы одну {self._type_to_text(type)}. Сколько различных кодов может составить Андрей?"""

        alphabet_len = len(alphabet)
        dont_start_with_banned = (alphabet_len - 1) * (code_len - 1) ** alphabet_len

        if type == 1:
            if banned_first_letter in vowels:
                first = alphabet_len - vowels_count
            else:
                first = alphabet_len - vowels_count - 1
            dont_start_with_banned_and_without_task_type = first * (code_len - 1) ** (alphabet_len - vowels_count)
        else:
            if banned_first_letter in consonants:
                first = alphabet_len - consonants_count
            else:
                first = alphabet_len - consonants_count - alphabet_len - 1
            dont_start_with_banned_and_without_task_type = first * (code_len - 1) ** (alphabet_len - consonants_count)

        self.correct = dont_start_with_banned - dont_start_with_banned_and_without_task_type

        return self


class WordEncoding2(DirectInput):
    def generate(self):
        code_len = self.rnd.in_range(3, 7)
        vowels_count = self.rnd.in_range(2, 4)
        consonants_count = code_len - vowels_count
        vowels = self.rnd.pick_n(vowels_count, Russian.vowels)
        consonants = self.rnd.pick_n(consonants_count, Russian.consonants)

        alphabet = self.rnd.shuffle(vowels + consonants)

        self.text = f"""Света составляет {code_len}-буквенные коды из букв {', '.join(alphabet)}. 
        Каждую букву нужно использовать ровно один раз, при этом нельзя ставить рядом две гласные. 
        Сколько различных кодов может составить Света?"""

        one_letter_usage = factorial(code_len)
        vowels_1_2 = vowels_count * (vowels_count - 1)
        tail = 1
        for i in range(0, code_len - 2):
            tail *= consonants_count - i

        self.correct = one_letter_usage - (vowels_1_2 * tail * (code_len - 1))

        return self

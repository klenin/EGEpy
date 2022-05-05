from EGE import Russian
from ...GenBase import DirectInput
from ...RussianModules.NumText import num_bits, num_text
from math import ceil, log, log2, factorial
from string import ascii_uppercase


class CellEncoding():
    def _resolve(self, q):
        return ceil(log(q) / log(2))


class ChessCellEncoding(DirectInput, CellEncoding):
    def generate(self):
        cols = self.rnd.in_range(3, 32)
        rows = cols
        self.correct = self._resolve(rows * cols)
        self.text = f"""
Шахматная доска состоит из {cols} столбцов и {rows} строк. 
Какое минимальное количество бит потребуется для кодирования координат одной шахматной клетки?"""
        return self


class PositiveInts(DirectInput, CellEncoding):
    def generate(self):
        n = self.rnd.in_range(2, 1024)
        self.correct = self._resolve(n - 1)
        self.text = f"Какое минимальное количество бит потребуется для кодирования целых положительных чисел, меньших {n}?"
        return self


class TicTacToe(DirectInput, CellEncoding):
    def generate(self):
        cols = self.rnd.in_range(3, 32)
        rows = cols
        self.correct = self._resolve(cols * rows)
        self.text = f"""
Двое играют в «крестики-нолики» на поле {cols} на {rows} клетки. Какое количество информации (в битах) получил 
второй игрок, узнав ход первого игрока?"""
        return self


class BlackWhiteBalls(DirectInput):
    def generate(self):
        prob_inverse = 2 ** self.rnd.in_range(2, 10)
        black = self.rnd.in_range(2, 10)
        white = prob_inverse * black - black
        self.correct = ceil(log2(prob_inverse))
        self.text = f"""
В корзине лежат {black} черных шаров и {white} белых. 
Сколько бит информации несет сообщение о том, что достали черный шар?"""
        return self


class Pencils(DirectInput):
    def _pencils_to_text(self, n):
        return num_text(n, [ 'цветной карандаш', 'цветных карандаша', 'цветных карадашей' ])

    def generate(self):
        bits = self.rnd.in_range(1, 10)
        num = self.rnd.in_range(bits ** 2, 1024)

        while num % (bits ** 2) != 0:
            num -= 1

        self.text = f"""
В коробке лежат {self._pencils_to_text(num)}. Сообщение о том, что достали белый карандаш, 
несет {num_bits(bits)} информации. Сколько белых карандашей было в коробке?"""
        self.correct = ceil(num / bits ** 2)
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
        self.text = f"""
В корзине лежат черные и белые шары. Среди них {self._balls_to_text(num)}. 
Сообщение о том, что достали белый шар, несет {num_bits(bits)} информации. 
Сколько всего шаров в корзине?"""
        self.accept_number()
        return self


class Pencils2(DirectInput):
    def _pencils_to_text(self, n):
        return num_text(n, [ 'карандаш', 'карандаша', 'карадашей' ])

    def generate(self):
        bits = self.rnd.in_range(2, 5)
        num = self.rnd.in_range(bits ** 2 + 10, 256)

        while not is_int((num * 2 ** bits - num) / 2 ** bits):
            num += 1

        self.text = f"""
В закрытом ящике находится {self._pencils_to_text(num)}, некоторые из них синего цвета. 
Наугад вынимается один карандаш. Сообщение «этот карандаш – НЕ синий» несёт {num_bits(bits)} информации. 
Сколько синих карандашей в ящике?"""
        self.correct = ceil((num * 2 ** bits - num) / 2 ** bits)
        self.accept_number()
        return self


class VasyaMarks(DirectInput):
    def _marks_to_text(self, n):
        return num_text(n, [ 'оценку', 'оценки', 'оценок' ])

    def generate(self):
        bits = self.rnd.in_range(1, 10)
        num = self.rnd.in_range(bits ** 2, 1024)

        while num % (bits ** 2) != 0:
            num -= 1

        self.text = f"""
За четверть Василий Пупкин получил {num} оценок. Сообщение о том, что он вчера получил четверку, 
несет {num_bits(bits)} информации. Сколько четверок получил Василий за четверть?"""
        self.correct = ceil(num / bits ** 2)
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
            return f"""
Некоторый алфавит содержит {num_text(m, ['', 'различных символа', 'различных символов'])}. 
Сколько {self._word_size_to_text(n)} слов можно составить из символов этого алфавита, если символы в слове могут повторяться?"""
        if v == 2:
            return f"""
Сколько слов длины {n} можно составить из букв {self._get_alphabet(m)}? 
Каждая буква может входить в слово несколько раз."""

    def generate(self):
        n = self.rnd.in_range(3, 7)
        m = self.rnd.in_range(3, 5)

        self.text = self._get_text(n, m)
        self.correct = m ** n
        self.accept_number()
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

        self.text = f"""
Сколько есть различных символьных последовательностей длины от {self._len_to_text(len_from)} до {self._len_to_text(len_to)} 
в {self._alphabet_size_to_text(alphabet_size)}?"""
        self.correct = sum([ alphabet_size ** n for n in range(len_from, len_to + 1) ])
        self.accept_number()
        return self


class LightPanel(DirectInput):
    def generate(self):
        first = self.rnd.in_range(5, 10)
        last = self.rnd.in_range(4, 9)
        n = first + last

        self.text = f"""
На световой панели в ряд расположены {n} лампочек.
Каждая из первых {first} лампочек может гореть красным, жёлтым или зелёным цветом.
Каждая из остальных {last} лампочек может гореть одним из двух цветов — красным или белым.
Сколько различных сигналов можно передать с помощью панели
все лампочки должны гореть, порядок цветов имеет значение)?"""
        self.correct = 3 ** first * 2 ** last
        self.accept_number()
        return self


class LightPanel2(DirectInput):
    def _len_to_text(self, n):
        text = [ 'одного', 'двух', 'трех', 'четырех', 'пяти' ]
        return text[n - 1]

    def generate(self):
        n = self.rnd.in_range(2, 5)
        m = self.rnd.in_range(2, 5)

        self.text = f"""
Световое табло состоит из {self._len_to_text(n)} светящихся элементов, каждый из которых может светиться одним 
из {self._len_to_text(m)} различных цветов. Каждая комбинация из {self._len_to_text(n)} цветов кодирует определённый сигнал. Сколько различных 
сигналов можно передать при помощи табло при условии, что все элементы должны светиться?"""
        self.correct = m ** n
        self.accept_number()
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

        self.text = f"""
Сколько слов длины {word_length}, начинающихся с {self._type_to_text(task_type)} буквы, можно составить из букв {', '.join(alphabet)}? 
Каждая буква может входить в слово несколько раз. Слова не обязательно должны быть осмысленными словами русского языка."""
        if task_type == 1:
            self.correct = vowels_count * (len(alphabet)) ** (word_length - 1)
        else:
            self.correct = consonants_count * (len(alphabet)) ** (word_length - 1)
        self.accept_number()
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
        task_type = self.rnd.coin()

        alphabet_len = len(alphabet)
        dont_start_with_banned = (alphabet_len - 1) * (code_len - 1) ** alphabet_len

        sound = vowels_count if task_type == 1 else consonants_count
        if banned_first_letter in (vowels if task_type == 1 else consonants):
            first = alphabet_len - sound
        else:
            first = alphabet_len - sound - 1
        dont_start_with_banned_and_without_task_type = first * (code_len - 1) ** (alphabet_len - sound)

        self.text = f"""
Андрей составляет {code_len}-буквенные коды из букв {', '.join(alphabet)}. 
Каждую букву можно использовать любое количество раз, при этом код не может начинаться с буквы {banned_first_letter} и должен 
содержать хотя бы одну {self._type_to_text(task_type )}. Сколько различных кодов может составить Андрей?"""
        self.correct = dont_start_with_banned - dont_start_with_banned_and_without_task_type
        self.accept_number()
        return self


class WordEncoding2(DirectInput):
    def generate(self):
        code_len = self.rnd.in_range(3, 7)
        vowels_count = self.rnd.in_range(2, 4)
        consonants_count = code_len - vowels_count
        vowels = self.rnd.pick_n(vowels_count, Russian.vowels)
        consonants = self.rnd.pick_n(consonants_count, Russian.consonants)

        alphabet = self.rnd.shuffle(vowels + consonants)
        one_letter_usage = factorial(code_len)
        vowels_on_start_positions = vowels_count * (vowels_count - 1)
        tail = 1
        for i in range(code_len - 2):
            tail *= consonants_count - i

        self.text = f"""
Света составляет {code_len}-буквенные коды из букв {', '.join(alphabet)}. 
Каждую букву нужно использовать ровно один раз, при этом нельзя ставить рядом две гласные. 
Сколько различных кодов может составить Света?"""
        self.correct = one_letter_usage - (vowels_on_start_positions * tail * (code_len - 1))
        self.accept_number()
        return self


class WordEncoding3(DirectInput):
    def generate(self):
        code_len = self.rnd.in_range(5, 9)
        consonants_count = self.rnd.in_range(2, 5)
        vowels_count = self.rnd.in_range(2, 4)
        vowels = self.rnd.pick_n(vowels_count, Russian.vowels)
        consonants = self.rnd.pick_n(consonants_count, Russian.consonants)

        alphabet = self.rnd.shuffle(vowels + consonants)
        one_usage_required = self.rnd.pick_n(2, alphabet)
        banned_on_start = self.rnd.pick(one_usage_required)

        alphabet_size = len(alphabet)
        n = (code_len - 1) * (alphabet_size - 2) ** (code_len - 2)
        m = ((alphabet_size - 1) * (alphabet_size - 2) ** (code_len - 2)) * (code_len - 1)

        self.text = f"""
Андрей составляет {code_len}-буквенные коды из букв {', '.join(alphabet)}. 
Буквы {one_usage_required[0]} и {one_usage_required[1]} должны встречаться в коде ровно по одному разу, при этом буква {banned_on_start} 
не может стоять на первом месте.  Остальные допустимые буквы могут встречаться произвольное количество раз или не 
встречаться совсем. Сколько различных кодов может составить Андрей?"""
        self.correct = n + m
        self.accept_number()
        return self


class WordEncoding4(DirectInput):
    def generate(self):
        code_len = self.rnd.in_range(5, 9)
        consonants_count = self.rnd.in_range(3, 5)
        vowels_count = 2
        vowels = self.rnd.pick_n(vowels_count, Russian.vowels)
        consonants = self.rnd.pick_n(consonants_count, Russian.consonants)

        alphabet = self.rnd.shuffle(vowels + consonants)
        without_consonants = consonants_count ** code_len
        only_one_vowel = code_len * consonants_count ** (code_len - 1)
        two_vowels = consonants_count ** (code_len - vowels_count) * (code_len - 1) * code_len

        self.text = f"""
Настя составляет {code_len}-буквенные коды из букв {', '.join(alphabet)}. 
Каждая допустимая гласная буква может входить в код не более одного раза. 
Сколько кодов может составить Настя?"""
        self.correct = two_vowels + only_one_vowel * 2 + without_consonants
        self.accept_number()
        return self

"""Генератор B04"""
import math

import EGE.Random
import EGE.Russian
import EGE.Prog
import EGE.ProgModules.Lang
import EGE.Html as html
import EGE.RussianModules.Animals
from EGE.RussianModules.NumText import num_by_words
from EGE.GenBase import DirectInput
from EGE.Utils import product, minmax, nrange

class ImplBorder(DirectInput):
    """
    Генерация заданий B04 типа "граничное значение в импликации"
    """
    def __make_xx(self):
        xx = self.rnd.pick_n(2, [ 'X', [ '+', 'X', 1 ], [ '-', 'X', 1 ] ])
        return [ '*', *xx ]

    def __make_side(self):
        a = self.__make_xx()
        return [
            self.rnd.pick("> < >= <=".split()),
            self.__make_xx(),
            self.rnd.in_range(30, 99)
        ]

    @staticmethod
    def __find_first(v, q: list):
        try:
            return q.index(v)
        except ValueError:
            return None

    @staticmethod
    def __find_last(v, q: list):
        try:
            return len(q) - q[:-1].index(v) - 1
        except ValueError:
            return None

    def generate(self):
        n = 15
        e = None
        values = []
        while not (1 <= sum(values) <= n) or e is None:
            e = EGE.Prog.make_expr([ '=>', self.__make_side(), self.__make_side() ])
            values = [ e.run({ 'X': i }) for i in range(n + 1) ]

        et = html.cdata(e.to_lang_named('Logic'))
        shfls = self.rnd.shuffle([ dict(
            t1='наименьшее наибольшее'.split()[i // 2],
            t2='ложно истинно'.split()[i % 2],
            v=(lambda i, v, q: self.__find_first(v, q) if i < 2 else self.__find_last(v, q))(i, i % 2, values)
        ) for i in range(4) ])
        facet = next(( el for el in shfls if 1 <= el['v'] <= n - 1 ))
        self.text = f"""
Каково {facet['t1']} целое число X, при котором {facet['t2']} высказывание {et}?"""
        self.correct = facet['v']
        self.accept_number()
        return self

class LexOrder(DirectInput):
    """
    Генератор B4 lex_order - найти n-ю строку в отсортированном списке слов, составленных из n букв.
    """
    def __next_ptrn_lex(self, ptrn: list, alph_len: int):
        i = len(ptrn) - 1
        while i > -1 and ptrn[i] == alph_len - 1:
            ptrn[i] = 0
            i -= 1
        if i > -1:
            ptrn[i] += 1
        return ( None, ptrn )[i == -1]

    def __prev_ptrn_lex(self, ptrn: list, alph_len: int):
        i = len(ptrn) - 1
        while i > -1 and not ptrn[i]:
            ptrn[i] = alph_len - 1
            i -= 1
        if i > -1:
            ptrn[i] -= 1
        return ( None, ptrn )[i == -1]

    def __ptrn_to_str(self, ptrn: list, alph: list):
        return ''.join([ alph[i] for i in ptrn ])

    def generate(self):
        alph_len = self.rnd.in_range(3, 5)
        ptrn_len = self.rnd.in_range(4, 6)
        delta = self.rnd.in_range(1, alph_len)
        alph = sorted(self.rnd.pick_n(alph_len, 'А Е И О У Э Ю Я'.split()))

        ptrn = [ alph_len - 1 ] * ptrn_len
        for _ in range(delta):
            self.__prev_ptrn_lex(ptrn, alph_len)
        self.correct = self.__ptrn_to_str(ptrn, alph)
        pos = alph_len ** ptrn_len - delta

        ptrn = [ 0 ] * ptrn_len
        ptrn_list = html.li(self.__ptrn_to_str(ptrn, alph))
        for _ in range(alph_len):
            self.__next_ptrn_lex(ptrn, alph_len)
            ptrn_list += html.li(self.__ptrn_to_str(ptrn, alph))
        ptrn_list = html.ol(ptrn_list + html.li('...'))

        alph_text = ', '.join(alph)
        self.text = f"""
Все {ptrn_len}-буквенные слова, составленные из букв {alph_text}, записаны
 в алфавитном порядке.<br/>Вот начало списка: {''.join(ptrn_list)} Запишите слово,
 которое стоит на <strong>{pos}-м месте</strong> от начала списка."""
        return self

class Morse(DirectInput):
    """
    Описание задания: сколько различных символов можно закодировать,используя код азбуки Морзе.
    """
    def generate(self):
        first = self.rnd.in_range(2, 6)
        second = self.rnd.in_range(first + 1, 10)

        self.text = f"""
Азбука Морзе позволяет кодировать символы для сообщений по радиосвязи, задавая комбинацию точек и тире.
Сколько различных символов (цифр, букв, знаков пунктуации и т.д.) можно закодировать,
используя код азбуки Морзе длиной не менее {first} и не более {second} сигналов (точек и тире)?"""

        answer = sum([ 2 ** i for i in range(first, second + 1) ])
        self.correct = answer
        self.accept_number()
        return self

class Bulbs(DirectInput):
    """
    Найти количество сигналов
    """
    def generate(self):
        count = self.rnd.in_range(3, 100)

        self.text = f"""
Световое табло состоит из лампочек. Каждая лампочка может находиться в одном из трех состояний 
(«включено», «выключено» или «мигает»). Какое наименьшее количество лампочек должно находиться 
на табло, чтобы с его помощью можно было передать {count} различных сигналов?"""

        self.correct = math.ceil(math.log(count) / math.log(3))
        self.accept_number()
        return self

class PlusMinus(DirectInput):
    def generate(self):
        num = self.rnd.in_range(5, 10)
        text_num = num_by_words(num, 0, 'nominative')

        self.text = f"""
Сколь­ко су­ще­ству­ет раз­лич­ных по­сле­до­ва­тель­но­стей из сим­во­лов «плюс» и «минус», 
дли­ной ровно в {text_num} сим­во­лов? """

        self.correct = 2 ** num
        self.accept_number()
        return self

class LetterCombinatorics(DirectInput):
    """
    Задача заключается в использовании базовых знаний из комбинаторики о вычислении размещений. За основу задачи взята задача из базы заданий ЕГЭ c сайта fipi.ru: 830B20
    """
    def generate(self):
        word_length = self.rnd.in_range(5, 7)
        vowels_count = self.rnd.in_range(1, 3)
        consonants_count = word_length - vowels_count
        vowels = self.rnd.pick_n(vowels_count, EGE.Russian.vowels)
        consonants = self.rnd.pick_n(consonants_count, EGE.Russian.consonants)

        letters = self.rnd.shuffle([ *vowels, *consonants ])

        letters = ', '.join(letters)
        self.text = f"""
Вася составляет {word_length}-буквенные слова, в которых встречаются только буквы {letters}, 
причём в каждом слове есть ровно одна гласная буква. Каждая из допустимых согласных букв может встречаться 
в кодовом слове любое количество раз или не встречаться совсем. Словом считается любая допустимая 
последовательность букв, не обязательно осмысленная. 
Сколько существует таких слов, которые может написать Вася?"""

        self.correct = word_length * vowels_count * consonants_count ** (word_length - 1)
        self.accept_number()
        return self

import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from Russian.NumText import *
else:
    from ..RussianModules.NumText import *

class Test_NumText(unittest.TestCase):

    def test_NumText(self):
        eq = self.assertEqual

        with self.assertRaises(KeyError):
            num_by_words(555, 0, 'zzz')

        eq(num_bytes(1), '1 байт', 'num_bytes 1')
        eq(num_bytes(3), '3 байта', 'num_bytes 3')
        eq(num_bytes(7), '7 байтов', 'num_bytes 7')

        eq(num_by_words(0, 0), 'ноль', 'w 0')
        eq(num_by_words(1, 1), 'одна', 'w 1')
        eq(num_by_words(22, 1), 'двадцать две', 'w 22')
        eq(num_by_words(40, 0), 'сорок', 'w 40')
        eq(num_by_words(105, 0), 'сто пять', 'w 105')
        eq(num_by_words(712, 0), 'семьсот двенадцать', 'w 712')

        eq(num_by_words(1, 1, 'genitive'), 'одной', 'w 1 g')
        eq(num_by_words(934, 0, 'genitive'), 'девятисот тридцати четырёх', 'w 1 g')

        eq(num_by_words(404, 0, 'dative'), 'четырёмстам четырём', 'w 0 d')
        eq(num_by_words(258, 0, 'instrumental'), 'двумястами пятьюдесятью восемью', 'w 0 i')
        eq(num_by_words(101, 0, 'accusative_animate'), 'сто одного', 'w 0 aa')
        eq(num_by_words(821, 0, 'prepositional'), 'восьмистах двадцати одном', 'w 0 p')

        fs = 'штуки штук штук'.split()
        t = [ num_by_words_text(n, 1, 'genitive', fs) for n in [ 1, 2, 3 ] ]
        eq(t[0], 'одной штуки', 'nwt 1')
        eq(t[1], 'двух штук', 'nwt 2')
        eq(t[2], 'трёх штук', 'nwt 3')

        fs = 'раз раза раз'.split()
        t = [ num_by_words_text(n, 0, 'nominative', fs) for n in [ 51, 22, 5 ] ]
        eq(t[0], 'пятьдесят один раз', 'nwtn 1')
        eq(t[1], 'двадцать два раза', 'nwtn 2')
        eq(t[2], 'пять раз', 'nwtn 3')


if __name__ == '__main__':
    unittest.main(verbosity=1)

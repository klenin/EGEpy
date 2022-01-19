from collections import Counter
import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from RussianModules import Animals, Names, SimpleNames
    from . import Russian
    from Random import Random
else:
    from ..RussianModules import Animals, Names, SimpleNames
    from ..Random import Random
    from .. import Russian

class Test_Random(unittest.TestCase):
    def setUp(self):
        self.rnd = Random(123)

    def test_alphabet(self):
        self.assertEqual(len(Russian.alphabet), 33, 'alphabet')

    def test_join_comma_and(self):
        eq = self.assertEqual
        eq(Russian.join_comma_and([ 'a' ]), 'a', 'join a')
        eq(Russian.join_comma_and([ 'a', 'b' ]), 'a и b', 'join a b')
        eq(Russian.join_comma_and([ 'a', 'b', 'c' ]), 'a, b и c', 'join a b c')

    def test_different_males(self):
        for i in range(5):
            n1, n2 = Names.different_males(self.rnd, 2)
            self.assertNotEqual(n1[0], n2[0], f'different_males {i + 1}')

    def test_simple_names_genitive(self):
        self.assertEqual(SimpleNames.genitive('Вий'), 'Вия', 'SimpleNames::genitive')

    def test_names_genitive(self):
        n = [['Валерий', 'Валерия'],
             ['Игорь', 'Игоря'],
             ['Альфреа', 'Альфреи'],
             ['Ядвига', 'Ядвиги'],
             ['Лука', 'Луки'],
             ['Анжелика', 'Анжелики'],
             ['Кузьма', 'Кузьмы'],
             ['Глория', 'Глории'],
             ['Лев', 'Льва'],
        ]
        for i in range(len(n)):
            self.assertEqual(Names.genitive(n[i][0]), n[i][1], f'Names::genitive {i + 1}')

    def test_names_ablative(self):
        n = [['Валерий', 'Валерием'],
             ['Игорь', 'Игорем'],
             ['Альфреа', 'Альфреей'],
             ['Ядвига', 'Ядвигой'],
             ['Лука', 'Лукой'],
             ['Анжелика', 'Анжеликой'],
             ['Кузьма', 'Кузьмой'],
             ['Глория', 'Глорией'],
             ['Лев', 'Львом'],
             ['Илья', 'Ильёй'],
             ['Наталья', 'Натальей'],
        ]
        for i in range(len(n)):
            self.assertEqual(Names.ablative(n[i][0]), n[i][1], f'Names::ablative {i + 1}')

    def test_names_dative(self):
        n = [['Валерий', 'Валерию'],
             ['Игорь', 'Игорю'],
             ['Альфреа', 'Альфрее'],
             ['Ядвига', 'Ядвиге'],
             ['Анжелика', 'Анжелике'],
             ['Кузьма', 'Кузьме'],
             ['Глория', 'Глории'],
             ['Лев', 'Льву'],
             ['Илья', 'Илье'],
             ['София', 'Софии'],
             ['Архип', 'Архипу'],
        ]
        for i in range(len(n)):
            self.assertEqual(Names.dative(n[i][0]), n[i][1], f'Names::dative {i + 1}')

    def test_animals_distinct_letters(self):
        eq = self.assertEqual
        eq(list(filter(lambda x: x == 'Лемур', Animals.distinct_letters)), [ 'Лемур' ], 'distinct_letters 1')
        eq(list(filter(lambda x: x == 'Скунс', Animals.distinct_letters)), [  ], 'distinct_letters 0')

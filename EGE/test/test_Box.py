import unittest

from EGE.Utils import Box


class Test_Box(unittest.TestCase):

    def test_init(self):
        eq = self.assertEqual

        with self.subTest(msg='Box init None'):
            box = Box()
            eq(None, box)
            eq(None, box.value)
            eq([ None ], box._value)

        with self.subTest(msg='Box init int'):
            box = Box(1)
            eq(1, box)
            eq(1, box.value)
            eq([ 1 ], box._value)

        with self.subTest(msg='Box init float'):
            box = Box(1.0)
            eq(1.0, box)
            eq(1.0, box.value)
            eq([ 1.0 ], box._value)

        with self.subTest(msg='Box init str'):
            box = Box('1')
            eq('1', box)
            eq('1', box.value)
            eq([ '1' ], box._value)

        with self.subTest(msg='Box init list'):
            seq = [ None, 1, 2.0, '3' ]
            box = Box(seq)
            eq(seq, box)
            eq(seq, box.value)
            eq([ seq ], box._value)
            eq(id(seq), id(box.value))

        with self.subTest(msg='Box init dict'):
            data = { 'name': 'Vladimir', 'age': 24, 'morale ': None }
            box = Box(data)
            eq(data, box)
            eq(data, box.value)
            eq([ data ], box._value)
            eq(id(data), id(box.value))

        with self.subTest(msg='Box init Box'):
            neq = self.assertNotEqual
            other = Box(1)
            box = Box(other)
            eq(other, box)
            eq(other.value, box.value)
            eq(other._value, box._value)
            eq(id(other.value), id(box.value))
            neq(id(other), id(box))


    def test_modify_list(self):
        eq = self.assertEqual
        with self.subTest(msg='Change from list'):
            seq = [ None, 1, 2.0, '3' ]
            box = Box(seq)

            for i in range(len(seq)):
                seq[i] = 1
            eq([ 1 for _ in seq ], seq)
            eq(seq, box)

        with self.subTest(msg='Change from Box'):
            seq = [ None, 1, 2.0, '3' ]
            box = Box(seq)

            for i in range(len(box.value)):
                box.value[i] = 1
            eq([ 1 for _ in seq ], seq)
            eq(seq, box)

    def test_change_value(self):
        eq = self.assertEqual

        with self.subTest(msg="Box change int"):
            box = Box(1)
            box += 3
            eq(4, box)
            box -= 2
            eq(2, box)
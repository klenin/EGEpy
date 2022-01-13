import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from NotationBase import *
else:
    from ..NotationBase import *


class Test_NotationBase(unittest.TestCase):
    def test_base_to_dec(self):
        eq = self.assertEqual
        eq(base_to_dec(10, '39058'), 39058, 'base_to_dec 10')
        eq(base_to_dec(2, '1111'), 15, 'base_to_dec 2')
        eq(base_to_dec(36, 'az'), 10 * 36 + 35, 'base_to_dec az')
        eq(base_to_dec(36, 'ZA'), 35 * 36 + 10, 'base_to_dec ZA')
        with self.assertRaises(ValueError):
            base_to_dec(5, '?')
        with self.assertRaises(ValueError):
            base_to_dec(5, '12345')

    def test_dec_to_base(self):
        eq = self.assertEqual
        eq(dec_to_base(10, 92384), '92384', 'dec_to_base 10')
        eq(dec_to_base(2, 31), '11111', 'dec_to_base 3')
        eq(dec_to_base(36, 10 * 36 + 35), 'AZ', 'dec_to_base AZ')


if __name__ == '__main__':
    unittest.main(verbosity=1)

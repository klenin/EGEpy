import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from Utils import *
else:
    from ..Utils import *


class Test_Utils(unittest.TestCase):
    def test_gcd(self):
        eq = self.assertEqual
        eq(gcd(0, 2), 2, 'gcd 0 2')
        eq(gcd(3, 0), 3, 'gcd 3 0')
        eq(gcd(9, 6), 3, 'gcd 3')
        eq(gcd(3, 7), 1, 'gcd 1')

    def test_product(self):
        eq = self.assertEqual
        eq(product(1, 0, 5), 0, 'product 0')
        eq(product(2, 3, 4), 24, 'product 1')


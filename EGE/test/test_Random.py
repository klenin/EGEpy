from collections import Counter
import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from Random import Random
else:
    from ..Random import Random

class Test_Random(unittest.TestCase):

    def setUp(self):
        self.rnd = Random(123)

    def char_range(a, b):
        for c in range(ord(a), ord(b) + 1):
            yield c

    def test_Random(self):
        eq = self.assertEqual

        eq(sum(1 for i in range(100) if not(0 <= self.rnd.get(10) <= 9)), 0,
            'in_range get')
        eq(sum(1 for i in range(100) if not(5 <= self.rnd.in_range(5, 11) <= 11)), 0,
            'in_range')
        self.assertIn(self.rnd.coin(), [ 0, 1 ], 'coin')

        with self.assertRaisesRegex(ValueError, '<', msg='in_range empty'):
            self.rnd.in_range(1, 0)

        eq(self.rnd.in_range(1, 2, exclude=1), 2, 'in_range exclude')
        eq(self.rnd.in_range(1, 4, exclude=[ 1, 2, 3 ]), 4, 'in_range exclude many')

        cnt = Counter()
        for _ in range(3000):
            cnt[self.rnd.in_range(1, 7, exclude=[ 1, 3, 4, 6 ])] += 1
        eq(set(cnt), { 2, 5, 7 }, 'in_range exclude historgam 1')
        eq(sum(1 for _, c in cnt.items() if abs(c - 1000) > 99), 0, 'in_range exclude historgam 2')

        eq(self.rnd.pick([ 99 ]), 99, 'pick 1')

        alph = [ chr(c) for c in range(ord('a'), ord('z') + 1) ]
        self.assertIn(self.rnd.pick(alph), alph, 'pick')

        def test_pick_n(n, msg):
            v = self.rnd.pick_n(n, alph);
            eq(len(set(v)), n, msg)
            self.assertTrue(set(v) <= set(alph), msg)
        test_pick_n(2, 'pick_n few')
        test_pick_n(25, 'pick_n many')

        a_d = [ 'a', 'b', 'c', 'd' ]
        for i in range(1, 4):
            p = self.rnd.pick(a_d)
            v = self.rnd.pick(a_d, exclude=p)
            self.assertIn(v, a_d, f"in {i}")
            self.assertNotEqual(v, p, f"out {i}")

        v = self.rnd.shuffle(alph)
        eq(set(v), set(alph), 'shuffle')

        with self.assertRaisesRegex(ValueError, 'empty', msg='pick from empty'):
            self.rnd.pick([])
        with self.assertRaisesRegex(ValueError, 'pick_n', msg='pick_n too many'):
            self.rnd.pick_n(3, [ 1, 2 ])
        with self.assertRaisesRegex(ValueError, 'exclude', msg='exclude nothing'):
            self.rnd.pick([1], exclude=1)

        eq(Random(999, 888).in_range(0, 1 << 31), 2034720810, 'stable from seed')
        #isnt(EGE::Random->new->in_range(0, 1 << 31), EGE::Random->new->in_range(0, 1 << 31), 'unique');


if __name__ == '__main__':
    unittest.main(verbosity=1)

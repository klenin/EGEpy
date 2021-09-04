import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from GenBase import *
    from Random import Random
else:
    from ..GenBase import *
    from ..Random import Random

class Test_Question(unittest.TestCase):

    def test_SingleChoice(self):
        q = SingleChoice(None, 'blabla')
        q.set_formatted_variants('%d!', [ 1, 2 ])
        self.assertEqual(q.variants, [ '1!', '2!' ])
        q.check_distinct_variants()
        q.variants.append('1!')

        with self.assertRaisesRegex(EGEError, '1!'):
            q.check_distinct_variants()

    def test_SingleChoice_shuffle(self):
        q = SingleChoice(Random(321), 'blabla', 1)
        q.variants = [ 0, 1, 2 ]
        q.shuffle_variants()
        self.assertEqual(set(q.variants), { 0, 1, 2 })
        self.assertEqual(q.variants[q.correct], 1)

if __name__ == '__main__':
    unittest.main(verbosity=1)

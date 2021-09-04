import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from Html import *
else:
    from ..Html import *

class Test_Html(unittest.TestCase):

    def test_Html(self):
        eq = self.assertEqual

        eq(tag('a', 'b'), '<a>b</a>', 'simple tag')
        eq(tag('br'), '<br/>', 'empty tag')
        eq(tag('a', [ 'b', 'c', 'd' ]), '<a>bcd</a>', 'array body tag')

        eq(tag('div', 'body', color='red'), '<div color="red">body</div>', 'simple attr')
        eq(tag('div', 'body', width='1%', height='2%'),
            '<div height="2%" width="1%">body</div>', 'multi attr')
        eq(tag('hr', width='1px'), '<hr width="1px"/>', 'empty tag attr')
        eq(div('body', width='1%'), '<div width="1%">body</div>', 'generated')


if __name__ == '__main__':
    unittest.main(verbosity=1)

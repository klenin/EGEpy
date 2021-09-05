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
        eq(row('td', [ 1, 2, 3 ]), '<tr><td>1</td><td>2</td><td>3</td></tr>', 'row')

        eq(style(font='Arial', color='black'), { 'style': 'color: black; font: Arial;' }, 'style')
        eq(style(list_style='none'), { 'style': 'list-style: none;' }, 'style _')

        eq(
            div_xy('text', 7, 8, margin=0),
            '<div style="height: 8px; margin: 0; width: 7px;">text</div>', 'div_xy')

        eq(ol_li([ 'a', 'b' ], { 'id': 'qq' }, {}), '<ol id="qq"><li>a</li><li>b</li></ol>', 'ol_li')
        eq(ul_li([ 'a', 'b' ], {}, { 'x': 'y' }), '<ul><li x="y">a</li><li x="y">b</li></ul>', 'ul_li')

        eq(code('a'), '<code>a</code>', 'code')

        eq(escape('abc def'), 'abc def', 'string with nothing to escape')
        eq(escape('<&tag&>'), '&lt;&amp;tag&amp;&gt;', 'normal html escapes')
        eq(escape(''), '', 'escape empty string')

if __name__ == '__main__':
    unittest.main(verbosity=1)

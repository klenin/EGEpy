import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from Logic import *
    from Prog import make_expr
else:
    from ..Logic import *
    from ..Prog import make_expr

class Test_Logic(unittest.TestCase):
    def test_Logic(self):
        eq = self.assertEqual

        t = (
            { 'e': 0, 'r': '0', 'c': 0 },
            { 'e': [ '&&', 1, 'a' ], 'r': '01', 'c': 1 },
            { 'e': [ '=>', 'a', 'b' ], 'r': '1011', 'c': 2 },
            { 'e': [ 'eq', 'a', 'b' ], 'r': '1001', 'c': 2 },
            { 'e': [ '^', 'a', [ '^', 'b', 'x' ] ], 'r': '01101001', 'c': 3 },
        )
        for i in t[1:]:
            eq(truth_table_string(make_expr(i['e'])), i['r'], '')

        eq(
            make_expr([ 'eq', [ '=>', 'a', 'b' ], [ '||', [ '!', 'a' ], 'b' ]]).to_lang_named('Logic', { 'html': 1 }),
            '<i>a</i> → <i>b</i> ≡ ¬ <i>a</i> ∨ <i>b</i>',
            'logic text'
        )

        eq(
            make_expr([ '**', 'a', 'b' ]).to_lang_named('Logic', { 'html': 1 }),
            '<i>a</i><sup><i>b</i></sup>',
            'logic power'
        )

        eq(
            make_expr([ '[]', 'a', [ '+', 'i', 1 ] ]).to_lang_named('Logic', { 'html': 1 }),
            '<i>a</i><sub><i>i</i> + 1</sub>',
            'logic index'
        )

        eq(make_expr([ '**', 'a', [ '+', 'i', 1 ] ]).to_lang_named('Logic'), 'a ^ (i + 1)', 'logic power without html')

        t = (
            {
                'e': 'a',
                'r': [ '!', [ '!', 'a' ] ],
            },
            {
                'e': [ '&&', 'a', 'b' ],
                'r': [ '!', [ '||', [ '!', 'a' ], [ '!', 'b' ] ] ],
            },
            {
                'e': [ '!', [ '=>', 'a', 'b' ] ],
                'r': [ '&&', 'a', [ '!', 'b' ] ],
            },
        )
        for i in t:
            e = make_expr(i['e'])
            e_text = e.to_lang_named('Pascal')
            e1 = equiv_not(e)
            # eq(e1, make_expr(i['r']), f"equiv_not {e_text}")
            eq(e1.to_lang_named('Pascal'), make_expr(i['r']).to_lang_named('Pascal'), f"equiv_not {e_text}")
            eq(truth_table_string(e), truth_table_string(e1), "tts equiv_not $e_text")


if __name__ == '__main__':
    unittest.main(verbosity=1)

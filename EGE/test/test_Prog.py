import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from Prog import *
else:
    from ..Prog import *

class Test_Prog(unittest.TestCase):

    def test_ops(self):
        eq = self.assertEqual
        t = [
            [['+', 4, 5], 9],
            [['*', 4, 5], 20],
            [['/', 4, 5], 0.8],
            [['%', 14, 5], 4],
            [['//', 14, 5], 2],
            [['<', 4, 5], 1],
            [['&', 1, 0], 0],
            [['|', 1, 0], 1],
            [['-', 4], -4],
            [['!', 0], 1],
            [['**', 2, 8], 256],
            [['&', 14, 9], 8],
            [['|', 8, 7], 15],
            [['^', 15, 4], 11],
            [55, 55],
            [lambda x: 77, 77]
        ]
        for idx, test in enumerate(t):
            eq(make_expr(test[0]).run({}), test[1], 'op ' + str(idx + 1))

    def test_black_box(self):
        eq = self.assertEqual
        eq(make_expr(lambda x: x['z'] * 2).run({'z': 9}), 18, 'black box')
        h = {'y' : 5}
        def t3(x):
            x['y'] = 6
        make_expr(t3).run(h)
        eq(h['y'], 6, 'black box assign')

    def test_not(self):
        eq = self.assertEqual
        e = make_expr(['!', ['>', 'A', 'B']])
        eq(e.to_lang_named('Basic'), 'NOT (A > B)', 'not()')
        eq(e.to_lang_named('Logic', {'html': 1}), '¬ (<i>A</i> &gt; <i>B</i>)', 'not in html logic')
        eq(e.to_lang_named('Logic'), '¬ (A > B)', 'not in logic')
        make_expr(['||', ['!', ['&&', 1, 1]], 1])

    def test_between(self):
        eq = self.assertEqual
        e = make_expr(['between', 'a', '1', ['+', '2', '5']])
        eq(e.run({'a': 3}), 1, 'between 1')
        eq(e.run({'a': 8}), 0, 'between 2')
        eq(e.to_lang_named('C'), '1 <= a && a <= 2 + 5', 'between C')
        eq(e.to_lang_named('C', {'html': 1}), '1 &lt;= a &amp;&amp; a &lt;= 2 + 5', 'between html C')
        eq(e.to_lang_named('Pascal'), 'InRange(a, 1, 2 + 5)', 'between Pascal')
        eq(e.to_lang_named('SQL'), 'a BETWEEN 1 AND 2 + 5', 'between SQL')

    def test_run(self):
        eq = self.assertEqual
        e = make_expr(['[]', 'a', 2])
        eq(e.run({'a': [i for i in range(1, 4)]}), 3, 'run []')

    def test_make_expr(self):
        eq = self.assertEqual
        e = make_expr(['+', 'a', 3])
        eq(make_expr(e), e, 'double make_expr')

    def test_vars(self):
        eq = self.assertEqual
        env = {'a_1': 2, 'a_b': 3};
        eq(make_expr('a_b').run(env), 3, 'var underline')
        eq(make_expr('a_1').run(env), 2, 'var digit');

    def test_dfs(self):
        eq = self.assertEqual
        def plus2minus(t):
            t.op = '+' if t.op == '-' else t.op
        e = make_expr(['-', ['-', 3, ['-', 2, 1]]])
        eq(e.run(None), -2, 'visit_dfs before')
        #eq(e.visit_dfs1(plus2minus).run(None), 6, 'visit_dfs after')
        #eq(e.count_if(lambda x: 1), 6, 'visit_dfs count all')
        #eq(e.count_if(lambda x: isinstance(x, Const)), 3, 'count_if')
        #eq([ e.gather_if(lambda x: isinstance(x, BinOp))],
        #[ e.arg, e.arg.right ], 'gather_if');

    def check_lang(self, lang, expr, str, name):
        eq = self.assertEqual
        eq(make_expr(expr).to_lang_named(lang), str, name)

    def check_prio_C(self, expr, str, priority):
        self.check_lang('C', expr, str, "priorities " + priority)

    def test_prio_C(self):
        self.check_prio_C(['*', ['+', 'a', 1], ['-', 'b', 2]], '(a + 1) * (b - 2)', '1')
        self.check_prio_C(['+', ['*', 'a', 1], ['/', 'b', 2]], 'a * 1 + b / 2', '2')
        self.check_prio_C(['*', 5, ['-', 'x']], '5 * - x', 'unary 1')
        self.check_prio_C(['+', 5, ['-', 'x']], '5 + - x', 'unary 2')
        self.check_prio_C(['-', ['+', 'x', 5]], '- (x + 5)', 'unary 3')
        self.check_prio_C(['+', ['-', 'x']], '+ - x', 'unary 4')

        e = ['+', ['&&', 'x', 'y']]
        self.check_lang('Pascal', e, '+ (x and y)', 'prio Pascal not')
        self.check_prio_C(e, '+ (x && y)', 'C not')
        self.check_lang('Pascal', [ '+', 'x', [ '**', 'x', 2 ] ], 'x + x ** 2', 'Pascal power')

    def test_logic_prio(self):
        eq = self.assertEqual
        e = make_expr(['&&', ['<=', 1, 'a'], ['<=', 'a', 'n']])
        eq(e.to_lang_named('C'), '1 <= a && a <= n', 'logic priorities C')
        eq(e.to_lang_named('Pascal'), '(1 <= a) and (a <= n)', 'logic priorities Pascal')

    def test_empty_block(self):
        eq = self.assertEqual
        b = make_block([], None)
        for keys in lang_names():
            eq(b.to_lang_named(keys), '', keys)

    def test_Alg_assign(self):
        eq = self.assertEqual
        b = make_block(['=', 'x', 99], None)
        eq(b.to_lang_named('Alg'), 'x := 99')
        eq(b.run_val('x'), 99)

    def test_Perl_assign(self):
        eq = self.assertEqual
        b = make_block(['=', 'x', 3, '=', 'y', 'x'], None)
        eq(b.to_lang_named('Perl'), "$x = 3;\n$y = $x;")
        eq(b.run_val('y'), 3)

    def test_run_simple(self):
        eq = self.assertEqual
        m = 5
        b = make_block(['=', 'x', ['+', m, 1]], None)
        eq(b.run_val('x'), 6)
        m = 10
        b = make_block(['=', 'x', ['+', m, 1]], None)
        eq(b.run_val('x'), 11)

    def test_text(self):
        eq = self.assertEqual
        b = make_block(['#', {'Basic': 'basic text'}], None)
        eq(b.to_lang_named('Basic'), 'basic text')
        eq(b.to_lang_named('C'), '')

    def test_Pascal(self):
        eq = self.assertEqual
        b = make_block(['=', ['[]', 'A', 2], 5], None)
        eq(b.to_lang_named('Pascal'), 'A[2] := 5;')
        #eq(b.run_val('A'), [None, None, 5])

    def test_loops(self):
        eq = self.assertEqual
        b = make_block([
                'for', 'i', 0, 4, ['=', ['[]', 'M', 'i'], 'i']
        ], None)
        p = "for i := 0 to 4 do\n  M[i] := i;"
        eq(b.to_lang_named('Pascal'), p, 'loop in Pascal')
        #eq(b.run_val('M'), [0, 1, 2, 3, 4], 'loop run')

if __name__ == '__main__':
    unittest.main(verbosity=1)

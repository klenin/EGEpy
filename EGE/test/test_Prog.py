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
            [ [ '+', 4, 5 ], 9 ],
            [ [ '*', 4, 5 ], 20 ],
            [ [ '/', 4, 5 ], 0.8 ],
            [ [ '%', 14, 5 ], 4 ],
            [ [ '//', 14, 5 ], 2 ],
            [ [ '<', 4, 5 ], 1 ],
            [ [ '&', 1, 0 ], 0 ],
            [ [ '|', 1, 0 ], 1 ],
            [ [ '-', 4 ], -4 ],
            [ [ '!', 0 ], 1 ],
            [ [ '**', 2, 8 ], 256 ],
            [ [ '&', 14, 9 ], 8 ],
            [ [ '|', 8, 7 ], 15 ],
            [ [ '^', 15, 4 ], 11 ],
            [ 55, 55 ],
            [ lambda x: 77, 77 ]
        ]
        for idx, test in enumerate(t):
            eq(make_expr(test[0]).run({}), test[1], 'op ' + str(idx + 1))
        env = { 'a': Box(2), 'b': Box(3) }
        eq(make_expr('b').run(env), 3, 'basic env 1')
        eq(make_expr([ '*', 'a', [ '+', 'b', 7 ] ]).run(env), 20, 'basic env 2')

    def test_black_box(self):
        eq = self.assertEqual
        eq(make_expr(lambda x: x['z'] * 2).run({ 'z': Box(9) }), 18, 'black box')
        h = {'y' : Box(5)}
        def t3(x):
            x['y'] = 6
        make_expr(t3).run(h)
        eq(h['y'], 6, 'black box assign')

    def test_not(self):
        eq = self.assertEqual
        e = make_expr([ '!', [ '>', 'A', 'B' ] ])
        eq(e.to_lang_named('Basic'), 'NOT (A > B)', 'not()')
        eq(e.to_lang_named('Logic', { 'html': 1 }), '¬ (<i>A</i> &gt; <i>B</i>)', 'not in html logic')
        eq(e.to_lang_named('Logic'), '¬ (A > B)', 'not in logic')
        make_expr([ '||', [ '!', [ '&&', 1, 1 ] ], 1 ])

    def test_between(self):
        eq = self.assertEqual
        e = make_expr(['between', 'a', '1', ['+', '2', '5']])
        eq(e.run({ 'a': Box(3) }), 1, 'between 1')
        eq(e.run({ 'a': Box(8) }), 0, 'between 2')
        eq(e.to_lang_named('C'), '1 <= a && a <= 2 + 5', 'between C')
        eq(e.to_lang_named('C', {'html': 1}), '1 &lt;= a &amp;&amp; a &lt;= 2 + 5', 'between html C')
        eq(e.to_lang_named('Pascal'), 'InRange(a, 1, 2 + 5)', 'between Pascal')
        eq(e.to_lang_named('SQL'), 'a BETWEEN 1 AND 2 + 5', 'between SQL')

    def test_run(self):
        eq = self.assertEqual
        e = make_expr(['[]', 'a', 2])
        eq(e.run({ 'a': Box([ i for i in range(1, 4) ]) }), 3, 'run []')

    def test_make_expr(self):
        eq = self.assertEqual
        e = make_expr([ '+', 'a', 3 ])
        eq(make_expr(e), e, 'double make_expr')

    def test_vars(self):
        eq = self.assertEqual
        env = { 'a_1': Box(2), 'a_b': Box(3) }
        eq(make_expr('a_b').run(env), 3, 'var underline')
        eq(make_expr('a_1').run(env), 2, 'var digit')

    def test_dfs(self):
        eq = self.assertEqual
        def plus2minus(t):
            if hasattr(t, 'op') and t.op == '-':
                t.op = '+'
            return t
        e = make_expr(['-', ['-', 3, ['-', 2, 1]]])
        eq(e.run(None), -2, 'visit_dfs before')
        eq(e.visit_dfs(plus2minus).run(None), 6, 'visit_dfs after')
        eq(e.count_if(lambda x: 1), 6, 'visit_dfs count all')
        eq(e.count_if(lambda x: isinstance(x, Const)), 3, 'count_if')

    def check_lang(self, lang, expr, str, name):
        eq = self.assertEqual
        eq(make_expr(expr).to_lang_named(lang), str, name)

    def check_prio_C(self, expr, str, priority):
        self.check_lang('C', expr, str, "priorities " + priority)

    def test_prio_C(self):
        self.check_prio_C([ '*', [ '+', 'a', 1 ], [ '-', 'b', 2 ] ], '(a + 1) * (b - 2)', '1')
        self.check_prio_C([ '+', [ '*', 'a', 1 ], [ '/', 'b', 2 ] ], 'a * 1 + b / 2', '2')
        self.check_prio_C([ '*', 5, [ '-', 'x' ] ], '5 * - x', 'unary 1')
        self.check_prio_C([ '+', 5, [ '-', 'x' ] ], '5 + - x', 'unary 2')
        self.check_prio_C([ '-', [ '+', 'x', 5 ] ], '- (x + 5)', 'unary 3')
        self.check_prio_C([ '+', [ '-', 'x' ] ], '+ - x', 'unary 4')

        e = [ '+', [ '&&', 'x', 'y' ] ]
        self.check_lang('Pascal', e, '+ (x and y)', 'prio Pascal not')
        self.check_prio_C(e, '+ (x && y)', 'C not')
        self.check_lang('Pascal', [ '+', 'x', [ '**', 'x', 2 ] ], 'x + x ** 2', 'Pascal power')

    def test_logic_prio(self):
        eq = self.assertEqual
        e = make_expr(['&&', [ '<=', 1, 'a' ], [ '<=', 'a', 'n' ]])
        eq(e.to_lang_named('C'), '1 <= a && a <= n', 'logic priorities C')
        eq(e.to_lang_named('Pascal'), '(1 <= a) and (a <= n)', 'logic priorities Pascal')

    def test_empty_block(self):
        eq = self.assertEqual
        b = make_block([])
        for keys in lang_names():
            eq(b.to_lang_named(keys), '', keys)

    def test_Alg_assign(self):
        eq = self.assertEqual
        b = make_block([ '=', 'x', 99 ])
        eq(b.to_lang_named('Alg'), 'x := 99')
        eq(b.run_val('x'), 99)

    def test_Perl_assign(self):
        eq = self.assertEqual
        b = make_block([ '=', 'x', 3, '=', 'y', 'x' ])
        eq(b.to_lang_named('Perl'), "$x = 3;\n$y = $x;")
        eq(b.run_val('y'), 3)

        b = make_block(['=', 'y', 3, '=', 'y', 'x'])
        with self.assertRaisesRegex(ValueError, 'x'):
            b.run_val('y')

    def test_run_simple(self):
        eq = self.assertEqual
        m = 5
        b = make_block([ '=', 'x', [ '+', m, 1 ] ])
        eq(b.run_val('x'), 6)
        m = 10
        b = make_block([ '=', 'x', [ '+', m, 1 ] ])
        eq(b.run_val('x'), 11)

    def test_text(self):
        eq = self.assertEqual
        b = make_block(['#', {'Basic': 'basic text'}])
        eq(b.to_lang_named('Basic'), 'basic text')
        eq(b.to_lang_named('C'), '')

    def test_Pascal(self):
        eq = self.assertEqual
        b = make_block([ '=', [ '[]', 'A', 2 ], 5 ])
        eq(b.to_lang_named('Pascal'), 'A[2] := 5;')
        eq(b.run_val('A'), [ None, None, 5 ])

    def test_loops(self):
        eq = self.assertEqual
        b = make_block([
            'for', 'i', 0, 4, [ '=', [ '[]', 'M', 'i' ], 'i' ]
        ])
        p = "for i := 0 to 4 do\n  M[i] := i;"
        eq(b.to_lang_named('Pascal'), p, 'loop in Pascal')
        eq(b.run_val('M'), [ 0, 1, 2, 3, 4 ], 'loop run')

    def test_double_array(self):
        eq = self.assertEqual
        b = make_block([
            'for', 'i', 0, 4, [
                'for', 'j', 0, 4, [
                    '=',
                    [ '[]', 'A', 'i', 'j' ],
                    [ '*', 'i', 'j' ]
                ]
            ]
        ])
        p = "for i := 0 to 4 do\n  for j := 0 to 4 do\n    A[i, j] := i * j;"
        eq(b.to_lang_named('Pascal'), p, 'double array in Pascal')
        w = [ [ i * j for j in range(5) ] for i in range(5) ]
        eq(b.run_val('A'), w, 'double array run')

    def test_triple_array(self):
        eq = self.assertEqual
        b = make_block([
            'for', 'i', 0, 2, [
                'for', 'j', 0, 2, [
                    'for', 'k', 0, 2, [
                        '=',
                        [ '[]', 'A', 'i', 'j', 'k' ],
                        [ '*', 'i', ['*', 'j', 'k' ]]
                    ]
                ]
            ]
        ])
        p = "for i := 0 to 2 do\n  for j := 0 to 2 do\n    for k := 0 to 2 do\n      A[i, j, k] := i * j * k;"
        eq(b.to_lang_named('Pascal'), p, 'triple array in Pascal')
        w = [ [ [ i * j * k for k in range(3) ] for j in range(3) ] for i in range(3) ]
        eq(b.run_val('A'), w, 'triple array run')

    def test_Pascal_loop(self):
        eq = self.assertEqual
        b = make_block([
            'for', 'i', 0, 4, [
                '=', [ '[]', 'M', 'i' ], 'i',
                '=', [ '[]', 'M', 'i' ], 'i',
        ]])
        p = """for i := 0 to 4 do begin
  M[i] := i;
  M[i] := i;
end;"""
        eq(b.to_lang_named('Pascal'), p, 'loop in Pascal with begin-end')

    def test_Alg_loop(self):
        eq = self.assertEqual
        b = make_block([
            '=', 'a', 1,
            'for', 'i', 1, 3, [ '=', 'a', [ '*', 'a', '2' ] ]
        ])
        p = """a := 1
нц для i от 1 до 3
  a := a * 2
кц"""
        eq(b.to_lang_named('Alg'), p, 'loop in Alg')
        eq(b.run_val('a'), 8, 'loop run')

    def test_ifs(self):
        eq = self.assertEqual
        b = make_block([
            'if', 'a', [ '=', 'x', 7 ],
        ])
        eq(b.to_lang_named('Basic'), 'IF a THEN x = 7', 'if in Basic')
        eq(b.to_lang_named('Perl'), "if ($a) {\n  $x = 7;\n}", 'if in Perl')
        eq(b.run_val('x', { 'a': Box(0) }), None, 'if (false) run')
        eq(b.run_val('x', { 'a': Box(1) }), 7, 'if (true) run')

    def test_while(self):
        eq = self.assertEqual
        b = make_block([
            'while', [ '>', 'a', 0 ], [ '=', 'a', [ '-', 'a', 1 ] ]
        ])
        eq(b.to_lang_named('Basic'), "DO WHILE a > 0\n  a = a - 1\nEND DO",
           'while in Basic')

        eq(b.to_lang_named('C'), "while (a > 0)\n  a = a - 1;", 'while in C')
        eq(b.run_val('a', {'a': Box(5)}), 0, 'while run')

    def test_while_with_assign(self):
        eq = self.assertEqual
        b = make_block([
            '=', 'x', '64',
            'while', [ '>', 'x', 7 ], [
                '=', 'x', [ '/', 'x', 2 ]
            ]
        ])
        eq(b.run_val('x'), 4, 'while run 2')

    def test_until(self):
        eq = self.assertEqual
        b = make_block([
            'until', [ '==', 'a', 0 ], [ '=', 'a', [ '-', 'a', 1 ] ]
        ])
        eq(b.to_lang_named('Basic'), "DO UNTIL a = 0\n  a = a - 1\nEND DO",
           'until in Basic')

        eq(b.to_lang_named('C'), "while (!(a == 0))\n  a = a - 1;",
           'until in C')
        eq(b.run_val('a', { 'a': Box(5) }), 0, 'until run')

    def test_gather(self):
        eq = self.assertEqual
        e = make_expr(['+', 'x', ['-', 'y']])
        v = {}
        e.gather_vars(v)
        eq(v, {'x': 1, 'y': 1}, 'gather_vars')

    def check_sub(self, lang, block, code, name, opts=None):
        eq = self.assertEqual
        eq(block.to_lang_named(lang, opts), "\n".join(i for i in code), name)

    def test_funcs_p_style(self):
        eq = self.assertEqual
        b = make_block([
            'func', [ 'g', 'a', 'b' ],
            [ '=', 'g', [ '-', 'a', 'b' ] ],
            '=', 'a', [ '()', 'g', 3, 2 ]
        ])
        c = {'Basic': [
                      'FUNCTION g(a, b)',
                      '  g = a - b',
                      'END FUNCTION',
                      '',
                      'a = g(3, 2)',
                      ],
            "Alg": [
                        'алг цел g(цел a, b)',
                        'нач',
                        '  g := a - b',
                        'кон',
                        '',
                        'a := g(3, 2)',
                    ],
            'Pascal': [
                        'function g(a, b: integer): integer;',
                        'begin',
                        '  g := a - b;',
                        'end;',
                        '',
                        'a := g(3, 2);',
                     ],
            "C": [
                        'int g(int a, int b) {',
                        '  int g;',
                        '  g = a - b;',
                        '  return g;',
                        '}',
                        '',
                        'a = g(3, 2);',
                   ],
            'Perl': [
                        'sub g {',
                        '  my $g;',
                        '  my ($a, $b) = @_;',
                        '  $g = $a - $b;',
                        '  return $g;',
                        '}',
                        '',
                        '$a = g(3, 2);',
                    ]
        }
        for lang in c.keys():
            self.check_sub(lang, b, c[lang], f"function calling, definition in {lang}")
        eq(b.run_val('a'), 1, 'run call function')

    def test_funcs_c_style(self):
        eq = self.assertEqual
        b = make_block([
            'func', [ 'g', 'a', 'b' ],
            [ 'return', [ '-', 'a', 'b' ] ],
            '=', 'a', [ '()', 'g', 3, 2 ]
        ])
        c = {
            'Basic': [
                      'FUNCTION g(a, b)',
                      '  RETURN a - b',
                      'END FUNCTION',
                      '',
                      'a = g(3, 2)',
                      ],
            'Alg': [
                      'алг цел g(цел a, b)',
                      'нач',
                      '  выход_алг a - b | выход_алг выраж - оператор выхода из алгоритма, с возвращением результата выраж',
                      'кон',
                      '',
                      'a := g(3, 2)',
                    ],
            'Pascal': [
                     'function g(a, b: integer): integer;',
                     'begin',
                     '  exit(a - b);',
                     'end;',
                     '',
                     'a := g(3, 2);',
                    ],
            'C': [
                       'int g(int a, int b) {',
                       '  return a - b;',
                       '}',
                       '',
                       'a = g(3, 2);',
                    ],
            'Perl': [
                        'sub g {',
                        '  my ($a, $b) = @_;',
                        '  return $a - $b;',
                        '}',
                        '',
                        '$a = g(3, 2);',
                    ],
        }
        for lang in c.keys():
            self.check_sub(lang, b, c[lang], "c style function calling, definition in $_")
        eq(b.run_val('a'), 1, 'run call c style function')

    def test_logic_func(self):
        eq = self.assertEqual
        b = make_expr(['()', 'f', ['()', 'g', 1]])
        eq(b.to_lang_named('Logic'), 'f(g(1))', 'Logic func text')
        eq(b.to_lang_named('Logic', {'html': 1}), '<i>f</i>(<i>g</i>(1))', 'Logic func html')

    def test_print(self):
        eq = self.assertEqual
        b = make_block([
            'for', 'i', 0, 9, [
                'expr', [ 'print', 'num', 'i', 0 ]
            ]
        ])
        c = {
            'Basic': [
                        'FOR i = 0 TO 9',
                        '  PRINT i, 0',
                        'NEXT i',
                    ],
            'Alg': [
                        'нц для i от 0 до 9',
                        '  вывод i, 0',
                        'кц',
                    ],
            'Pascal': [
                         'for i := 0 to 9 do',
                         '  write(i, 0);',
                    ],
            'C': [
                        'for (i = 0; i <= 9; ++i)',
                        '  print(i, 0);',
                    ],
            'Perl': [
                        'for ($i = 0; $i <= 9; ++$i) {',
                        '  print($i, 0);',
                        '}',
                    ],
        }
        for lang in c:
            self.check_sub(lang, b, c[lang], f"print in {lang}")
        eq(b.run_val('<out>'), "\n".join(str(i) + ' 0' for i in range(10)), 'run print')

    def test_inc(self):
        eq = self.assertEqual
        eq(make_expr([ '++{}', 'i' ]).run({ 'i': Box(2) }), 3, 'run prefix increment')
        eq(make_expr([ '{}--', 'i' ]).run({ 'i': Box(4) }), 4, 'run postfix decrement')

        e = make_expr([ '+', [ '++{}', 'i' ], [ '++{}', 'i' ] ])
        eq(e.to_lang_named('C'), '++i + ++i', 'to lang increment')

        env = {'i': Box(5)}
        eq(e.run(env), 13, 'run increment return value')
        eq(env['i'], 7, 'run increment side effect')

    def test_plain_text(self):
        eq = self.assertEqual
        b = make_expr(['#', 'BUMP'])
        eq(b.to_lang_named('C'), 'BUMP', 'to lang expr with plain text')

    def test_return_funcs_c_style(self):
        eq = self.assertEqual
        b = make_block([
            'func', [ 'f', 'x', 'y' ], [
                'if', [ '==', 'x', 'y' ], [ 'return', 1 ],
                'return', 0
            ],
            '=', 'a', [ '()', 'f', 1, 2 ],
            '=', 'b', [ '()', 'f', 3, 3 ]
        ])
        eq(b.run_val('a'), 0, 'return c_style func 0')
        eq(b.run_val('b'), 1, 'return c_style func 1')

    def test_return_funcs_p_style(self):
        eq = self.assertEqual
        b = make_block([
            'func', [ 'f', 'x', 'y' ], [
                 '=', 'f', 1,
                 'if', [ '==', 'x', 'y' ], [ 'return', [] ],
                 '=', 'f', 0,
             ],
             '=', 'a', [ '()', 'f', 1, 2 ],
             '=', 'b', [ '()', 'f', 3, 3 ]
        ])
        eq(b.run_val('a'), 0, 'return p_style func 0')
        eq(b.run_val('b'), 1, 'return p_style func 1')

    def test_html(self):
        b = make_block([
            'while', [ '>', 'a', 0] , [
                '=', 'a', [ '-', 'a', 1 ],
                'expr', [ '*', 2, 2 ]
            ]
        ])
        c1 = [
            '<span style="color: blue;">DO WHILE a &gt; 0</span>',
            '  a = a - 1',
            '  2 * 2',
            '<span style="color: blue;">END DO</span>',
        ]
        self.check_sub('Basic', b, c1, 'Basic html with coloring',
                                {'html': {'coloring': ['blue']}})

        c2 = [
            '<pre class="C"><span style="color: blue;">while (a &gt; 0) {</span></pre>',
            '<pre class="C">  a = a - 1;</pre>',
            '<pre class="C">  2 * 2;</pre>',
            '<pre class="C"><span style="color: blue;">}</span></pre>',
        ]
        self.check_sub('C', b, c2, 'C html with coloring+lang_marking',
                            {'html': {'coloring': ['blue'], 'lang_marking': 1}})

        c3 = [
            'while a > 0 do begin',
            'a := a - 1;',
            '2 * 2;',
            'end;',
        ]
        self.check_sub('Pascal', b, c3, 'Pascal unindent', {'unindent': 1})

        b1 = make_block([
            'while', [ '>', 'a', 0 ], [
                'if', [ '%', 'a', 10 ], [
                    '=', 'a', 20
                ],
                '=', 'a', [ '-', 'a', 1 ],
            ]
        ])
        c4 = [
            '<span style="color: blue;">while (a &gt; 0) {</span>',
            '  <span style="color: fuchsia;">if (a % 10) {</span>',
            '    a = 20;',
            '  <span style="color: fuchsia;">}</span>',
            '  a = a - 1;',
            '<span style="color: blue;">}</span>',
        ]
        self.check_sub('C', b1, c4, 'C html with multicoloring',
                             { 'html': {'coloring': ['blue', 'fuchsia']}, 'body_is_block': 1 })

    def test_sql(self):
        eq = self.assertEqual

        html = 0
        def check_sql(expr, ans, test_name):
            eq(make_expr(expr).to_lang_named('SQL', {'html': html}), ans, f"SQL {test_name}")
        check_sql(
            [ '&&', [ '<=', 1, 'a' ], [ '<=', 'a', 'n' ] ],
            '1 <= a AND a <= n', 'AND')
        check_sql(
            [ '||', [ '!=', 1, 'a' ], [ '!', 'a' ] ],
            '1 <> a OR NOT a', 'OR NOT')
        check_sql(
            [ '&&', [ '||', 'x', 'y' ], [ '==', 'a', 1 ] ],
            '(x OR y) AND a = 1', 'priorities')
        html = 1
        check_sql(
            [ '&&', [ '<=', 1, 'a' ], [ '<=', 'a', 'n' ] ],
            '1 &lt;= a AND a &lt;= n', 'AND html')
        check_sql(
            [ '||', [ '!=', 1, 'a' ], [ '!', 'a' ] ],
            '1 &lt;&gt; a OR NOT a', 'OR NOT html')

    def test_add_statement(self):
        eq = self.assertEqual
        b = make_block([
            '=', 'M', 3
        ])
        add_statement(b, ['=', 'M', 4])
        c = {
            'Basic': [
                        'M = 3',
                        'M = 4',
                    ],
            'Alg': [
                        'M := 3',
                        'M := 4',
                    ],
            'Pascal': [
                        'M := 3;',
                        'M := 4;',
                    ],
            'C': [
                        'M = 3;',
                        'M = 4;',
                    ],
            'Perl': [
                        '$M = 3;',
                        '$M = 4;',
                    ],
        }
        for lang in c.keys():
            self.check_sub(lang, b, c[lang], 'add_statement')
        eq(b.run_val('M'), 4, 'add_statement run')

    def test_move_statement(self):
        eq = self.assertEqual
        b = make_block([
            '=', 'M', 3,
            '=', 'M', 4,
        ])
        move_statement(b, 1, 0)
        c = {
            'Basic': [
                        'M = 4',
                        'M = 3',
                    ],
            'Alg': [
                        'M := 4',
                        'M := 3',
                    ],
            'Pascal': [
                        'M := 4;',
                        'M := 3;',
                    ],
            'C': [
                        'M = 4;',
                        'M = 3;',
                    ],
            'Perl': [
                        '$M = 4;',
                        '$M = 3;',
                    ],
        }
        for lang in c.keys():
            self.check_sub(lang, b, c[lang], 'move_statement')
        eq(b.run_val('M'), 3, 'move_statement run')

    def test_print_star(self):
        b = make_block([ 'expr', [ 'print', 'str', '*' ] ])
        c = {
            'Basic': [ 'PRINT "*"' ],
            'Alg': [ 'вывод "*"' ],
            'Pascal': [ "write('*');" ],
            'C': [ 'printf("*");' ],
            'Perl': [ "print('*');" ],
        }
        for lang in c.keys():
            self.check_sub(lang, b, c[lang], f"print str in {lang}")

    def test_input_int(self):
        eq = self.assertEqual
        b = make_block([ 'expr', [ 'input', 'i' ] ])
        c = {
            'Basic': [ 'INPUT i' ],
            'Alg': [ 'ввод i' ],
            'Pascal': [ 'readln(i);' ],
            'C': [ 'scanf("%d", &i);' ],
        }
        for lang in c:
            self.check_sub(lang, b, c[lang], f"print in {lang}")


if __name__ == '__main__':
    unittest.main(verbosity=1)

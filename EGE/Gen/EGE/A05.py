import copy

from ...GenBase import SingleChoice
from EGE.Prog import make_block, BinOp
from EGE.LangTable import table, unpre
from EGE.Bits import Bits

def without_op(expr, index):
    def get_left_oeperand(f, args):
        if isinstance(f, BinOp):
            args[0] += 1
        return hasattr(f, 'left') and f.left and isinstance(f, BinOp) and args[0] == args[1] and f.left or f

    return expr.visit_dfs(get_left_oeperand, [0, index])

class Arith(SingleChoice):
    def generate(self):
        v1 = self.rnd.in_range(1, 9)
        v2 = self.rnd.in_range(1, 9)
        v3 = self.rnd.in_range(2, 4)
        ab1 = self.rnd.pick([ 'a', 'b' ])
        ab2 = self.rnd.shuffle([ 'a', 'b' ])

        def make_block_arith(v1, v2, v3):
            return make_block([
                '=', 'a', v1, '=', ab1, [self.rnd.pick(['+', '-']), 'a', v2],
                '=', 'b', ['-', (1 if self.rnd.coin() else None), ab1],
                '=', 'c', ['+', ['-', ab2[0]], ['*', v3, ab2[1]]],
            ])

        b = make_block_arith(v1, v2, v3)

        lt = table(b, [ [ 'Basic', 'Alg' ], [ 'Pascal', 'C' ] ])
        self.text = f'Определите значение переменной <i>c</i> после выполнения следующего фрагмента программы: {lt}'
        get_c = lambda x: x.run_val('c', {})

        errors = []
        for i in range(3):
            args = [v1, v2, v3]
            args[i] += 1
            errors.append(get_c(make_block_arith(*args)))
            args[i] -= 2
            errors.append(get_c(make_block_arith(*args)))

        for i in range(b.count_if(lambda x: isinstance(x, BinOp))):
            errors.append(str(get_c(without_op(copy.deepcopy(b), i+1))))
        correct = str(get_c(b))

        errors = list(filter(lambda x: x != correct, set(errors)))
        while len(errors) < 3:
            errors.append(max(errors) + self.rnd.in_range(1, 3))

        self.set_variants([correct, *self.rnd.pick_n(3, errors)])
        return self

def replace_ops(expr, repls):
    def replace_op(f, args):
        newop = args[0].get(hasattr(f, 'op') and f.op or '')
        if newop is not None:
            f.op = newop
        return f

    return expr.visit_dfs(replace_op, [repls])

def div_mod_common(self, q, src, get_fn):
    cc = (', вычисляющие результат деления нацело первого аргумента на второй ' +
         'и остаток от деления соответственно')

    b = make_block([*src,
                    '#', {
                        'Basic': unpre(f"\'\\ и MOD — операции{cc}"),
                        'Pascal': unpre(f"{{div и mod — операции{cc}}}"),
                        'Alg': unpre(f"|div и mod — функции{cc}")
                    },
    ])

    def get_v(block, get_fn):
        env = {}
        block.run(env)
        return get_fn(env)

    correct = get_v(b, get_fn)
    lt = table(b, [ [ 'Basic', 'Pascal', 'Alg' ] ])
    self.text = f"{q} после выполнения следующего фрагмента программы: {lt}"
    errors = []

    for repl in { '%': '//' }, { '//': '%' }, { '%': '//', '//': '%' }:
        errors.append(get_v(replace_ops(copy.deepcopy(b), repl), get_fn))
    for i in range(b.count_if(lambda x: isinstance(x, BinOp))):
        errors.append(get_v(without_op(copy.deepcopy(b), i+1), get_fn))

    errors = list(filter(lambda x: x != correct, set(errors)))
    self.set_variants([correct, *(errors if len(errors) < 3 else self.rnd.pick_n(3, errors))])
    return self

class DivMod10(SingleChoice):
    def generate(self):
        v2 = self.rnd.in_range(2, 9)
        v3 = self.rnd.in_range(2, 9)

        return div_mod_common(self,
                              'Определите значение целочисленных переменных <i>x</i> и <i>y</i>',
                              [
                                  '=', 'x', [ '+', self.rnd.in_range(1, 9), [ '*', v2, v3 ] ],
                                  '=', 'y', [ '+', [ '%', 'x', 10 ], self.rnd.in_range(11, 19) ],
                                  '=', 'x', [ '+', [ '//', 'y', 10 ], self.rnd.in_range(1, 9) ],
                              ],
                              lambda x: f"<i>x</i> = {x['x']}, <i>y</i> = {x['y']}")

class DivModRotate(SingleChoice):
    def generate(self):
        return div_mod_common(self,
                              'Переменные <i>x</i> и <i>y</i> описаны в программе как целочисленные. '
                              'Определите значение переменной <i>x</i>',
                              [
                                  '=', 'x', self.rnd.in_range(101, 999),
                                  '=', 'y', [ '//', 'x', 100 ],
                                  '=', 'x', [ '*', [ '%', 'x', 100 ], 10 ],
                                  '=', 'x', [ '+', 'x', 'y' ],
                              ],
                              lambda x: x['x'])

class DigitByDigit(SingleChoice):
    def generate(self):
        good = lambda: self.rnd.in_range(10, 18)
        bad1 = lambda: self.rnd.in_range(0, 9)
        bad2 = lambda: 19

        vars = [sorted([good(), good(), good()], reverse=True),
                sorted([good(), good(), good()]),
                sorted([bad1(), good(), good()], reverse=True),
                sorted([bad2(), good(), good()], reverse=True)]

        self.text = """Автомат получает на вход два трехзначных числа. По этим числам строится новое
число по следующим правилам.
<ol>
  <li>
    Вычисляются три числа – сумма старших разрядов заданных трехзначных чисел,
    сумма средних разрядов этих чисел, сумма младших разрядов.
  </li>
  <li>
    Полученные три числа записываются друг за другом в порядке убывания (без разделителей).
  </li>
</ol>
<i>Пример. Исходные трехзначные
числа:  835, 196. Поразрядные суммы: 9, 12, 11. Результат: 12119</i>
<br/>Определите, какое из следующих чисел может быть результатом работы автомата.
"""
        self.set_variants([''.join("{:02d}".format(i) for i in var) for var in vars])
        return self

class CRC(SingleChoice):
    def random_0_1(self, zeroes, ones, used, cond=lambda x: 1):
        bits = Bits()
        while True:
            bits.set_bin(self.rnd.shuffle([*[0 for _ in range(zeroes)], *[1 for _ in range(ones)]]), True)
            if not used.get(bits.get_bin()) and cond(bits):
                break
        used[bits.get_bin()] = 1
        return bits

    def generate(self):
        digits, digits_text, control_text = self.rnd.pick([
            [6, 'шести', 'седьмой'],
            [7, 'семи', 'восьмой'],
            [8, 'восьми', 'девятый']]
        )

        zero_out = "".join('0' for _ in range(digits + 1))
        ones = digits // 2 + digits // 2 % 2
        used = {}
        sample_0 = self.random_0_1(digits - ones, ones, used, lambda x: x.xor_bits() == 0).get_bin()
        sample_1 = self.random_0_1(digits - ones + 1, ones - 1, used, lambda x: x.xor_bits() == 1).get_bin()

        msg = [self.random_0_1(digits - ones, ones, used) for _ in range(3)]
        for b in msg:
            if not hasattr(b, 'v'):
                b.v = []
            b.v.append(b.xor_bits())

        unchanged, single, double = self.rnd.shuffle([i for i in range(3)])
        bad = [b.dup() for b in msg]
        bad[single].flip([self.rnd.in_range(0, digits+1)])
        for i in self.rnd.pick_n(2, [i for i in range(digits)]):
            bad[double].flip([i])

        def msg_as_text(*t):
            cmsg = bad.copy()
            for i in t:
                cmsg[i] = None
            return '<tt>' + ' '.join(c.get_bin() if c else zero_out for c in cmsg) + '</tt>'

        self.correct = single
        self.text = (f"<p>В не­ко­то­рой ин­фор­ма­ци­он­ной си­сте­ме ин­фор­ма­ция ко­ди­ру­ет­ся дво­ич­ны­ми {digits_text}раз­ряд­ны­ми сло­ва­ми. " +
                    f"При пе­ре­да­че дан­ных воз­мож­ны их ис­ка­же­ния, по­это­му в конец каж­до­го слова до­бав­ля­ет­ся {control_text} " +
                    "(кон­троль­ный) раз­ряд таким об­ра­зом, чтобы сумма раз­ря­дов но­во­го слова, счи­тая кон­троль­ный, была чётной. " +
                    f"На­при­мер, к слову <tt>{sample_0}</tt> спра­ва будет до­бав­лен <tt>0</tt>, а к слову <tt>{sample_1}</tt> — <tt>1</tt>.</p>" +
                    "<p>После приёма слова про­из­во­дит­ся его об­ра­бот­ка. При этом про­ве­ря­ет­ся сумма его раз­ря­дов, вклю­чая кон­троль­ный. " +
                    "Если она нечётна, это озна­ча­ет, что при пе­ре­да­че этого слова про­изошёл сбой, " +
                    f"и оно ав­то­ма­ти­че­ски за­ме­ня­ет­ся на за­ре­зер­ви­ро­ван­ное слово <tt>{zero_out}</tt>. " +
                    "Если она чётна, это озна­ча­ет, что сбоя не было или сбоев было боль­ше од­но­го. В этом слу­чае при­ня­тое слово не из­ме­ня­ет­ся.</p>" +
                    f"<p>Ис­ход­ное со­об­ще­ние</p><pre>{' '.join(i.get_bin() for i in msg)}</pre><p>было при­ня­то в виде</p><pre> {msg_as_text()} " +
                    "</pre><p>Как будет вы­гля­деть при­ня­тое со­об­ще­ние после об­ра­бот­ки?</p>")

        self.set_variants([*[msg_as_text(i) for i in range(3)], msg_as_text(single, double)])
        return self

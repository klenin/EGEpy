from ...GenBase import SingleChoice, EGEError
from ...Logic import random_logic_expr, bits_to_vars
from ...Russian import join_comma_and
from ...Bits import Bits
from ... import Html as html
from ...Utils import char_range

class TruthTableFragment(SingleChoice):

    def rand_expr_text(self, vars_: list):
        e = random_logic_expr(self.rnd, vars_)
        return e, e.to_lang_named('Logic', { 'html': 1 })

    @staticmethod
    def tt_row(expr, bits, vars_: list):
        r = bits_to_vars(bits, vars_)
        r['F'] = expr.run(r)
        return r

    @staticmethod
    def tt_html(table, vars_: list):
        r = html.row_n('th', vars_)
        for i in table:
            r += html.row_n('td', [ i[var] for var in vars_ ])
        return html.table(r, attrs={ 'border': 1 })

    @staticmethod
    def check_rows(table, expr):
        for i in table:
            if expr.run(i) != i['F']:
                return False
        return True

    def generate(self):
        vars_ = [ 'X', 'Y', 'Z' ]
        e, e_text = self.rand_expr_text(vars_)
        rows = sorted(self.rnd.pick_n(3, list(range(2 ** len(vars_)))))
        bits = [ Bits().set_size(4).set_dec(i) for i in rows ]
        fragment = [ self.tt_row(e, i, vars_) for i in bits ]

        seen = set(e_text)
        bad = []
        while len(bad) < 3:
            while True:
                e1, e1_text = self.rand_expr_text(vars_)
                if e1_text not in seen:
                    break
            if not self.check_rows(fragment, e1):
                bad.append(e1_text)

        tt_text = self.tt_html(fragment, vars_ + ['F'])
        self.text = f'''Символом F обозначено одно из указанных ниже логических выражений от трёх аргументов X, Y, Z. 
            Дан фрагмент таблицы истинности выражения F: \n{tt_text}\n Какое выражение соответствует F?'''
        self.set_variants([e_text] + bad)
        return self

class FindVarLenCode(SingleChoice):

    def _build_tree(self, l):
        if not l:
            return None
        elif self.rnd.coin():
            return { 'l': self._build_tree(l - 1), 'r': self._build_tree(l - 1) }
        else:
            return { self.rnd.pick([ 'l', 'r' ]): self._build_tree(l - 1) }

    def _gain_codes(self, node, res, accum):
        if 'r' in node and node['r'] is not None:
            self._gain_codes(node['r'], res, accum + '1')
        else:
            res.append(accum + '1')

        if 'l' in node and node['l'] is not None:
            self._gain_codes(node['l'], res, accum + '0')
        else:
            res.append(accum + '0')

    def _build_codes(self, length, tree=None):
        res = []
        if tree is None:
            tree = self._build_tree(length)
        self._gain_codes(tree, res, '')
        return res

    def generate(self):
        codes = self._build_codes(3)
        codes = self.rnd.pick_n(self.rnd.in_range(3, min(len(codes), 6)), codes)
        ans = codes.pop(0)

        bad = []
        for code in codes:
            bad.append(code + '0')
            bad.append(code + '1')
            if len(code) > 1:
                bad.append(code[:-1])
        self.set_variants([ans] + self.rnd.pick_n(3, bad))

        letters = list(char_range('A', 'Z'))
        alph = [ letters[i] for i in range(len(codes)) ]
        self.text = '''Для кодирования некоторой последовательности, состоящей из букв {}, 
            решили использовать неравномерный двоичный код, позволяющий 
            однозначно декодировать двоичную последовательность, появляющуюся на 
            приёмной стороне канала связи. Использовали код: {}. 
            Укажите, каким кодовым словом может быть закодирована буква {}. 
            Код должен удовлетворять свойству однозначного декодирования.'''.format(
            ', '.join(alph),
            ', '.join([ f'{alph[i]}−{codes[i]}' for i in range(len(codes)) ]),
            chr(ord(alph[-1]) + 1))
        return self

class ErrorCorrectionCode(SingleChoice):

    def generate(self):
        digits = self.rnd.in_range(5, 6)
        used = set()
        letters = [ { 'bits': Bits().set_size(digits), 'letter': i } for i in [ 'А', 'Б', 'В' ] ]
        for l in letters:
            while True:
                l['bits'].set_dec(self.rnd.in_range(0, 2 ** digits - 1))
                if l['bits'].get_dec() not in used:
                    break
            used.add(l['bits'].get_dec())
            for i in range(digits):
                used.add(l['bits'].dup().flip([i]).get_dec())
                for j in range(i+1, digits):
                    used.add(l['bits'].dup().flip([ i, j ]).get_dec())
        msg = self.rnd.shuffle(letters) + [self.rnd.pick(letters)]
        sample = self.rnd.pick(letters)

        def msg_with_errors(errors):
            errors.append(-1)
            return ''.join([ 'x' if i in errors else msg[i]['letter'] for i in range(len(msg)) ])

        error_variants = [ self.rnd.pick_n(i, list(range(len(msg)))) for i in self.rnd.pick_n(4, list(range(len(msg)))) ]
        self.set_variants([ msg_with_errors(i) for i in error_variants ])
        correct = error_variants[0] + [-1]

        def check_almost_equal(bits):
            for letter in letters:
                count = 0
                for i in range(len(bits)):
                    count += int(letter['bits'].get_bin()[i] != bits[i])
                if count < 2:
                    return True
            return False

        msg_bits_with_errors = []
        for i in range(len(msg)):
            if i in correct:
                bits = msg[i]['bits'].dup().get_bin()
                while check_almost_equal(bits):
                    bits = msg[i]['bits'].dup().flip(self.rnd.pick_n(2, list(range(digits)))).get_bin()
                msg_bits_with_errors.append(bits)
            else:
                msg_bits_with_errors.append(msg[i]['bits'].dup().flip([self.rnd.pick(list(range(digits)))]).get_bin())

        self.text = (f'''<p>Для передачи данных по каналу связи используется {digits}-битовый код. 
            Сообщение содержит только буквы ''' +
            join_comma_and([ i['letter'] for i in letters ]) +
            ', которые кодируются следующими кодовыми словами:</p><p>' +
            ', '.join([ f'{i["letter"]} – <tt>' + i['bits'].get_bin() + '</tt>' for i in letters ]) +
            '''.</p><p>При передаче возможны помехи. Однако некоторые ошибки можно попытаться исправить. 
            Любые два из этих трёх кодовых слов отличаются друг от друга не менее чем в трёх позициях. 
            Поэтому если при передаче слова произошла ошибка не более чем в одной позиции, 
            то можно сделать обоснованное предположение о том, какая буква передавалась. 
            (Говорят, что «код исправляет одну ошибку».) Например, если получено кодовое слово <tt>''' +
            sample['bits'].dup().flip([self.rnd.in_range(0, digits - 1)]).get_bin() +
            f'''</tt>, считается, что передавалась буква {sample["letter"]}. 
            (Отличие от кодового слова для {sample["letter"]} только в одной позиции, 
            для остальных кодовых слов отличий больше.) 
            Если принятое кодовое слово отличается от кодовых слов для букв ''' +
            ', '.join([ i['letter'] for i in letters ]) +
            ''' более чем в одной позиции, то считается, что произошла ошибка (она обозначается ‘x’).</p>
            <p>Получено сообщение <tt>''' +
            ' '.join(msg_bits_with_errors) +
            '</tt>. Декодируйте это сообщение — выберите правильный вариант.</p>')

        return self

class HammingCode(SingleChoice):

    def _hamming_random_bits(self):
        return Bits().set_size(5).set_dec(self.rnd.in_range(0, 31))

    def _count_diff_bits(self, bits1, bits2):
        return bits1.dup().logic_op('xor', bits2).count_ones()

    def _hamming_make_random_code(self, codes, max_):
        if len(codes) >= max_:
            return True
        for bin_ in self.rnd.shuffle(list(range(32))):
            code = Bits().set_size(5).set_dec(bin_)
            cont = False
            for c in codes:
                if self._count_diff_bits(code, c) < 3:
                    cont = True
                    break
            if cont:
                continue
            codes.append(code)
            if self._hamming_make_random_code(codes, max_):
                return True
            codes.pop()
        return False

    def generate(self):
        codes = [self._hamming_random_bits()]
        if not self._hamming_make_random_code(codes, 4):
            raise EGEError(' '.join([ i.get_bin() for i in codes ]))

        bad = []
        while len(bad) < 3:
            code = self._hamming_random_bits()
            for c in codes:
                cnt = self._count_diff_bits(code, c)
                if cnt == 1 or cnt == 2:
                    bad.append(code.get_bin())

        self.set_variants([codes[0].get_bin()] + bad)

        w = [ i for i in self.rnd.pick([ 'АИСТ', 'ПОРТ',  'МАРТ', 'РИСК', 'СВЕТ', 'ЛИСТ' ]) ]
        self.text = (f'''<p>По каналу связи передаются сообщения, содержащие только 4 буквы {w[0]}, {w[1]}, {w[2]}, {w[3]}. 
            Для кодирования букв {w[0]}, {w[1]}, {w[2]} используются 5-битовые кодовые слова:</p><p>''' +
            ', '.join([ f'{w[i]} - <tt>{codes[i + 1].get_bin()}</tt>' for i in range(3) ]) +
            f'''</p><p>Для этих кодовых слов выполнено такое свойство: кодовые 
            слова для разных букв отличаются не менее, чем в трех позициях. Это свойство 
            важно для расшифровки сообщений при наличии помех. 
            Для буквы {w[3]} нужно выбрать кодовое слово так, чтобы оно тоже отличалось от кодовых 
            слов для букв {w[0]}, {w[1]}, {w[2]} не менее, чем в трех позициях.</p> 
            <p>Какое из перечисленных ниже кодовых слов можно использовать для буквы {w[3]}?</p>''')

        return self

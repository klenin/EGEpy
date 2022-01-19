from ...GenBase import DirectInput
from ...RussianModules.Names import different_males, ablative, genitive
from ...RussianModules.Jobs import different_jobs
from ...Russian import join_comma_and
from ... import Html as html
from ...Prog import make_expr
from dataclasses import dataclass
from enum import Enum
from math import ceil, log

@dataclass
class Relation:
    v: dir = {},
    is_sym: bool = False

    def init_value(self):
        self.v = { 0: {}, 1: {}, 2: {}, 3: {} }

    def add_value(self, i: int, j: int):
        self.v[i][j] = True
        if self.is_sym:
            self.v[j][i] = True

    def remove_value(self, i: int, j: int):
        self.v[i].pop(j, True)
        if self.is_sym:
            self.v[j].pop(i, True)

    def get_value(self, i: int, j: int):
        return self.v[i].get(j, False)

class RelationKey(Enum):
    ToRight = 0
    Together = 1
    NotTogether = 2
    PosLeft = 3
    PosRight = 4
    Pos = 5
    NotPos = 6

class Solve(DirectInput):
    def generate(self):
        self.init_relations()
        names = different_males(self.rnd, 4)
        prof = different_jobs(self.rnd, 4)

        prof_order = self.create_conditions([ RelationKey.Together, RelationKey.NotTogether ])

        descr = {
            RelationKey.ToRight: lambda x, y: self.on_right(prof[x], prof[y]),
            RelationKey.Together: lambda x, y: self.together(prof[x], prof[y]),
            RelationKey.NotTogether: lambda x, y: self.not_together(prof[x], prof[y]),
        }
        questions = self.create_questions(descr)
        ans = self.create_conditions(list(self.relations.keys()))

        descr = {
            RelationKey.ToRight: lambda x, y: self.on_right(names[x], names[y]),
            RelationKey.Together: lambda x, y: self.together(names[x], names[y]),
            RelationKey.NotTogether: lambda x, y: self.not_together(names[x], names[y]),
            RelationKey.PosLeft: lambda x, y: self.on_right(prof[prof_order[y]], names[x]),
            RelationKey.PosRight: lambda x, y: self.on_right(names[x], prof[prof_order[y]]),
            RelationKey.Pos: lambda x, y: f'{names[x]} работает {ablative(prof[prof_order[y]])}',
            RelationKey.NotPos: lambda x, y: f'{names[x]} не работает {ablative(prof[prof_order[y]])}'
        }
        questions += self.create_questions(descr)

        self.text = f'''На одной улице стоят в ряд 4 дома, в которых живут 4 человека:
                    {', '.join([ html.tag('strong', n) for n in names ])}
                    . Известно, что каждый из них владеет ровно одной из следующих профессий:
                    {', '.join([ html.tag('strong', p) for p in prof ])}
                    , но неизвестно, кто какой и неизвестно, кто в каком доме живет. Однако,
                    известно, что: {html.ol_li(self.rnd.shuffle(questions))}'''

        example = self.rnd.shuffle(names)
        self.text += f'''Выясните, кто какой профессии, и кто где живет, и дайте ответ в виде
                        заглавных букв имени людей, в порядке слева направо. Например, если бы
                        в домах жили (слева направо) {', '.join(example)}
                        , ответ был бы: {''.join([ e[0] for e in example ])}'''
        self.correct = ''.join([ names[a][0] for a in ans ])
        return self

    def init_relations(self):
        self.relations = {
            RelationKey.ToRight:        Relation(is_sym=False),
            RelationKey.Together:       Relation(is_sym=True),
            RelationKey.NotTogether:    Relation(is_sym=True),
            RelationKey.PosLeft:        Relation(is_sym=False),
            RelationKey.PosRight:       Relation(is_sym=False),
            RelationKey.Pos:            Relation(is_sym=False),
            RelationKey.NotPos:         Relation(is_sym=False),
        }

    @staticmethod
    def unique_pairs(n: int):
        return [ [i, j] for i in range(n) for j in range(i + 1, n) ]

    @staticmethod
    def all_pairs(n: int):
        return [ [i, j] for i in range(n) for j in range(n) ]

    @staticmethod
    def get_all_conditions(els: list):
        def rec(curr_res: list, tot_res: list, elems: list):
            if not elems:
                tot_res.append(curr_res)
                return
            for i in range(len(elems)):
                rec([ *curr_res, elems[i] ], tot_res, elems[:i] + elems[i + 1:])
        res = []
        rec([], res, els)
        return res

    def clear_relations(self):
        for k in self.relations:
            self.relations[k].init_value()

    def init_conditions(self, cnt: int):
        self.clear_relations()
        edges = self.rnd.pick_n(cnt, self.unique_pairs(4))
        for i, j in edges:
            # создать ограничения "правее": важно, чтобы не было циклов
            self.relations[RelationKey.ToRight].add_value(j, i)

    def check_condition(self, conditions: list):
        pos = { conditions[i]: i for i in range(4) }
        for i in range(len(conditions)):
            curr = conditions[i]
            for j in self.relations[RelationKey.Together].v[curr]:
                if not abs(pos[j] - i) == 1:
                    return False
            for j in self.relations[RelationKey.NotTogether].v[curr]:
                if abs(pos[j] - i) == 1:
                    return False
            for j in self.relations[RelationKey.ToRight].v[curr]:
                if i <= pos[j]:
                    return False
            for j in self.relations[RelationKey.PosLeft].v[curr]:
                if j <= i:
                    return False
            for j in self.relations[RelationKey.PosRight].v[curr]:
                if j >= i:
                    return False
            for j in self.relations[RelationKey.Pos].v[curr]:
                if i != j:
                    return False
            for j in self.relations[RelationKey.NotPos].v[curr]:
                if i == j:
                    return False
        return True

    def filter_conditions(self, conditions: list):
        return list(filter(lambda x: self.check_condition(x), conditions))

    def try_new_condition(self, cond: list, answers: list):
        relation = self.relations[cond[2]]
        if relation.get_value(cond[0], cond[1]):
            return answers
        relation.add_value(cond[0], cond[1])
        new_ans = self.filter_conditions(answers)
        if new_ans == answers or not new_ans:
            relation.remove_value(cond[0], cond[1])
            return answers
        else:
            return new_ans

    def clear_conditions(self):
        conditions = self.get_all_conditions(list(range(4)))
        orig_answer = self.filter_conditions(conditions)
        ok = True
        while ok:
            ok = False
            for rel in self.relations:
                for i in range(4):
                    for j in list(self.relations[rel].v[i]):
                        self.relations[rel].remove_value(i, j)
                        if self.filter_conditions(conditions) != orig_answer:
                            self.relations[rel].add_value(i, j)
                        else:
                            ok = True

    def make_pairs(self, relation_keys: list):
        pairs = []
        for rel in relation_keys:
            tmp = self.unique_pairs(4) if self.relations[rel].is_sym else self.all_pairs(4)
            pairs += [ [ i, j, rel ] for i, j in tmp ]
        self.rnd.shuffle(pairs)
        return pairs

    def create_conditions(self, relation_keys: list):
        pairs = self.make_pairs(relation_keys)
        while True:
            self.init_conditions(self.rnd.pick([ 2, 2, 3 ]))
            answers = self.filter_conditions(self.get_all_conditions(list(range(4))))
            if answers:
                break

        while len(answers) != 1:
            answers = self.try_new_condition(pairs.pop(), answers)
            if not pairs:
                pairs = self.make_pairs(relation_keys)
        self.clear_conditions()
        return answers[0]

    def create_questions(self, descr: dict):
        conditions = []
        for k in self.relations:
            rel = self.relations[k]
            conditions += [ descr[k](i, j) for i in rel.v for j in rel.v[i] if not rel.is_sym or i > j ]
        return conditions

    def on_right(self, i: int, j: int):
        t = [
            lambda x, y: f'{y}  живет левее {genitive(x)}',
            lambda x, y: f'{x}  живёт правее {genitive(y)}',
            lambda x, y: f'{y}  живет левее, чем {x}',
            lambda x, y: f'{x}  живёт правее, чем {y}',
        ]
        return self.rnd.pick(t)(i, j)

    def together(self, i: int, j: int):
        return f'{i}  живёт рядом c {ablative(j)}'

    def not_together(self, i: int, j: int):
        return f'{i}  живёт не рядом c {ablative(j)}'

class RecursiveFunction(DirectInput):
    def generate(self):
        first_num = self.rnd.in_range(2, 6)
        second_num = self.rnd.in_range(2, 6, first_num)
        first_val = self.rnd.in_range(0, 5)
        second_val = self.rnd.in_range(1, 5)
        n = self.rnd.in_range(4, 7)

        exprs = [
            [ '==', [ '()', 'F', 0 ], first_val ],
            [ '==', [ '()', 'F', 1 ], second_val ],
            [ '==',
                [ '()', 'F', 'n' ],
                    [ '+',
                        [ '*', [ '()', 'F', [ '-', 'n', 1 ] ], first_num ],
                        [ '*', [ '()', 'F', [ '-', 'n', 2 ] ], second_num ] ]
            ],
            [ '()', 'F', 'n' ],
            [ '>=', 'n', 2 ],
            [ '()', 'F', n ],
        ]

        texts = [ make_expr(e).to_lang_named('Logic', {'html': 1}) for e in exprs ]
        self.accept_number()
        self.correct = self._rec_calculate(first_val, second_val, first_num, second_num, n)
        self.text = f'''Алгоритм вычисления значения функции {texts[3]}, где <i>n</i> — натуральное число, 
                        задан следующими соотношениями:
                        {html.ul_li(
                            [ f'{texts[0]}, {texts[1]}', f'{texts[2]}, при {texts[4]}'], 
                            html.style(list_style_type='none')
                        )}
                         Чему равно значение функции {texts[5]}? В ответе запишите только натуральное число.'''
        return self

    def _rec_calculate(self, f_v: int, s_v: int, f_n: int, s_n: int, n: int):
        func = 0
        for i in range(2, n + 1):
            func = s_v * f_n + f_v * s_n
            f_v = s_v
            s_v = func
        return func

class PasswordMeta(DirectInput):
    def generate(self):
        users_count = self.rnd.in_range(10, 20) * 10
        password_length = self.rnd.in_range(8, 20)

        case_messages = {
            'lower': 'латинские буквы только нижнего регистра (строчные)',
            'upper': 'латинские буквы только верхнего регистра (прописные)',
            'both': 'как прописные, так и строчные латинские буквы',
        }
        character_case = self.rnd.pick(list(case_messages.keys()))
        character_variants_count = 26 * (2 if character_case == 'both' else 1)

        conditions = [ case_messages[character_case] ]
        if self.rnd.coin():
            character_variants_count += 10
            conditions += [ 'хотя бы одну десятичную цифру' ]

        if self.rnd.coin():
            cnt = self.rnd.in_range(5, 11)
            special_character = list("!@#$%^&*_-=+;:{}\\|/,.<>?~`()'")
            special_character = self.rnd.pick_n(cnt, special_character)
            character_set = ', '.join([ html.escape(f'«{s}»') for s in special_character ])
            conditions += [ f'не менее одного символа из {cnt}-символьного набора: {character_set}' ]
            character_variants_count += cnt

        conditions_text = join_comma_and(self.rnd.shuffle(conditions))
        bits_per_character = ceil(log(character_variants_count) / log(2))
        bytes_per_password = ceil(bits_per_character * password_length / 8)

        meta_payload = self.rnd.in_range(50, 200)
        total_db_size = (bytes_per_password + meta_payload) * users_count

        self.accept_number()
        self.correct = meta_payload
        self.text = f'''При регистрации в компьютерной системе каждому пользователю выдаётся пароль, 
                        состоящий из {password_length} символов. 
                        Из соображений информационной безопасности каждый пароль должен содержать {conditions_text}. 
                        В базе данных для хранения сведений о каждом пользователе отведено одинаковое 
                        и минимально возможное целое число байт. При этом используют посимвольное кодирование паролей, 
                        все символы кодируют одинаковым и минимально возможным количеством бит. 
                        Кроме собственно пароля, для каждого пользователя в системе хранятся дополнительные сведения, 
                        для чего выделено целое число байт; это число одно и то же для всех пользователей. 
                        Для хранения сведений о {users_count} пользователях потребовалось {total_db_size} байт. 
                        Сколько байт выделено для хранения дополнительных сведений об одном пользователе? 
                        В ответе запишите только целое число – количество байт. 
                        <br/><i>Примечание: В латинском алфавите 26 букв.</i>'''
        return self


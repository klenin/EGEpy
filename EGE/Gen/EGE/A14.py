from ...GenBase import SingleChoice
from ...RussianModules.FamilyNames import family_names
from ...RussianModules.Subjects import subjects
from EGE.Prog import make_block, make_expr
from ... import Html as html
import re

class Database(SingleChoice):

    def generate(self):
        # families = self.rnd.pick_n_sorted(6, family_names)
        reg = re.compile(r'!\s')
        subjects_ = self.rnd.pick_n(5, list(filter(reg.search, subjects)))
        table = EGE::SQL::Table->new([ qw(Фамилия Пол), subjects_ ]);
        for i in families:
            sex = self.rnd.coin()
            table.insert_row(i + ('' if sex else 'а'), sex, [ self.rnd.in_range(50, 90) for _ in subjects_ ])

        cond = ''
        count = 0
        while True:
            s1, s2 = self.rnd.pick_n(2, list(range(len(subjects_))))
            sex = 1 if self.rnd.coin() else 0
            e = make_expr([
                self.rnd.pick('&&', '||'),
                [ '==', 'Пол', sex ],
                [ self.rnd.pick(ops::comp), subjects_[s1, s2] ],
            ])
            count = table.select([], e).count()
            if count and count < table.count():
                sex = sex ? q~'м'~ : q~'ж'~;
                cond = html.cdata(e.to_lang_named('Alg'))
                last;
            }
        }
        table.update(make_block [ '=', 'Пол', lambda x: 'м' if x[0]['Пол'] else 'ж' ])
        self.text =
            "Результаты тестирования представлены в таблице\n" . table.table_html() . "\n" .
            "Сколько записей в ней удовлетворяют условию «$cond»?",
        self.variants(count, self.rnd.pick_n(3, grep $_ != $count, 1 .. $table->count));
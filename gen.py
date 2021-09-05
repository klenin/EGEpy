import sys

import EGE.GenBase
import EGE.Html
import EGE.Random
import EGE.Gen.EGE.A01
import EGE.Gen.EGE.A03

rnd = EGE.Random.Random(2342134)

questions = [ q.generate() for q in [
    EGE.Gen.EGE.A01.Recode(rnd),
    EGE.Gen.EGE.A01.Simple(rnd),
    EGE.Gen.EGE.A03.Ones(rnd),
] ]

if not sys.stdout.isatty():
    sys.stdout.reconfigure(encoding='utf-8')
print(EGE.Html.make_html(questions))

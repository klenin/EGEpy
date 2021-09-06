import sys

import EGE.GenBase
import EGE.Html
import EGE.Random
from EGE.Gen.EGE import A01, A02, A03

rnd = EGE.Random.Random(2342134)

questions = [ q.generate() for q in [
    A01.Recode(rnd),
    A01.Simple(rnd),
    A02.SportsmanNumbers(rnd),
    A02.CarNumbers(rnd),
    A03.Ones(rnd),
] ]

if not sys.stdout.isatty():
    sys.stdout.reconfigure(encoding='utf-8')
print(EGE.Html.make_html(questions))

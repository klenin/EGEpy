import EGE.GenBase
import EGE.Html
import EGE.Random
import EGE.Gen.EGE.A03

rnd = EGE.Random.Random(2342134)

questions = [
    EGE.Gen.EGE.A03.Ones(rnd).generate(),
    EGE.Gen.EGE.A03.Ones(rnd).generate(),
    EGE.GenBase.SingleChoice(rnd, 'q2', 1).set_variants([ 'v1', 'v2', 'v3' ]),
]

print(EGE.Html.make_html(questions))

import sys

import EGE.GenBase
import EGE.Html
import EGE.Random
from EGE.Gen.EGE import A01, A02, A03, A04, A05, A10, A11, A12, A13

rnd = EGE.Random.Random(2342134)

questions = [q.generate() for q in [
    A01.Recode(rnd),
    A01.Simple(rnd),
    A02.SportsmanNumbers(rnd),
    A02.CarNumbers(rnd),
    A02.Units(rnd),
    A02.MinRoutes(rnd),
    A02.SportAthleteNumbers(rnd),
    A03.Ones(rnd),
    A04.SumNumbers(rnd),
    A04.CountZeroOne(rnd),
    A05.Arith(rnd),
    A05.DivMod10(rnd),
    A05.DivModRotate(rnd),
    A05.DigitByDigit(rnd),
    A05.CRC(rnd),
    A10.GraphByMatrix(rnd),
    A10.LightPanel(rnd),
    A10.MinAlphabet(rnd),
    A11.VariableLength(rnd),
    A11.FixedLength(rnd),
    A11.PasswordLength(rnd),
    A12.Beads(rnd),
    A12.ArrayFlip(rnd),
    A13.GetFileNameByMask(rnd),
    A13.GetFileNameByFourMasks(rnd),
    A13.GetMaskByTwoFileNames(rnd),
]]

if not sys.stdout.isatty():
    sys.stdout.reconfigure(encoding='utf-8') # type: ignore
print(EGE.Html.make_html(questions))

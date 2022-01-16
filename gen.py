import sys

import EGE.GenBase
import EGE.Html
import EGE.Random
from EGE.Gen.EGE import A01, A02, A03, A04, A05, A07, A08, A09, A10, A11, A12, A13, A15, A16, A17, A18, B01, B02, B03, B04, B06

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
    A07.Names(rnd),
    A07.Animals(rnd),
    A07.RandomSequences(rnd),
    A07.RestorePassword(rnd),
    A07.SpreadsheetShift(rnd),
    A08.Equiv3(rnd),
    A08.Equiv4(rnd),
    A08.AudioSize(rnd),
    A08.AudioTime(rnd),
    A09.TruthTableFragment(rnd),
    A09.FindVarLenCode(rnd),
    A09.ErrorCorrectionCode(rnd),
    A09.HammingCode(rnd),
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
    A15.RGB(rnd),
    A16.Spreadsheet(rnd),
    A17.Diagram(rnd),
    A18.RobotLoop(rnd),
    B01.Recode2(rnd),
    B01.Direct(rnd),
    B02.Flowchart(rnd),
    B02.SimpleWhile(rnd),
    B03.Q1234(rnd),
    B03.LastDigit(rnd),
    B03.LastDigitBase(rnd),
    B03.CountDigits(rnd),
    B03.SimpleEquation(rnd),
    B03.CountOnes(rnd),
    B03.MusicTimeToTime(rnd),
    B03.MusicSizeToSize(rnd),
    B03.MusicFormatTimeToTime(rnd),
    B03.SelectBase(rnd),
    B03.MoveNumber(rnd),
    B03.RangeCount(rnd),
    B03.MinRequiredBase(rnd),
    B04.ImplBorder(rnd),
    B06.Solve(rnd),
    B06.RecursiveFunction(rnd),
    B06.PasswordMeta(rnd),
]]

if not sys.stdout.isatty():
    sys.stdout.reconfigure(encoding='utf-8') # type: ignore
print(EGE.Html.make_html(questions))

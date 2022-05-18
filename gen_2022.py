import sys

import EGE.GenBase
import EGE.Html
import EGE.Random

from EGE.Gen.EGE2022 import N03, N05, N06, N07, N08, N11, N14, N18, N19

rnd = EGE.Random.Random(2342134)

questions = [q.generate() for q in [
    N03.GenDatabase(rnd),
    N05.FindNumber(rnd),
    N05.MinAddDigits(rnd),
    N05.Draftsman(rnd),
    N05.RobotMigrant(rnd),
    N05.RobotAndIronCurtain(rnd),
    N05.Grasshopper(rnd),
    N05.CalculatorBothWays(rnd),
    N05.FourDigitNumber(rnd),
    N05.ThreeDigitNumber(rnd),
    N05.FiveDigitNumber(rnd),
    N05.NaturalNumber(rnd),
    N05.FourDigitOddNumber(rnd),
    N05.RemainderOfDivision(rnd),
    N05.RemoveLastBit(rnd),
    N05.EightBitNumber(rnd),
    N05.EvenOddNumber(rnd),
    N05.BitsSumRemainder(rnd),
    N05.EvenOddBitsSum(rnd),
    N05.ReverseBits(rnd),
    N05.ComparingZerosAndOnes(rnd),
    N05.TernaryNumber(rnd),
    N06.SumOfTwoLinearFunctions(rnd),
    N06.ArithmeticProgression(rnd),
    N06.TwoLinearFunctions(rnd),
    N06.InputTwoLinearFunctions(rnd),
    N07.ImageTransferTime(rnd),
    N07.ImageStorageSize(rnd),
    N07.ImageStoragePalette(rnd),
    N07.ImageStorageResizePalette(rnd),
    N07.ImageStoragePicturesN(rnd),
    N07.ImageStoragePicturesNForPeriod(rnd),
    N07.ImageStoragePicturesNPalette(rnd),
    N07.ImageStorageDpiSize(rnd),
    N07.ImageStorageDpiResize(rnd),
    N07.TextTransferTime(rnd),
    N07.TextTransferDataLength(rnd),
    N07.TextFileResizeDiff(rnd),
    N07.TextFileResizeSymbolsN(rnd),
    N08.ChessCellEncoding(rnd),
    N08.PositiveInts(rnd),
    N08.TicTacToe(rnd),
    N08.BlackWhiteBalls(rnd),
    N08.BlackWhiteBalls2(rnd),
    N08.Pencils(rnd),
    N08.Pencils2(rnd),
    N08.VasyaMarks(rnd),
    N08.WordCount(rnd),
    N08.WordCount2(rnd),
    N08.LightPanel(rnd),
    N08.LightPanel2(rnd),
    N08.WordsWithRestrictions(rnd),
    N08.WordEncoding(rnd),
    N08.WordEncoding2(rnd),
    N08.WordEncoding3(rnd),
    N08.WordEncoding4(rnd),
    N11.AmountOfInformationSport(rnd),
    N11.AmountOfInformationPasswordsExtra(rnd),
    N11.AmountOfInformationPasswords(rnd),
    N11.AmountOfInformationCars(rnd),
    N14.DirectSumDigits(rnd),
    N18.RobotExecuter(rnd),
    N19.MinimalOneHeapSize(rnd),
    N19.MinimalTwoHeapSize(rnd),
]]

if not sys.stdout.isatty():
    sys.stdout.reconfigure(encoding='utf-8') # type: ignore
print(EGE.Html.make_html(questions))

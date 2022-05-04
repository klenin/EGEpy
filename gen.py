import sys

import EGE.GenBase
import EGE.Html
import EGE.Random

from EGE.Gen.EGE import A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, A11, A12, A13, A15, A16, A17, A18
from EGE.Gen.EGE import B01, B02, B03, B04, B05, B06, B07, B08, B10, B11, B12, B13, B14, B15
from EGE.Gen.EGE import Z06, Z09, Z10, Z11, Z12, Z13, Z15, Z16, Z18, Z22

from EGE.Gen.EGE2022 import N03, N05, N06, N07, N11, N14

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
    A06.CountBySign(rnd),
    A06.FindMinMax(rnd),
    A06.CountOddEven(rnd),
    A06.AlgMinMax(rnd),
    A06.AlgAvg(rnd),
    A06.BusStation(rnd),
    A06.CrcMessage(rnd),
    A06.InfSize(rnd),
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
    B04.LexOrder(rnd),
    B04.Morse(rnd),
    B04.Bulbs(rnd),
    B04.PlusMinus(rnd),
    B04.LetterCombinatorics(rnd),
    B04.SignalRockets(rnd),
    B04.HowManySequences1(rnd),
    B04.HowManySequences2(rnd),
    B05.Calculator(rnd),
    B05.ComleteSpreadsheet(rnd),
    B05.AdslSpeed(rnd),
    B06.Solve(rnd),
    B06.RecursiveFunction(rnd),
    B06.PasswordMeta(rnd),
    B07.WhoIsRight(rnd),
    B08.IdentifyLetter(rnd),
    B08.FindCalcSystem(rnd),
    B08.FirstSumDigits(rnd),
    B10.TransRate(rnd),
    B10.TransTime(rnd),
    B10.TransLatency(rnd),
    B10.MinPeriodOfTime(rnd),
    B10.TransText(rnd),
    B10.TransTimeSize(rnd),
    B11.IpMask(rnd),
    B11.SubnetMask(rnd),
    B12.SearchQuery(rnd),
    B13.PlusMinus(rnd),
    B14.FindFuncMin(rnd),
    B15.LogicVarSet(rnd),
    Z06.FindNumber(rnd),
    Z06.Grasshopper(rnd),
    Z06.MinAddDigits(rnd),
    Z09.GetMemorySize(rnd),
    Z10.WordsCount(rnd),
    Z11.RecursiveAlg(rnd),
    Z12.IpComputerNumber(rnd),
    Z13.Tumblers(rnd),
    Z13.TumblersMin(rnd),
    Z13.YoungSpy(rnd),
    Z15.CityRoads(rnd),
    Z16.BaseGcd(rnd),
    Z18.BitwiseConjunction(rnd),
    Z22.CalculatorFindPrgmCount(rnd),
]]

questions_2022 = [q.generate() for q in [
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
    N11.AmountOfInformationSport(rnd),
    N11.AmountOfInformationPasswordsExtra(rnd),
    N11.AmountOfInformationPasswords(rnd),
    N11.AmountOfInformationCars(rnd),
    N14.DirectSumDigits(rnd),
]]

if not sys.stdout.isatty():
    sys.stdout.reconfigure(encoding='utf-8') # type: ignore
print(EGE.Html.make_html(questions_2022))
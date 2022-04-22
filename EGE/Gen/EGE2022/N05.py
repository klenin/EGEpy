from dataclasses import dataclass
from math import dist

from ..EGE.Z06 import FindNumber, MinAddDigits, Grasshopper
from ..EGE.B05 import Calculator

from ...Bits import Bits
from ...GenBase import DirectInput

import EGE.Random

class FindBinaryNumber(FindNumber):
    pass

class MachineMinAddDigits(MinAddDigits):
    pass

@dataclass
class Offset:
    x: float = 0
    y: float = 0

    @property
    def distance(self) -> float:
        return dist([self.x, self.y], [0, 0])

class Draftsman(DirectInput):
    def generate(self):
        algorithm, self.correct = self._generate_algorithm()
        self.text = f"""
            Исполнитель Чертежник имеет перо, которое можно поднимать, опускать и перемещать. При перемещении опущенного
            пера за ним остается след в виде прямой линии. У исполнителя существуют следующие команды:<br/>Сместиться на
            вектор (а, b) – исполнитель перемещается в точку, в которую можно попасть из данной, пройдя а единиц по
            горизонтали и b – по вертикали.<br/>Запись: Повторить 5 [Команда 1 Команда 2] означает, что
            последовательность команд в квадратных скобках повторяется 5 раз.<br/>Чертежник находится в начале
            координат. Чертежнику дан для исполнения следующий алгоритм:<br/><b>{algorithm}</b>На каком расстоянии от
            начала координат будет находиться исполнитель Чертежник в результате выполнения данного алгоритма?<br/>
            <b>В ответе отбросьте дробную часть.</b>"""
        self.accept_number()

        return self

    def _generate_algorithm(self) -> (str, int):
        actions = {0: "Сместиться на вектор", 1: "Повторить"}
        offset = Offset()
        algorithm = ""
        for i in range(4):
            x_offset = self.rnd.in_range(-10, 10)
            y_offset = self.rnd.in_range(-10, 10)
            repeats = 1
            if self.rnd.coin():
                repeats = self.rnd.in_range(1, 3)
                algorithm += f"{actions[1]} {repeats} [{actions[0]} ({x_offset}, {y_offset})]<br/>"
            else:
                algorithm += f"{actions[0]} ({x_offset}, {y_offset})<br/>"

            offset.x += repeats * x_offset
            offset.y += repeats * y_offset

        return algorithm, int(offset.distance)

class Robot(DirectInput):
    def __init__(self, rnd: EGE.Random.Random, text: str = None, correct: int = 0):
        super().__init__(rnd, text, correct)
        self.directions = {1: "вверх", 2: "вниз", 3: "вправо", 4: "влево"}
        self.opposite_directions = {1: 2, 2: 1, 3: 4, 4: 3}

    def _generate_path(self, length: int = 10) -> list:
        if length < 1:
            raise ValueError(f"Path length must be greater or equal to 1, {length} given")

        path = [self.rnd.pick(list(self.directions))]
        for i in range(1, length):
            path.append(self.rnd.pick(list(self.directions), self.opposite_directions[int(path[i - 1])]))

        return path

class RobotMigrant(Robot):
    def generate(self):
        path = self._generate_path(8)

        tasks = [
            "Укажите наименьшее возможное число команд, которое необходимо для того, чтобы Робот вернулся в ту же"
            "клетку, из которой начал движение.",
            "Укажите наименьшее возможное число команд в программе, переводящей Робота из той же начальной клетки в ту"
            "же конечную.",
            "Укажите наименьшее возможное число команд в программе, которая вернет Робота в начальную точку.",
        ]

        self.text = f"""
            Исполнитель Робот ходит по клеткам бесконечной вертикальной клетчатой доски, переходя
            по одной из команд <b>вверх</b>, <b>вниз</b>, <b>вправо</b>, <b>влево</b> в соседнюю
            клетку в указанном направлении. Робот выполнил следующую программу:<br/>
            <b>{"<br/>".join([self.directions[direction] for direction in path])}</b><br/>{self.rnd.pick(tasks)}"""

        self.correct = self._get_min_path_length(path)
        self.accept_number()

        return self

    def _get_min_path_length(self, path: list) -> int:
        directions_sums = {i: 0 for i in list(self.directions)}
        for direction in path:
            directions_sums[direction] += 1

        return abs(directions_sums[1] - directions_sums[2]) + abs(directions_sums[3] - directions_sums[4])

class RobotAndIronCurtain(Robot):
    def generate(self):
        path = self._generate_path(7)

        self.text = f"""
            Исполнитель Робот действует на клетчатой доске, между соседними клетками которой могут стоять стены.
            Робот передвигается по клеткам доски и может выполнять команды <b>1 (вверх)</b>, <b>2 (вниз)</b>,
            <b>3 (вправо)</b> и <b>4 ( влево)</b>, переходя на соседнюю клетку в направлении, указанном в скобках.
            Если в этом направлении между клетками стоит стена, то Робот разрушается. Робот успешно выполнил
            программу<br/><b>{"".join(map(str, path))}</b>.<br/>Какую последовательность из четырех команд должен
            выполнить Робот, чтобы вернуться в ту клетку, где он был перед началом выполнения программы, и не
            разрушиться вне зависимости от того, какие стены стоят на поле?"""

        path = self._remove_cycles(path)
        self.correct = int("".join(map(str, self._get_reversed_path(path))))
        self.accept_number()

        return self

    def _remove_cycles(self, path: list) -> list:
        cycles = ["1324", "1423", "2314", "2413", "3142", "3241", "4132", "4231"]
        path = "".join(map(str, path))
        for cycle in cycles:
            path = path.replace(cycle, '')

        return list(map(int, path))

    def _get_reversed_path(self, path: list) -> list:
        return [self.opposite_directions[direction] for direction in reversed(path)]

class CalculatorBothWays(Calculator):
    def _get_commands(self):
        v1 = self.rnd.in_range(1, 9)
        v2 = self.rnd.in_range(2, 5)
        v3 = self.rnd.in_range(1, 4)

        return [[
            f"прибавь {v1}",
            f"прибавляет к числу на экране {v1}",
            f"прибавляет к нему {v1}",
            lambda x: x + v1,
        ], [
            f"умножь на {v2}",
            f"умножает число на экране на {v2}",
            f"умножает его на {v2}",
            lambda x: x * v2,
        ], [
            "возведи в квадрат",
            "возводит число на экране в квадрат",
            "возводит его в квадрат",
            lambda x: x ** 2,
        ], [
            f"""{self.rnd.pick(["вычти", "отними"])} {v3}""",
            f"уменьшает число на экране на {v3}",
            f"отнимает от числа на экране {v3}",
            lambda x: x - v3,
        ], ]

class DecimalSymbolConversion(DirectInput):
    def __init__(self, rnd: EGE.Random.Random):
        super().__init__(rnd)

        self.selections = [{
            "function": min,
            "text": "Укажите <b>наименьшее</b> число, в результате обработки которого автомат выдаст число",
        }, {
            "function": max,
            "text": "Укажите <b>наибольшее</b> число, в результате обработки которого автомат выдаст число",
        }, {
            "function": len,
            "text": "<b>Сколько</b> существует чисел, в результате обработки которых автомат выдаст число",
        }, ]
        self.actions = [
            {"operator": '*', "function": self._get_product, "verb": "Перемножаются", "noun": "Произведения"},
            {"operator": '+', "function": self._get_sum, "verb": "Складываются", "noun": "Суммы"},
        ]
        self.sorts = [
            {"reverse": True, "text": ["убывания", "невозрастания"]},
            {"reverse": False, "text": ["возрастания", "неубывания"]},
        ]

    def _get_possible_results(self, number_of_digits: int, function, remove_min_processed_digit: bool, reverse: bool, step: int = 1) -> dict:
        results = {}
        for number in range(10 ** (number_of_digits - 1), 10 ** number_of_digits):
            processed_digits = self._get_processed_digits(number, function, step)
            if remove_min_processed_digit:
                processed_digits.remove(min(processed_digits))
            processed_digits.sort(reverse=reverse)
            result = int("".join(map(str, processed_digits)))
            if result in list(results):
                results[result].append(number)
            else:
                results[result] = [number]

        return results

    def _get_processed_digits(self, number: int, function, step: int = 1) -> list:
        string_number = str(number)
        if len(string_number) == 5:
            processed = [int(string_number[0]), int(string_number[1])]
            for i, digit in enumerate(string_number[2:]):
                processed[i % 2] = function(processed[i % 2], int(digit))
        else:
            processed = []
            for _ in range(len(string_number) - step):
                processed.append(function(number % 10, number // 10 % 10))
                number //= 10 ** step

        return processed

    def _get_sum(self, a: int, b: int) -> int:
        return a + b

    def _get_product(self, a: int, b: int) -> int:
        return a * b

class ThreeDigitNumber(DecimalSymbolConversion):
    def generate(self):
        number_of_digits = 3
        sort = self.rnd.pick(self.sorts)
        action = self.rnd.pick(self.actions)
        selection = self.rnd.pick(self.selections)

        possible_results = self._get_possible_results(
            number_of_digits=number_of_digits,
            function=action["function"],
            remove_min_processed_digit=False,
            reverse=sort["reverse"],
        )
        result = self.rnd.pick(list(possible_results))
        initial = selection["function"](possible_results[result])

        example_text = f"""
            <i>Пример.</i> Исходное число: 348. {action["noun"]}: 3 {action["operator"]} 4 = {action["function"](3, 4)};
            4 {action["operator"]} 8 = {action["function"](4, 8)}. Результат:
            {"".join(map(str, sorted([action["function"](3, 4), action["function"](4, 8)], reverse=sort["reverse"])))}.
            <br/>"""

        self.text = f"""
            Автомат получает на вход трёхзначное число. По этому числу строится новое число по следующим правилам.
            <ol><li>{action["verb"]} первая и вторая, а также вторая и третья цифры исходного числа.</li><li>Полученные
            два числа записываются друг за другом в порядке {sort["text"][self.rnd.coin()]} (без разделителей).
            </li></ol>{example_text}{selection["text"]} <b>{result}</b>."""
        self.correct = initial
        self.accept_number()

        return self

class FourDigitNumber(DecimalSymbolConversion):
    def generate(self):
        number_of_digits = 4
        sort = self.rnd.pick(self.sorts)
        action = self.rnd.pick(self.actions)
        selection = self.rnd.pick(self.selections, self.selections[2])
        variant = self.rnd.pick([{
            "step": 1,
            "remove_min_processed_digit": True,
            "text": f"""{action["verb"]} отдельно первая и вторая, вторая и третья, третья и четвёртая цифры числа.""",
        }, {
            "step": 2,
            "remove_min_processed_digit": False,
            "text": f"""{action["verb"]} первая и вторая, а также третья и четвёртая цифры исходного числа.""",
        }, ])

        possible_results = self._get_possible_results(
            number_of_digits=number_of_digits,
            function=action["function"],
            remove_min_processed_digit=variant["remove_min_processed_digit"],
            reverse=sort["reverse"],
            step=variant["step"],
        )
        result = self.rnd.pick(list(possible_results))
        initial = selection["function"](possible_results[result])

        self.text = f"""
            Автомат получает на вход четырёхзначное число (число не может начинаться с нуля). По этому
            числу строится новое число по следующим правилам.<ol><li>{variant["text"]}</li>
            {"<li>Наименьшее из полученных чисел удаляется.</li>" if variant["remove_min_processed_digit"] else ""}
            <li>Получившиеся два числа записываются друг за другом в порядке {sort["text"][self.rnd.coin()]} без
            разделителей.</li></ol>{selection["text"]} <b>{result}</b>.<br/>
            {"<b>Примечание.</b> Если меньшие из чисел равны на 2 шаге, то отбрасывают только одно число."
            if variant["remove_min_processed_digit"] else ""}"""
        self.correct = initial
        self.accept_number()

        return self

class FiveDigitNumber(DecimalSymbolConversion):
    def generate(self):
        number_of_digits = 5
        action = self.actions[1]
        sort = self.sorts[1]
        selection = self.selections[0]

        possible_results = self._get_possible_results(
            number_of_digits=number_of_digits,
            function=action["function"],
            remove_min_processed_digit=False,
            reverse=sort["reverse"],
        )
        result = self.rnd.pick(list(possible_results))
        initial = selection["function"](possible_results[result])

        example_text = f"""
            <i>Пример.</i> Исходное число: 63179. {action["noun"]}: 6 {action["operator"]} 1 {action["operator"]} 9 =
            {action["function"](action["function"](6, 1), 9)}; 3 {action["operator"]} 7 = {action["function"](3, 7)}.
            Результат: {"".join(map(str, sorted([action["function"](action["function"](6, 1), 9), action["function"](3, 7)], reverse=sort["reverse"])))}.
            <br/>"""

        self.text = f"""
            Автомат получает на вход пятизначное число. По этому числу строится новое число по следующим правилам.
            <ol><li>{action["verb"]} отдельно первая, третья и пятая цифры, а также вторая и четвёртая цифры.</li>
            <li>Полученные два числа записываются друг за другом в порядке {sort["text"][self.rnd.coin()]} без 
            разделителей.</li></ol>{example_text}{selection["text"]} <b>{result}</b>."""
        self.correct = initial
        self.accept_number()

        return self

class NaturalNumber(DirectInput):
    def generate(self):
        possible_results = self._get_possible_results()
        result = self.rnd.pick(list(possible_results))
        initial = possible_results[result]

        self.text = f"""
            На вход алгоритма подаётся натуральное число N. Алгоритм строит по нему новое число следующим образом.
            <ol><li>Из цифр, образующих десятичную запись N, строятся наибольшее и наименьшее возможные двузначные числа
            (числа не могут начинаться с нуля).</li><li>На экран выводится разность полученных двузначных чисел.</li>
            </ol><i>Пример.</i> Дано число N = 238. Алгоритм работает следующим образом:<ol><li>Наибольшее двузначное
            число из заданных цифр — 83, наименьшее - 23.</li><li>На экран выводится разность 83 − 23 = 60.</li></ol>
            Чему равно <b>наименьшее</b> возможное <b>трёхзначное</b> число N, в результате обработки которого на экране
            автомата появится число <b>{result}</b>?"""
        self.correct = initial
        self.accept_number()

        return self

    def _get_possible_results(self):
        results = {}
        for number in range(101, 1000):
            digits = sorted([int(a) for a in str(number)])
            max_number = int(str(digits[2]) + str(digits[1]))
            min_number = int(str(digits[0]) + str(digits[1])) if digits[0] != 0 else int(str(digits[1]) + str(digits[0]))
            result = max_number - min_number
            results[result] = min(results[result], number) if result in list(results) else number

        return results

class BinaryNumberMachine(DirectInput):
    def generate(self):
        result = self.rnd.in_range(2, 3000, 13)
        number = Bits().set_dec(result)
        last_bits = number.get_bits()[-2:]
        initial = Bits().set_bin_array(number.get_bits()[:-2] + ([1 if last_bits == [1, 0] else 0])).get_dec()

        self.text = f"""
            Автомат обрабатывает натуральное число N > 1 по следующему алгоритму.<br/><ol><li>Строится
            двоичная запись числа N.</li><li>Последняя цифра двоичной записи удаляется.</li><li>Если исходное число N
            было нечётным, в конец записи (справа) дописываются цифры 10, если чётным - 01.</li><li>Результат
            переводится в десятичную систему и выводится на экран.</li></ol><br/><i>Пример.</i> Дано число 
            N = 13. Алгоритм работает следующим образом. <ol><li>Двоичная запись числа N: 1101.</li>
            <li>Удаляется последняя цифра, новая запись: 110.</li><li>Исходное число нечётно, дописываются цифры 10,
            новая запись: 11010</li><li>На экран выводитсячисло 26.</li></ol>Какое число нужно ввести в автомат,
            чтобы в результате получилось <b>{result}</b>?"""
        self.correct = initial
        self.accept_number()

        return self

class EightBitNumber(DirectInput):
    def generate(self):
        initial = self.rnd.in_range(128, 255, 131)
        result = 2 * initial - 255

        self.text = f"""
            Автомат обрабатывает натуральное число N (128 ≤ N ≤ 255) по следующему алгоритму:
            <ol><li>Строится восьмибитная двоичная запись числа N.</li>
            <li>Все цифры двоичной записи заменяются на противоположные (0 на 1, 1 на 0).</li>
            <li>Полученное число переводится в десятичную запись.</li>
            <li>Из исходного числа вычитается полученное, разность выводится на экран.</li></ol>
            <i>Пример.</i> Дано число N = 131. Алгоритм работает следующим образом:
            <ol><li>Восьмибитная двоичная запись числа N: 10000011.</li>
            <li>Все цифры заменяются на противоположные, новая запись: 01111100.</li>
            <li>Десятичное значение полученного числа: 124.</li>
            <li>На экран выводится число: 131 – 124 = 7.</li></ol>
            Какое число нужно ввести в автомат, чтобы в результате получилось <b>{result}</b>?"""
        self.correct = initial
        self.accept_number()

        return self

class LessOrEqualMachine(DirectInput):
    def generate(self):
        target = self.rnd.in_range(100, 3000)
        number = target
        while True:
            bits = Bits().set_dec(number).get_bits()
            last_bits = bits[-2:]
            if last_bits != [1, 1] and last_bits != [0, 0]:
                if last_bits == [0, 1] and Bits().set_bin_array(bits[:-2]).get_dec() % 2 == 1:
                    break
                if last_bits == [1, 0] and Bits().set_bin_array(bits[:-2]).get_dec() % 2 == 0:
                    break
            number -= 1

        self.text = f"""
            Автомат обрабатывает натуральное число N по следующему алгоритму: <ol><li>Строится двоичная запись числа
            N.</li><li>К этой записи дописываются справа ещё два разряда по следующему правилу: если N чётное,
            в конец числа (справа) дописывается 10, в противном случае справа дописывается 01. Например, двоичная
            запись 1001 числа 9 будет преобразована в 100101.</li></ol>Полученная таким образом запись
            (в ней на два разряда больше, чем в записи исходного числа N) является двоичной записью числа — результата
            работы данного алгоритма.<br/>Укажите максимальное число R, которое не превышает <b>{target}</b> и
            может являться результатом работы данного алгоритма. В ответе это число запишите в десятичной
            системе счисления."""
        self.correct = number
        self.accept_number()

        return self

class ReverseBitsMachine(DirectInput):
    def generate(self):
        result = self.rnd.in_range(1, 50)
        limit = self.rnd.in_range(100, 300)
        bits = Bits().set_dec(result).reverse_().get_bits()
        index = self._get_valuable_index(bits)
        del bits[:index]
        while True:
            if Bits().set_bin_array(bits).get_dec() > limit:
                break
            bits.append(0)

        self.text = f"""
            Автомат обрабатывает натуральное число N по следующему алгоритму:<ol><li>Строится двоичная запись
            числа N.</li><li>Запись «переворачивается», то есть читается справа налево. Если при этом
            появляются ведущие нули, они отбрасываются.</li><li>Полученное число переводится в десятичную
            запись и выводится на экран.</li></ol><i>Пример</i>. Дано число N = 58. Алгоритм работает следующим образом.
            <ol><li>Двоичная запись числа N: 111010.</li><li>Запись справа налево: 10111 (ведущий ноль отброшен).</li>
            <li>На экран выводится десятичное значение полученного числа 23.</li></ol>Какое наибольшее число,
            не превышающее <b>{limit}</b>, после обработки автоматом даёт результат <b>{result}</b>?"""
        self.correct = Bits().set_bin_array(bits[:-1]).get_dec()
        self.accept_number()

        return self

    def _get_valuable_index(self, bits: list) -> int:
        index = -1
        for i, bit in enumerate(bits):
            if bit == 1:
                index = i
                break

        return index

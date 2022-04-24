from abc import abstractmethod
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

    def _get_possible_results(self, number_of_digits: int, function, remove_min_processed_digit: bool, reverse: bool,
                              step: int = 1, only_odd_digits: bool = False) -> dict:
        results = {}
        for number in range(10 ** (number_of_digits - 1), 10 ** number_of_digits):
            if only_odd_digits and not self._odd_parity_check(number):
                continue

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

    def _odd_parity_check(self, number: int) -> bool:
        for digit in str(number):
            if int(digit) % 2 == 0:
                return False

        return True

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

class FourDigitOddNumber(DecimalSymbolConversion):
    def generate(self):
        number_of_digits = 4
        sort = self.sorts[1]
        action = self.actions[1]
        selection = self.selections[2]

        possible_results = self._get_possible_results(
            number_of_digits=number_of_digits,
            function=action["function"],
            remove_min_processed_digit=False,
            reverse=sort["reverse"],
            step=2,
            only_odd_digits=True,
        )
        result = self.rnd.pick(list(possible_results))
        initial = selection["function"](possible_results[result])

        self.text = f"""
            Автомат получает на вход четырёхзначное десятичное число, в котором все цифры <b>нечётные</b>.
            По этому числу строится новое число по следующим правилам.<ol><li>{action["verb"]} первая и вторая,
            а также третья и четвёртая цифры исходного числа.</li><li>Получившиеся два числа записываются
            друг за другом в порядке {sort["text"][self.rnd.coin()]} без разделителей.</li></ol>{selection["text"]}
            <b>{result}</b>.<br/>"""
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

    def _get_possible_results(self) -> dict:
        results = {}
        for number in range(101, 1000):
            digits = sorted([int(a) for a in str(number)])

            max_number = int(str(digits[2]) + str(digits[1]))
            if digits[0] != 0:
                min_number = int(str(digits[0]) + str(digits[1]))
            else:
                min_number = int(str(digits[1]) + str(digits[0]))

            result = max_number - min_number
            results[result] = min(results[result], number) if result in list(results) else number

        return results

class RemainderOfDivision(DirectInput):
    def generate(self):
        possible_results = self._get_possible_results()
        result = self.rnd.pick(list(possible_results))
        initial = possible_results[result]

        self.text = f"""
            Автомат получает на вход <b>нечётное</b> число X. По этому числу строится трёхзначное число Y по следующим
            правилам.<ol><li>Первая цифра числа Y (разряд сотен) — остаток от деления X на 4.</li><li>Вторая цифра
            числа Y (разряд десятков) — остаток от деления X на 3.</li><li>Третья цифра числа Y (разряд единиц) —
            остаток от деления X на 2.</li></ol><i>Пример.</i> Исходное число: 63179. Остаток от деления на 4 равен 3;
            остаток от деления на 3 равен 2; остаток от деления на 2 равен 1. Результат работы автомата: 321.<br/>
            Укажите <b>наименьшее двузначное</b> число, при обработке которого автомат выдаёт результат {result}."""
        self.correct = initial
        self.accept_number()

        return self

    def _get_possible_results(self) -> dict:
        results = {}
        for number in range(10, 100):
            if number % 2 == 0:
                continue
            result = (number % 4) * 100 + (number % 3) * 10 + (number % 2)
            results[result] = min(results[result], number) if result in list(results) else number

        return results

class RemoveLastBit(DirectInput):
    def generate(self):
        result = self.rnd.in_range(1000, 3000, 26)
        number = Bits().set_dec(result)
        last_bits = number.get_bits()[-2:]
        initial = Bits().set_bin_array(number.get_bits()[:-2] + ([1 if last_bits == [1, 0] else 0])).get_dec()

        self.text = f"""
            Автомат обрабатывает натуральное число N > 1 по следующему алгоритму.<br/><ol><li>Строится
            двоичная запись числа N.</li><li>Последняя цифра двоичной записи удаляется.</li><li>Если исходное число N
            было нечётным, в конец записи (справа) дописываются цифры <b>10</b>, если чётным - <b>01</b>.</li><li>
            Результат переводится в десятичную систему и выводится на экран.</li></ol><i>Пример.</i> Дано число 
            N = 13. Алгоритм работает следующим образом.<ol><li>Двоичная запись числа N: 1101.</li>
            <li>Удаляется последняя цифра, новая запись: 110.</li><li>Исходное число нечётно, дописываются цифры 10,
            новая запись: 11010</li><li>На экран выводится число 26.</li></ol>Какое число нужно ввести в автомат,
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

class BinarySymbolConversion(DirectInput):
    def __init__(self, rnd: EGE.Random.Random):
        super().__init__(rnd)

        self.target = self.rnd.in_range(100, 300)
        self.task = self.rnd.pick([{
            "selection": [{
                "text": f"Укажите <b>максимальное</b> число R, которое <b>не превышает {self.target}</b>.",
                "get_initial": False,
            }, {
                "text": f"Укажите <b>максимальное</b> число N, для которого результат <b>не превышает {self.target}</b>.",
                "get_initial": True,
            }, ][self.rnd.coin()],
            "step": -1,
            "check_equal": True,
        }, {
            "selection": [{
                "text": f"Укажите <b>максимальное</b> число R, которое <b>меньше {self.target}</b>.",
                "get_initial": False,
            }, {
                "text": f"Укажите <b>максимальное</b> число N, для которого результат будет <b>меньше {self.target}</b>.",
                "get_initial": True,
            }, ][self.rnd.coin()],
            "step": -1,
            "check_equal": False,
        }, {
            "selection": [{
                "text": f"Укажите <b>минимальное</b> число R, которое <b>не меньше {self.target}</b>.",
                "get_initial": False,
            }, {
                "text": f"Укажите <b>минимальное</b> число N, для которого результат будет <b>не меньше {self.target}</b>.",
                "get_initial": True,
            }, ][self.rnd.coin()],
            "step": 1,
            "check_equal": True,
        },  {
            "selection": [{
                "text": f"Укажите <b>минимальное</b> число R, которое <b>больше {self.target}</b>.",
                "get_initial": False,
            }, {
                "text": f"Укажите <b>минимальное</b> число N, для которого результат будет <b>больше {self.target}</b>.",
                "get_initial": True,
            }, ][self.rnd.coin()],
            "step": 1,
            "check_equal": False,
        }, ])
        self.algorithm = ""
        self.example = ""

    def generate(self):
        self.text = f"""
            На вход алгоритма подаётся натуральное число N. Алгоритм строит по нему новое число R следующим
            образом. {self.algorithm}{self.example}{self.task["selection"]["text"]} В ответе укажите число в десятичной
            системе счисления, которое может являться результатом работы данного алгоритма."""
        self.correct = self._find_suitable_number(
            target=self.target,
            step=self.task["step"],
            check_equal=self.task["check_equal"],
            get_initial=self.task["selection"]["get_initial"],
        )
        self.accept_number()

        return self

    @abstractmethod
    def _find_suitable_number(self, target: int, step: int, check_equal: bool, get_initial: bool) -> int:
        pass

class EvenOddNumber(BinarySymbolConversion):
    def __init__(self, rnd: EGE.Random.Random):
        super().__init__(rnd)

        self.variant = self.rnd.pick([{
            "even": {"text": "чётное", "addition": [0, 1]},
            "odd": {"text": "нечётное", "addition": [1, 0]},
        }, {
            "even": {"text": "чётное", "addition": [1, 0]},
            "odd": {"text": "нечётное", "addition": [0, 1]},
        }, {
            "even": {"text": "чётное", "addition": [0, 0]},
            "odd": {"text": "нечётное", "addition": [1, 1]},
        }, ])
        self.algorithm = f"""
            <ol><li>Строится двоичная запись числа N.</li><li>К этой записи дописываются справа ещё
            два разряда по следующему правилу: если N {self.variant["even"]["text"]}, в конец числа
            (справа) дописывается <b>{"".join(map(str, self.variant["even"]["addition"]))}</b>, в противном
            случае справа дописывается <b>{"".join(map(str, self.variant["odd"]["addition"]))}</b>.</li></ol>
            Полученная таким образом запись (в ней на два разряда больше, чем в записи исходного числа N)
            является двоичной записью числа — результата работы данного алгоритма.<br/>"""
        self.example = f"""
            <i>Пример.</i> Двоичная запись 1001 числа 9 будет преобразована
            в 1001{"".join(map(str, self.variant["odd"]["addition"]))}.<br/>"""

    def _find_suitable_number(self, target: int, step: int, check_equal: bool, get_initial: bool) -> int:
        number = target if check_equal else target + step
        while True:
            bits = Bits().set_dec(number).get_bits()
            last_bits = bits[-2:]
            initial_number = Bits().set_bin_array(bits[:-2]).get_dec()
            if last_bits == self.variant["even"]["addition"] and initial_number % 2 == 0:
                break
            if last_bits == self.variant["odd"]["addition"] and initial_number % 2 == 1:
                break

            number += step

        return initial_number if get_initial else number

class BitsSumRemainder(BinarySymbolConversion):
    def __init__(self, rnd: EGE.Random.Random):
        super().__init__(rnd)

        self.algorithm = f"""
            <ol><li>Строится двоичная запись числа N.</li><li>К этой записи дописываются справа ещё два
            разряда по следующему правилу:<ol type="a"><li>складываются все цифры двоичной записи, и
            остаток от деления суммы на 2 дописывается в конец числа (справа);</li><li>над получившейся
            записью производятся те же действия — справа дописывается остаток от деления суммы цифр на 2.
            </li></ol></li></ol>Полученная таким образом запись (в ней на два разряда больше, чем в записи
            исходного числа N) является двоичной записью числа — результатаработы данного алгоритма.<br/>"""
        self.example = f"""<i>Пример.</i> Двоичная запись 11100 преобразуется в запись 1110010.<br/>"""

    def _find_suitable_number(self, target: int, step: int, check_equal: bool, get_initial: bool) -> int:
        number = target if check_equal else target + step
        while True:
            bits = Bits().set_dec(number).get_bits()
            last_bits = bits[-2:]
            if last_bits == [0, 0] and Bits().set_bin_array(bits[:-2]).count_ones() % 2 == 0:
                break
            if last_bits == [1, 0] and Bits().set_bin_array(bits[:-2]).count_ones() % 2 == 1:
                break

            number += step

        return number

class EvenOddBitsSum(BinarySymbolConversion):
    def __init__(self, rnd: EGE.Random.Random):
        super().__init__(rnd)

        self.algorithm = f"""
            <ol><li>Строится двоичная запись числа N.</li><li>К этой записи дописываются справа ещё два
            разряда по следующему правилу: складываются все цифры двоичной записи, если<ol type="a"><li>сумма
            нечетная, к числу дописывается <b>11</b>;</li><li>сумма четная, дописывается <b>00</b>.</li></ol>
            </li></ol>Полученная таким образом запись (в ней на два разряда больше, чем в записи исходного
            числа N) является двоичной записью числа — результата работы данного алгоритма.<br/>"""

    def _find_suitable_number(self, target: int, step: int, check_equal: bool, get_initial: bool) -> int:
        number = target if check_equal else target + step
        while True:
            bits = Bits().set_dec(number).get_bits()
            last_bits = bits[-2:]
            if last_bits == [0, 0] and Bits().set_bin_array(bits[:-2]).count_ones() % 2 == 0:
                break
            if last_bits == [1, 1] and Bits().set_bin_array(bits[:-2]).count_ones() % 2 == 1:
                break
            number += step

        return number

class ComparingZerosAndOnes(BinarySymbolConversion):
    def __init__(self, rnd: EGE.Random.Random):
        super().__init__(rnd)

        self.algorithm = f"""
            <ol><li>Строится двоичная запись числа N.</li><li>Если в полученной записи единиц больше, чем нулей, то
            справа приписывается <b>единица</b>. Если нулей больше или нулей и единиц поровну, то справа приписывается
            <b>ноль</b>.</li><li>Полученное число переводится в десятичную запись и выводится на экран.</li></ol>"""
        self.example = f"""
            <i>Пример.</i> Дано число N = 13. Алгоритм работает следующим образом.<ol><li>Двоичная запись
            числа N: 1101.</li><li>В записи больше единиц, справа приписывается единица: 11011.</li>
            <li>На экран выводится десятичное значение полученного числа 27.</li></ol>"""

    def _find_suitable_number(self, target: int, step: int, check_equal: bool, get_initial: bool) -> int:
        number = target if check_equal else target + step
        while True:
            bits = Bits().set_dec(number).get_bits()
            last_bit = bits[-1]
            ones_counter = Bits().set_bin_array(bits[:-1]).count_ones()
            zeros_counter = Bits().set_bin_array(bits[:-1]).get_size() - ones_counter
            if last_bit == 0 and zeros_counter >= ones_counter:
                break
            if last_bit == 1 and zeros_counter < ones_counter:
                break

            number += step

        return number

class ReverseBits(DirectInput):
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
            <li>На экран выводится десятичное значение полученного числа 23.</li></ol>Какое <b>наибольшее</b> число,
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

class TernaryNumber(DirectInput):
    def generate(self):
        variant = self.rnd.pick([{
            "text": "трёхзначное",
            "number_of_digits": 3,
        }, {
            "text": "четырёхзначное",
            "number_of_digits": 4,
        }, {
            "text": "пятизначное",
            "number_of_digits": 5,
        }, ])

        self.text = f"""
            Автомат обрабатывает натуральное число N по следующему алгоритму:<ol><li>Строится троичная запись
            числа N.</li><li>В конец записи (справа) дописывается остаток от деления числа N на <b>3</b>.</li><li>
            Результат переводится из троичной системы в десятичную и выводится на экран.</li></ol><i>Пример.</i>
            Дано число N = 11. Алгоритм работает следующим образом:<ol><li>Троичная запись числа N: 102.</li>
            <li>Остаток от деления 11 на 3 равен 2, новая запись 1022.</li><li>На экран выводится число 35.</li></ol>
            Какое <b>наименьшее {variant["text"]}</b> число может появиться на экране в результате работы автомата?"""
        self.correct = self._find_suitable_number(variant["number_of_digits"])
        self.accept_number()

        return self

    def _find_suitable_number(self, number_of_digits: int) -> int:
        for number in range(10 ** (number_of_digits - 1), 10 ** number_of_digits):
            ternary = self._get_ternary_array(number)
            if ternary[-2] == ternary[-1]:
                return number

        return -1

    def _get_ternary_array(self, number: int) -> list:
        if number == 0:
            return [0]
        digits = []
        while number:
            number, r = divmod(number, 3)
            digits.append(r)

        return digits[::-1]

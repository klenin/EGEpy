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

    def _generate_path(self, length: int = 10):
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
            "Укажите наименьшее возможное число команд в программе, которая вернет Робота в начальную точку."
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

class FourDigitNumber(DirectInput):
    def generate(self):
        initial = self.rnd.in_range(1000, 9999, 1982)
        sums = self._get_digits_sums(initial)
        sums.remove(min(sums))
        sums.sort()
        result = int("".join(map(str, sums)))

        self.text = f"""
            Автомат получает на вход четырёхзначное число (число не может начинаться с нуля). По этому числу строится
            новое число по следующим правилам.<ol><li>Складываются отдельно первая и вторая, вторая и третья,
            третья и четвёртая цифры заданного числа.</li><li>Наименьшая из полученных трёх сумм удаляется.</li>
            <li>Оставшиеся две суммы записываются друг за другом в порядке неубывания без разделителей.</li></ol>
            <i>Пример.</i> Исходное число: 1982. Суммы: 1 + 9 = 10, 9 + 8 = 17, 8 + 2 = 10. Удаляется 10.
            Результат: 1017.<br/>Укажите наименьшее число, при обработке которого автомат выдаёт результат
            <b>{result}</b>.<br/><b>Примечание.</b> Если меньшие из сумм равны, то отбрасывают одну из них."""
        self.correct = initial
        self.accept_number()

        return self

    def _get_digits_sums(self, number: int) -> list:
        if not (1000 <= number <= 9999):
            raise ValueError(f"{number} is not 4-digit number")

        sums = []
        for _ in range(3):
            sums.append(number % 10 + number // 10 % 10)
            number //= 10

        return sums

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

from ..EGE.Z06 import FindNumber, MinAddDigits
from ...GenBase import DirectInput

class FindBinaryNumber(FindNumber):
    pass

class MachineMinAddDigits(MinAddDigits):
    pass

class Robot(DirectInput):
    def generate(self):
        cycles = ["1324", "1423", "2314", "2413", "3142", "3241", "4132", "4231"]
        opposite_directions = {1: 2, 2: 1, 3: 4, 4: 3}
        directions = list(opposite_directions.keys())
        path = str(self.rnd.pick(directions))
        for i in range(1, 7):
            path += str(self.rnd.pick(directions, opposite_directions[int(path[i - 1])]))

        self.text = f""" Исполнитель Робот действует на клетчатой доске, между соседними клетками которой могут 
        стоять стены. Робот передвигается по клеткам доски и может выполнять команды <b>1 (вверх)</b>, 
        <b>2 (вниз)</b>, <b>3 (вправо)</b> и <b>4 ( влево)</b>, переходя на соседнюю клетку в направлении, 
        указанном в скобках. Если в этом направлении между клетками стоит стена, то Робот разрушается. Робот успешно 
        выполнил программу<br/><b>{path}</b>.<br/>Какую последовательность из четырех команд должен выполнить Робот, 
        чтобы вернуться в ту клетку, где он был перед началом выполнения программы, и не разрушиться вне зависимости 
        от того, какие стены стоят на поле?"""

        for cycle in cycles:
            path = path.replace(cycle, '')

        self.correct = int("".join([str(opposite_directions[int(direction)]) for direction in reversed(path)]))
        self.accept_number()

        return self

class Calculator(DirectInput):
    def generate(self):
        initial = self.rnd.in_range(10, 50)
        add = self.rnd.in_range(1, 3)
        multiply = self.rnd.in_range(2, 3)
        result, amount = self._generate_number(initial, add, multiply)

        self.text = f"""
            Исполнитель КАЛЬКУЛЯТОР имеет только две команды, которым присвоены номера:<br/>
            <ol><b><li>прибавь {add}</li><li>умножь на {multiply}</li></b></ol> Выполняя команду номер 1, КАЛЬКУЛЯТОР 
            прибавляет к числу на экране {add}, а выполняя команду номер 2, умножает число на экране на {multiply}. 
            Укажите минимальное число команд, которое должен выполнить исполнитель, чтобы получить из числа <b>{initial}
            </b> число <b>{result}</b>."""
        self.correct = amount
        self.accept_number()

        return self

    def _generate_number(self, initial: int, add: int, multiply: int) -> (int, int):
        result = initial
        amount = self.rnd.in_range(5, 15)
        for _ in range(amount):
            if self.rnd.coin() == 0:
                result += add
            else:
                result *= multiply

        return result, amount

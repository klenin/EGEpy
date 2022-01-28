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

        self.text = f"""
            Исполнитель Робот действует на клетчатой доске, между соседними клетками которой могут стоять 
            стены. Робот передвигается по клеткам доски и может выполнять команды 1 (вверх), 2 (вниз), 3 (вправо) и 4 ( 
            влево), переходя на соседнюю клетку в направлении, указанном в скобках. Если в этом направлении между 
            клетками стоит стена, то Робот разрушается. Робот успешно выполнил программу<br/><b>{path}</b>.<br/>Какую 
            последовательность из четырех команд должен выполнить Робот, чтобы вернуться в ту клетку, где он был 
            перед началом выполнения программы, и не разрушиться вне зависимости от того, какие стены стоят на 
            поле?"""

        for cycle in cycles:
            path = path.replace(cycle, '')

        self.correct = int("".join([str(opposite_directions[int(direction)]) for direction in reversed(path)]))
        self.accept_number()

        return self

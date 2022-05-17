import enum
from dataclasses import dataclass

import pandas as pd

from ...GenBase import DirectInput

class HorizonatlMove(enum.Enum):
    Left = -1
    Right = 1

class VerticalMove(enum.Enum):
    Down = -1
    Up = 1

@dataclass
class Position:
    row: int
    col: int


class RobotExecuter(DirectInput):
    def generate(self):
        self.file_path = "EGE/Gen/EGE2022/RobotExecuter" + str(self.rnd.get(100000)) + ".xlsx"

        self.min_map_size = 1
        self.max_map_size = 17

        self.min_coin_value = 1
        self.max_coin_value = 100

        self.horizontal_move = self.rnd.pick([ HorizonatlMove.Left, HorizonatlMove.Right ])
        self.vertical_move = self.rnd.pick([ VerticalMove.Down, VerticalMove.Up ])

        self._generate_map()
        self._generate_text()

        self.accept_number()
        self.correct = self._get_answer()

        return self
    
    def _generate_map(self):
        self.map_size = self.rnd.in_range(1, 17)
        self.map = [
            [ self.rnd.in_range(self.min_coin_value, self.max_coin_value) for _ in range(self.map_size) ] for _ in range(self.map_size)
        ]
        
        self.writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter')

        self.map = pd.DataFrame(self.map)
        self.map.to_excel(self.writer, index=False, header=False)
        self.writer.save()

    def _generate_text(self):
        text_command_hor = "влево" if self.horizontal_move == HorizonatlMove.Left else "вправо"
        text_command_ver = "вниз" if self.vertical_move == VerticalMove.Down else "вверх"

        text_to_hor = "левую" if self.horizontal_move == HorizonatlMove.Left else "правую"
        text_to_ver = "нижнюю" if self.vertical_move == VerticalMove.Down else "верхнюю"

        self.text = f"""
Квадрат разлинован на NxN клеток ({self.min_map_size} &lt; N &lt; {self.max_map_size}). 
Исполнитель Робот может перемещаться по клеткам, выполняя за одно перемещение одну из двух команд: 
<b>{text_command_hor}</b> или <b>{text_command_ver}</b>. 
По команде {text_command_hor} Робот перемещается в соседнюю {text_to_hor} клетку, 
по команде {text_command_ver} — в соседнюю {text_to_ver}. 
При попытке выхода за границу квадрата Робот разрушается. Перед каждым запуском Робота 
в каждой клетке квадрата лежит монета достоинством от {self.min_coin_value} до {self.max_coin_value}. 
Посетив клетку, Робот забирает монету с собой; это также относится к начальной и конечной клетке маршрута Робота."""
        self.text += f"""<p><center><a href=\"{self.file_path}\">Задание 18</a></center></p>"""

        text_from_hor = "правой" if self.horizontal_move == HorizonatlMove.Left else "левой"
        text_from_ver = "верхней" if self.vertical_move == VerticalMove.Down else "нижней"      

        self.text += f"""
Откройте файл. Определите максимальную и минимальную денежную сумму, которую может собрать Робот, пройдя из 
<b>{text_from_hor} {text_from_ver}</b> клетки в <b>{text_to_hor} {text_to_ver}</b>. 
В ответ запишите два числа друг за другом без разделительных знаков — сначала максимальную сумму, затем минимальную. 
Исходные данные представляют собой электронную таблицу размером NxN, каждая ячейка которой соответствует клетке квадрата. 
"""
        self._generate_example()

    def _generate_example(self):
        example_table = [
            [  1,  8,  8,  4],
            [ 10,  1,  1,  3],
            [  1,  3, 12,  2],
            [  2,  3,  5,  6],
        ]
        
        example_table_html_text = '<table style="margin:auto">'
        example_table_html_text += '<tbody>'
        for row in example_table:
            example_table_html_text += '<tr>'
            for el in row:
                example_table_html_text += f'<td style="text-align:center">{el}</td>'
            example_table_html_text += '</tr>'
        example_table_html_text += '</tbody></table>'
        
        self.text += "<i>Пример входных данных:</i>" + example_table_html_text

        if self.horizontal_move == HorizonatlMove.Left:
            if self.vertical_move == VerticalMove.Down:
                example_answer = (35, 15)
            else:
                example_answer = (41, 22)
        else:
            if self.vertical_move == VerticalMove.Down:
                example_answer = (41, 22)
            else:
                example_answer = (35, 15)
        
        self.text += f"Для указанных входных данных ответом должна быть пара чисел {example_answer[0]} и {example_answer[1]}."

    def _get_answer(self) -> int:
        start_pos = Position(
            0 if self.vertical_move == VerticalMove.Down else self.map_size - 1,
            0 if self.horizontal_move == HorizonatlMove.Right else self.map_size - 1
        )

        end_pos = Position(
            self.map_size - 1 if self.vertical_move == VerticalMove.Down else 0,
            self.map_size - 1 if self.horizontal_move == HorizonatlMove.Right else 0
        )

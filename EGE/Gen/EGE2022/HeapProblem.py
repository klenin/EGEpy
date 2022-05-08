from ...GenBase import DirectInput
from ...Russian import join_comma_and, alphabet
from ...RussianModules import Names, NumText

class Operation:
    def __init__(self, value: int = 1):
        self.value = value

class Add(Operation):
    def __init__(self, value: int = 1):
        super().__init__(value)
        self.operator = '+'

    def __str__(self) -> str:
        str_value = NumText.num_by_words(self.value, 0)
        stone_word = NumText.num_stones(self.value).split()[1]
        return f"добавить в кучу {str_value} {stone_word}"

class Remove(Operation):
    def __init__(self, value: int = 1):
        super().__init__(value)
        self.operator = '-'

    def __str__(self) -> str:
        str_value = NumText.num_by_words(self.value, 0)
        stone_word = NumText.num_stones(self.value).split()[1]
        return f"убрать из кучи {str_value} {stone_word}"

class Multiply(Operation):
    def __init__(self, value: int = 1):
        super().__init__(value)
        self.operator = '*'
    
    def __str__(self) -> str:
        str_value = NumText.num_by_words(self.value, 0)
        times = NumText.num_times(self.value).split()[1]
        return f"увеличить количество камней в куче в {str_value} {times}"

class Move:
    def __init__(self, operations) -> None:
        self.operations = operations
    
    def __str__(self) -> str:
        return join_comma_and([str(op) for op in self.operations])
    
    def make(self, lhs: int) -> int:
        result = lhs
        for operation in self.operations:
            result = eval(f"{result}{operation.operator}{operation.value}")
        return result


class OneHeapPoblem(DirectInput):
    def _generate_game(self):
        names = self._generate_names()
        self.first_player = names[0]
        self.second_player = names[1]
        self.moves = self._generate_moves()
        self.final_count = self.rnd.in_range(28, 76)

    def _generate_names(self) -> list:
        return self.rnd.pick_n(2, self.rnd.shuffle(Names.male + Names.female))

    def _generate_moves(self) -> list:
        moves = [ Move([ Add(1) ]) ]
        type = self.rnd.get(4)
        if type == 0:
            moves.append(Move([ Add(self.rnd.in_range(2, 5))]))
            moves.append(Move([ Multiply(self.rnd.in_range(2, 5))]))
        elif type == 1:
            moves.append(Move([ Multiply(self.rnd.in_range(2, 5))]))
        elif type == 2:
            moves.append(Move([
                Multiply(self.rnd.in_range(2, 3)),
                Remove(self.rnd.in_range(1, 4))
            ]))
        elif type == 3:
            moves.append(Move([
                Multiply(self.rnd.in_range(2, 3)),
                Add(self.rnd.in_range(1, 4))
            ]))
        return moves

    def _generate_text(self):
        self.text = self._get_intro_statement()
        self.text += " " + self._get_move_statement()
        self.text += " " + self._get_example_statement()
        self.text += " У каждого игрока, чтобы делать ходы, есть неограниченное количество камней."
        self.text += " " + self._get_end_statement()
        self.text += self._get_win_statement()
        self.text += self._get_strategy_statement()
        self.text += self._get_task_statement()

    def _get_intro_statement(self) -> str:
        return f"""
Два игрока, {self.first_player} и {self.second_player}, играют в следующую игру. Перед игроками лежит куча камней.
Игроки ходят по очереди, первый ход делает {self.first_player}."""

    def _get_move_statement(self) -> str:
        statement = "За один ход игрок может: "
        statements_number = len(self.moves)
        for i in range(statements_number):
            statement += f"<p><b>{self.moves[i]} (действие {alphabet[i]})</b>"
            if i < statements_number - 1:
                statement += " или"
            elif i == statements_number - 1:
                statement += "."
            statement += "</p>"
        return statement

    def _get_example_statement(self) -> str:
        example_count = self.rnd.in_range(10, 15)
        heap_str = join_comma_and([ str(move.make(example_count)) for move in self.moves ])
        return f"""
Например, имея кучу из {example_count} камней, за один ход можно получить кучу из {heap_str} камней."""

    def _get_end_statement(self) -> str:
        return f"""
Игра завершается в тот момент, когда количество камней в куче становится не менее {self.final_count}."""

    def _get_win_statement(self) -> str:
        return f"""
Победителем считается игрок, сделавший последний ход, т.е. первым получивший кучу, в которой будет 
{self.final_count} или больше камней. В начальный момент в куче было S камней; 1 &lt;= S &lt;= {self.final_count - 1}."""

    def _get_strategy_statement(self) -> str:
        return """
Будем говорить, что игрок имеет выигрышную стратегию, если он может выиграть при любых ходах противника.
Описать стратегию игрока — значит, описать, какой ход он должен сделать в любой ситуации, которая 
ему может встретиться при различной игре противника. В описание выигрышной стратегии <b>не следует</b> 
включать ходы играющего по этой стратегии игрока, не являющиеся для него безусловно выигрышными, 
т.е. не являющиеся выигрышными независимо от игры противника.
"""

    def _get_task_statement(self) -> str:
        return ""

from ...GenBase import DirectInput
from ...Russian import join_comma_and, alphabet
from ...RussianModules import Names, NumText

class Operation:
    def __init__(self, value: int = 1):
        self.value = value

class OneSideOperation(Operation):
    def execute(self, lhs: int):
        return eval(f"{lhs}{self.operator}{self.value}")

class TwoSideOperation(Operation):
    def execute(self, lhs: int, rhs: int):
        return eval(f"{lhs}{self.operator}{rhs}")    

class Add(OneSideOperation):
    def __init__(self, value: int = 1):
        super().__init__(value)
        self.operator = '+'

    def __str__(self) -> str:
        str_value = NumText.num_by_words(self.value, 0)
        stone_word = NumText.num_stones(self.value).split()[1]
        return f"добавить в кучу {str_value} {stone_word}"

class Remove(OneSideOperation):
    def __init__(self, value: int = 1):
        super().__init__(value)
        self.operator = '-'

    def __str__(self) -> str:
        str_value = NumText.num_by_words(self.value, 0)
        stone_word = NumText.num_stones(self.value).split()[1]
        return f"убрать из кучи {str_value} {stone_word}"

class Multiply(OneSideOperation):
    def __init__(self, value: int = 1):
        super().__init__(value)
        self.operator = '*'
    
    def __str__(self) -> str:
        str_value = NumText.num_by_words(self.value, 0)
        times = NumText.num_times(self.value).split()[1]
        return f"увеличить количество камней в куче в {str_value} {times}"

class AddOther(TwoSideOperation):
    def __init__(self):
        super().__init__()
        self.operator = '+'
    
    def __str__(self) -> str:
        return "добавить столько камней, сколько их в данный момент в другой куче"

class Move:
    def __init__(self, operations) -> None:
        self.operations = operations
    
    def __str__(self) -> str:
        return join_comma_and([str(op) for op in self.operations])
    
    def make(self, lhs: int, rhs: int = None) -> int:
        for operation in self.operations:
            if isinstance(operation, OneSideOperation):
                lhs = operation.execute(lhs)
            elif isinstance(operation, TwoSideOperation):
                if rhs is None:
                    rhs = 0
                lhs = operation.execute(lhs, rhs)
        return lhs

class HeapProblem(DirectInput):
    def _generate_game(self):
        self._generate_names()
        self._generate_moves()
        self._generate_final_size()

    def _generate_names(self) -> list:
        names = self.rnd.pick_n(2, self.rnd.shuffle(Names.male + Names.female))
        self.first_player = names[0]
        self.second_player = names[1]
    
    def _generate_text(self):
        self.text = self._get_intro_statement()
        self.text += " " + self._get_move_statement()
        self.text += " " + self._get_example_statement()
        self.text += " У каждого игрока, чтобы делать ходы, есть неограниченное количество камней."
        self.text += " " + self._get_end_statement()
        self.text += self._get_win_statement()
        self.text += self._get_strategy_statement()
        self.text += self._get_task_statement()

    def _get_strategy_statement(self) -> str:
        return """
Будем говорить, что игрок имеет выигрышную стратегию, если он может выиграть при любых ходах противника.
Описать стратегию игрока — значит, описать, какой ход он должен сделать в любой ситуации, которая 
ему может встретиться при различной игре противника. В описание выигрышной стратегии <b>не следует</b> 
включать ходы играющего по этой стратегии игрока, не являющиеся для него безусловно выигрышными, 
т.е. не являющиеся выигрышными независимо от игры противника.
"""

class OneHeapPoblem(HeapProblem):
    def _generate_final_size(self):
        self.final_size = self.rnd.in_range(28, 76)

    def _generate_moves(self) -> list:
        self.moves = [ Move([ Add(1) ]) ]
        type = self.rnd.get(4)
        if type == 0:
            self.moves.append(Move([ Add(self.rnd.in_range(2, 5))]))
            self.moves.append(Move([ Multiply(self.rnd.in_range(2, 5))]))
        elif type == 1:
            self.moves.append(Move([ Multiply(self.rnd.in_range(2, 5))]))
        elif type == 2:
            self.moves.append(Move([
                Multiply(self.rnd.in_range(2, 3)),
                Remove(self.rnd.in_range(1, 4))
            ]))
        elif type == 3:
            self.moves.append(Move([
                Multiply(self.rnd.in_range(2, 3)),
                Add(self.rnd.in_range(1, 4))
            ]))

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
Игра завершается в тот момент, когда количество камней в куче становится не менее {self.final_size}."""

    def _get_win_statement(self) -> str:
        return f"""
Победителем считается игрок, сделавший последний ход, т.е. первым получивший кучу, в которой будет 
{self.final_size} или больше камней. В начальный момент в куче было S камней; 1 &lt;= S &lt;= {self.final_size - 1}."""

class TwoHeapProblem(HeapProblem):
    def _generate_game(self):
        super()._generate_game()
        self.first_heap_size = self.rnd.in_range(2, 27)

    def _generate_final_size(self):
        self.final_size = self.rnd.in_range(28, 76)

    def _generate_moves(self) -> list:
        self.moves = [ Move([ Add(1) ]) ]
        type = self.rnd.get(2)
        if type == 0:
            self.moves.append(Move([ Multiply(self.rnd.in_range(2, 4))]))
        elif type == 1:
            self.moves.append(Move([ AddOther() ]))

    def _get_intro_statement(self) -> str:
        return f"""
Два игрока, {self.first_player} и {self.second_player}, играют в следующую игру. Перед лежит дву кучи камней.
Игроки ходят по очереди, первый ход делает {self.first_player}."""

    def _get_move_statement(self) -> str:
        statement = "За один ход игрок может в одной из куч (по своему выбору): "
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
        example_heaps = [ self.rnd.in_range(10, 15), self.rnd.in_range(10, 15) ]
        example_stone_words = [ NumText.num_stones(heap).split()[1] for heap in example_heaps ]

        start_pos = f"({example_heaps[0]}, {example_heaps[1]})"

        statement = f"""
Например, пусть в одной из куч {example_heaps[0]} {example_stone_words[0]}, а в другой
 {example_heaps[1]} {example_stone_words[1]}; такую позицию мы будем обозначать {start_pos}.
 За один ход из позиции {start_pos} можно получить любую из четырёх позиций: """

        positions = []
        indices = range(2)
        for heap_number in indices:
            for move in self.moves:
                new_position = [ example_heaps[i] for i in indices ]
                new_position[heap_number] = move.make(new_position[heap_number], new_position[(heap_number + 1) % 2])
                positions.append(new_position)
        
        statement += ', '.join([ '(' + str(p[0]) + ', ' + str(p[1]) + ')' for p in positions]) + '.'
        return statement

    def _get_end_statement(self) -> str:
        return f"""
Игра завершается в тот момент, когда суммарное количество камней в кучах становится не менее {self.final_size}."""

    def _get_win_statement(self) -> str:
        return f"""
Победителем считается игрок, сделавший последний ход, то есть первым получивший позицию, в которой в кучах будет {self.final_size} или больше камней.
 В начальный момент в первой куче было {self.first_heap_size} камней, во второй куче — S камней; 1 &lt;= S &lt;= {self.final_size - 1}."""
        
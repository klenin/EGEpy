from EGE.Gen.EGE2022.HeapProblem import OneHeapPoblem
from ...RussianModules.Names import genitive

class MinimalHeapSize(OneHeapPoblem):
    def generate(self):
        self._generate_game()
        self._generate_text()

        self.accept_number()
        self._calc_answer()

        return self

    def _calc_answer(self) -> int:
        for candidate in range(1, self.final_count):
            for first_move in self.moves:
                first_value = first_move.make(candidate)
                if first_value < self.final_count:
                    for second_move in self.moves:
                        second_value = second_move.make(first_value)
                        if second_value >= self.final_count:
                            self.correct = candidate
                            return
        raise Exception("Can't find answer in N19 problem")

    def _get_task_statement(self) -> str:
        return f"""
Известно, что {self.second_player} выиграл своим первым ходом после неудачного первого хода {genitive(self.second_player)}. 
Укажите минимальное значение S, когда такая ситуация возможна."""

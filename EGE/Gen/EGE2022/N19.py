from EGE.Gen.EGE2022.HeapProblem import OneHeapPoblem, TwoHeapProblem
from ...RussianModules.Names import genitive

class MinimalOneHeapSize(OneHeapPoblem):
    def generate(self):
        self._generate_game()
        self._generate_text()

        self.accept_number()
        self._calc_answer()

        return self

    def _calc_answer(self) -> int:
        for candidate in range(1, self.final_size):
            for first_move in self.moves:
                first_value = first_move.make(candidate)
                if first_value < self.final_size:
                    for second_move in self.moves:
                        second_value = second_move.make(first_value)
                        if second_value >= self.final_size:
                            self.correct = candidate
                            return
        raise Exception("Can't find answer in MinimalOneHeapSize problem")

    def _get_task_statement(self) -> str:
        return f"""
Известно, что {self.second_player} выиграл своим первым ходом после неудачного первого хода {genitive(self.first_player)}. 
Укажите минимальное значение S, когда такая ситуация возможна."""

class MinimalTwoHeapSize(TwoHeapProblem):
    def generate(self):
        self._generate_game()
        self._generate_text()

        self.accept_number()
        self._calc_answer()

        return self

    def _calc_answer(self) -> int:
        for candidate in range(1, self.final_size):
            heaps = [ self.first_heap_size, candidate ]
            for heap_number in range(2):
                for first_move in self.moves:
                    first_value = first_move.make(heaps[heap_number], heaps[(heap_number + 1) % 2])
                    if first_value < self.final_size:
                        for second_move in self.moves:
                            second_value = second_move.make(first_value, heaps[(heap_number + 1) % 2])
                            if second_value >= self.final_size:
                                self.correct = candidate
                                return
        raise Exception("Can't find answer in MinimalTwoHeapSize problem")

    def _get_task_statement(self) -> str:
        return f"""
Известно, что {self.second_player} выиграл своим первым ходом после неудачного первого хода {genitive(self.first_player)}. 
Укажите минимальное значение S, когда такая ситуация возможна."""

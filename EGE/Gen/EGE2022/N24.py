import string
from enum import Enum

from ...GenBase import DirectInput
from ...Russian import join_comma_and

class ThreeSymbolsInFile(DirectInput):
    class SymbolsInFileProblem(Enum):
        MaxSuccesiveDifferent = 0,
        MaxSuccesiveFirstSymbol = 1,
        MaxSuccesiveSecondSymbol = 2,
        MaxSuccesiveThirdSymbol = 3,

    def generate(self):
        self.min_length = 9 * 1e5
        self.max_length = 1e6

        self.symbols = self.rnd.pick_n(3, list(string.ascii_uppercase))
        self.file_name = "EGE/Gen/EGE2022/ThreeSymbolsInFile" + str(self.rnd.get(1e6)) + ".txt"
        self.symbols_count = int(self.rnd.in_range(self.min_length, self.max_length))

        self.string = ''.join([ self.rnd.pick(self.symbols) for _ in range(self.symbols_count) ])
        with open(self.file_name, "w") as file:
            file.write(self.string)

        problem_type = self.rnd.pick([
            self.SymbolsInFileProblem.MaxSuccesiveDifferent,
            self.SymbolsInFileProblem.MaxSuccesiveFirstSymbol,
            self.SymbolsInFileProblem.MaxSuccesiveSecondSymbol,
            self.SymbolsInFileProblem.MaxSuccesiveThirdSymbol,
        ])

        self.accept_number()

        self.text = f"<p>Текстовый файл состоит не более чем из 10<sup>6</sup> символов {join_comma_and(self.symbols)}."

        if problem_type == self.SymbolsInFileProblem.MaxSuccesiveDifferent:
            self.correct  = self.find_succesive_different()
            self.text += """
 Определите максимальное количество идущих подряд символов, среди которых каждые два соседних различны."""
        elif problem_type == self.SymbolsInFileProblem.MaxSuccesiveFirstSymbol:
            self.correct = self.find_succesive_symbol(self.symbols[0])
            self.text += f"""
 Определите длину самой длинной последовательности, состоящей из символов {self.symbols[0]}.
 Хотя бы один символ {self.symbols[0]} находится в последовательности."""
        elif problem_type == self.SymbolsInFileProblem.MaxSuccesiveSecondSymbol:
            self.correct = self.find_succesive_symbol(self.symbols[1])
            self.text += f"""
 Определите длину самой длинной последовательности, состоящей из символов {self.symbols[1]}.
 Хотя бы один символ {self.symbols[1]} находится в последовательности."""
        elif problem_type == self.SymbolsInFileProblem.MaxSuccesiveThirdSymbol:
            self.correct = self.find_succesive_symbol(self.symbols[2])
            self.text += f"""
 Определите длину самой длинной последовательности, состоящей из символов {self.symbols[2]}.
 Хотя бы один символ {self.symbols[2]} находится в последовательности."""

        self.text += "</p>"

        self.text += "<p>Для выполнения этого задания следует написать программу."
        self.text += " Ниже приведён файл, который необходимо обработать с помощью данного алгоритма.</p>"
        self.text += f"<center><a href=\"{self.file_name}\">Файл</a></center>"

        return self

    def find_succesive_symbol(self, symbol: str) -> int:
        index = 0
        answer = 0
        is_counting = False
        current_count = 0
        while index < self.symbols_count:
            if self.string[index] == symbol:
                if is_counting:
                    current_count += 1
                else:
                    is_counting = True
                    current_count = 1
            else:
                if is_counting:
                    answer = max(answer, current_count)
                    is_counting = False
                    current_count = 0
            index += 1
        answer = max(answer, current_count)
        return answer
                
    def find_succesive_different(self) -> int:
        index = 1
        answer = 0
        is_counting = False
        current_count = 0
        prev_symbol = self.string[0]
        while index < self.symbols_count:
            if self.string[index] != prev_symbol:
                if is_counting:
                    current_count += 1
                else:
                    is_counting = True
                    current_count = 2
            else:
                if is_counting:
                    answer = max(answer, current_count)
                    is_counting = False
                    current_count = 0
            prev_symbol = self.string[index]
            index += 1
        answer = max(answer, current_count)
        return answer





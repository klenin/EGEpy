from ...GenBase import DirectInput

class ProcessingPositiveIntegres(DirectInput):
    def generate(self):
        self._generate_file()
        self._generate_params()
        self._generate_text()
        self._calc_answer()
        return self
    
    def _generate_file(self):
        self.file_name = "EGE/Gen/EGE2022/ProcessingPositiveIntegers" + str(self.rnd.get(1000000)) + ".txt"
        with open(self.file_name, "w") as file:
            for _ in range(10000):
                file.write(str(self.rnd.in_range(1, 10000)) + '\n')

    def _generate_params(self):
        pass

    def _generate_text(self):
        self.text = """
В файле содержится последовательность из 10 000 целых положительных чисел. Каждое число не превышает 10 000. 
 Определите и запишите в ответе сначала количество пар элементов последовательности, """
        self.text += self._get_first_condition() + ', '
        self.text += self._get_second_condition() + '. '
        self.text += """
В данной задаче под парой подразумевается два различных элемента последовательности.
 Порядок элементов в паре не важен.
"""
        self.text += f"<p><center><a href=\"{self.file_name}\">Файл</a></center></p>"

    def _get_first_condition(self) -> str:
        pass

    def _get_second_condition(self) -> str:
        pass

    def _calc_answer(self):
        pairs_count = processed_value = 0
        with open(self.file_name, "r") as file:
            numbers = [ int(i) for i in file ]
            for i in range(len(numbers) - 1):
                for j in range(i + 1, len(numbers)):
                    if self._check_pair(numbers[i], numbers[j]):
                        pairs_count += 1
                        processed_value = self._process_value(processed_value, numbers[i], numbers[j])
        self.correct = str(pairs_count) + ' ' + str(processed_value)
    
    def _check_pair(self, first: int, second: int) -> bool:
        pass
    
    def _process_value(self, value: int, first: int, second: int) -> int:
        pass


class ProcessingPoistiveIntegersSumType(ProcessingPositiveIntegres):
    def _process_value(self, value: int, first: int, second: int) -> int:
        return max(value, first + second)

    def _get_second_condition(self) -> str:
        return "затем максимальную из сумм элементов таких пар"


class ProcessingPoistiveIntegersDifType(ProcessingPositiveIntegres):
    def _process_value(self, value: int, first: int, second: int) -> int:
        return max(value, abs(first - second))

    def _get_second_condition(self) -> str:
        return "затем максимальную из разностей элементов таких пар"


class DifferenceEvenAndMultiplicity(ProcessingPoistiveIntegersSumType):
    def _generate_params(self):
        self.param = self.rnd.get(50)

    def _get_first_condition(self) -> str:
        return f"разность которых четна и хотя бы одно из чисел делится на {self.param}"

    def _check_pair(self, first: int, second: int) -> bool:
        return (first - second) % 2 == 0 and (first % self.param == 0 or second % self.param == 0)


class MultiplicityOfMultiplication(ProcessingPoistiveIntegersSumType):
    def _generate_params(self):
        self.param = self.rnd.get(70)

    def _get_first_condition(self) -> str:
        return f"для которых произведение элементов делится без остатка на {self.param}"

    def _check_pair(self, first: int, second: int) -> bool:
        return first * second % self.param == 0


class NotMultiplicityOfMultiplication(ProcessingPoistiveIntegersSumType):
    def _generate_params(self):
        self.param = self.rnd.get(50)

    def _get_first_condition(self) -> str:
        return f"для которых произведение элементов не кратно {self.param}"

    def _check_pair(self, first: int, second: int) -> bool:
        return first * second % self.param != 0


class OddSumAndMultiplicityOfMultiplication(ProcessingPoistiveIntegersSumType):
    def _generate_params(self):
        self.param = self.rnd.get(15)

    def _get_first_condition(self) -> str:
        return f"у которых сумма нечётна, а произведение делится на {self.param}"

    def _check_pair(self, first: int, second: int) -> bool:
        return (first + second) % 2 != 0 and (first * second) % self.param == 0


class MultiplicityOfSum(ProcessingPoistiveIntegersSumType):
    def _generate_params(self):
        self.param = self.rnd.get(130)

    def _get_first_condition(self) -> str:
        return f"у которых сумма элементов кратна {self.param}"

    def _check_pair(self, first: int, second: int) -> bool:
        return (first + second) % self.param == 0


class MultiplicityOfSumAndMultiplicityOfOneElement(ProcessingPoistiveIntegersSumType):
    def _generate_params(self):
        self.first_param = self.rnd.get(100)
        self.second_param = self.rnd.get(60)

    def _get_first_condition(self) -> str:
        return f"""
у которых сумма элементов кратна {self.first_param} и хотя бы один элемент из пары делится на {self.second_param}"""

    def _check_pair(self, first: int, second: int) -> bool:
        return ((first + second) % self.first_param == 0) and (first % self.second_param == 0 or second % self.second_param == 0)

class MultiplicityOfDifference(ProcessingPoistiveIntegersDifType):
    def _generate_params(self):
        self.param = self.rnd.get(100)   
    
    def _get_first_condition(self) -> str:
        return f"у которых разность элементов кратна {self.param}"

    def _check_pair(self, first: int, second: int) -> bool:
        return (first - second) % self.param == 0

class MultiplicityOfDifferenceAndMultiplicityOfOneElement(ProcessingPoistiveIntegersDifType):
    def _generate_params(self):
        self.first_param = self.rnd.get(70)
        self.second_param = self.rnd.get(30)

    def _get_first_condition(self) -> str:
        return f"у которых разность элементов кратна {self.first_param} и хотя бы один из элементов кратен {self.second_param}"

    def _check_pair(self, first: int, second: int) -> bool:
        return (first - second) % self.first_param == 0 and (first % self.second_param == 0 or second % self.second_param == 0)


from EGE.GenBase import DirectInput
from ...Utils import gcd

class BaseGcd(DirectInput):
    def generate(self):
        n = self.rnd.in_range(3, 15)
        m = n + self.rnd.in_range(1, 9)
        self.accept_number()
        self.correct = (n * m) / gcd(n, m)
        self.text = f'''
Запись десятичного числа в системах счисления с основаниями {n} и {m} 
в обоих случаях имеет последней цифрой 0. 
Какое минимальное натуральное десятичное число удовлетворяет этому требованию?
'''
        return self

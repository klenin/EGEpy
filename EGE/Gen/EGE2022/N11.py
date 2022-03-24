from ...GenBase import DirectInput

class AmountOfInformationCars(DirectInput):
    def __init__(self, rnd):
        self.rnd = rnd
        self.amount_of_symbols = self.rnd.in_range(5, 10)
        self.amount_of_letters = self.rnd.in_range(15, 33)
        self.amount_of_car_numbers = self.rnd.in_range(20, 200)
        self.text = ''

    def get_text(self, amount_of_symbols, amount_of_letters, amount_of_car_numbers):
        if amount_of_letters in [ 21, 31 ]:
            text_for_letters = 'различная буква'
        elif amount_of_letters in [ 22, 23, 24, 32, 33 ]:
            text_for_letters = 'различные буквы'
        else:
            text_for_letters = 'различных букв'

        self.text += f'''<p>В некоторой стране автомобильный номер длиной {amount_of_symbols} символов составляют из
заглавных букв (используются только {amount_of_letters} {text_for_letters}) и десятичных цифр в любом порядке.</p>
<p>Каждый такой номер в компьютерной программе записывается минимально возможным и одинаковым целым количеством 
байтов (при этом используют посимвольное кодирование и все символы кодируются одинаковым и минимально возможным количеством битов).</p>       
<p>Определите объём памяти, отводимый этой программой для записи {amount_of_car_numbers} номеров. (Ответ дайте в байтах.)</p>'''

        letters_and_digits = amount_of_letters + 10
        if letters_and_digits <= 32:
            amount_of_bits_for_one_symbol = 5
        else:
            amount_of_bits_for_one_symbol = 6
        amount_of_bits = amount_of_bits_for_one_symbol * amount_of_symbols
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1

        self.correct = amount_of_bytes * amount_of_car_numbers

    def generate(self):
        amount_of_symbols = self.amount_of_symbols
        amount_of_letters = self.amount_of_letters
        amount_of_car_numbers = self.amount_of_car_numbers
        self.get_text(amount_of_symbols, amount_of_letters, amount_of_car_numbers)
        return self

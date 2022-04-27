from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text, num_bits, num_bytes

class AmountOfInformation(DirectInput):
    def __init__(self, rnd):
        self.rnd = rnd
        self.letters = [ 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
                         'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ы', 'Э', 'Ю', 'Я' ]
        self.digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
        self.letters_and_digits = self.letters + self.digits

    def get_random_russian_letters(self, amount_of_letters):
        return ','.join(self.rnd.pick_n(amount_of_letters, self.letters))

    def get_random_russian_letters_and_digits(self, amount_of_symbols):
        return ','.join(self.rnd.pick_n(amount_of_symbols, self.letters_and_digits))

    def get_amount_of_bits(self, letters_and_digits):
        amount_of_bits_for_one_symbol = 0
        for i in range(1, 11):
            if 2 ** i >= letters_and_digits:
                amount_of_bits_for_one_symbol = i
                break
        return amount_of_bits_for_one_symbol

    def get_amount_of_bytes(self, amount_of_bits):
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1
        return amount_of_bytes

class AmountOfInformationCars(AmountOfInformation):
    def generate_text_1(self):
        self.amount_of_letters = self.rnd.in_range(15, 33)
        text_for_symbols = num_text(self.amount_of_symbols, [ 'символ', 'символа', 'символов' ])
        text_for_letters = num_text(self.amount_of_letters, [ 'различная буква', 'различные буквы', 'различных букв' ])
        text_for_car_numbers = num_text(self.amount_of_car_numbers, [ 'номер', 'номеров', 'номеров' ])

        self.text = f'''<p>В некоторой стране автомобильный номер длиной {text_for_symbols} составляют из
заглавных букв (используются только {text_for_letters}) и десятичных цифр в любом порядке.</p>
<p>Каждый такой номер в компьютерной программе записывается минимально возможным и одинаковым целым количеством 
байтов (при этом используют посимвольное кодирование и все символы кодируются одинаковым и минимально возможным количеством битов).</p>       
<p>Определите объём памяти, отводимый этой программой для записи {text_for_car_numbers}. (Ответ дайте в байтах.)</p>'''

        letters_and_digits = self.amount_of_letters + 10
        amount_of_bits_for_one_symbol = self.get_amount_of_bits(letters_and_digits)
        amount_of_bits = amount_of_bits_for_one_symbol * self.amount_of_symbols
        amount_of_bytes = self.get_amount_of_bytes(amount_of_bits)

        self.correct = amount_of_bytes * self.amount_of_car_numbers

        return self.text

    def generate_text_2(self):
        amount_of_letters = self.rnd.in_range(3, 10)
        text_for_symbols = num_text(self.amount_of_symbols, [ 'символ', 'символа', 'символов' ])
        text_for_letters = num_text(amount_of_letters, [ 'заглавная буква', 'заглавные буквы', 'заглавных букв' ])
        text_for_letters_10 = num_text(amount_of_letters + 10, [' допустимого символа', 'допустимых символов', 'допустимых символов' ])
        text_for_car_numbers = num_text(self.amount_of_car_numbers, [ 'автомобильного номера', 'автомобильных номеров', 'автомобильных номеров' ])

        picked_letters = self.get_random_russian_letters(amount_of_letters)

        self.text = f'''<p>Автомобильный номер состоит из {text_for_symbols}.
Допустимыми символами считаются 10 цифр и {text_for_letters}: {picked_letters}.
Для хранения каждого из {text_for_letters_10} используется одинаковое и наименьшее возможное количество бит.
Для хранения каждого номера используется одинаковое и минимально возможное количество байт.</p>
<p>Сколько байт памяти потребуется для хранения {text_for_car_numbers}? Номера хранятся без разделителей.</p>'''

        letters_and_digits = amount_of_letters + 10
        amount_of_bits_for_one_symbol = self.get_amount_of_bits(letters_and_digits)
        amount_of_bits = amount_of_bits_for_one_symbol * self.amount_of_symbols
        amount_of_bytes = self.get_amount_of_bytes(amount_of_bits)

        self.correct = amount_of_bytes * self.amount_of_car_numbers

        return self.text

    def generate(self):
        self.amount_of_symbols = self.rnd.in_range(5, 10)
        self.amount_of_car_numbers = self.rnd.in_range(20, 500)
        self.rnd.pick([ self.generate_text_1, self.generate_text_2, ])()
        return self

class AmountOfInformationPasswords(AmountOfInformation):
    def generate_text_1(self):
        amount_of_letters = self.rnd.in_range(4, 10)
        text_for_symbols = num_text(self.amount_of_symbols, [ 'символа', 'символов', 'символов' ])
        text_for_passwords = num_text(self.amount_of_passwords, [ 'пароля', 'паролей', 'паролей' ])

        picked_symbols = self.get_random_russian_letters_and_digits(amount_of_letters)

        self.text = f'''<p>При регистрации в компьютерной системе каждому пользователю выдаётся пароль, состоящий из
{text_for_symbols} и содержащий только символы {picked_symbols}.</p>
<p>Каждый такой пароль в компьютерной программе записывается минимально возможным и одинаковым целым количеством байт
(при этом используют посимвольное кодирование и все символы кодируются одинаковым и минимально возможным количеством бит).</p>
<p>Определите объём памяти, отводимый этой программой для записи {text_for_passwords}. (Ответ дайте в байтах.)</p>'''

        letters_and_digits = amount_of_letters
        amount_of_bits_for_one_symbol = self.get_amount_of_bits(letters_and_digits)
        amount_of_bits = amount_of_bits_for_one_symbol * self.amount_of_symbols
        amount_of_bytes = self.get_amount_of_bytes(amount_of_bits)

        self.correct = amount_of_bytes * self.amount_of_passwords

        return self.text

    def generate_text_2(self):
        amount_of_letters = self.rnd.in_range(10, 33)
        text_for_symbols = num_text(self.amount_of_symbols, [ 'символа', 'символов', 'символов' ])
        text_for_letters = num_text(amount_of_letters, [ 'различная буква', 'различные буквы', 'различных букв' ])
        text_for_passwords = num_text(self.amount_of_passwords, [ 'пароля', 'паролей', 'паролей' ])

        self.text = f'''<p>Для регистрации на сайте некоторой страны пользователю требуется придумать пароль.
Длина пароля— ровно {text_for_symbols}. В качестве символов могут быть использованы десятичные цифры и
{text_for_letters} местного алфавита, причём все буквы используются в двух начертаниях:
как строчные, так и прописные (регистр буквы имеет значение!).</p>
<p>Под хранение каждого такого пароля на компьютере отводится одинаковое и минимально возможное целое количество байтов.
При этом используется посимвольное кодирование, и все символы кодируются одинаковым и минимально возможным количеством битов.</p> 
<p>Определите объём памяти, который используется для хранения  {text_for_passwords}. (Ответ дайте в байтах.)</p>'''

        letters_and_digits = amount_of_letters * 2 + 10
        amount_of_bits_for_one_symbol = self.get_amount_of_bits(letters_and_digits)
        amount_of_bits = amount_of_bits_for_one_symbol * self.amount_of_symbols
        amount_of_bytes = self.get_amount_of_bytes(amount_of_bits)

        self.correct = amount_of_bytes * self.amount_of_passwords

    def generate(self):
        self.amount_of_symbols = self.rnd.in_range(5, 30)
        self.amount_of_passwords = self.rnd.in_range(10, 200)
        self.rnd.pick([ self.generate_text_1, self.generate_text_2, ])()
        return self

class AmountOfInformationPasswordsExtra(AmountOfInformation):
    def generate_text_1(self):
        amount_of_letters = self.rnd.in_range(4, 10)
        text_for_symbols = num_text(self.amount_of_symbols, [ 'символа', 'символов', 'символов' ])
        text_for_users = num_text(self.amount_of_users, [ 'пользователе', 'пользователях', 'пользователях' ])
        text_for_bytes = num_bytes(self.amount_of_extra_bytes)
        picked_letters = self.get_random_russian_letters_and_digits(amount_of_letters)

        self.text = f'''<p>При регистрации в компьютерной системе каждому пользователю выдаётся пароль, состоящий из
{text_for_symbols} и содержащий только символы из {amount_of_letters}-символьного набора: {picked_letters}.</p>
<p>В базе данных для хранения сведений о каждом пользователе отведено одинаковое и минимально возможное целое число байт.
При этом используют посимвольное кодирование паролей, все символы кодируются одинаковым и минимально возможным количеством бит.
Кроме пароля для каждого пользователя в системе хранятся дополнительные сведения, для чего отведено {text_for_bytes}.</p>
<p>Определите объём памяти, необходимый для хранения сведений о {text_for_users}. (Ответ дайте в байтах.)</p>'''

        letters_and_digits = amount_of_letters
        amount_of_bits_for_one_symbol = self.get_amount_of_bits(letters_and_digits)
        amount_of_bits = amount_of_bits_for_one_symbol * self.amount_of_symbols
        amount_of_bytes = self.get_amount_of_bytes(amount_of_bits) + self.amount_of_extra_bytes

        self.correct = amount_of_bytes * self.amount_of_users

        return self.text

    def generate_text_2(self):
        amount_of_letters = self.rnd.in_range(4, 10)
        text_for_symbols = num_text(self.amount_of_symbols, [ 'символа', 'символов', 'символов' ])
        text_for_users = num_text(self.amount_of_users, [ 'пользователе', 'пользователях', 'пользователях' ])

        picked_letters = self.get_random_russian_letters_and_digits(amount_of_letters)

        letters_and_digits = amount_of_letters
        amount_of_bits_for_one_symbol = self.get_amount_of_bits(letters_and_digits)
        amount_of_bits = amount_of_bits_for_one_symbol * self.amount_of_symbols
        amount_of_bytes = self.get_amount_of_bytes(amount_of_bits)
        final_amount_of_bytes = (amount_of_bytes + self.amount_of_extra_bytes) * self.amount_of_users

        text_for_bytes = num_bytes(final_amount_of_bytes)

        self.text = f'''<p>При регистрации в компьютерной системе каждому пользователю выдаётся пароль, состоящий из
{text_for_symbols} и содержащий только символы из {amount_of_letters}-символьного набора: {picked_letters}.</p>
<p>В базе данных для хранения сведений о каждом пользователе отведено одинаковое минимально возможное целое число байт.
При этом используют посимвольное кодирование паролей, все символы кодируют одинаковым минимально возможным количеством бит.
Кроме собственно пароля для каждого пользователя в системе хранятся дополнительные сведения, для чего выделено целое число байт,
одно и то же для всех пользователей.</p>
<p>Для хранения сведений о {text_for_users} потребовалось {text_for_bytes}.
Сколько байт выделено для хранения дополнительных сведений об одном пользователе?
В ответе запишите только целое число— количество байт.</p>'''

        self.correct = self.amount_of_extra_bytes

        return self.text

    def generate_text_3(self):
        amount_of_letters = self.rnd.in_range(5, 30)
        text_for_symbols = num_text(self.amount_of_symbols, [ 'буквы', 'букв', 'букв' ])
        text_for_letters = num_text(amount_of_letters, [ 'различная буква', 'различные буквы', 'различных букв' ])

        letters_and_digits = amount_of_letters * 2
        amount_of_bits_for_one_symbol = self.get_amount_of_bits(letters_and_digits)
        amount_of_bits = amount_of_bits_for_one_symbol * self.amount_of_symbols
        amount_of_bytes = self.get_amount_of_bytes(amount_of_bits)
        final_amount_of_bytes = amount_of_bytes + self.amount_of_extra_bytes + 2

        text_for_bytes = num_bytes(final_amount_of_bytes)

        self.text = f'''<p>Каждый сотрудник предприятия получает электронный пропуск, на котором записаны личный код сотрудника,
код подразделения и некоторая дополнительная информация. Личный код состоит из {text_for_symbols}.
Для формирования кодов используется {text_for_letters}, каждая из которых может быть заглавной или строчной. </p>
<p>Для записи кода на пропуске отведено минимально возможное целое число байт. При этом используют посимвольное кодирование,
все символы кодируют одинаковым минимально возможным количеством бит. Код подразделения— целое четырёхзначное число,
он записан на пропуске как двоичное число и занимает минимально возможное целое число байт.
Всего на пропуске хранится {text_for_bytes} данных.</p>
<p>Сколько байт выделено для хранения дополнительных сведений об одном сотруднике?
В ответе запишите только целое число— количество байт.</p>'''

        self.correct = self.amount_of_extra_bytes

        return self.text

    def generate(self):
        self.amount_of_symbols = self.rnd.in_range(5, 30)
        self.amount_of_extra_bytes = self.rnd.in_range(1, 30)
        self.amount_of_users = self.rnd.in_range(1, 50)
        self.rnd.pick([ self.generate_text_1, self.generate_text_2, self.generate_text_3, ])()
        return self

class AmountOfInformationSport(AmountOfInformation):
    def generate_text_1(self):
        text_for_athletes = num_text(self.amount_of_athletes, [ 'спортсмен', 'спортсмена', 'спортсменов' ])

        self.text = f'''<p>В велокроссе участвуют {text_for_athletes}.
Специальное устройство регистрирует прохождение каждым из участников промежуточного финиша,
записывая его номер с использованием минимально возможного количества бит, одинакового для каждого спортсмена.</p>
<p>Какой объём памяти будет использован устройством, когда все спортсмены прошли промежуточный финиш? (Ответ дайте в битах.)</p>'''

        amount_of_bits = self.get_amount_of_bits(self.amount_of_athletes)
        self.correct = amount_of_bits * self.amount_of_athletes

        return self.text

    def generate_text_2(self):
        finished_athletes = self.rnd.in_range(10, self.amount_of_athletes - 5)
        text_for_athletes = num_text(self.amount_of_athletes, [ 'спортсмен', 'спортсмена', 'спортсменов' ])
        text_for_finished_athletes = num_text(finished_athletes, [ 'велосипедист', 'велосипедиста', 'велосипедистов' ])

        self.text = f'''<p>В велокроссе участвуют {text_for_athletes}.
Специальное устройство регистрирует прохождение каждым из участников промежуточного финиша,
записывая его номер с использованием минимально возможного количества бит, одинакового для каждого спортсмена. </p>
<p>Каков информационный объем сообщения, записанного устройством, после того как промежуточный финиш прошли
{text_for_finished_athletes}? (Ответ дайте в байтах.)</p>'''

        amount_of_bits = self.get_amount_of_bits(self.amount_of_athletes) * finished_athletes
        amount_of_bytes = self.get_amount_of_bytes(amount_of_bits)
        self.correct = amount_of_bytes

        return self.text

    def generate(self):
        self.amount_of_athletes = self.rnd.in_range(20, 1000)
        self.rnd.pick([ self.generate_text_1, self.generate_text_2, ])()
        return self

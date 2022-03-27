from ...GenBase import DirectInput

class AmountOfInformationCars(DirectInput):
    def __init__(self, rnd):
        self.rnd = rnd
        self.amount_of_symbols = self.rnd.in_range(5, 10)
        self.amount_of_car_numbers = self.rnd.in_range(20, 500)
        self.text = ''

    def get_text_1(self, amount_of_symbols, amount_of_car_numbers):
        amount_of_letters = self.rnd.in_range(15, 33)

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
        amount_of_bits_for_one_symbol = 0
        for i in range(1, 11):
            if 2 ** i >= letters_and_digits:
                amount_of_bits_for_one_symbol = i
                break
        amount_of_bits = amount_of_bits_for_one_symbol * amount_of_symbols
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1

        self.correct = amount_of_bytes * amount_of_car_numbers

    def get_text_2(self, amount_of_symbols, amount_of_car_numbers):
        amount_of_letters = self.rnd.in_range(3, 10)

        if amount_of_letters in [ 3, 4 ]:
            text_for_letters = 'заглавные буквы'
        else:
            text_for_letters = 'заглавных букв'

        letters = [ 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
                    'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ы', 'Э', 'Ю', 'Я' ]
        random_letters = self.rnd.pick_n(amount_of_letters, letters)
        picked_letters = ''

        for i in range(amount_of_letters):
            if i == amount_of_letters - 1:
                picked_letters += random_letters[i]
            else:
                picked_letters += random_letters[i] + ', '

        self.text += f'''<p>Автомобильный номер состоит из {amount_of_symbols} символов.
Допустимыми символами считаются 10 цифр и {amount_of_letters} {text_for_letters}: {picked_letters}.
Для хранения каждого из {10 + amount_of_letters} допустимых символов используется одинаковое и наименьшее возможное количество бит.
Для хранения каждого номера используется одинаковое и минимально возможное количество байт.</p>
<p>Сколько байт памяти потребуется для хранения {amount_of_car_numbers} автомобильных номеров? Номера хранятся без разделителей.</p>'''

        letters_and_digits = amount_of_letters + 10
        amount_of_bits_for_one_symbol = 0
        for i in range(1, 11):
            if 2 ** i >= letters_and_digits:
                amount_of_bits_for_one_symbol = i
                break
        amount_of_bits = amount_of_bits_for_one_symbol * amount_of_symbols
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1

        self.correct = amount_of_bytes * amount_of_car_numbers

    def generate(self):
        amount_of_symbols = self.amount_of_symbols
        amount_of_car_numbers = self.amount_of_car_numbers
        if self.rnd.coin():
            self.get_text_1(amount_of_symbols, amount_of_car_numbers)
        else:
            self.get_text_2(amount_of_symbols, amount_of_car_numbers)
        return self

class AmountOfInformationPasswords(DirectInput):
    def __init__(self, rnd):
        self.rnd = rnd
        self.amount_of_symbols = self.rnd.in_range(5, 30)
        self.amount_of_passwords = self.rnd.in_range(10, 200)
        self.text = ''

    def get_text_1(self, amount_of_symbols, amount_of_passwords):
        amount_of_letters = self.rnd.in_range(4, 10)

        if amount_of_symbols == 21:
            text_for_symbols = 'символа'
        else:
            text_for_symbols = 'символов'

        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
                   'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ы', 'Э', 'Ю', 'Я', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        random_letters = self.rnd.pick_n(amount_of_letters, letters)
        picked_letters = ''

        for i in range(amount_of_letters):
            if i == amount_of_letters - 1:
                picked_letters += random_letters[i]
            else:
                picked_letters += random_letters[i] + ', '

        self.text += f'''<p>При регистрации в компьютерной системе каждому пользователю выдаётся пароль, состоящий из
{amount_of_symbols} {text_for_symbols} и содержащий только символы {picked_letters}.</p>
<p>Каждый такой пароль в компьютерной программе записывается минимально возможным и одинаковым целым количеством байт
(при этом используют посимвольное кодирование и все символы кодируются одинаковым и минимально возможным количеством бит).</p>
<p>Определите объём памяти, отводимый этой программой для записи {amount_of_passwords} паролей. (Ответ дайте в байтах.)</p>'''

        letters_and_digits = amount_of_letters
        amount_of_bits_for_one_symbol = 0
        for i in range(1, 11):
            if 2 ** i >= letters_and_digits:
                amount_of_bits_for_one_symbol = i
                break
        amount_of_bits = amount_of_bits_for_one_symbol * amount_of_symbols
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1

        self.correct = amount_of_bytes * amount_of_passwords

    def get_text_2(self, amount_of_symbols, amount_of_passwords):
        amount_of_letters = self.rnd.in_range(10, 33)

        if amount_of_symbols == 21:
            text_for_symbols = 'символ'
        elif amount_of_symbols in [ 22, 23, 24, 32, 33 ]:
            text_for_symbols = 'символа'
        else:
            text_for_symbols = 'символов'

        if amount_of_letters in [ 21, 31 ]:
            text_for_letters = 'различная буква'
        elif amount_of_letters in [ 22, 23, 24, 32, 33 ]:
            text_for_letters = 'различные буквы'
        else:
            text_for_letters = 'различных букв'


        self.text += f'''<p>Для регистрации на сайте некоторой страны пользователю требуется придумать пароль.
Длина пароля— ровно {amount_of_symbols} {text_for_symbols}. В качестве символов могут быть использованы десятичные цифры и
{amount_of_letters} {text_for_letters} местного алфавита, причём все буквы используются в двух начертаниях:
как строчные, так и прописные (регистр буквы имеет значение!).</p>
<p>Под хранение каждого такого пароля на компьютере отводится одинаковое и минимально возможное целое количество байтов.
При этом используется посимвольное кодирование, и все символы кодируются одинаковым и минимально возможным количеством битов.</p> 
<p>Определите объём памяти, который используется для хранения {amount_of_passwords} паролей.  (Ответ дайте в байтах.)</p>'''

        letters_and_digits = amount_of_letters * 2 + 10
        amount_of_bits_for_one_symbol = 0
        for i in range(1, 11):
            if 2 ** i >= letters_and_digits:
                amount_of_bits_for_one_symbol = i
                break
        amount_of_bits = amount_of_bits_for_one_symbol * amount_of_symbols
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1

        self.correct = amount_of_bytes * amount_of_passwords

    def generate(self):
        amount_of_symbols = self.amount_of_symbols
        amount_of_passwords = self.amount_of_passwords
        if self.rnd.coin():
            self.get_text_1(amount_of_symbols, amount_of_passwords)
        else:
            self.get_text_2(amount_of_symbols, amount_of_passwords)
        return self

class AmountOfInformationPasswordsExtra(DirectInput):
    def __init__(self, rnd):
        self.rnd = rnd
        self.amount_of_symbols = self.rnd.in_range(5, 30)
        self.amount_of_extra_bytes = self.rnd.in_range(1, 30)
        self.amount_of_users = self.rnd.in_range(1, 50)
        self.text = ''
        self.task_choice = self.rnd.in_range(1, 3)

    def get_text_1(self, amount_of_symbols, amount_of_extra_bytes, amount_of_users):
        amount_of_letters = self.rnd.in_range(4, 10)
        if amount_of_symbols == 21:
            text_for_symbols = 'символа'
        else:
            text_for_symbols = 'символов'

        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
                   'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ы', 'Э', 'Ю', 'Я', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        random_letters = self.rnd.pick_n(amount_of_letters, letters)
        picked_letters = ''

        for i in range(amount_of_letters):
            if i == amount_of_letters - 1:
                picked_letters += random_letters[i]
            else:
                picked_letters += random_letters[i] + ', '

        self.text += f'''<p>При регистрации в компьютерной системе каждому пользователю выдаётся пароль, состоящий из
{amount_of_symbols} {text_for_symbols} и содержащий только символы из {amount_of_letters}-буквенного набора: {picked_letters}.</p>
<p>В базе данных для хранения сведений о каждом пользователе отведено одинаковое и минимально возможное целое число байт.
При этом используют посимвольное кодирование паролей, все символы кодируются одинаковым и минимально возможным количеством бит.
Кроме пароля для каждого пользователя в системе хранятся дополнительные сведения, для чего отведено {amount_of_extra_bytes} байт.</p>
<p>Определите объём памяти, необходимый для хранения сведений о {amount_of_users} пользователях. (Ответ дайте в байтах.)</p>'''

        letters_and_digits = amount_of_letters
        amount_of_bits_for_one_symbol = 0
        for i in range(1, 11):
            if 2 ** i >= letters_and_digits:
                amount_of_bits_for_one_symbol = i
                break
        amount_of_bits = amount_of_bits_for_one_symbol * amount_of_symbols
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1
        amount_of_bytes += amount_of_extra_bytes

        self.correct = amount_of_bytes * amount_of_users

    def get_text_2(self, amount_of_symbols, amount_of_extra_bytes, amount_of_users):
        amount_of_letters = self.rnd.in_range(4, 10)
        if amount_of_symbols == 21:
            text_for_symbols = 'символа'
        else:
            text_for_symbols = 'символов'

        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
                   'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ы', 'Э', 'Ю', 'Я', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        random_letters = self.rnd.pick_n(amount_of_letters, letters)
        picked_letters = ''

        for i in range(amount_of_letters):
            if i == amount_of_letters - 1:
                picked_letters += random_letters[i]
            else:
                picked_letters += random_letters[i] + ', '

        letters_and_digits = amount_of_letters
        amount_of_bits_for_one_symbol = 0
        for i in range(1, 11):
            if 2 ** i >= letters_and_digits:
                amount_of_bits_for_one_symbol = i
                break
        amount_of_bits = amount_of_bits_for_one_symbol * amount_of_symbols
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1
        final_amount_of_bytes = (amount_of_bytes + amount_of_extra_bytes) * amount_of_users

        self.text += f'''<p>При регистрации в компьютерной системе каждому пользователю выдаётся пароль, состоящий из
{amount_of_symbols} {text_for_symbols} и содержащий только символы из {amount_of_letters}-буквенного набора: {picked_letters}.</p>
<p>В базе данных для хранения сведений о каждом пользователе отведено одинаковое минимально возможное целое число байт.
При этом используют посимвольное кодирование паролей, все символы кодируют одинаковым минимально возможным количеством бит.
Кроме собственно пароля для каждого пользователя в системе хранятся дополнительные сведения, для чего выделено целое число байт,
одно и то же для всех пользователей.</p>
<p>Для хранения сведений о {amount_of_users} пользователях потребовалось {final_amount_of_bytes} байт.
Сколько байт выделено для хранения дополнительных сведений об одном пользователе?
В ответе запишите только целое число— количество байт.</p>'''

        self.correct = amount_of_extra_bytes

    def get_text_3(self, amount_of_symbols, amount_of_extra_bytes):
        amount_of_letters = self.rnd.in_range(5, 30)
        if amount_of_symbols == 21:
            text_for_symbols = 'буквы'
        else:
            text_for_symbols = 'букв'

        if amount_of_letters in [ 21, 31 ]:
            text_for_letters = 'различная буква'
        elif amount_of_letters in [ 22, 23, 24, 32, 33 ]:
            text_for_letters = 'различные буквы'
        else:
            text_for_letters = 'различных букв'

        letters_and_digits = amount_of_letters * 2
        amount_of_bits_for_one_symbol = 0
        for i in range(1, 11):
            if 2 ** i >= letters_and_digits:
                amount_of_bits_for_one_symbol = i
                break
        amount_of_bits = amount_of_bits_for_one_symbol * amount_of_symbols
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1
        final_amount_of_bytes = amount_of_bytes + amount_of_extra_bytes + 2

        self.text += f'''<p>Каждый сотрудник предприятия получает электронный пропуск, на котором записаны личный код сотрудника,
код подразделения и некоторая дополнительная информация. Личный код состоит из {amount_of_symbols} {text_for_symbols}.
Для формирования кодов используется {amount_of_letters} {text_for_letters}, каждая из которых может быть заглавной или строчной. </p>
<p>Для записи кода на пропуске отведено минимально возможное целое число байт. При этом используют посимвольное кодирование,
все символы кодируют одинаковым минимально возможным количеством бит. Код подразделения— целое четырёхзначное число,
он записан на пропуске как двоичное число и занимает минимально возможное целое число байт.
Всего на пропуске хранится {final_amount_of_bytes} байт данных.</p>
<p>Сколько байт выделено для хранения дополнительных сведений об одном сотруднике?
В ответе запишите только целое число— количество байт.</p>'''

        self.correct = amount_of_extra_bytes

    def generate(self):
        amount_of_symbols = self.amount_of_symbols
        amount_of_extra_bytes = self.amount_of_extra_bytes
        amount_of_users = self.amount_of_users
        task_choice = self.task_choice
        if task_choice == 1:
            self.get_text_1(amount_of_symbols, amount_of_extra_bytes, amount_of_users)
        elif task_choice == 2:
            self.get_text_2(amount_of_symbols, amount_of_extra_bytes, amount_of_users)
        else:
            self.get_text_3(amount_of_symbols, amount_of_extra_bytes)
        return self

class AmountOfInformationSport(DirectInput):
    def __init__(self, rnd):
        self.rnd = rnd
        self.amount_of_athletes = self.rnd.in_range(20, 1000)
        self.text = ''

    def get_text_1(self, amount_of_athletes):
        self.text += f'''<p>В велокроссе участвуют {amount_of_athletes} спортсменов.
Специальное устройство регистрирует прохождение каждым из участников промежуточного финиша,
записывая его номер с использованием минимально возможного количества бит, одинакового для каждого спортсмена.</p>
<p>Какой объём памяти будет использован устройством, когда все спортсмены прошли промежуточный финиш? (Ответ дайте в битах.)</p>'''

        amount_of_bits = 0
        for i in range(1, 11):
            if 2 ** i >= amount_of_athletes:
                amount_of_bits = i
                break

        self.correct = amount_of_bits * amount_of_athletes

    def get_text_2(self, amount_of_athletes):
        finished_athletes = self.rnd.in_range(10, amount_of_athletes - 5)

        self.text += f'''<p>В велокроссе участвуют {amount_of_athletes} спортсменов.
Специальное устройство регистрирует прохождение каждым из участников промежуточного финиша,
записывая его номер с использованием минимально возможного количества бит, одинакового для каждого спортсмена. </p>
<p>Каков информационный объем сообщения, записанного устройством, после того как промежуточный финиш прошли {finished_athletes} велосипедистов?
(Ответ дайте в байтах.)</p>'''

        amount_of_bits = 0
        for i in range(1, 11):
            if 2 ** i >= amount_of_athletes:
                amount_of_bits = i
                break
        amount_of_bits = amount_of_bits * finished_athletes
        amount_of_bytes = amount_of_bits // 8
        if amount_of_bits % 8 != 0:
            amount_of_bytes += 1

        self.correct = amount_of_bytes

    def generate(self):
        amount_of_athletes = self.amount_of_athletes
        if self.rnd.coin():
            self.get_text_1(amount_of_athletes)
        else:
            self.get_text_2(amount_of_athletes)
        return self

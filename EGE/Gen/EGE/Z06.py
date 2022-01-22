from math import log

from ...Bits import Bits
from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text

class FindNumber(DirectInput):
    def generate(self):
        minimal_number = self.rnd.in_range(8, 4096)
        number = Bits()
        number.set_size(int(log(minimal_number + 1) / log(2)) + 1)
        number.set_dec(minimal_number + 1)

        if number.get_bit(0) == 1:
            number.inc_autosize()
        
        while True:
            size = number.get_size()
            unit_count = 0
            for i in range(2, size):
                if number.get_bit(i):
                    unit_count += 1
            if number.get_bit(1) == unit_count % 2:
                break
            for i in range(1, 3):
                number.inc_autosize()
        
        number.shift_(2)

        self.text = f'''
На вход ал­го­рит­ма подаётся на­ту­раль­ное число N. Ал­го­ритм стро­ит по нему новое число R сле­ду­ю­щим об­ра­зом: <br />
1. Стро­ит­ся дво­ич­ная за­пись числа N.<br />
2. К этой за­пи­си до­пи­сы­ва­ют­ся спра­ва ещё два раз­ря­да по сле­ду­ю­ще­му пра­ви­лу: <br />
а) скла­ды­ва­ют­ся все цифры дво­ич­ной за­пи­си, и оста­ток от де­ле­ния суммы на 2 до­пи­сы­ва­ет­ся в конец числа (спра­ва).<br />
На­при­мер, за­пись 11100 пре­об­ра­зу­ет­ся в за­пись 111001; <br />
б) над этой за­пи­сью про­из­во­дят­ся те же дей­ствия – спра­ва до­пи­сы­ва­ет­ся оста­ток от де­ле­ния суммы цифр на 2. <br />
По­лу­чен­ная таким об­ра­зом за­пись (в ней на два раз­ря­да боль­ше, чем в за­пи­си ис­ход­но­го числа N) яв­ля­ет­ся дво­ич­ной за­пи­сью ис­ко­мо­го числа R.<br />
Ука­жи­те такое наи­мень­шее число N, для ко­то­ро­го ре­зуль­тат ра­бо­ты ал­го­рит­ма боль­ше {minimal_number}. В от­ве­те это число за­пи­ши­те в де­ся­тич­ной си­сте­ме счис­ле­ния.'''
        self.correct = number.get_dec()
        return self

class MinAddDigits(DirectInput):
    def generate(self):
        while True:
            # Не генерируем числа кратные 100.
            original = self.rnd.in_range(1, 9) * 100 + self.rnd.in_range(1, 99)
            result = self._convert(original)
            # Не генерируем число из примера.
            if (result != 712):
                break

        self.text = f'''
Автомат получает на вход трёхзначное число. По этому числу строится новое число по следующим правилам.
<ol>
<li>Складываются первая и вторая, а также вторая и третья цифры исходного числа.</li>
<li>Полученные два числа записываются друг за другом в порядке возрастания (без разделителей).</li>
</ol>
Пример. Исходное число: 348. Суммы: 3+4 = 7; 4+8 = 12. Результат: 712.<br />
Укажите наименьшее число, в результате обработки которого автомат выдаст число {result}.'''

        self.correct = self._get_min_origin(result)
        if result != self._convert(self.correct) or self.correct > original:
            raise ValueError(f"{original} => {result}, min = {self.correct}")
        return self

    def _convert(self, original: int) -> int:
        x, y, z = original // 100, (original // 10) % 10, original % 10
        a, b = sorted([ x + y, y + z ])
        return int(str(a) + str(b))

    def _get_min_origin(self, result: int) -> int:
        if result < 100:
            y, z = (result // 10) % 10, result % 10
            parts = [ 1, y - 1, z - y + 1 ]
        elif result < 1000:
            x, y, z = result // 100, (result // 10) % 10, result % 10
            part = y * 10 + z
            if part - x == 9:
                parts = [ 1, y - 1, z - y + 1 ]
            else:
                parts = [ 1, x - 1, part - x + 1 ]
        elif result < 10000:
            w, x, y, z = result // 1000, (result // 100) % 10, (result // 10) % 10, result % 10
            parts = [ w * 10 + x - 9, 9, y * 10 + z - 9 ]
        else:
            raise ValueError("result more or equal then 10000")
        return int(''.join([ str(part) for part in parts ]))

class Grasshopper(DirectInput):
    def generate(self):
        gcd = self.rnd.in_range(2, 5)
        forward = self.rnd.pick([ 3, 5, 7, 11, 13, 17, 19, ])
        backward = self.rnd.in_range(2, 20, forward)
        back_cnt = self.rnd.in_range(2, forward - 1)

        offset = ((forward - backward) * back_cnt) % forward

        start_pnt = self.rnd.in_range(0, 20)
        end_pnt = start_pnt + offset * gcd
        fg = forward * gcd
        bg = backward * gcd

        text_forms = [ 'единицу', 'единицы', 'единиц', ]
        fg_text = num_text(fg, text_forms)
        bg_text = num_text(bg, text_forms)

        self.text = f''' 
Исполнитель КУЗНЕЧИК живёт на числовой оси.
Начальное положение КУЗНЕЧИКА – точка {start_pnt}. Система команд Кузнечика:<br />
Вперед {fg} – Кузнечик прыгает вперёд на {fg_text},<br />
Назад {bg} – Кузнечик прыгает назад на {bg_text}.<br />
Какое наименьшее количество раз должна встретиться в программе команда «Назад {bg}»,
чтобы Кузнечик оказался в точке {end_pnt}?'''
        self.correct = back_cnt
        self.accept_number()
        return self

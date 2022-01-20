from math import log

from ...Bits import Bits
from ...GenBase import DirectInput


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
        return self

    def _convert(self):
        pass

    def _get_min_origin(self):
        pass

class Grasshopper(DirectInput):
    def generate(self):
        return self

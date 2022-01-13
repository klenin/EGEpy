from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text, num_by_words
from ...NotationBase import base_to_dec, dec_to_base

class Q1234(DirectInput):
    def generate(self):
        base = self.rnd.pick([ 5, 6, 7, 9, 11 ])
        self.correct = base_to_dec(base, '1234')
        self.accept_number()
        self.text = f'''Какое десятичное число в системе счисления по основанию {base} 
                        записывается как 1234<sub>{base}</sub>?'''
        return self

class LastDigit(DirectInput):
    def generate(self):
        base = self.rnd.in_range(5, 9)
        last = self.rnd.in_range(0, base - 1)
        corr = [ last + base * i for i in range(4) ]
        limit = corr[-1] + self.rnd.in_range(0, base - 1)
        self.correct = ','.join([ str(c) for c in corr ])
        self.accept = r'^(?:\d+,)+(\d+)$'
        self.text = f'''Укажите в порядке возрастания через запятую без пробелов 
                    все неотрицательные десятичные числа, 
                    <b><u>не превосходящие</u></b> {limit}, запись которых в системе 
                    счисления с основанием {base} оканчивается на {last}.'''
        return self

class LastDigitBase(DirectInput):
    def generate(self):
        while True:
            number = self.rnd.in_range(10, 60)
            rem = self.rnd.in_range(1, 9)
            bases = list(filter(lambda x: number % x == rem, range(2, number)))
            if len(bases) >= 2:
                break
        self.correct = ','.join([ str(b) for b in bases ])
        self.accept = r'^(?:\d+,)+\d+$'
        self.text = f'''Укажите в порядке возрастания через запятую без пробелов все основания систем счисления, 
                    в которых запись числа {number} оканчивается на {rem}.'''
        return self

class CountDigits(DirectInput):
    def generate(self):
        while True:
            num = self.rnd.in_range(200, 900)
            base = self.rnd.in_range(3, 9)
            self.correct = len(dec_to_base(base, num))
            if self.correct > 3:
                break
        self.accept_number()
        self.text = f'''Сколько значащих цифр в записи десятичного числа {num} 
                    в системе счисления с основанием {base}?'''
        return self

class SimpleEquation(DirectInput):
    def generate(self):
        dec_nums = [ self.rnd.pick(list(range(20, 201))) for _ in range(2) ]
        dec_nums.append(dec_nums[0] + dec_nums[1])
        bases = [ self.rnd.pick(list(range(2, 9))) for _ in range(3) ]
        nums = [ dec_to_base(bases[i], dec_nums[i]) for i in range(3) ]
        self.correct = nums[1]
        self.accept_number()
        self.text = f'''Решите уравнение {nums[0]}<sub>{bases[0]}</sub> + <i>x</i> = {nums[2]}<sub>{bases[2]}</sub> 
                        Ответ запишите в системе счисления с основанием {bases[1]}.'''
        return self

class CountOnes(DirectInput):
    def generate(self):
        base = self.rnd.in_range(2, 10)
        large_power = [ self.rnd.in_range(2013, 2025) for _ in range(2) ]
        base_power = [ self.rnd.in_range(1, 4) for _ in range(3) ]
        summands_base = [ base ** b for b in base_power ]
        answ = [ large_power[i] * base_power[i] for i in range(2) ]
        nums_text = [ 'единиц', 'двоек', 'троек', 'четверок', 'пятерок',
                      'шестерок', 'семерок', 'восьмерок', 'девяток' ]
        bases_text = [  'двоичной', 'троичной', 'четверичной', 'пятиричной', 'шестеричной',
                       'семеричной', 'восьмеричной', 'девятиричной', 'десятичной' ]
        self.correct = min(answ) - base_power[2] + int(base == 2)
        self.accept_number()
        self.text = f'''Cколько {nums_text[base - 2]} в {bases_text[base - 2]} записи числа 
                        {summands_base[0]}<sup>{large_power[0]}</sup> + 
                        {summands_base[1]}<sup>{large_power[1]}</sup> - {summands_base[2]}?'''
        return self

class SelectBase(DirectInput):
    def generate(self):
        base = self.rnd.in_range(3, 9)
        num = self.rnd.in_range(12, 500)
        converted_num = dec_to_base(base, num)
        self.correct = base
        self.accept_number()
        self.text = f'''В системе счисления с некоторым основанием десятичное число 
                    {num} записывается в виде {converted_num}. Укажите это основание.'''
        return self

class MoveNumber(DirectInput):
    def generate(self):
        base = self.rnd.in_range(3, 9)
        num = self.rnd.in_range(12, 500)
        converted_num = dec_to_base(base, num)
        self.correct = converted_num
        self.accept_number()
        self.text = f'''Запишите десятичное число {num} в системе счисления с основанием {base}. 
                        Основание системы счисления (нижний индекс после числа) писать не нужно.'''
        return self

class RangeCount(DirectInput):
    def generate(self):
        numbers_count = self.rnd.in_range(0, 1000)
        bounds = [ self.rnd.in_range(20, 1000) ]
        bounds.append(bounds[0] + numbers_count + 1)
        bases = self.rnd.pick_n(2, list(range(2, 17)))
        self.correct = numbers_count
        self.accept_number()
        dec_numbers = [ f'{dec_to_base(bases[i], bounds[i])}<sub>{bases[i]}</sub>' for i in range(2) ]
        self.text = f'''Сколько существует натуральных чисел x, для которых выполнено неравенство: 
                    {dec_numbers[0]} &lt; x &lt; {dec_numbers[1]}?<br/>
                    В ответе укажите только количество чисел, сами числа писать не нужно.'''
        return self

class MinRequiredBase(DirectInput):
    def generate(self):
        num = self.rnd.in_range(27, 500)
        len_base = lambda x: len(dec_to_base(x, num))
        length = self.rnd.in_range(3, len_base(3))
        base = 2
        while len_base(base) > length:
            base += 1
        self.correct = base
        self.accept_number()
        self.text = f'''Укажите наименьшее основание системы счисления, 
                        в которой запись числа {num}  {num_by_words(len_base(base), 1, 'genitive')} значна.'''
        return self

class MusicData:
    channels_title = [ 'моно', 'стерео (двухканальная запись)' ]
    more_less_title = [ 'больше', 'меньше' ]
    high_low_title = [ 'выше', 'ниже' ]

    def __init__(self, rnd, func_num: int):
        self.more_less_ = rnd.coin()
        self.hig_low1_ = rnd.coin()
        self.hig_low2_ = rnd.coin()
        self.channels_n = rnd.coin()
        self.sec_min_ = rnd.coin()
        self.time = rnd.in_range(1, 5)
        self.freq_ = rnd.in_range(2, 5)
        self.resol_ = rnd.in_range(2, 5)
        self.cap_ = rnd.in_range(2, 5)
        self.size = rnd.pick([ 10, 12, 15, 21, 25, 28, 35, 50 ])

        self.channels_w_1 = self.channels_title[self.channels_n]
        self.channels_n = 0 if self.channels_n == 1 else 1
        self.channels_w_2 = self.channels_title[self.channels_n]

        frac, c = 1, 0
        if self.hig_low1_:
            frac *= self.resol_
            c += 1
        if self.more_less_:
            frac *= self.freq_
            c += 1
        if not self.hig_low2_:
            frac *= self.cap_
            c += 1
        if not self.channels_n and func_num:
            frac *= 2
            c += 1

        if not c:
            self.ans_time = self.resol_ * self.freq_ * self.cap_ * self.time
            if func_num:
                self.ans_time *= 2
        elif c == 4 or c == 3 and not func_num:
            self.ans_time = rnd.in_range(2, 8)
            self.time = frac * self.ans_time
        else:
            self.ans_time = rnd.in_range(1, 8)
            self.time = frac * self.ans_time
            if not self.hig_low1_:
                self.ans_time *= self.resol_
            if not self.more_less_:
                self.ans_time *= self.freq_
            if self.hig_low2_:
                self.ans_time *= self.cap_
            if self.channels_n and func_num:
                self.ans_time *= 2

        self.more_less = self.more_less_title[self.more_less_]
        self.hig_low_1 = self.high_low_title[self.hig_low1_]
        self.hig_low_2 = self.high_low_title[self.hig_low2_]

        forms = [ 'секунду', 'секунды', 'секунд' ] if self.sec_min_ else [ 'минуту', 'минуты', 'минут' ]
        self.time_word_1 = num_text(self.time, forms)
        self.question = 'секунд' if self.sec_min_ else 'минут'

        forms = [ 'раз', 'раза', 'раз' ]
        self.resol = num_text(self.resol_, forms)
        self.freq = num_text(self.freq_, forms)
        self.cap = num_text(self.cap_, forms)

        frac, c = 1, 0
        if self.hig_low1_:
            frac *= self.resol_
            c += 1
        if self.more_less_:
            frac *= self.freq_
            c += 1
        if not self.channels_n:
            frac *= 2
            c += 1

        if not c:
            self.ans_size = self.size * self.resol_ * self.freq_ * 2
        elif c == 3:
            self.ans_size = rnd.in_range(2, 8)
            self.size = frac * self.ans_size
        else:
            self.ans_size = rnd.in_range(1, 8)
            self.size = frac * self.ans_size
            if not self.hig_low1_:
                self.ans_size *= self.resol_
            if not self.more_less_:
                self.ans_size *= self.freq_
            if self.channels_n:
                self.ans_size *= 2

class MusicTimeToTime(DirectInput):
    def generate(self):
        data = MusicData(self.rnd, 0)
        self.correct = data.ans_time
        self.accept_number()
        self.text = f'''Музыкальный фрагмент был оцифрован и записан в виде файла без использования сжатия данных. 
            Получившийся файл был передан в город А по каналу связи за {data.time_word_1}. 
            Затем тот же музыкальный фрагмент был оцифрован повторно с разрешением в {data.resol} {data.hig_low_1} 
            и частотой дискретизации в {data.freq} {data.more_less}, чем в первый раз. Сжатие данных не производилось. 
            Полученный файл был передан в город Б; пропускная способность канала связи с городом Б 
            в {data.cap} {data.hig_low_2}, чем канала связи с городом А. Сколько {data.question} длилась передача 
            файла в город Б? В ответе запишите только целое число, единицу измерения писать не нужно.'''
        return self

class MusicSizeToSize(DirectInput):
    def generate(self):
        data = MusicData(self.rnd, 1)
        self.correct = data.ans_size
        self.accept_number()
        self.text = f'''Музыкальный фрагмент был записан в формате {data.channels_w_1}, оцифрован и сохранён в виде файла 
            без использования сжатия данных. Размер полученного файла – {data.size} Мбайт. Затем тот 
            же музыкальный фрагмент был записан повторно в формате {data.channels_w_2} и 
            оцифрован с разрешением в {data.resol} {data.hig_low_1} и частотой дискретизации 
            в {data.freq} {data.more_less}, чем в первый раз. Сжатие данных не производилось. Укажите размер файла в Мбайт, 
            полученного при повторной записи. В ответе запишите только целое число, единицу измерения писать не нужно.'''
        return self

class MusicFormatTimeToTime(DirectInput):
    def generate(self):
        data = MusicData(self.rnd, 2)
        self.correct = data.ans_time
        self.accept_number()
        self.text = f'''Музыкальный фрагмент был записан в формате {data.channels_w_1}, оцифрован и сохранён в виде файла, 
            затем оцифрован и сохранён в виде файла без использования сжатия данных. Получившийся файл был 
            передан в город А по каналу связи за {data.time_word_1}. Затем тот же музыкальный фрагмент был 
            повторно записан в формате {data.channels_w_2} и оцифрован с разрешением в {data.resol} {data.hig_low_1} 
            и частотой дискретизации в {data.freq} {data.more_less}, чем в первый раз. Сжатие данных не производилось. 
            Полученный файл был передан в город Б; пропускная способность канала связи с городом Б в 
            {data.cap} {data.hig_low_2}, чем канала связи с городом А. Сколько {data.question} длилась передача файла в город Б? 
            В ответе запишите только целое число, единицу измерения писать не нужно.'''
        return self


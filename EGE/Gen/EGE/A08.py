from ...GenBase import SingleChoice
from ...RussianModules.NumText import num_text
from ...Logic import random_logic_expr, truth_table_string, equiv_not


class AudioData:
    channels_title = [
        'одноканальная (моно)',
        'двухканальная (стерео)',
        'четырехканальная (квадро)'
    ]

    def __init__(self, rnd):
        self.freq = rnd.pick([ 8, 11, 16, 22, 32, 44, 48, 50, 96, 176, 192 ])
        self.resol = 8 * rnd.in_range(2, 10)
        self.time = rnd.in_range(1, 10)
        self.channels_n = rnd.in_range(0, 2)
        self.channels_word = AudioData.channels_title[self.channels_n]
        self.time_word = num_text(self.time, [ 'минуту', 'минуты', 'минут' ])
        self.size = 2**self.channels_n * self.freq * 1000 * self.resol * self.time * 60.0 / 8

    def bad_ans(self, rnd, time: float):
        return rnd.pick_n(3, list(
            filter(
                lambda x: x >= 1,
                [ time * i for i in [ 0.1, 0.2, 0.25, 0.5, 2, 3, 4, 5, 10 ] ]
            )))

    def out(self, rnd, time: int, size: int, units: list):
        while time > size:
            time /= size
            units = units[1:] + [ units[1] ]
        return [ f'{i:.1f} {units[0]}' for i in [ time ] + self.bad_ans(rnd, time) ]


class AudioSize(SingleChoice):
    def generate(self):
        data = AudioData(self.rnd)
        self.text = f'''Производится {data.channels_word} звукозапись с частотой дискретизации 
                    {data.freq} кГц и {data.resol}-битным разрешением. 
                    Запись длится {data.time_word}, ее результаты записываются 
                    в файл, сжатие данных не производится. 
                    Какая из приведенных ниже величин наиболее близка к размеру полученного файла?'''
        self.set_variants(data.out(self.rnd, data.size, 1024, [ 'Байт', 'Кбайт', 'Мбайт', 'Гбайт' ]))
        return self


class AudioTime(SingleChoice):
    def generate(self):
        data = AudioData(self.rnd)
        self.text = f'''Производится {data.channels_word} звукозапись с частотой дискретизации 
                    {data.freq} кГц и {data.resol}-битным разрешением. Результаты записи записываются в файл, 
                    размер полученного файла — {data.size} байт; сжатие данных не производилось. 
                    Какая из приведенных ниже величин наиболее близка к времени, 
                    в течение которого происходила запись?'''
        self.set_variants([ f'{i:.1f} мин' for i in [ data.time ] + data.bad_ans(self.rnd, data.time) ])
        return self


class EquivCommon(SingleChoice):
    def generate_common(self, vars: list):
        e, e_text = self.rand_expr_text(vars)
        e_tts = truth_table_string(e)
        seen = {e_tts: 1}
        good, bad = [], []
        while not (good and len(bad) >= 3):
            if len(bad) > 30:
                # случайный перебор может работать долго, поэтому
                # через некоторое время применяем эквивалентное преобразование
                e1 = equiv_not(e)
                e1_text = e1.to_lang_named('Logic', { 'html': 1 })
            else:
                while True:
                    e1, e1_text = self.rand_expr_text(vars)
                    if e1_text not in seen:
                        seen[e1_text] = 1
                        break
            if truth_table_string(e1) == e_tts:
                good.append(e1_text)
            else:
                bad.append(e1_text)
        self.text = f'Укажите, какое логическое выражение равносильно выражению {e_text}.'
        self.set_variants([ good[0] ] + bad[0:3])
        return self

    def rand_expr_text(self, vars: list):
        e = random_logic_expr(self.rnd, vars)
        return e, e.to_lang_named('Logic', { 'html': 1 })


class Equiv3(EquivCommon):
    def generate(self):
        return self.generate_common([ 'A', 'B', 'C' ])


class Equiv4(EquivCommon):
    def generate(self):
        return self.generate_common([ 'A', 'B', 'C', 'D' ])


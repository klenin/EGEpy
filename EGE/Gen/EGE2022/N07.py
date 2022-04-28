from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text

from collections import namedtuple
from math import log, ceil, pow


range_tuple = namedtuple('range_tuple', [ 'min', 'max' ])
speed_range = range_tuple(19500, 120000)
palette_range = range_tuple(8, 64)
size_range = range_tuple(50, 2000)
bits_range = range_tuple(1, 64)
time_range = range_tuple(1, 360)


class LoggableData:
    def __str__(self):
        attrs = vars(self)
        fields = ', '.join("%s: %s" % item for item in attrs.items())
        return f'{self.__class__.__name__}: {fields}'


class ImageData(LoggableData):
    def __init__(self, rnd):
        self.speed = rnd.in_range(speed_range.min, speed_range.max)
        self.palette = rnd.in_range(palette_range.min, palette_range.max)
        self.bits = int(ceil(log(self.palette)))
        self.w = rnd.in_range(size_range.min, size_range.max)
        self.h = rnd.in_range(size_range.min, size_range.max)
        self.size = self.bits * self.w * self.h
        self.time = int(ceil(self.size / self.speed))


class ImageTransferTime(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        colors_word = num_text(data.palette, [ 'цвета', 'цветов', 'цветов' ])
        bits_word = num_text(data.bits, [ 'битом', 'битами', 'битами' ])
        variant = self.rnd.pick([
            f'цвет каждого пикселя кодируется {bits_word}',
            f'в палитре {colors_word}',
        ])

        self.text = f'''
Сколько секунд потребуется модему, передающему информацию 
со скоростью {data.speed} бит/с, чтобы передать 
растровое изображение размером {data.w} на {data.h} пикселей, 
при условии, что {variant}? 
Ответ округлить вверх до ближайшего целого.'''
        self.correct = data.time
        self.accept_number()

        return self


class TextData(LoggableData):
    def __init__(self, rnd):
        get_root = lambda m, n: int(ceil(pow(m, 1.0/n)))
        pages = get_root(rnd.in_range(speed_range.min, speed_range.max), 2)
        x = get_root(rnd.in_range(bits_range.min, bits_range.max), 2)
        y = get_root(rnd.in_range(bits_range.min, bits_range.max), 2)
        rows = get_root(rnd.in_range(time_range.min, time_range.max), 3)
        cols = get_root(rnd.in_range(time_range.min, time_range.max), 3)

        self.pages = pages
        self.rows = rows
        self.cols = cols
 
        self.symbols_per_page = self.rows * self.cols
        self.symbols_n = self.pages * self.symbols_per_page

        self.speed = self.pages * x
        self.time = y * self.symbols_per_page

        self.encoding_bits = x * y
        self.size = self.symbols_n * self.encoding_bits
        self.bigger_encoding_bits = rnd.in_range(self.encoding_bits, 2 * self.encoding_bits)
        self.bigger_size = self.symbols_n * self.bigger_encoding_bits
        self.size_diff_kb = int(ceil((self.bigger_size - self.size) / 2 ** 10))


class TextTransferTime(DirectInput):
    def generate(self):
        data = TextData(self.rnd)

        pages_word = num_text(data.pages, [ 'страница', 'страницы', 'страниц' ])
        symbols_n_word = num_text(data.symbols_n, [ 'символ', 'символа', 'символов' ])
        rows_word = num_text(data.rows, [ 'строку', 'строки', 'строк' ])
        cols_word = num_text(data.cols, [ 'символ', 'символа', 'символов' ])
        encoding_bits_word = num_text(data.encoding_bits, [ 'битом', 'битами', 'битами' ])
        variant = self.rnd.pick([
            f'{pages_word} текста по {symbols_n_word} каждая',
            f'{pages_word} текста в {rows_word} по {cols_word} каждая',
        ])

        self.text = f'''
Сколько секунд потребуется модему, передающему сообщения 
со скоростью {data.speed} бит/с, чтобы передать {variant}, 
при условии, что каждый символ кодируется {encoding_bits_word}?'''
        self.correct = data.time
        self.accept_number()

        return self


class TextTransferDataLength(DirectInput):
    def generate(self):
        data = TextData(self.rnd)

        symbols_per_page_word = num_text(data.symbols_per_page, [ 'символ', 'символа', 'символов' ])
        time_word = num_text(data.time, ['секунду', 'секунды', 'секунд'])
        variant = self.rnd.pick([
            [f'страниц содержал переданный текст, при условии, что на одной странице в среднем {symbols_per_page_word}', data.pages],
            [f'символов содержал переданный текст', data.symbols_n],
        ])

        self.text = f'''
Скорость передачи данных через интернет соединение равна {data.speed} бит/с. 
Передача текстового файла через это соединение заняла {time_word}. 
Определите, сколько {variant[0]}, 
если известно, что он был представлен в {data.encoding_bits}-битной кодировке.'''
        self.correct = variant[1]
        self.accept_number()

        return self


class TextFileResizeDiff(DirectInput):
    def generate(self):
        data = TextData(self.rnd)

        symbols_n_word = num_text(data.symbols_n, [ 'символа', 'символов', 'символов' ])

        self.text = f'''
Текстовый документ, состоящий из {symbols_n_word}, 
хранился в {data.encoding_bits}-битной кодировке. 
Этот документ был преобразован в {data.bigger_encoding_bits}-битную кодировку. 
Укажите, какое дополнительное количество Кбайт потребуется 
для хранения документа. В ответе запишите только число с округлением вверх.'''
        self.correct = data.size_diff_kb
        self.accept_number()

        return self


class TextFileResizeSymbolsN(DirectInput):
    def generate(self):
        data = TextData(self.rnd)

        self.text = f'''
Текстовый документ хранился в {data.encoding_bits}-битной кодировке. 
Этот документ был преобразован в {data.bigger_encoding_bits}-битную кодировку, 
при этом размер памяти, необходимой для хранения документа 
увеличился на {data.size_diff_kb} Кбайт. 
При этом хранится только последовательность кодов символов. 
Укажите, сколько символов в документе. 
В ответе запишите только число.'''
        self.correct = data.symbols_n
        self.accept_number()

        return self
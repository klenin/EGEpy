from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text, num_bits

from collections import namedtuple
from math import log, ceil, pow


range_tuple = namedtuple('range_tuple', [ 'min', 'max' ])
speed_range = range_tuple(19500, 120000)
palette_range = range_tuple(8, 64)
size_range = range_tuple(50, 2000)
bits_range = range_tuple(8, 256)
degrees_range = range_tuple(3, 64)
time_range = range_tuple(1, 360)


class LoggableData:
    def __str__(self):
        attrs = vars(self)
        fields = ', '.join("%s: %s" % item for item in attrs.items())
        return f'{self.__class__.__name__}: {fields}'


class ImageData(LoggableData):
    def __init__(self, rnd):
        self.speed = rnd.in_range(speed_range.min, speed_range.max)
        self.bits = rnd.pick([i for i in range(degrees_range.min, degrees_range.max + 1) if i % 3 == 0])
        self.w = rnd.in_range(size_range.min, size_range.max)
        self.h = rnd.in_range(size_range.min, size_range.max)
        self.palette = 2 ** self.bits
        self.size = self.bits * self.w * self.h
        self.size_kb = int(ceil(self.size / 2 ** 10 / 8))
        self.time = int(ceil(self.size / self.speed))

        self.bigger_bits = rnd.pick([i for i in range(self.bits + 1, degrees_range.max + 7) if i % 3 == 0])
        self.bigger_palette = 2 ** self.bigger_bits
        self.bigger_size = self.bigger_bits * self.w * self.h
        self.bigger_size_kb = int(ceil(self.bigger_size / 2 ** 10 / 8))

        self.extra_kb = rnd.in_range(10, 60)
        self.with_extra_size = self.size + self.extra_kb * 2 ** 13
        self.with_extra_size_kb = int(ceil(self.with_extra_size / 2 ** 13))

        self.time = rnd.in_range(time_range.min, time_range.max)#[i for i in range(1, 24 * 60 * 60 + 1) if abs(i * self.pictures_n - 24 * 60 * 60) < i][0]#int(ceil((24 * 60 * 60) / self.pictures_n))
        self.pictures_n = 24 * 60 * 60 // self.time
        self.file_size_pure = self.size * self.pictures_n
        self.file_size_pure_kb = int(ceil(self.file_size_pure / 2 ** 13))
        self.file_size_with_extra = self.with_extra_size * self.pictures_n
        self.file_size_kb = int(ceil(self.file_size_with_extra / 2 ** 13))   


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


class ImageStorageSize(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.h, [ 'пиксель', 'пикселя', 'пикселей' ])
        colors_word = num_text(data.palette, [ 'цвет', 'цвета', 'цветов' ])

        self.text = f'''
Какой минимальный объём памяти (в Кбайт) нужно зарезервировать, 
чтобы можно было сохранить любое растровое изображение 
размером {data.w} на {pixel_word} при условии, 
что в изображении могут использоваться {colors_word}? 
В ответе запишите только целое число с округлением вверх, 
единицу измерения писать не нужно.'''
        self.correct = data.size_kb
        self.accept_number()

        return self


class ImageStoragePalette(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.h, [ 'пиксель', 'пикселя', 'пикселей' ])
        variant = self.rnd.pick([
            [f'никакая дополнительная информация не сохраняется', data.size_kb],
            [f'{data.extra_kb} Кбайт необходимо выделить для служебной информации', data.with_extra_size_kb],
        ])

        self.text = f'''
Автоматическая фотокамера производит растровые изображения 
размером {data.w} на {pixel_word}. При этом объём файла с изображением 
не может превышать {variant[1]} Кбайт и {variant[0]}, упаковка данных не производится. 
Какое максимальное количество цветов можно использовать в палитре?'''
        self.correct = data.palette
        self.accept_number()

        return self


class ImageStorageResizePalette(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        self.text = f'''
Автоматическая фотокамера с {data.size_kb} Кбайт видеопамяти производит 
растровые изображения c фиксированным разрешением и {data.palette}-цветной палитрой. 
Сколько цветов можно будет использовать в палитре, 
если увеличить видеопамять до {data.bigger_size_kb} Кбайт?'''
        self.correct = data.bigger_palette
        self.accept_number()

        return self


class ImageStoragePicturesN(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.h, [ 'пиксель', 'пикселя', 'пикселей' ])
        colors_word = num_text(data.palette, [ 'цвет', 'цвета', 'цветов' ])

        self.text = f'''
Для проведения эксперимента создаются изображения, 
содержащие случайные наборы цветных пикселей. 
В палитре {colors_word}, размер изображения — {data.w} x {pixel_word}, 
при сохранении каждый пиксель кодируется одинаковым числом битов, 
все коды пикселей записываются подряд, методы сжатия не используются. 
Для каждого изображения дополнительно записывается 
{data.extra_kb} Кбайт служебной информации. 
Сколько изображений удастся записать, 
если для их хранения выделено {data.file_size_kb} Кбайт?'''
        self.correct = data.pictures_n
        self.accept_number()

        return self


class ImageStoragePicturesNForPeriod(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.h, [ 'пиксель', 'пикселя', 'пикселей' ])
        colors_word = num_text(data.palette, [ 'оттенок', 'оттенка', 'оттенков' ])

        self.text = f'''
Автоматическая фотокамера каждые {data.time} секунд 
создаёт черно-белое растровое изображение, 
содержащее {colors_word}. Размер изображения — {data.w} × {pixel_word}. 
Все полученные изображения и коды пикселей внутри одного изображения 
записываются подряд, никакая дополнительная информация не сохраняется, 
данные не сжимаются. Сколько Кбайт нужно выделить для хранения 
всех изображений, полученных за сутки? 
В ответе укажите только целое число — количество Кбайт с округлением вверх,
единицу измерения указывать не надо.'''
        self.correct = data.file_size_pure_kb
        self.accept_number()

        return self


class ImageStoragePicturesNPalette(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.h, [ 'пиксель', 'пикселя', 'пикселей' ])
        colors_word = num_text(data.palette, [ 'оттенок', 'оттенка', 'оттенков' ])
        file_size_bits_word = num_bits(data.file_size_with_extra)

        self.text = f'''
В информационной системе хранятся изображения 
размером {data.w} × {pixel_word}. Методы сжатия изображений не используются. 
Каждое изображение дополняется служебной информацией, 
которая занимает {data.extra_kb} Кбайт. Для хранения {data.pictures_n} изображений 
потребовалось {file_size_bits_word}. Сколько цветов использовано 
в палитре каждого изображения?'''
        self.correct = data.palette
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
        self.bigger_encoding_bits = rnd.in_range(self.encoding_bits + 1, 2 * self.encoding_bits)
        self.bigger_size = self.symbols_n * self.bigger_encoding_bits
        self.size_diff_kb = int(ceil((self.bigger_size - self.size) / 2 ** 10 / 8))


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
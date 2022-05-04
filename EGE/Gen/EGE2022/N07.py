from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text, num_bits

from collections import namedtuple
from math import log, ceil, pow


range_tuple = namedtuple('range_tuple', [ 'min', 'max' ])
speed_range = range_tuple(19500, 120000)
palette_range = range_tuple(8, 32)
size_range = range_tuple(50, 2000)
bits_range = range_tuple(8, 256)
degrees_range = range_tuple(3, 64)
time_range = range_tuple(1, 360)
inches_range = range_tuple(2, 9)
dpi_range = range_tuple(100, 600)


class LoggableData:
    def __str__(self):
        attrs = vars(self)
        fields = ', '.join("%s: %s" % item for item in attrs.items())
        return f'{self.__class__.__name__}: {fields}'


class ImageData(LoggableData):
    def __init__(self, rnd):
        self.speed = rnd.in_range(speed_range.min, speed_range.max)
        self.bits = rnd.pick([ i for i in range(degrees_range.min, degrees_range.max + 1) if i % 3 == 0 ])
        self.width = rnd.in_range(size_range.min, size_range.max)
        self.height = rnd.in_range(size_range.min, size_range.max)
        self.palette = 2 ** self.bits
        self.size = self.bits * self.width * self.height
        self.size_kilobytes = int(ceil(self.size / 2 ** 10 / 8))
        self.time = int(ceil(self.size / self.speed))

        self.bigger_bits = rnd.pick([ i for i in range(self.bits + 1, degrees_range.max + 7) if i % 3 == 0 ])
        self.bigger_palette = 2 ** self.bigger_bits
        self.bigger_size = self.bigger_bits * self.width* self.height
        self.bigger_size_kilobytes = int(ceil(self.bigger_size / 2 ** 10 / 8))

        self.extra_kilobytes = rnd.in_range(10, 60)
        self.with_extra_size = self.size + self.extra_kilobytes * 2 ** 13
        self.with_extra_size_kilobytes = int(ceil(self.with_extra_size / 2 ** 13))

        self.daily_time_seconds = rnd.in_range(time_range.min, time_range.max)
        self.pictures_number= 24 * 60 * 60 // self.daily_time_seconds
        self.file_size_pure = self.size * self.pictures_number
        self.file_size_pure_kilobytes = int(ceil(self.file_size_pure / 2 ** 13))
        self.file_size_with_extra = self.with_extra_size * self.pictures_number
        self.file_size_kilobytes = int(ceil(self.file_size_with_extra / 2 ** 13))   

        self.inches_width = rnd.in_range(inches_range.min, inches_range.max)
        self.inches_height = rnd.in_range(inches_range.min, inches_range.max)
        self.dpi = rnd.in_range(dpi_range.min, dpi_range.max)
        self.dots = self.inches_width * self.inches_height * self.dpi
        self.size_inches_bits = self.dots * self.bits
        self.size_inches_kilobytes = int(ceil(self.size_inches_bits / 2 ** 13))

        self.bigger_dpi = rnd.in_range(self.dpi + 1, 2 * self.dpi)
        self.bigger_size_inches_bits = self.inches_width * self.inches_height * self.bigger_dpi * self.bigger_bits


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
растровое изображение размером {data.width} на {data.height} пикселей, 
при условии, что {variant}? 
Ответ округлить вверх до ближайшего целого.'''
        self.correct = data.time
        self.accept_number()

        return self


class ImageStorageSize(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.height, [ 'пиксель', 'пикселя', 'пикселей' ])
        colors_word = num_text(data.palette, [ 'цвет', 'цвета', 'цветов' ])

        self.text = f'''
Какой минимальный объём памяти (в Кбайт) нужно зарезервировать, 
чтобы можно было сохранить любое растровое изображение 
размером {data.width} на {pixel_word} при условии, 
что в изображении могут использоваться {colors_word}? 
В ответе запишите только целое число с округлением вверх, 
единицу измерения писать не нужно.'''
        self.correct = data.size_kilobytes
        self.accept_number()

        return self


class ImageStoragePalette(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.height, [ 'пиксель', 'пикселя', 'пикселей' ])
        variant = self.rnd.pick([
            [ f'никакая дополнительная информация не сохраняется', data.size_kilobytes ],
            [ f'{data.extra_kilobytes} Кбайт необходимо выделить для служебной информации', data.with_extra_size_kilobytes ],
        ])

        self.text = f'''
Автоматическая фотокамера производит растровые изображения 
размером {data.width} на {pixel_word}. При этом объём файла с изображением 
не может превышать {variant[1]} Кбайт и {variant[0]}, упаковка данных не производится. 
Какое максимальное количество цветов можно использовать в палитре?'''
        self.correct = data.palette
        self.accept_number()

        return self


class ImageStorageResizePalette(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        self.text = f'''
Автоматическая фотокамера с {data.size_kilobytes} Кбайт видеопамяти производит 
растровые изображения c фиксированным разрешением и {data.palette}-цветной палитрой. 
Сколько цветов можно будет использовать в палитре, 
если увеличить видеопамять до {data.bigger_size_kilobytes} Кбайт?'''
        self.correct = data.bigger_palette
        self.accept_number()

        return self


class ImageStoragePicturesN(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.height, [ 'пиксель', 'пикселя', 'пикселей' ])
        colors_word = num_text(data.palette, [ 'цвет', 'цвета', 'цветов' ])

        self.text = f'''
Для проведения эксперимента создаются изображения, 
содержащие случайные наборы цветных пикселей. 
В палитре {colors_word}, размер изображения — {data.width} x {pixel_word}, 
при сохранении каждый пиксель кодируется одинаковым числом битов, 
все коды пикселей записываются подряд, методы сжатия не используются. 
Для каждого изображения дополнительно записывается 
{data.extra_kilobytes} Кбайт служебной информации. 
Сколько изображений удастся записать, 
если для их хранения выделено {data.file_size_kilobytes} Кбайт?'''
        self.correct = data.pictures_number
        self.accept_number()

        return self


class ImageStoragePicturesNForPeriod(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.height, [ 'пиксель', 'пикселя', 'пикселей' ])
        colors_word = num_text(data.palette, [ 'оттенок', 'оттенка', 'оттенков' ])

        self.text = f'''
Автоматическая фотокамера каждые {data.daily_time_seconds} секунд 
создаёт черно-белое растровое изображение, 
содержащее {colors_word}. Размер изображения — {data.width} × {pixel_word}. 
Все полученные изображения и коды пикселей внутри одного изображения 
записываются подряд, никакая дополнительная информация не сохраняется, 
данные не сжимаются. Сколько Кбайт нужно выделить для хранения 
всех изображений, полученных за сутки? 
В ответе укажите только целое число — количество Кбайт с округлением вверх,
единицу измерения указывать не надо.'''
        self.correct = data.file_size_pure_kilobytes
        self.accept_number()

        return self


class ImageStoragePicturesNPalette(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        pixel_word = num_text(data.height, [ 'пиксель', 'пикселя', 'пикселей' ])
        colors_word = num_text(data.palette, [ 'оттенок', 'оттенка', 'оттенков' ])
        file_size_bits_word = num_bits(data.file_size_with_extra)

        self.text = f'''
В информационной системе хранятся изображения 
размером {data.width} × {pixel_word}. Методы сжатия изображений не используются. 
Каждое изображение дополняется служебной информацией, 
которая занимает {data.extra_kilobytes} Кбайт. Для хранения {data.pictures_number} изображений 
потребовалось {file_size_bits_word}. Сколько цветов использовано 
в палитре каждого изображения?'''
        self.correct = data.palette
        self.accept_number()

        return self


class ImageStorageDpiSize(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        colors_word = num_text(data.palette, [ 'цвета', 'цветов', 'цветов' ])
        inches_word = num_text(data.inches_height, [ 'дюйм', 'дюйма', 'дюймов' ])

        self.text = f'''
Рисунок размером {data.inches_width} x {inches_word} отсканировали 
с разрешением {data.dpi} dpi и использованием {colors_word}. 
Определите размер полученного файла без учёта 
служебных данных и возможного сжатия. 
В ответе запишите целое число — размер файла в Кбайтах с округлением вверх.'''
        self.correct = data.size_inches_kilobytes
        self.accept_number()

        return self


class ImageStorageDpiResize(DirectInput):
    def generate(self):
        data = ImageData(self.rnd)

        bigger_colors_word = num_text(data.bigger_palette, [ 'цвет', 'цветв', 'цветов' ])
        colors_word = num_text(data.palette, [ 'цвет', 'цветв', 'цветов' ])
        bigger_size_inches_bits_word = num_bits(data.bigger_size_inches_bits)

        self.text = f'''
Для хранения в информационной системе документы 
сканируются с разрешением {data.bigger_dpi} dpi и цветовой системой, 
содержащей {bigger_colors_word}. Методы сжатия изображений 
не используются. Средний размер отсканированного документа 
составляет {bigger_size_inches_bits_word}. В целях экономии было решено перейти 
на разрешение {data.dpi} dpi и цветовую систему, содержащую {colors_word}. 
Сколько бит будет составлять средний размер документа, 
отсканированного с изменёнными параметрами?'''
        self.correct = data.size_inches_bits
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
        self.symbols_number= self.pages * self.symbols_per_page

        self.speed = self.pages * x
        self.time = y * self.symbols_per_page

        self.encoding_bits = x * y
        self.size = self.symbols_number* self.encoding_bits
        self.bigger_encoding_bits = rnd.in_range(self.encoding_bits + 1, 2 * self.encoding_bits)
        self.bigger_size = self.symbols_number * self.bigger_encoding_bits
        self.size_diff_kilobytes = int(ceil((self.bigger_size - self.size) / 2 ** 10 / 8))


class TextTransferTime(DirectInput):
    def generate(self):
        data = TextData(self.rnd)

        pages_word = num_text(data.pages, [ 'страница', 'страницы', 'страниц' ])
        symbols_number_word = num_text(data.symbols_number, [ 'символ', 'символа', 'символов' ])
        rows_word = num_text(data.rows, [ 'строку', 'строки', 'строк' ])
        cols_word = num_text(data.cols, [ 'символ', 'символа', 'символов' ])
        encoding_bits_word = num_text(data.encoding_bits, [ 'битом', 'битами', 'битами' ])
        variant = self.rnd.pick([
            f'{pages_word} текста по {symbols_number_word} каждая',
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
            [ f'страниц содержал переданный текст, при условии, что на одной странице в среднем {symbols_per_page_word}', data.pages ],
            [ f'символов содержал переданный текст', data.symbols_number],
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

        symbols_number_word = num_text(data.symbols_number, [ 'символа', 'символов', 'символов' ])

        self.text = f'''
Текстовый документ, состоящий из {symbols_number_word}, 
хранился в {data.encoding_bits}-битной кодировке. 
Этот документ был преобразован в {data.bigger_encoding_bits}-битную кодировку. 
Укажите, какое дополнительное количество Кбайт потребуется 
для хранения документа. В ответе запишите только число с округлением вверх.'''
        self.correct = data.size_diff_kilobytes
        self.accept_number()

        return self


class TextFileResizeSymbolsN(DirectInput):
    def generate(self):
        data = TextData(self.rnd)

        self.text = f'''
Текстовый документ хранился в {data.encoding_bits}-битной кодировке. 
Этот документ был преобразован в {data.bigger_encoding_bits}-битную кодировку, 
при этом размер памяти, необходимой для хранения документа 
увеличился на {data.size_diff_kilobytes} Кбайт. 
При этом хранится только последовательность кодов символов. 
Укажите, сколько символов в документе. 
В ответе запишите только число.'''
        self.correct = data.symbols_number
        self.accept_number()

        return self

from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text

from collections import namedtuple
from math import log, ceil


range_tuple = namedtuple('range_tuple', ['min', 'max'])
speed_range = range_tuple(19500, 50000)
palette_range = range_tuple(8, 64)
size_range = range_tuple(50, 2000)


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

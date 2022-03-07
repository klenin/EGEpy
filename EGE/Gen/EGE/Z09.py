from math import log

from ...GenBase import DirectInput

class GetMemorySize(DirectInput):
    def generate(self):
        color_count = 2 ** self.rnd.in_range(6, 10)
        picture_size = 2 ** self.rnd.in_range(6, 10)

        self.text = f'''
Какой минимальный объём памяти (в Кбайт) нужно зарезервировать, чтобы
можно было сохранить любое растровое изображение размером
{picture_size}×{picture_size} пикселов при условии, что в изображении могут использоваться
{color_count} различных цветов?
В ответе запишите только целое число, единицу измерения писать не нужно.'''

        self.correct = picture_size ** 2 * log(color_count) / log(2) / 8 / 1024
        return self

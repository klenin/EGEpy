from ...GenBase import SingleChoice

class RGB(SingleChoice):
    def generate(self):
        rgb = [ self.rnd.coin() for _ in range(3) ]
        pure = self.rnd.coin()
        level = 'FF' if pure else f'{self.rnd.in_range(200, 250):X}'
        color = ''.join([ level if r else '00' for r in rgb ])
        self.set_variants([ self.color_name(pure, self.invert(i, rgb)) for i in range(-1, 3) ])
        self.text = f'''Для кодирования цвета фона страницы Интернет используется атрибут
                    bgcolor="#XXXXXX", где в кавычках задаются шестнадцатеричные значения
                    интенсивности цветовых компонент в 24-битной RGB-модели.
                    Какой цвет будет у страницы, заданной тегом &lt;body bgcolor="{color}">?'''
        return self

    def color_name(self, pure: bool, rgb: list):
        colors = {
            '000': 'Чёрный',
            '001': 'Синий',
            '010': 'Зелёный',
            '011': 'Голубой',
            '100': 'Красный',
            '101': 'Фиолетовый',
            '110': 'Желтый',
            '111': 'Белый' if pure else 'Серый',
        }
        return colors.get(''.join([ str(i) for i in rgb ]))

    def invert(self, index: int, rgb: list):
        return [ rgb[i] ^ (i == index) for i in range(len(rgb)) ]


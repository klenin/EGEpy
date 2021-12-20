from ...GenBase import SingleChoice
from ...Bin import Bin
from ...Bits import Bits
from ...Russian.NumText import num_text


class SumNumbers(SingleChoice):
    def generate(self):
        av = self.rnd.in_range(17, 127)
        bv = self.rnd.in_range(17, 127)
        r = av + bv
        atext = Bin.oct_text(av)
        btext = Bin.oct_text(bv)

        self.text = f'Чему равна сумма чисел <i>a</i> = {atext} и <i>b</i> = {btext}?'
        errors = self.rnd.pick_n(3, list(map(lambda x: av ^ (1 << x), range(8))))
        self.set_variants(list(map(lambda x: Bin.bin_hex_or_oct(x, self.rnd.in_range(0, 2)), [r] + errors)))

        return self


class CountZeroOne(SingleChoice):
    def __generate_by_count(self, val, size, count):
        return Bits() \
            .set_bin([1] + [(1 - val) for _ in range(size - 1)]) \
            .flip(self.rnd.pick_n(count - val, list(range(size - 1)))) \
            .get_dec()

    def generate(self):
        val = self.rnd.coin()
        num_size = self.rnd.in_range(7, 10)
        count = self.rnd.in_range(2, num_size - 4)

        self.set_variants(list(map(lambda x: self.__generate_by_count(val, num_size, count + x), range(-1, 3))))

        self.text = 'Для каждого из перечисленных ниже десятичных чисел построили двоичную запись. ' \
                    + 'Укажите число, двоичная запись которого содержит ровно %s.' % \
                    num_text(
                        count,
                        ['единица', 'единицы', 'единиц']
                        if val != 0 else
                        ['значащий нуль', 'значащих нуля', 'значащих нулей']
                    )
        self.correct = 1

        return self

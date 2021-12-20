class Bin:
    @staticmethod
    def bin_text(number):
        return bin(number) + '<sub>2</sub>'

    @staticmethod
    def oct_text(number):
        return '%o<sub>8</sub>' % number

    @staticmethod
    def hex_text(number):
        return '%X<sub>16</sub>' % number

    @staticmethod
    def bin_hex_or_oct(number, numeral_system_index):
        return [Bin.bin_text, Bin.oct_text, Bin.hex_text][numeral_system_index](number)

from EGE.GenBase import DirectInput
import re


class DotDict(dict):
    """
    a dictionary that supports dot notation 
    as well as dictionary access notation 
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value


def _generate_string(rnd, str_len):
    result = ''.join([chr(rnd.pick([rnd.in_range(ord('0'), ord('9')), 
                                        rnd.in_range(ord('A'), ord('Z')),
                                        rnd.in_range(ord('a'), ord('z'))])) for i in range(str_len)])
    return result


class LengthOfSymbolsSequence(DirectInput):
    def generate(self):
        str_len = self.rnd.in_range(10**5, 10**6)
        rnd_str = _generate_string(self.rnd, str_len)

        filename = 'N24_string.txt'

        with open(filename, 'w') as fout:
            fout.write(rnd_str)

        types = [
            DotDict({
                'type': 'одинаковых символов',
                'ans_func': self._same_symbols_len
            }),
            DotDict({
                'type': 'цифр',
                'ans_func': self._numbers_len
            }),
        ]

        rnd_type = self.rnd.get(2)
        chosen_type = types[rnd_type]

        text = f"""\
                    В файле <a href="{filename}" download="{filename}">{filename}</a> записана последовательность символов.
                    Укажите длину самой длинной последовательности, состоящей из {chosen_type.type}.
                    """
        self.text = '\n'.join([line.strip() for line in text.split('\n') if line.strip() != ''])
        self.correct = chosen_type.ans_func(rnd_str)
        self.accept_number()

        return self

    def _same_symbols_len(self, s):
        result = 1
        tmp_result = 1

        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                tmp_result += 1
            else:
                result = max(result, tmp_result)
                tmp_result = 1

        result = max(result, tmp_result)

        return result
    
    def _numbers_len(self, s):
        numbers_str = '0123456789'

        result = 0
        tmp_result = s[0] in numbers_str

        for i in range(1, len(s)):
            if s[i] in numbers_str and s[i - 1] in numbers_str:
                tmp_result += 1
            else:
                result = max(result, tmp_result)
                tmp_result = s[i] in numbers_str

        result = max(result, tmp_result)

        return result


class NthOccurenceInString(DirectInput):
    def generate(self):
        str_len = self.rnd.in_range(10**5, 10**6)
        rnd_str = _generate_string(self.rnd, str_len)

        filename = 'N24_nth_occurence_string.txt'

        with open(filename, 'w') as fout:
            fout.write(rnd_str)

        rnd_symbol = self.rnd.pick(list(set(rnd_str)))
        symbol_n = len(re.findall(rnd_symbol, rnd_str))
        rnd_pos = self.rnd.get(symbol_n)

        text = f"""\
                    В файле <a href="{filename}" download="{filename}">{filename}</a> записана последовательность символов. На какой позиции от начала строки
                    встречается {rnd_pos} символ «{rnd_symbol}»? Нумерация символов в строке ведется с единицы.
                    """
        self.text = '\n'.join([line.strip() for line in text.split('\n') if line.strip() != ''])
        self.correct =  self._find_symbol_start(rnd_symbol, rnd_str, rnd_pos)
        self.accept_number()

        return self
    
    def _find_symbol_start(self, symbol, string, occurence):
        return list(re.finditer(symbol, string))[occurence].start() + 1

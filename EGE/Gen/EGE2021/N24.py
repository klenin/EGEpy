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

allowed_symbols = [chr(x) for x in range(ord('0'), ord('9') + 1)] \
                    + [chr(x) for x in range(ord('A'), ord('Z') + 1)] \
                    + [chr(x) for x in range(ord('a'), ord('z') + 1)]

def _generate_string_from(rnd, str_len, allowed=None):
    if allowed == None:
        allowed = allowed_symbols

    result = ''.join([rnd.pick(allowed) for i in range(str_len)])
    return result


class LengthOfSymbolsSequence(DirectInput):
    def generate(self):
        str_len = self.rnd.in_range(10**5, 10**6)
        rnd_str = _generate_string_from(self.rnd, str_len)

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
        rnd_str = _generate_string_from(self.rnd, str_len)

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


class SubstringOccurencesInString(DirectInput):
    def generate(self):
        substr_len = self.rnd.get(10) + 1
        rnd_substr = ''.join(self.rnd.pick_n(substr_len, allowed_symbols))

        substr_n = self.rnd.in_range(1000, 2000)
        rnd_strs = []
        for i in range(substr_n + 1):
            str_len = self.rnd.in_range(1, 100)
            rnd_strs.append(_generate_string_from(self.rnd, str_len, [c for c in allowed_symbols if not (c == rnd_substr[-1])]))
        
        rnd_str = rnd_substr.join(rnd_strs)

        filename = 'N24_substr_occurence.txt'

        with open(filename, 'w') as fout:
            fout.write(rnd_str)

        text = f"""\
                    В файле <a href="{filename}" download="{filename}">{filename}</a> записана последовательность символов. 
                    Сколько подстрок «{rnd_substr}» содержится в файле?
                    """
        self.text = '\n'.join([line.strip() for line in text.split('\n') if line.strip() != ''])
        self.correct = substr_n
        self.accept_number()

        return self

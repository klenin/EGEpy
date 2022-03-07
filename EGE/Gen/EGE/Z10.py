from ...GenBase import DirectInput

class WordsCount(DirectInput):
    def generate(self):
        length = self.rnd.in_range(4, 6)

        consonants = list('БВГДЖЗКЛМНПРСТФХ'.strip())
        consonants_count = self.rnd.in_range(1, 3)
        consonants = self.rnd.pick_n(consonants_count, consonants)

        vowels = list('АЕИОУЫЭЮЯ'.strip())
        vowels_count = length - consonants_count
        vowels = self.rnd.pick_n(vowels_count, vowels)

        if self.rnd.coin() == 1:
            case = {
                'first': 'гласной',
                'num': vowels_count * length ** (length - 1)
            }
        else:
            case = {
                'first': 'согласной',
                'num': consonants_count * length ** (length - 1)
            }

        self.text = f'''
Сколь­ко слов длины {length}, на­чи­на­ю­щих­ся с {case['first']} буквы, можно со­ста­вить из букв:
{', '.join(self.rnd.shuffle(consonants + vowels))}.
Каж­дая буква может вхо­дить в слово не­сколь­ко раз.
Слова не обя­за­тель­но долж­ны быть осмыс­лен­ны­ми сло­ва­ми рус­ско­го языка.'''
        self.correct = case['num']
        return self

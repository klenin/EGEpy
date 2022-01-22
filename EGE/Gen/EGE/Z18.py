from EGE.GenBase import DirectInput, EGEError

class BitwiseConjunction(DirectInput):
    def generate(self):
        p1 = self.rnd.in_range(1, 255)
        p2 = self.rnd.in_range(1, 255, p1)
        ans = p1 & p2 ^ p1
        x = self.rnd.in_range(1, 255)
        if not ((x & p1) == 0 or (x & p2) != 0 or (x & ans) != 0):
            raise EGEError()
        self.correct = ans
        self.accept_number()
        and_text = '&nbsp;&amp;&nbsp;'
        self.text = f'''
Обозначим через <i>m</i>{and_text}<i>n</i> поразрядную конъюнкцию неотрицательных целых чисел <i>m</i> и <i>n</i>. 
Так, например, 14{and_text}5 = 1110<sub>2</sub>{and_text}0101<sub>2</sub> = 0100<sub>2</sub> = 4. 
Для какого наименьшего неотрицательного целого числа <i>А</i> формула 
<blockquote><i>x</i>{and_text}{p1} = 0 ∨ (<i>x</i>{and_text}{p2} = 0 → <i>x</i>{and_text}<i>А</i> ≠ 0)</blockquote> 
тождественно истинна (т.е. принимает значение 1 при любом 
неотрицательном целом значении переменной <i>х</i>)?
'''
        return self

import math

import EGE.RussianModules.Names
from EGE.GenBase import DirectInput
from EGE.Utils import nrange, ucfirst
from EGE.RussianModules.NumText import num_by_words

class WhoIsRight(DirectInput):
    def __positive_stmt(self, p: list, me: int, rest: list):
        if not rest:
            return 'никто не разбил'
        stmt = self.rnd.pick([
            [ 'это' ] * 3,
            [ 'это сделал', 'это сделала', 'это сделали' ],
            [ 'виноват', 'виновата', 'виноваты' ],
            [ 'всему виной' ] * 3,
        ])
        s = stmt[2 if len(rest) > 1 else p[rest[0]]['gender']]
        return f"{ucfirst(s)} {' или '.join([ 'я' if i == me else p[i]['name'] for i in rest ])}"

    def __negative_stmt(self, p: list, me: int, rest: list):
        if not rest:
            return 'никто не разбил'
        neg = self.rnd.pick([
            [ 'не виноват', 'не виновата', 'не виновны' ],
            [ 'этого не делал', 'этого не делала', 'этого не делали' ],
            [ 'не разбивал', 'не разбивала', 'не разбивали' ],
        ])
        if len(rest) > 1:
            s = ', '.join([ 'ни я' if i == me else f"ни {p[i]['name']}" for i in rest ])
        else:
            s = 'я' if rest[0] == me else p[rest[0]]['name']
        return f"{ucfirst(s)} {neg[2 if len(rest) > 1 else p[rest[0]]['gender']]}"

    def __make_powers(self, n: int):
        ans_pow = self.rnd.in_range(1, n - 1)
        ans_index = self.rnd.in_range(0, n - 1)
        powers = [self.rnd.in_range(0, n - 3) for _ in range(0, n)]
        powers = [p + 2 if p >= ans_pow else p + 1 for p in powers]
        powers[ans_index] = ans_pow
        return powers

    def __make_stmts(self, n: int):
        row_powers = self.__make_powers(n)

        ans = {}
        for i in range(0, n):
            ans[i] = {s: 1 for s in self.rnd.pick_n(row_powers[i], nrange(0, n - 1))}
        col_powers = [ 0 ] * n
        for i in range(0, n):
            for j in range(0, n):
                if i in ans and j in ans[i]:
                    col_powers[j] += 1
        pow_col = {}
        for i in range(0, n):
            if col_powers[i] not in pow_col:
                pow_col[col_powers[i]] = []
            pow_col[col_powers[i]].append(i)
        min, mi = n + 1, -1
        for pow in pow_col.keys():
            if len(pow_col[pow]) < min:
                min, mi = len(pow_col[pow]), pow
        # если нет столбца с уникальной степенью - добавляем новую строку
        # и в ней ставим единички так, чтобы появился столбец с уникальной ст-ю
        elems = self.rnd.shuffle(pow_col[mi])
        ans_index = elems.pop(0)
        if elems:
            ans[n] = { e: 1 for e in elems }
            n += 1
        return n, col_powers[ans_index], ans_index, ans


    def generate(self):
        n = self.rnd.in_range(7, 9)
        people = EGE.RussianModules.Names.different_names(self.rnd, n + 1)

        n, ans_pow, ans_index, stmts = self.__make_stmts(n)
        self.text = ''
        for i in range(0, n):
            h = stmts[i]
            if len(h) <= math.ceil(5 / 2):
                s = self.__positive_stmt(people, i, list(h.keys()))
            else:
                s = self.__negative_stmt(people, i, [ i for i in range(0, n) if i not in h ])
            self.text += f"{people[i]['name']}:  «{s}»<br/>"

        action = self.rnd.pick([
            [ 'разбил окно', 'в кабинете' ],
            [ 'разбил цветочный горшок', 'в кабинете' ],
            [ 'разбил мензурки', 'в лаборатории' ],
            [ 'разбил люстру', 'в учительской' ],
        ])

        big_men = self.rnd.pick([
            [ 'директору', 'директора' ],
            [ 'завучу', 'завуча' ],
            [ 'классному руководителю', 'руководителя' ],
            [ 'участковому', 'участкового' ],
        ])

        self.text = f"""
{ucfirst(num_by_words(n, 0))} школьников, остававшихся в классе на перемене, были вызваны 
к {big_men[0]}. <strong>Один из них</strong> {' '.join(action)}. На вопрос {big_men[1]}
, кто это сделал, были получены следующие ответы:<br/><p>{self.text}</p>
Кто {action[0]}, если известно, что из этих {num_by_words(n, 0, 'genitive')} высказываний 
{'истинно' if ans_pow == 1 else 'истинны'} <strong>только {num_by_words(ans_pow, 2)}</strong>
? Ответ запишите в виде первой буквы имени."""

        self.correct = people[ans_index]['name'][0]
        return self

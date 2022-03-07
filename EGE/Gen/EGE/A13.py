from ...GenBase import SingleChoice
from functools import reduce
import re

extensions = [ 'txt', 'doc', 'png', 'lst', 'gif', 'jpg', 'map', 'cpp', 'pas', 'bas' ]
introduction_text = '''<p>Для групповых операций с файлами используются <b>маски имён файлов</b>.
        Маска представляет собой последовательность букв, цифр, и прочих допустимых
        в именах файлов символов, в которой также могут встречаться следующие символы:
        </p>
        <p>Символ «?» (вопросительный знак) означает ровно один произвольный символ.
        </p>
        <p>Символ «*» (звёздочка) означает любую последовательность символов произвольной длины,
        в том числе и пустую последовательность.
        </p>'''

def random_chars(rnd, n: int):
    return [ rnd.english_letter() for _ in range(n) ]

def random_str(rnd, n: int):
    return ''.join(random_chars(rnd, n))

def exact_gen_file(rnd, mask: str, ok: bool):
    fn = ''
    for c in mask:
        if c == '?':
            fn += random_str(rnd, 1 if ok else rnd.pick([0, 2, 3]))
        elif c == '*':
            fn += random_str(rnd, rnd.in_range(0, 3))
        else:
            fn += c
    return fn

def select_pos(rnd, len: int, metachars: int):
    while True:
        pos = sorted(rnd.pick_n(metachars, list(range(len))), reverse=True)
        if metachars <= 1 or pos[0] != pos[1] + 1:
            break
    return pos

def put_mask_to_s(s: str, m: list, pos: list):
    t = s
    for i in range(len(pos)):
        t = t[:pos[i]] + m[i] + t[pos[i] + 1:]
    return t

def join_arr(a: list, b: list):
    return [ f'{ai}.{bi}' for bi in b for ai in a ]


class GetFileNameByMask(SingleChoice):
    def gen_file(self, mask: str, bad_q: int):
        fn = ''
        for c in mask:
            if c == '?':
                bad_q -= 1
                fn += random_str(self.rnd, 1 if bad_q else self.rnd.pick([0, 2, 3]))
            elif c == '*':
                fn += random_str(self.rnd, self.rnd.in_range(0, 3))
            else:
                fn += c
        return f'<tt>{fn}</tt>'

    def generate(self):
        ext = self.rnd.pick(extensions)
        i = self.rnd.in_range(0, len(ext) - 1)
        ext_mask = ext[:i] + '?' + ext[i + self.rnd.coin():]

        while True:
            mask = ''.join(self.rnd.shuffle(self.rnd.pick_n(2, [ '?', '?', '*' ]) + random_chars(self.rnd, 5)))
            if not re.search(r'(\?\*|\*\?)', mask):
                break
        mask += '.' + ext_mask
        bad_mask = re.sub(r'(\w)(\w)', r'\1' + self.rnd.english_letter() + r'\2', mask, count=1)

        self.text = introduction_text
        self.text += f'Определите, какие из указанных имён файлов удовлетворяют маске <tt>{mask}</tt>'
        self.set_variants([ self.gen_file(bad_mask, 0) ] + [ self.gen_file(mask, i) for i in range(3) ])
        self.correct = 1
        return self


class GetFileNameByFourMasks(SingleChoice):
    def gen_masks(self, s: str, metachars: int):
        pos = select_pos(self.rnd, len(s), metachars)
        was_q = False
        while True:
            res = []
            for _ in range(4):
                m = [ self.rnd.pick(['?', '*']) for _ in range(metachars) ]
                res.append(m)
                for mi in m:
                    was_q |= mi == '?'
            if was_q:
                break
        return [ put_mask_to_s(s, r, pos) for r in res ]

    def gen_names(self, masks: list, patterns: list, good: bool, count: int):
        check_l = [
            lambda a, pattern, s: a or not re.search(pattern, s),
            lambda a, pattern, s: a and re.search(pattern, s)
        ]
        check = check_l[int(good)]
        res = []
        i = 0
        used = {}
        while len(res) < count:
            f = exact_gen_file(self.rnd, masks[i], good)
            if f in used:
                continue
            if reduce(lambda a, b: check(a, patterns[b], f), [ int(good) ] + list(range(4))):
                res.append(f)
                used[f] = 1
            i = (i + 1) % count
        return res

    def mask_to_regexp(self, mask: str):
        mask = re.sub(r'\*', '.*', mask)
        mask = re.sub(r'\?', '.', mask)
        return f'^{mask}$'

    def gen_good_bad_names(self, s: str, metachars: int):
        masks = self.gen_masks(s, metachars)
        patterns = [ self.mask_to_regexp(m) for m in masks ]
        good = self.gen_names(masks, patterns, True, 1)
        bad = self.gen_names(masks, patterns, False, 2)
        return masks, good, bad

    def generate(self):
        s = random_str(self.rnd, self.rnd.in_range(5, 8))
        ext = self.rnd.pick(extensions)

        base_masks, good_base, bad_base = self.gen_good_bad_names(s, 2)
        ext_masks, good_ext, bad_ext = self.gen_good_bad_names(ext, 1)

        good_ans = join_arr(good_base, good_ext)
        bad_ans = [
            join_arr(good_base, bad_ext),
            join_arr(bad_base, good_ext),
            join_arr(bad_base, bad_ext)
        ]
        self.set_variants(good_ans + self.rnd.pick_n(3, bad_ans))
        self.text = introduction_text
        self.text += ' Определите, какой из указанных файлов удовлетворяет всем маскам:<ul>'
        self.text += ''.join([ f'<li>{base_masks[i]}.{ext_masks[i]}</li>' for i in range(4) ]) + '</ul>'
        return self


class GetMaskByTwoFileNames(SingleChoice):
    def gen_masks_names(self, s: str, metachars: int):
        pos = select_pos(self.rnd, len(s), metachars)
        masks_arr = [
            [ [ '*' ], [ '?' ] ],
            [ [ '*', '*' ], [ '*', '?' ], [ '?', '*' ], [ '?', '?' ] ],
        ]
        mask_arr = masks_arr[metachars - 1]
        masks = [ put_mask_to_s(s, m, pos) for m in mask_arr ]
        names = [ exact_gen_file(self.rnd, m, False) for m in masks ]
        return masks, names

    def generate(self):
        s = random_str(self.rnd, self.rnd.in_range(5, 8))
        ext = self.rnd.pick(extensions)
        base_masks, base_names = self.gen_masks_names(s, 2)
        ext_masks, ext_names = self.gen_masks_names(ext, self.rnd.pick([1, 2]))

        masks = join_arr(base_masks, ext_masks)
        good, bad = masks[0], masks[1:]
        self.set_variants([ good ] + self.rnd.pick_n(3, bad))

        # FIXME: Правильный ответ содержит только *.
        self.text = introduction_text
        self.text += ' Определите, по какой из масок будет выбрана указанная группа файлов: <ul>'
        self.text += ''.join([ f'<li>{base_names[i]}.{ext_names[i]}</li>' for i in range(2) ]) + '</ul>'
        return self


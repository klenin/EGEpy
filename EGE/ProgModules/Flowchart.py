from dataclasses import dataclass
import re

import EGE.Svg as svg
import EGE.Html as html

FONT_SZ = 15

@dataclass
class Jump:
    src: dict = None
    dest: dict = None
    dir: str = None
    label: str = None

#TODO add dataclasses for points and enums for anchors and directions

def arrow_head(dir: str):
    AL, AW = 10, 5
    dx, dy, v = {
        'right':   [ -AL, AW, False ],
        'up':      [ AW, AL, True   ],
        'left':    [ AL, AW, False  ],
        'down':    [ AW, -AL, True  ]
    }[dir]
    ndx, ndy = -dx, -dy
    return f"l{dx},{dy} m{ndx},{ndy} l" + (f"{ndx},{dy} " if v else f"{dx},{ndy} ")

def quote_tspan(*args):
    a = [a for a in args]
    if re.search(r"[<&]", a[0]):
        a[0] = html.cdata(a[0])
    return svg.tspan(a[0], **a[1])


class Flowchart:

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.texts_ = {}
        self.jumps_ = []

    def add_text(self, anchor: str, *args):
        if anchor in self.texts_:
            self.texts_[anchor].append(args)
        else:
            self.texts_[anchor] = [args]

    def make_jump(self, jump_data: Jump = None):
        if jump_data is None:
            jump_data = Jump()
        self.jumps_.append(jump_data)
        return self.jumps_[len(self.jumps_) - 1]

    def down(self, step=30):
        self.y2 += step

    def point(self, x: float = None, y: float = None):
        return {'x': 0 if x is None else x,
                'y': self.y2 if y is None else y}

    def add_box(self, statements: list, enter: Jump, exit_: Jump):
        w = max(map(len, statements)) * FONT_SZ
        self.x1 = min(self.x1, -w / 2)
        self.x2 = max(self.x2, w / 2)
        y = self.y2 + FONT_SZ
        for st in statements:
            self.add_text('middle', st, { 'x': 0, 'y': y })
            y += FONT_SZ

        r = svg.rect(
            x=-w / 2, y=self.y2,
            width=w, height=y - self.y2
        )
        if enter:
            enter.dest = self.point()
        self.y2 = y
        if exit_:
            exit_.src = self.point()
        return r

    def add_rhomb(self, cond: str, enter: Jump, exits: dict[str, Jump]):
        w = len(cond) * FONT_SZ
        self.x1 = min(self.x1, -w)
        self.x2 = max(self.x2, w)
        fs = FONT_SZ * 2
        if enter:
            enter.dest = self.point()
        r = svg.path(
            d=f"M0,{self.y2} l-{w},{fs} l{w},{fs} l{w},-{fs} z"
        )
        self.add_text('middle', cond, { 'x': 0, 'y': self.y2 + fs })

        exits_data = (
            ( 'left',  -w, fs     ),
            ( 'right',  w, fs     ),
            ( 'middle', 0, 2 * fs )
        )
        for exit_, x, dy in exits_data:
            if exit_ in exits:
                exits[exit_].src = { 'x': x, 'y': self.y2 + dy }
        self.down(fs * 2)
        return r

    def texts(self):
        r = ''
        for anchor in self.texts_.keys():
            t = self.texts_[anchor]
            r += svg.text('\n' + ''.join(map(lambda x: quote_tspan(*x), t)), **{
                'font-size': FONT_SZ,
                'text-anchor': anchor,
                'dominant-baseline': 'middle'
            })
        return r

    def jumps(self):
        p = ""
        for j in self.jumps_:
            sx, sy = j.src['x'], j.src['y']
            dx, dy = j.dest['x'], j.dest['y']
            label = j.label if j.label else ''
            p += f"M{sx},{sy} "
            if sx == 0 and (j.dir is None or len(j.dir) == 0):
                if label:
                    self.add_text(
                        'start', label,
                        { 'x': sx + FONT_SZ / 2, 'y': sy + FONT_SZ / 2 }
                    )
                p += f"V{dy} " + arrow_head('down')
                continue
            right = j.dir == 'right' or sx > 0
            dist = max(1, len(label)) * FONT_SZ
            if right:
                self.x2 += dist
            else:
                self.x1 -= dist
            x = self.x2 if right else self.x1
            if label:
                self.add_text(
                    'start' if right else 'end', label,
                    { 'x': sx, 'y': sy - FONT_SZ / 2 }
                )
            ah = arrow_head('down' if dy > sy else
                                 'left' if right else 'right')
            if dy > sy:
                dy -= 20
                ah = f"v20 {ah}"
            else:
                p += 'v10 '
            p += f"H{x} V{dy} H{dx} {ah}"
        return svg.path(d=p)

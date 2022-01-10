from ...GenBase import SingleChoice
from ... import Html as html
from ... import Svg as svg

class RobotLoop(SingleChoice):
    def generate(self):
        dirs = [ 'вверх', 'вниз', 'влево', 'вправо' ]
        tests = [ f'{i} свободно' for i in [ 'сверху', 'снизу', 'слева', 'справа' ] ]
        count = self.rnd.in_range(1, 4)
        self.correct = count - 1
        while True:
            lab = self.gen_labyrinth()
            program = self.gen_program()
            if self.count_loops(lab, program) == count:
                break
        html_program = '<br/>'.join([
            'НАЧАЛО',
            *[ f'ПОКА &lt; <b>{tests[p]}</b> > <b>{dirs[p]}</b>' for p in program ],
            'КОНЕЦ\n'
        ])
        self.text = f'''<p>Система команд исполнителя РОБОТ, «живущего» в прямоугольном 
                лабиринте на клетчатой плоскости:</p> {self.row(dirs)}
                 <p>При выполнении этих команд РОБОТ перемещается на одну клетку 
                соответственно: вверх ↑, вниз ↓, влево ←, вправо →.</p>
                <p>Четыре команды проверяют условие отсутствия стены у той клетки, 
                где находится РОБОТ</p> {self.row(tests)}
                 <p>Цикл<br/>ПОКА &lt; <i>условие</i> > <i>команда</i> <br/>
                выполняется, пока условие истинно, 
                иначе происходит переход на следующую строку.<br/> 
                Сколько клеток приведённого лабиринта соответствует условию, что, 
                выполнив предложенную ниже программу, 
                РОБОТ остановится в той же клетке, с которой он начал движение?</p>\n'''
        self.text += html.tag('table', html.row('td', [ html_program, self.svg_labyrinth(lab) ]))
        self.set_variants(list(range(1, 5)))
        return self

    def row(self, data: list):
        return html.tag('table', html.row('td', data), border=1)

    def walls(self, lab: list, x: int, y: int):
        return [
            int(not y) or lab[y - 1][x] & 2, lab[y][x] & 2,
            int(not x) or lab[y][x - 1] & 1, lab[y][x] & 1
        ]

    def gen_labyrinth(self):
        s = 5
        lab = [ [ 0 for _ in range(s + 1) ] for _ in range(s + 1) ]
        for i in range(s + 1):
            lab[i][s] |= 1
            lab[s][i] |= 2
        wall_count = self.rnd.in_range(8, 12)
        for _ in range(1, wall_count + 1):
            while True:
                x = self.rnd.in_range(0, s)
                y = self.rnd.in_range(0, s)
                w = self.rnd.coin() + 1
                if lab[y][x] & w or 3 not in set(filter(lambda z: z != 0, self.walls(lab, x, y))):
                    lab[y][x] |= w
                    break
        return lab

    def gen_program(self):
        c1, c2 = self.rnd.coin(), self.rnd.coin()
        program = [ c1, c2, 1 - c1, 1 - c2 ]
        for i in [ 0, 2 ] if self.rnd.coin() else [ 1, 3 ]:
            program[i] |= 2
        return program

    def execute_program(self, lab: list, program: list, x: int, y: int):
        offset = ( (-1, 0), (1, 0), (0, -1), (0, 1) )
        for move in program:
            while not self.walls(lab, x, y)[move]:
                y += offset[move][0]
                x += offset[move][1]
        return x, y

    def count_loops(self, lab: list, program: list):
        count = 0
        for sy in range(len(lab)):
            for sx in range(len(lab[sy])):
                x, y = self.execute_program(lab, program, sx, sy)
                if not (x == sx and y == sy):
                    continue
                count += 1
                lab[y][x] |= 8
        return count

    def mh(self, x: int, y: int, l: int, step: int):
        return f'M{x * step},{y * step} h{l * step}'

    def mv(self, x: int, y: int, l: int, step: int):
        return f'M{x * step},{y * step} v{l * step}'

    def svg_labyrinth(self, lab: list):
        step = 25
        nx, ny = len(lab[0]), len(lab)
        sizes = [ nx * step, ny * step ]
        mh_mv = [ self.mh(0, i, nx, step) for i in range(1, ny) ] + [ self.mv(i, 0, ny, step) for i in range(1, nx) ]
        r = '\n' + svg.start([ str(x) for x in [ 0, 0 ] + sizes ])
        r += svg.path(stroke='gray', d=' '.join(mh_mv))
        r += html.open_tag('g', { 'stroke': 'black', 'stroke-width': 2 })
        r += svg.rect(x=1, y=1, width=sizes[0] - 2, height=sizes[1] - 2, fill='none')
        p = []
        for y in range(ny):
            for x in range(nx):
                c = lab[y][x]
                if x < nx - 1 and c & 1:
                    p.append(self.mv(x + 1, y, 1, step))
                if y < ny - 1 and c & 2:
                    p.append(self.mh(x, y + 1, 1, step))
        r += svg.path(d=' '.join(p))
        return html.div_xy(r + html.close_tag('g') + svg.end(), sizes[0], sizes[1])


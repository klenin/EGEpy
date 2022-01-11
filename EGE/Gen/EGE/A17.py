from ...GenBase import SingleChoice
from ...Svg import *
from ...Html import open_tag, close_tag, div_xy
from ...RussianModules.Subjects import subjects
from math import ceil, sin, cos

def get_regions():
    return ['Адыгея',
            'Башкортостан',
            'Бурятия',
            'Алтай',
            'Дагестан',
            'Ингушетия',
            'Калмыкия',
            'Карелия',
            'Коми',
            'Мордовия',
            'Якутия',
            'Осетия',
            'Татарстан',
            'Удмуртия',
            'Хакасия',
            'Чувашия']

colors = [ 'red', 'green', 'blue' ]
SZ = 350
STEP = 10
LEFT_MARKS = 50
LEGEND = 200

def labels_text(labels, anchor, baseline):
    labels = labels.replace('\n', '')
    return text(labels, **{'text-anchor': anchor, 'dominant-baseline': baseline})

def bar_chart(data, labels1, labels2):
    max_y = STEP // 2 + max(max(i) for i in data)
    sizes = (SZ + LEFT_MARKS + LEGEND + 10, SZ + 20)
    r = start([ 0, 0, *sizes ])

    grid_path = ''
    y_labels = ''
    for i in range(0, max_y, STEP):
        y = int((1 - i / max_y) * SZ)
        y_labels += tspan(i, **{'x': LEFT_MARKS - 5, 'y': y})
        grid_path += ' M' + str(LEFT_MARKS) + ",$y h" + str(SZ)

    r += labels_text(y_labels, 'end', 'middle')

    r += open_tag('g', {'stroke': 'black'})
    r += rect(**{'x': LEFT_MARKS, 'width': SZ, 'height': SZ, 'fill': 'none'})
    r += path(**{'d': grid_path, 'stroke-dasharray': '3,3'})

    total_data = len(data) * (len(data[0]) + 1) + 1
    pos = 0
    color = 0
    paths = [
        'M0,0 L10,10 M0,-10 L20,10 M-10,0 L10,20',
        'M0,10 L10,0 M-10,10 L10,-10 M20,0 L0,20',
        'M0,0 L10,10 M10,0 L0,10']
    step = SZ / total_data

    for row in data:
        for val in row:
            y = ceil(val / max_y * SZ)
            r += pattern(
                path(**{'d': paths[color // len(paths)],
                        'stroke': colors[color % len(colors)],
                        'stroke-width': 2}),
                **{'patternUnits': 'userSpaceOnUse',
                   'id': f"p{color}", 'viewBox': '0 0 10 10',
                   'width': STEP / 2, 'height': STEP / 2}
            )
            r += rect(
                **{'stroke-width': 2,
                   'x': LEFT_MARKS + ceil((pos+1) * step), 'y': SZ - y,
                   'width': ceil(step), 'height': y,
                   'fill': f"url(#p{color})"}
            )
            pos += 1
            color += 1
        pos += 1

    r += rect(**{'x': LEFT_MARKS + SZ + 10,
                 'width': LEGEND, 'height': 5 + 25 * len(labels2),
                 'fill': 'none'})
    pos = 0
    y_labels = ''
    for label in labels2:
        r += rect(
            **{'x': LEFT_MARKS + SZ + 15, 'y': 5 + 25 * pos,
               'width': 20, 'height': 20, 'fill': colors[pos]}
        )
        y_labels += tspan(label, **{'x': LEFT_MARKS + SZ + 40, 'y': 15 + 25 * pos})
        pos += 1
    r += close_tag('g')
    r += labels_text(y_labels, 'start', 'middle')

    pos = 1
    x_labels = ''
    i = 0
    for label in labels1:
        d = len(data[i])
        x_labels += tspan(
            label, **{'x': LEFT_MARKS + ceil((pos + d / 2) * step), 'y': SZ + 1})
        pos += d + 1
        i += 1
    r += labels_text(x_labels, 'middle', 'text-before-edge')

    return div_xy(r + end(), *sizes)

DEFAULT_PIE_SZ = 40
PI = 3.141592653589793238

def pie_chart(data, params={}):
    pie_colors = params.get('colors') or colors
    pie_sz = params.get('size') or DEFAULT_PIE_SZ
    if len(pie_colors) < len(data):
        raise ValueError('not enough colors defined')
    r = start([ 0, 0, pie_sz, pie_sz ]) + open_tag('g', { 'stroke': 'black' })
    radius = pie_sz / 2 - 5
    cx, cy = pie_sz / 2, pie_sz / 2
    prev_x, prev_y, angle = cx + radius, cy, 0
    total = sum(data)
    color = 0
    for i in data:
        large_arc = 1 if 2 * i >= total else 0
        angle += i / total * 2 * PI
        x = '%.5f' % (radius * cos(angle) + cx)
        y = '%.5f' % (radius * sin(angle) + cy)
        r += path(**{'d': f"M{cx},{cy} L{prev_x},{prev_y} A{radius},{radius} 0 {large_arc},1 {x},{y} Z ",
                     'fill': pie_colors[color]})
        color += 1
        prev_x = x
        prev_y = y
    return div_xy(r + close_tag('g') + end(), pie_sz * 2, pie_sz * 2)

class Diagram(SingleChoice):
    def generate(self):
        regions = self.rnd.pick_n(3, get_regions())
        subj = self.rnd.pick_n(3, subjects)
        splits = ([ 2, 1, 1 ], [ 1, 1, 1 ], [ 2, 2, 1 ], [ 3, 2, 1 ])
        self.correct = self.rnd.in_range(0, len(splits)-1)
        k = self.rnd.in_range(10, 20)
        data = [[0 for _ in range(3)] for _ in range(3)]
        for c in range(3):
            s = self.rnd.split_number(k * splits[self.correct][c], 3)
            for j in range(3):
                data[j][c] = s[j] * STEP
        chart = bar_chart(data, regions, subj)
        self.text = f'''На диаграмме показано количество участников олимпиады
по трём предметам в трёх регионах России {chart}
Какая из диаграмм правильно отражает соотношение участников 
из всех регионов по каждому предмету?'''
        self.set_variants([ pie_chart(split) for split in splits ])
        return self

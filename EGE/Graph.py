from . import Html as html
from . import Svg as svg
from math import sqrt
from dataclasses import dataclass

@dataclass
class GraphVertex:
    at: list = None

class Graph:
    def __init__(self, vertices: dict):
        self.vertices = vertices
        self.edges = {}

    def vertex_names(self):
        return self.vertices.keys()

    def edge1(self, v1: str, v2: str, w: int = None):
        for v in [ v1, v2 ]:
            if v not in self.vertices:
                raise ValueError(f'Unknown vertex {v}')
        if v1 not in self.edges:
            self.edges[v1] = {}
        self.edges[v1][v2] = w

    def edge2(self, v1: str, v2: str, w=None):
        self.edge1(v1, v2, w)
        if v2 not in self.edges:
            self.edges[v2] = {}
        self.edges[v2][v1] = w

    def is_oriented(self):
        for v1 in self.vertex_names():
            for v2 in self.edges.get(v1, {}).keys():
                if v1 not in self.edges.get(v2, {}):
                    return True
        return False

    def is_connected(self):
        if not self.vertices:
            return True
        visited = {}

        def visit(v: str):
            if v in visited:
                return
            visited[v] = 1
            if v not in self.edges:
                return
            for e in self.edges[v].keys():
                visit(e)

        vnames = list(self.vertex_names())
        visit(vnames[0])
        return sorted(vnames) == sorted(visited.keys())

    def count_paths(self, src: str, dest: str, cache: dict = None):
        if cache is None:
            cache = {}

        def dfs(v: str):
            if v == dest:
                cache[v] = 1
                return 1
            if v in cache:
                return cache[v]
            cnt = 0
            for e in self.edges.get(v, {}).keys():
                cnt += dfs(e)
            cache[v] = cnt
            return cnt

        return dfs(src)

    def count_path_min_weight(self, src: str, dest: str):
        INF = 9999999999
        d = { i: INF for i in self.vertices }
        used = { i: False for i in self.vertices }
        d[src] = 0
        for i in self.vertices:
            v = -1
            for j in self.vertices:
                if not used[j] and (v == -1 or d[j] < d[v]):
                    v = j
            if d[v] == INF:
                break
            used[v] = True

            for to, l in self.edges.get(v, {}).items():
                if d[v] + l < d[to]:
                    d[to] = d[v] + l

        return d[dest]

    def html_matrix(self, vertex_view_names: dict = None):
        vnames = sorted(self.vertex_names())
        if vertex_view_names:
            v_view_names = [vertex_view_names[v] for v in vnames]
        else:
            v_view_names = vnames
        r = html.row_n('td', [ '' ] + v_view_names)
        for v in vnames:
            e = self.edges.get(v, {})
            v_view_name = vertex_view_names[v] if vertex_view_names else v
            r += html.row_n('td', [ v_view_name ] + [ e.get(v, ' ') for v in vnames ])
        return html.tag('table', r, border=1)

    def bounding_box(self):
        xmin, ymin, xmax, ymax = None, None, None, None
        for v in self.vertices.values():
            x, y = v.at
            if xmin is None or x < xmin:
                xmin = x
            if xmax is None or x > xmax:
                xmax = x
            if ymin is None or y < ymin:
                ymin = y
            if ymax is None or y > ymax:
                ymax = y
        return [ xmin, ymin, xmax, ymax ]

    @staticmethod
    def add(ar1: list, ar2: list):
        return [ ar1[i] + ar2[i] for i in range(len(ar1)) ]

    @staticmethod
    def size(a: list):
        return [ a[0], a[1], a[2] - a[0], a[3] - a[1] ]

    def xy(self, pt: list, x: str, y: str):
        return { x: pt[0], y: pt[1] }

    def _vertex_children_str(self, src: str):
        edges = self.edges.get(src, {})
        b = ','.join([ f'{e}:{edges[e]}' if edges[e] is not None else f'{e}' for e in sorted(edges.keys()) ])
        return '{' + b + '}'

    def edges_string(self):
        b = ','.join([ f'{v}->{self._vertex_children_str(v)}' for v in sorted(self.vertex_names()) ])
        return '{' + b + '}'

    def as_svg(self, oriented: bool = None, radius: int = 5):
        if oriented is None:
            oriented = self.is_oriented()
        font_size = 3 * radius

        texts, lines = [], []
        for src in self.vertex_names():
            at = self.vertices[src].at
            texts.append([ src, { 'x': at[0] + radius, 'y': at[1] - 3 } ])

            edges = self.edges.get(src, {})
            for e in edges.keys():
                dest_at = self.vertices[e].at
                c = [ 0.5 * (at[i] + dest_at[i]) for i in range(0, 2) ]
                if at[1] == dest_at[1]:
                    c[1] -= font_size // 2
                else:
                    c[0] += 5
                if at == dest_at:
                    continue
                vx, vy = dest_at[0] - at[0], dest_at[1] - at[1]
                length = sqrt(vx ** 2 + vy ** 2)
                k = radius / length
                dx, dy = vx * k, vy * k
                x1, y1 = at[0] + dx, at[1] + dy
                x2, y2 = dest_at[0] - dx, dest_at[1] - dy
                lines.append({ 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2 })
                texts.append([ edges[e], self.xy(c, 'x', 'y') ])

        viewBox = self.size(self.add(self.bounding_box(), [-radius-1, -radius-font_size, radius+font_size, radius+1]))
        s = svg.start([ str(x) for x in viewBox ])
        if oriented:
            s += svg.defs(svg.marker(
                svg.path(d='M0,0 L4,6 L0,12 L18,6 z', fill='black'),
                id='arrow',
                markerWidth=10,
                markerHeight=10,
                refX=18,
                refY=6,
                orient='auto',
                markerUnits='userSpaceOnUse',
                viewBox='0 0 20 20'
            ))
        s += svg.g([ svg.circle(cx=v.at[0], cy=v.at[1], r=radius) for v in self.vertices.values() ],
                   fill='black',
                   stroke='black'
        )

        params = { 'stroke': 'black', 'stroke-width': 1 }
        if oriented:
            params |= { 'marker-end': 'url(#arrow)' }
        s += svg.g([ svg.line(**l) for l in lines ], **params)
        s += svg.g([ svg.text(t[0], **t[1]) for t in texts ], **{ 'font-size': font_size })
        s += svg.end()
        return s


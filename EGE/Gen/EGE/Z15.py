from EGE.GenBase import DirectInput
from ... import Html as html
from ...Graph import Graph, GraphVertex
from ...Russian import join_comma_and
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class CityRoadsVertex(GraphVertex):
    in_vertex: list = None
    min_inners: int = 0
    inners: dict = None

class CityRoads(DirectInput):
    grids = [
        {
            'vertices': {
                'А': CityRoadsVertex(at=[   0,  50 ], in_vertex=[                         ], min_inners=0),
                'Б': CityRoadsVertex(at=[  50,   0 ], in_vertex=[ 'А', 'В', 'Д'           ], min_inners=2),
                'В': CityRoadsVertex(at=[ 100,  50 ], in_vertex=[ 'А', 'Б', 'Г', 'Д', 'Е' ], min_inners=3),
                'Г': CityRoadsVertex(at=[  50, 100 ], in_vertex=[ 'А', 'В', 'Е'           ], min_inners=1),
                'Д': CityRoadsVertex(at=[ 150,   0 ], in_vertex=[ 'Б', 'В', 'Ж'           ], min_inners=2),
                'Ж': CityRoadsVertex(at=[ 200,  50 ], in_vertex=[ 'В', 'Д', 'Е'           ], min_inners=1),
                'Е': CityRoadsVertex(at=[ 150, 100 ], in_vertex=[ 'Г', 'В', 'Ж'           ], min_inners=1),
                'И': CityRoadsVertex(at=[ 250,   0 ], in_vertex=[ 'Д', 'Ж'                ], min_inners=1),
                'К': CityRoadsVertex(at=[ 300,  50 ], in_vertex=[ 'И', 'Ж', 'Е', 'Д'      ], min_inners=2),
            },
            'first_city': 'А',
            'last_city':  'К',
        },
        {
            'vertices': {
                'А': CityRoadsVertex(at=[   0, 100 ], in_vertex=[                    ], min_inners=0),
                'Б': CityRoadsVertex(at=[  45,  35 ], in_vertex=[ 'А', 'В', 'Ж'      ], min_inners=2),
                'В': CityRoadsVertex(at=[  50, 100 ], in_vertex=[ 'А', 'Б', 'Г', 'Е' ], min_inners=3),
                'Г': CityRoadsVertex(at=[  45, 150 ], in_vertex=[ 'А', 'В', 'Д'      ], min_inners=1),
                'Д': CityRoadsVertex(at=[  40, 200 ], in_vertex=[ 'А', 'Г',          ], min_inners=2),
                'Е': CityRoadsVertex(at=[ 110,  20 ], in_vertex=[ 'Б', 'В', 'Ж'      ], min_inners=1),
                'Ж': CityRoadsVertex(at=[ 100,  84 ], in_vertex=[ 'Е', 'Б', 'В', 'Г' ], min_inners=2),
                'З': CityRoadsVertex(at=[ 107, 140 ], in_vertex=[ 'Ж', 'Г', 'Д', 'И' ], min_inners=1),
                'И': CityRoadsVertex(at=[ 150, 193 ], in_vertex=[ 'Д', 'З',          ], min_inners=1),
                'К': CityRoadsVertex(at=[ 200, 120 ], in_vertex=[ 'Е', 'Ж', 'З', 'И' ], min_inners=3),
            },
            'first_city': 'А',
            'last_city':  'К',
        }
    ]

    def generate(self):
        iterations = 0
        while True:
            grid = self.rnd.pick(self.grids)
            g = self._generate_graph(grid)
            answer = g.count_paths(grid['first_city'], grid['last_city'])
            if 7 <= answer <= 20 or iterations > 20:
                break
            iterations += 1
        w, h = [ int(i * 1.2) for i in Graph.size(g.bounding_box())[2:4] ]
        self.correct = answer
        self.accept_number()
        self.text = f'''
<p>В таблице представлена схема дорог, соединяющих города 
{join_comma_and(sorted(g.vertex_names()))}. 
Двигаться по каждой дороге можно только в направлении, указанном стрелкой. 
Сколько существует различных дорог из города {grid['first_city']} в город {grid['last_city']}?</p> 
{html.div_xy(g.as_svg(), w, h, margin='0 auto')}
'''
        return self

    def _generate_graph(self, grid: dict):
        grid = deepcopy(grid)
        vertices = grid['vertices']
        g = Graph(vertices=vertices)
        for vertex_name in self.rnd.shuffle(list(vertices.keys())):
            vertex = vertices[vertex_name]
            if not vertex.in_vertex:
                continue
            inners_count = self.rnd.in_range(vertex.min_inners, len(vertex.in_vertex))
            inners = self.rnd.pick_n(inners_count, vertex.in_vertex)
            while inners:
                ci = inners.pop()
                if g.vertices[ci].inners is not None and vertex_name in g.vertices[ci].inners:
                    continue
                self._forward_dfs(vertex_name, ci, g)
                g.edge1(ci, vertex_name)
        return g

    def _forward_dfs(self, city: str, inner: str, g):
        self._update_inners(city, inner, g)
        for k in g.edges.get(city, {}):
            self._forward_dfs(k, city, g)

    def _update_inners(self, city: str, inner: str, g):
        if g.vertices[city].inners is None:
            g.vertices[city].inners = {}
        inners = g.vertices[city].inners
        inners[inner] = 0
        if g.vertices[inner].inners is not None:
            for k in g.vertices[inner].inners:
                inners[k] = 0


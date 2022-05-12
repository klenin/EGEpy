from ... import Html as html
from ...Graph import Graph, GraphVertex
from ...GenBase import DirectInput


class AmbiguousTableAndGraphCorrelation(DirectInput):
    graphs = [
        {
            'vertices': {
                'A': GraphVertex(at=[  50,  0  ]),
                'B': GraphVertex(at=[  25, 40  ]),
                'C': GraphVertex(at=[  75, 40  ]),
                'D': GraphVertex(at=[  50, 80  ]),
                'E': GraphVertex(at=[  25, 105 ]),
                'F': GraphVertex(at=[  75, 105 ]),
            },
            'edges': [
                [ 'A', 'B' ],
                [ 'A', 'C' ],
                [ 'B', 'D' ],
                [ 'C', 'D' ],
                [ 'D', 'E' ],
                [ 'D', 'F' ],
                [ 'E', 'F' ],
            ],
            'sought_for_vertices': [
                ['B', 'C'],
                ['E', 'F'],
                ['A', 'D']
            ],
            'size': {
                'x': 100,
                'y': 180
            }
        },
        {
            'vertices': {
                'A': GraphVertex(at=[  25,  0 ]),
                'B': GraphVertex(at=[  75,  0 ]),
                'C': GraphVertex(at=[   0, 25 ]),
                'D': GraphVertex(at=[  50, 25 ]),
                'E': GraphVertex(at=[ 100, 25 ]),
                'F': GraphVertex(at=[  25, 50 ]),
                'G': GraphVertex(at=[  75, 65 ]),
            },
            'edges': [
                [ 'A', 'B' ],
                [ 'A', 'C' ],
                [ 'A', 'D' ],
                [ 'B', 'D' ],
                [ 'C', 'D' ],
                [ 'C', 'F' ],
                [ 'F', 'D' ],
                [ 'F', 'G' ],
                [ 'G', 'D' ],
                [ 'G', 'E' ],
                [ 'E', 'D' ],
            ],
            'sought_for_vertices': [
                ['B', 'E'],
                ['A', 'G'],
                ['C', 'F']
            ],
            'size': {
                'x': 160,
                'y': 140
            }
        },
        {
            'vertices': {
                'A': GraphVertex(at=[  25,  0 ]),
                'B': GraphVertex(at=[  65,  0 ]),
                'C': GraphVertex(at=[  85, 15 ]),
                'D': GraphVertex(at=[ 100, 40 ]),
                'E': GraphVertex(at=[  85, 70 ]),
                'F': GraphVertex(at=[  25, 70 ]),
                'G': GraphVertex(at=[   0, 35 ]),
            },
            'edges': [
                [ 'A', 'G' ],
                [ 'A', 'B' ],
                [ 'A', 'F' ],
                [ 'B', 'C' ],
                [ 'C', 'D' ],
                [ 'C', 'E' ],
                [ 'D', 'E' ],
                [ 'E', 'F' ],
                [ 'F', 'G' ],
            ],
            'sought_for_vertices': [
                ['E', 'F'],
            ],
            'size': {
                'x': 160,
                'y': 140
            }
        },
        {
            'vertices': {
                'A': GraphVertex(at=[  25,   0 ]),
                'B': GraphVertex(at=[  75,   0 ]),
                'C': GraphVertex(at=[   0,  25 ]),
                'D': GraphVertex(at=[  50,  25 ]),
                'E': GraphVertex(at=[ 100,  25 ]),
                'F': GraphVertex(at=[  25,  50 ]),
                'G': GraphVertex(at=[  75,  65 ]),
            },
            'edges': [
                [ 'A', 'B' ],
                [ 'A', 'C' ],
                [ 'B', 'E' ],
                [ 'C', 'D' ],
                [ 'C', 'F' ],
                [ 'F', 'D' ],
                [ 'F', 'G' ],
                [ 'G', 'D' ],
                [ 'G', 'E' ],
                [ 'E', 'D' ],
            ],
            'sought_for_vertices': [
                ['A', 'B'],
                ['C', 'E'],
                ['F', 'G']
            ],
            'size': {
                'x': 160,
                'y': 140
            }
        },
        {
            'vertices': {
                'A': GraphVertex(at=[   0,  0 ]),
                'B': GraphVertex(at=[ 100,  0 ]),
                'C': GraphVertex(at=[   0, 25 ]),
                'D': GraphVertex(at=[  25, 25 ]),
                'E': GraphVertex(at=[  75, 25 ]),
                'F': GraphVertex(at=[   0, 50 ]),
                'G': GraphVertex(at=[ 100, 50 ]),
            },
            'edges': [
                [ 'A', 'B' ],
                [ 'A', 'C' ],
                [ 'A', 'D' ],
                [ 'B', 'E' ],
                [ 'B', 'G' ],
                [ 'C', 'D' ],
                [ 'C', 'F' ],
                [ 'F', 'E' ],
                [ 'F', 'G' ],
                [ 'G', 'E' ],
                [ 'E', 'D' ],
            ],
            'sought_for_vertices': [
                ['B', 'C'],
                ['E', 'F'],
                ['A', 'D']
            ],
            'size': {
                'x': 160,
                'y': 100
            }
        },
    ]

    def _pick_graph_data(self):
        graph_data = self.rnd.pick(self.graphs)
        vertices = list(graph_data['vertices'].keys())

        vertices_rename_dict = dict(zip(vertices, self.rnd.shuffle(vertices)))
        graph_data['vertices'] = { vertices_rename_dict[k]: v for k, v in graph_data['vertices'].items() }
        graph_data['edges'] = [ [ vertices_rename_dict[i[0]], vertices_rename_dict[i[1]]] for i in graph_data['edges'] ]
        if 'sought_for_vertices' in graph_data:
            graph_data['sought_for_vertices'] = [
                [vertices_rename_dict[i[0]], vertices_rename_dict[i[1]]] for i in graph_data['sought_for_vertices']
            ]

        return graph_data

    @staticmethod
    def _create_graph(graph_data):
        g = Graph(graph_data['vertices'])
        for v1, v2 in graph_data['edges']:
            g.edge2(v1, v2)

        return g

    def _get_table_vertices_names(self, g):
        permutation = self.rnd.shuffle(list(range(1, len(g.vertex_names()) + 1)))
        table_vertices_names = dict(zip(g.vertex_names(), permutation))

        return table_vertices_names

    def generate(self):
        graph_data = self._pick_graph_data()
        g = self._create_graph(graph_data)

        table_vertices_names = self._get_table_vertices_names(g)
        g_for_table = Graph({ table_vertices_names[k]: v for k, v in graph_data['vertices'].items() })
        for v1, v2 in graph_data['edges']:
            g_for_table.edge2(table_vertices_names[v1], table_vertices_names[v2], '*')

        first_vertex, last_vertex = self.rnd.pick(list(graph_data['sought_for_vertices']))

        self.text = f'''
На рисунке справа схема дорог Н-ского района изображена в виде графа, в таблице содержатся
сведения о дорогах между населенными пунктами (звездочка означает, что дорога между соответствующими городами есть). 
{g_for_table.html_matrix()} {html.div_xy(g.as_svg(), graph_data['size']['x'], graph_data['size']['y'], margin='5px')} 
Так как таблицу и схему рисовали независимо друг от друга, то нумерация населённых пунктов в таблице никак не связана с 
буквенными обозначениями на графе. Определите номера населенных пунктов {first_vertex} и {last_vertex} в таблице. В 
ответе запишите числа в порядке возрастания без разделителей.'''

        self.correct = ''.join(sorted(map(str, [ table_vertices_names[first_vertex], table_vertices_names[last_vertex] ])))
        self.accept_number()

        return self


class TableAndGraphCorrelation(AmbiguousTableAndGraphCorrelation):
    graphs = [
        {
            'vertices': {
                'A': GraphVertex(at=[  25,   0 ]),
                'B': GraphVertex(at=[  75,   0 ]),
                'C': GraphVertex(at=[ 100,  25 ]),
                'D': GraphVertex(at=[ 100,  75 ]),
                'E': GraphVertex(at=[  75, 100 ]),
                'F': GraphVertex(at=[  25, 100 ]),
                'G': GraphVertex(at=[   0,  50 ]),
                'H': GraphVertex(at=[  50,  50 ]),
            },
            'edges': [
                [ 'A', 'B' ],
                [ 'A', 'G' ],
                [ 'A', 'H' ],
                [ 'B', 'C' ],
                [ 'B', 'H' ],
                [ 'C', 'D' ],
                [ 'D', 'E' ],
                [ 'E', 'F' ],
                [ 'E', 'H' ],
                [ 'F', 'G' ],
                [ 'G', 'H' ],
            ],
            'size': {
                'x': 160,
                'y': 160
            }
        },
        {
            'vertices': {
                'A': GraphVertex(at=[   0, 50 ]),
                'B': GraphVertex(at=[  40, 50 ]),
                'C': GraphVertex(at=[  80, 50 ]),
                'D': GraphVertex(at=[ 100, 50 ]),
                'E': GraphVertex(at=[  20,  0 ]),
                'F': GraphVertex(at=[  60,  0 ]),
            },
            'edges': [
                [ 'A', 'B' ],
                [ 'A', 'E' ],
                [ 'B', 'E' ],
                [ 'B', 'C' ],
                [ 'B', 'F' ],
                [ 'C', 'F' ],
                [ 'C', 'D' ],
            ],
            'size': {
                'x': 160,
                'y': 100
            }
        },
        {
            'vertices': {
                'A': GraphVertex(at=[  50,   0 ]),
                'B': GraphVertex(at=[ 100,   0 ]),
                'C': GraphVertex(at=[   0,  50 ]),
                'D': GraphVertex(at=[  50,  50 ]),
                'E': GraphVertex(at=[ 100,  50 ]),
                'F': GraphVertex(at=[  25, 100 ]),
                'G': GraphVertex(at=[  75, 100 ]),
            },
            'edges': [
                [ 'A', 'B' ],
                [ 'A', 'C' ],
                [ 'A', 'D' ],
                [ 'B', 'E' ],
                [ 'D', 'E' ],
                [ 'C', 'D' ],
                [ 'F', 'D' ],
                [ 'G', 'F' ],
                [ 'G', 'D' ],
            ],
            'size': {
                'x': 160,
                'y': 160
            }
        },
        {
            'vertices': {
                'A': GraphVertex(at=[   0,  0 ]),
                'B': GraphVertex(at=[  30,  0 ]),
                'C': GraphVertex(at=[  60,  0 ]),
                'D': GraphVertex(at=[ 100,  0 ]),
                'E': GraphVertex(at=[   0, 50 ]),
                'F': GraphVertex(at=[  60, 50 ]),
                'G': GraphVertex(at=[ 100, 50 ]),
            },
            'edges': [
                [ 'A', 'B' ],
                [ 'A', 'E' ],
                [ 'B', 'C' ],
                [ 'C', 'D' ],
                [ 'C', 'E' ],
                [ 'C', 'F' ],
                [ 'C', 'G' ],
                [ 'D', 'G' ],
                [ 'G', 'F' ],
                [ 'F', 'E' ],
            ],
            'size': {
                'x': 160,
                'y': 100
            }
        },
    ]

    def generate(self):
        graph_data = self._pick_graph_data()
        g = self._create_graph(graph_data)

        table_vertices_names = self._get_table_vertices_names(g)
        g_for_table = Graph({table_vertices_names[k]: v for k, v in graph_data['vertices'].items()})

        weights = []
        while len(weights) != len(graph_data['edges']):
            weight = self.rnd.in_range(1, 20) * 5
            if weight not in weights:
                weights.append(weight)

        for i in range(len(graph_data['edges'])):
            g_for_table.edge2(
                table_vertices_names[graph_data['edges'][i][0]],
                table_vertices_names[graph_data['edges'][i][1]],
                weights[i])

        first_vertex = self.rnd.pick(list(g.vertex_names()))
        last_vertex = self.rnd.pick(list(g.edges.get(first_vertex).keys()))

        self.text = f'''
На рисунке справа схема дорог Н-ского района изображена в виде графа, в таблице содержатся 
сведения о длинах этих дорог (в километрах). {g_for_table.html_matrix()} 
{html.div_xy(g.as_svg(), graph_data['size']['x'], graph_data['size']['y'], margin='5px')} Так как таблицу и схему 
рисовали независимо друг от друга, то нумерация населённых пунктов в таблице никак не связана с буквенными обозначениями 
на графе. Определите какова длина дороги из пункта {first_vertex} в пункт {last_vertex} в таблице. В ответе запишите 
целое число – так, как оно указано в таблице.'''

        self.correct = g_for_table.count_path_min_weight(
            table_vertices_names[first_vertex],
            table_vertices_names[last_vertex])

        self.accept_number()

        return self


class OptimalWayInTable(AmbiguousTableAndGraphCorrelation):
    def generate(self):
        graph_data = self._pick_graph_data()

        weights = []
        while len(weights) != len(graph_data['edges']):
            weight = self.rnd.in_range(1, 20) * 5
            if weight not in weights:
                weights.append(weight)

        g = Graph(graph_data['vertices'])
        for v1, v2 in graph_data['edges']:
            g.edge2(v1, v2, weights.pop())

        first_vertex, last_vertex = self.rnd.pick_n(2, list(g.vertex_names()))

        self.text = f'''
Между населёнными пунктами {', '.join(sorted(g.vertex_names()))} построены дороги, протяжённость 
которых приведена в таблице. (Отсутствие числа в таблице означает, что прямой дороги между пунктами нет.)
{g.html_matrix()} Определите длину кратчайшего пути между пунктами {first_vertex} и {last_vertex} (при 
условии, что передвигаться можно только по построенным дорогам).'''

        self.correct = g.count_path_min_weight(
            first_vertex,
            last_vertex)

        self.accept_number()

        return self

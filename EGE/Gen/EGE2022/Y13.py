from dataclasses import dataclass

from EGE.GenBase import DirectInput
from ...Graph import Graph, GraphVertex
from ... import Html as html

MinVerticesCount = 10
MaxVerticesCount = 18

MinLayerSize = 2
MaxLayerSize = 4

GraphSVGWidthDelta = 120
GraphSVGHeight = 240

ConcatenateFarVertices = True

@dataclass
class ObjectLabel:
    nominative: str
    genitive: str
    plural: str

class PathCounting(DirectInput):
    def generate(self):
        self.vertices_label = self.rnd.pick([
            ObjectLabel('город', 'города', 'города'),
            ObjectLabel('пункт', 'пункта', 'пункты'),
        ])

        self.graph = self._generate_graph()
        self.text = self._generate_text()
        return self

    def _generate_graph(self) -> Graph:
        self.vertices_number = self.rnd.in_range(MinVerticesCount, MaxVerticesCount)
        self.vertices_names = self.__generate_vertices_names()

        self.start_vertex_name = self.vertices_names[0]
        self.end_vertex_name = self.vertices_names[-1]
        
        self.reserved_vertices_names = [ self.start_vertex_name, self.end_vertex_name ]

        self.__prepare_vertices_layers()

        graph = self._create_graph()
        return graph

    def __generate_vertices_names(self) -> list:
        ignored_names = [ 'Ё', 'Й' ]

        is_cyrillic_names = self.rnd.coin() == 1
        # First symbol is cyrillic 'А', other is latin 'A'
        start_symbol = 'А' if is_cyrillic_names else 'A'
        symbol_code = ord(start_symbol)

        vertices_names = [ start_symbol for _ in range(self.vertices_number) ]
        names_count = 0
        while names_count < self.vertices_number:
            name = chr(symbol_code)
            symbol_code += 1
            if name in ignored_names:
                continue
            vertices_names[names_count] = name
            names_count += 1

        return vertices_names

    def __prepare_vertices_layers(self):
        self.layers = [ [ self.start_vertex_name ] ]
        vertices_count = 1
        while vertices_count < self.vertices_number - 1:
            remain_vertices = self.vertices_number - vertices_count - 1
            if remain_vertices == 1:
                self.layers[-1].append(self.vertices_names[vertices_count])
                vertices_count += 1
            else:
                new_layer_size = self.rnd.in_range(MinLayerSize, min(MaxLayerSize, remain_vertices))
                self.layers.append([ v for v in self.vertices_names[vertices_count:vertices_count + new_layer_size]])
                vertices_count += new_layer_size
        self.layers.append([ self.end_vertex_name ])

    def _create_graph(self) -> Graph:
        graph = Graph(self.__create_raw_graph())
        self.__set_edges_to_graph(graph)
        return graph

    def __create_raw_graph(self) -> dict:
        raw_graph = {}
        width = 0
        for layer in self.layers:
            layer_size = len(layer)
            if layer_size == 0:
                pass
            elif layer_size == 1:
                raw_graph[layer[0]] = GraphVertex(at=[ width, GraphSVGHeight / 2 ])
            elif layer_size == 2:
                raw_graph[layer[0]] = GraphVertex(at=[ width, GraphSVGHeight / 4 ])
                raw_graph[layer[1]] = GraphVertex(at=[ width, 3 * GraphSVGHeight / 4 ])
            else:
                delta = GraphSVGHeight // (layer_size - 1)
                height = 0
                for vertex in layer:
                    raw_graph[vertex] = GraphVertex(at=[ width, height ])
                    height += delta
            width += GraphSVGWidthDelta
        return raw_graph

    def __set_edges_to_graph(self, graph):
        if len(self.layers) == 1:
            return
        if len(self.layers) == 2:
            graph.edge1(self.start_vertex_name, self.end_vertex_name)
            return

        for vertex_name in self.layers[1]:
            graph.edge1(self.start_vertex_name, vertex_name)

        for i in range(1, len(self.layers) - 1):
            for j in self.rnd.shuffle(list(range(len(self.layers[i])))):
                current_vertex_name = self.layers[i][j]
                vertices_pull = self.layers[i + 1].copy()
                if ConcatenateFarVertices and i + 3 < len(self.layers):
                    vertices_pull += self.rnd.pick(self.layers[i + 2])
                if j > 0:
                    vertices_pull += self.layers[i][j - 1]
                if j + 1 < len(self.layers[i]):
                    vertices_pull += self.layers[i][j + 1]
                edges_number = min(self.rnd.in_range(1, 4), len(vertices_pull))
                for other_vertex_name in self.rnd.pick_n(edges_number, vertices_pull):
                    if not (other_vertex_name in graph.edges and current_vertex_name in graph.edges[other_vertex_name]):
                        graph.edge1(current_vertex_name, other_vertex_name)

        for vertex_name in self.layers[-2]:
            graph.edge1(vertex_name, self.end_vertex_name)

    def _generate_text(self) -> str:
        intro = self.__generate_intro()
        body = self.__generate_body()
        additional_statemant = self._generate_additional_statement()
        svg = self.__get_graph_svg()
        return intro + ' ' + body + additional_statemant  + '?' + svg

    def __generate_intro(self) -> str:
        return f'''
На рисунке {self.rnd.pick([ 'представлена', 'изображена', '—' ])}
схема дорог, связывающих {self.vertices_label.plural} {', '.join(self.vertices_names)}.
По каждой дороге можно двигаться только в одном направлении, указанном стрелкой.'''

    def __generate_body(self) -> str:
        return f'''
Сколько существует различных путей из {self.vertices_label.genitive} {self.start_vertex_name}
в {self.vertices_label.nominative} {self.end_vertex_name}'''

    def _generate_additional_statement(self) -> str:
        return ''

    def __get_graph_svg(self):
        return html.div_xy(self.graph.as_svg(oriented=True), (len(self.layers) - 1) * GraphSVGWidthDelta, GraphSVGHeight, margin='5px') 

    def _get_path_count(self):
        return self.graph.count_paths(self.start_vertex_name, self.end_vertex_name)

    def _get_and_reserve_random_free_vertex_name(self) -> str:
        vertex_name = self.rnd.pick(self._get_free_vertices_names())
        self.reserved_vertices_names.append(vertex_name)
        return vertex_name

    def _get_free_vertices_names(self) -> list:
        free_names = []
        if not self.vertices_names is None:
            free_names = self.rnd.pick(
                [ name for name in self.vertices_names if name not in self.reserved_vertices_names ]
            )
        return free_names

class PathCountingWithRequiredVertex(PathCounting):
    def _generate_graph(self) -> Graph:
        graph = super()._generate_graph()
        self._set_required_vertex()
        return graph

    def _set_required_vertex(self):
        self.required_vertex_name = self._get_and_reserve_random_free_vertex_name()

    def _generate_additional_statement(self) -> str:
        return self._generate_requried_statement()

    def _generate_requried_statement(self) -> str:
        return f", проходящих через {self.vertices_label.nominative} {self.required_vertex_name}"

class PathCountingWithIgnoredVertex(PathCounting):
    def _generate_graph(self) -> Graph:
        graph = super()._generate_graph()
        self._set_ignored_vertex()
        return graph
    
    def _set_ignored_vertex(self):
        self.ignored_vertex_name = self._get_and_reserve_random_free_vertex_name()

    def _generate_additional_statement(self) -> str:
        return self._generate_ignored_statement()

    def _generate_ignored_statement(self) -> str:
        return f" не проходящих через {self.vertices_label.nominative} {self.ignored_vertex_name}"

class PathCountingWithRequiredAndIgnoredVertex(PathCountingWithRequiredVertex, PathCountingWithIgnoredVertex):
    def _generate_graph(self) -> Graph:
        graph = PathCounting._generate_graph(self)
        self._set_required_vertex()
        self._set_ignored_vertex()
        return graph

    def _generate_additional_statement(self) -> str:
        statement = self._generate_requried_statement() + self.rnd.pick([ ', но', ' и', '' ])
        statement += self.rnd.pick([ ' при этом', '' ]) + self._generate_ignored_statement()
        return statement

# ToDo: Need better class name
class PathCountingWithMutuallyExclusiveAndRequiredVertices(PathCounting):
    def _generate_graph(self) -> Graph:
        graph = PathCounting._generate_graph(self)
        self.first_vertex_name = self._get_and_reserve_random_free_vertex_name()
        self.scond_vertex_name = self._get_and_reserve_random_free_vertex_name()
        return graph

    def _generate_additional_statement(self) -> str:
        return f'''
, проходящих через {self.vertices_label.nominative} {self.first_vertex_name} или через 
{self.vertices_label.nominative} {self.scond_vertex_name}, но не через оба этих {self.vertices_label.genitive}'''

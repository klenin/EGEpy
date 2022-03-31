from dataclasses import dataclass

from EGE.GenBase import DirectInput
from ...Graph import Graph, GraphVertex

@dataclass
class ObjectLabel:
    nominative: str
    genitive: str
    plural: str

class PathCounting(DirectInput):
    def generate(self):
        self.vertices_label = self.rnd.pick([
            ObjectLabel('город', 'города', 'города'),
            ObjectLabel('пункт', 'пукнта', 'пункты'),
        ])

        self.graph = self._generate_graph()
        self.text = self._generate_text()
        return self

    def _generate_text(self) -> str:
        return self._generate_intro() + ' ' + self._generate_body() + '?'

    def _generate_graph(self) -> Graph:
        self.vertices_count = self.rnd.in_range(10, 18)
        self.vertices_names = self.__generate_vertices_names()

        self.start_vertex_name = self.rnd.pick(self.vertices_names)
        self.end_vertex_name = self.rnd.pick(self.vertices_names, self.start_vertex_name)
        
        self.reserved_vertices_names = [ self.start_vertex_name, self.end_vertex_name ]

    def _generate_body(self) -> str:
        body = f"Сколько существует различных путей из {self.vertices_label.genitive} {self.start_vertex_name} "
        body += f"в {self.vertices_label.nominative} {self.end_vertex_name}"
        return body

    def _generate_intro(self) -> str:
        intro = f"На рисунке {self.rnd.pick([ 'представлена', 'изображена', '—' ])}"
        intro += f" схема дорог, связывающих {self.vertices_label.plural} {', '.join(self.vertices_names)}. "
        intro += 'По каждой дороге можно двигаться только в одном направлении, указанном стрелкой.'
        return intro

    def _get_free_vertices_names(self) -> list:
        free_names = []
        if not self.vertices_names is None:
            free_names = self.rnd.pick(
                [ name for name in self.vertices_names if name not in self.reserved_vertices_names ]
            )
        return free_names

    def __generate_vertices_names(self) -> list:
        ignored_names = [ 'Ё', 'Й' ]

        cyrillic = self.rnd.coin() == 1
        # First symbol is cyrillic 'А', other is latin 'A'
        start_symbol = 'А' if cyrillic else 'A'
        start_symbol_code = ord(start_symbol)

        names = [ start_symbol for _ in range(self.vertices_count) ]
        code = start_symbol_code
        count = 0
        while count < self.vertices_count:
            name = chr(code)
            code += 1
            if name in ignored_names:
                continue
            names[count] = name
            count += 1
            
        return names

class PathCountingWithRequiredVertex(PathCounting):
    def _generate_text(self) -> str:
        return self._generate_intro() + ' ' + self._generate_body() + self._generate_requried_statement() + '?'

    def _generate_graph(self) -> Graph:
        graph = super()._generate_graph()
        self._set_required_vertex()
        return graph

    def _set_required_vertex(self):
        self.required_vertex_name = self._get_free_vertices_names()
        self.reserved_vertices_names.append(self.required_vertex_name)

    def _generate_requried_statement(self) -> str:
        return f", проходящих через {self.vertices_label.nominative} {self.required_vertex_name}"

class PathCountingWithIgnoredVertex(PathCounting):
    def _generate_text(self) -> str:
        return self._generate_intro() + ' ' + self._generate_body() + self._generate_ignored_statement() + '?'

    def _generate_graph(self) -> Graph:
        graph = super()._generate_graph()
        self._set_ignored_vertex()
        return graph
    
    def _set_ignored_vertex(self):
        self.ignored_vertex_name = self._get_free_vertices_names()
        self.reserved_vertices_names.append(self.ignored_vertex_name)

    def _generate_ignored_statement(self) -> str:
        return f" не проходящих через {self.vertices_label.nominative} {self.ignored_vertex_name}"

class PathCountingWithRequiredAndIgnoredVertex(PathCountingWithRequiredVertex, PathCountingWithIgnoredVertex):
    def _generate_text(self) -> str:
        text = self._generate_intro() + ' ' + self._generate_body() + self._generate_requried_statement()
        text += self.rnd.pick([ ', но', ' и', ' и при этом' ]) + self._generate_ignored_statement() + '?'
        return text

    def _generate_graph(self) -> Graph:
        graph = PathCounting._generate_graph(self)
        self._set_required_vertex()
        self._set_ignored_vertex()
        return graph

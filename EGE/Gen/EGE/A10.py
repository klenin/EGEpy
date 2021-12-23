from ... import Html as html
from ...Graph import Graph
from ...GenBase import SingleChoice

class GraphByMatrix(SingleChoice):
    def generate(self):
        vertices = {
            'A': { 'at': [  50,  0 ] },
            'B': { 'at': [  25, 50 ] },
            'C': { 'at': [  75, 50 ] },
            'D': { 'at': [   0,  0 ] },
            'E': { 'at': [ 100,  0 ] },
        }
        edges = [
            ['A', 'B'],
            ['A', 'C'],
            ['A', 'D'],
            ['A', 'E'],
            ['B', 'C'],
            ['B', 'D'],
            ['C', 'E'],
        ]

        def make_random_graph():
            while (True):
                g = Graph(vertices)
                for v1, v2 in self.rnd.pick_n(5, edges):
                    g.edge2(v1, v2, self.rnd.in_range(2, 5))
                if g.is_connected():
                    return g

        g = make_random_graph()
        bad = []
        seen = { g.edges_string(): 1 }
        while len(bad) < 3:
            g1 = make_random_graph()
            while g1.edges_string() in seen:
                g1 = make_random_graph()
            seen[g1.edges_string()] = 1
            bad.append(g1)

        self.text = f'''В таблице приведена стоимость перевозки между соседними железнодорожными станциями.
            Укажите схему, соответствующую таблице: {g.html_matrix()}'''

        self.set_variants([ html.div_xy(x.as_svg(), 120, 80, margin='5px') for x in [ g ] + bad ])
        return self

class LightPanel(SingleChoice):
    def generate(self):
        first = self.rnd.in_range(5, 10)
        last = self.rnd.in_range(4, 9)
        n = first + last
        self.text = f'''На световой панели в ряд расположены {n} лампочек.
                    Каждая из первых {first} лампочек может гореть красным, жёлтым или зелёным цветом.
                    Каждая из остальных {last} лампочек может гореть одним из двух цветов — красным или белым.
                    Сколько различных сигналов можно передать с помощью панели
                    все лампочки должны гореть, порядок цветов имеет значение)?'''
        self.set_variants([
            3**first * 2**last,
            3**first + 2**last,
            first**3 * last**2,
            first**3 + last**2
        ])
        return self


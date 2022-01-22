import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from Graph import Graph, GraphVertex
else:
    from ..Graph import Graph, GraphVertex


class Test_Graph(unittest.TestCase):
    def test1_simple(self):
        g = Graph({ '1': GraphVertex(), '2': GraphVertex(), '3': GraphVertex() })
        self.assertListEqual(sorted(g.vertex_names()), [ '1', '2', '3' ], 'vertex names')
        with self.assertRaises(ValueError):
            g.edge1('3', '4')
            g.edge2('3', '4')

        g.edge1('1', '2')
        g.edge1('2', '1')
        g.edge1('2', '3')
        eq = self.assertEqual
        eq(g.is_oriented(), True, 'oriented')
        eq(g.edges_string(), '{1->{2},2->{1,3},3->{}}', 'edges_string')

        g.edge1('3', '2', 7)
        eq(g.is_oriented(), False, 'not oriented')
        eq(g.edges_string(), '{1->{2},2->{1,3},3->{2:7}}', 'edges_string weight')

    def test2_bounding_box(self):
        g = Graph({ 'A': GraphVertex(at=[ 10, 40 ]), 'B': GraphVertex(at=[ 20, 30 ]) })
        self.assertListEqual(g.bounding_box(), [ 10, 30, 20, 40 ], 'bounding_box')

    def test3_static_method(self):
        self.assertListEqual(Graph.add([ 1, 2, 3 ], [ 4, 5, 6 ]), [ 5, 7, 9 ], 'add')
        self.assertListEqual(Graph.size([ 1, 2, 3, 5 ]), [ 1, 2, 2, 3 ], 'size')

    def test4_connected(self):
        g = Graph({ '1': GraphVertex(), '2': GraphVertex(), '3': GraphVertex() })
        g.edge2('1', '2')
        self.assertEqual(g.is_connected(), False, 'not connected')
        g.edge2('3', '2')
        self.assertEqual(g.is_connected(), True, 'connected')

    def test5_count_paths(self):
        g = Graph({ '1': GraphVertex(), '2': GraphVertex(), '3': GraphVertex(), '4': GraphVertex() })
        g.edge1('1', '2')
        g.edge1('2', '3')
        g.edge1('3', '4')
        cache = {}
        self.assertEqual(g.count_paths('1', '4', cache), 1, 'count_paths 1')
        g.edge1('2', '4')
        self.assertEqual(g.count_paths('1', '4', cache), 1, 'count_paths cache')
        self.assertEqual(g.count_paths('1', '4'), 2, 'count_paths 2')

        g = Graph({ str(i): GraphVertex() for i in range(31) })
        for i in range(10):
            v = 3 * i
            g.edge1(str(v), str(v + 1))
            g.edge1(str(v), str(v + 2))
            g.edge1(str(v + 1), str(v + 3))
            g.edge1(str(v + 2), str(v + 3))
        self.assertEqual(g.count_paths('0', '30'), 1024, 'count_paths 2^n')

    def test6_html(self):
        g = Graph({ 'A': GraphVertex(), 'B': GraphVertex() })
        g.edge1('B', 'A', 7)
        old_str = g.edges_string()
        ans = '\n'.join(['<table border="1"><tr><td></td><td>A</td><td>B</td></tr>',
                         '<tr><td>A</td><td> </td><td> </td></tr>',
                         '<tr><td>B</td><td>7</td><td> </td></tr>',
                         '</table>'])
        self.assertEqual(g.html_matrix(), ans, 'html_matrix')
        self.assertEqual(g.edges_string(), old_str, 'html_matrix preserves graph')


if __name__ == '__main__':
    unittest.main(verbosity=1)


import unittest

from EGE.GenBase import EGEError
from EGE.Random import Random
from EGE.Prog import make_expr

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from SQL.Table import Table
    # from SQL.Utils import Utils
    # from SQL.RandomTable import RandomTable
else:
    from ..SQL.Table import Table
    # from ..SQL.Utils import Utils
    # from ..SQL.RandomTable import RandomTable

rnd = Random(2342134)

def join_sp(*elements):
    res = ' '.join([str(el) for el in elements])
    return res

def pack_table(table: Table):
    res = '|'.join([ join_sp(*[ str(f) for f in table.fields ]), *[ join_sp(*d) for d in table.data ] ])
    return res

def pack_table_sorted(table: Table):
    return '|'.join([ join_sp(table.fields) ] + [ join_sp(d) for d in sorted(table.data) ])

class test_SQL(unittest.TestCase):
    def test_create_table(self):
        eq = self.assertEqual

        with self.assertRaisesRegex(EGEError, 'fields', msg='no fields'):
            t = Table(None) #test seems to be useless because python throw exception if positional argument is missed
        t = Table(['a', 'b', 'c'], name='table')
        eq(t.name, 'table', 'table name')

    def test_insert_row_copies(self):
        eq = self.assertEqual

        tab = Table(['f'], name='table')
        r = 1
        tab.insert_row(r)
        r = 2
        eq('f|1', pack_table(tab), 'insert_row copies')

    def test_insert_rows_copies(self):
        eq = self.assertEqual

        tab = Table(['f'], name='table')
        r = [ 1 ]
        tab.insert_rows(r, r)
        r[0] = 2
        eq('f|1|1', pack_table(tab), 'insert_row copies')

    def test_select_insert_hash(self):
        eq = self.assertEqual
        tab = Table('id name'.split())

        self.assertDictEqual(tab._row_hash([ 2, 3 ]), { 'id': 2, 'name': 3 }, 'row hash')
        tab.insert_rows([ 1, 'aaa' ], [ 2, 'bbb' ])
        eq('id name|1 aaa|2 bbb', pack_table(tab.select([ 'id', 'name' ])), 'all fields')
        tab.insert_row(3, 'ccc')
        eq('id|1|2|3', pack_table(tab.select('id')), 'field 1')

        self.assertListEqual([ 1, 2, 3 ], tab.column_array('id'), 'column_array')
        self.assertListEqual([ 1, 2, 3 ], tab.column_array(1), 'column_array by number')
        with self.assertRaisesRegex(EGEError, 'zzz', msg='column_array none'):
            tab.column_array('zzz')
        with self.assertRaisesRegex(EGEError, '77', msg='column_array by number none'):
            tab.column_array(77)

        self.assertDictEqual({ 'aaa': 1, 'bbb': 1, 'ccc': 1 }, tab.column_hash('name'), 'column_hash')
        self.assertDictEqual({ 'aaa': 1, 'bbb': 1, 'ccc': 1 }, tab.column_hash(2), 'column_hash by number')
        with self.assertRaisesRegex(EGEError, 'xxx', msg='column_hash none'):
            tab.column_hash('xxx')

        eq('name|aaa|bbb|ccc', pack_table(tab.select('name')), 'field 2')
        eq('id id|1 1|2 2|3 3', pack_table(tab.select([ 'id', 'id' ])), 'duplicate field')
        # TODO exception used to be raised from Prog::Var::run, but it removed from there. Need to restore it or choose new place to raise
        with self.assertRaisesRegex(EGEError, 'zzz', msg='bad field'):
            tab.select('zzz')

        r = tab.random_row(rnd)[0]
        self.assertTrue(r == 1 or r == 2 or r == 3, 'random_row')

    def test_select_where(self):
        eq = self.assertEqual

        tab = Table('id name city'.split())
        tab.insert_rows([ 1, 'aaa', 3 ], [ 2, 'bbb', 2 ], [ 3, 'ccc', 1 ], [ 4, 'bbn', 2 ])
        e = make_expr([ '==', 'city', 2 ])
        eq('id name city|2 bbb 2|4 bbn 2', pack_table(tab.where(e)), 'where city == 2')
        eq(2, tab.count_where(e), 'count_where city == 2')
        eq('id name|2 bbb|4 bbn', pack_table(tab.select(['id', 'name'], e)), 'select id, name where city == 2')
        eq('||', pack_table(tab.select([], e)), 'select where city == 2')
        eq(4, tab.count(), 'count')
        eq(0, tab.where(make_expr(0)).count(), 'where false')
        eq(0, tab.count_where(make_expr(0)), 'count_where false')


if __name__ == '__main__':
    unittest.main(verbosity=1)
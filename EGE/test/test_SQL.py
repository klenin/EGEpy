import unittest

from EGE.GenBase import EGEError
from EGE.Random import Random

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
    def test_CreateTable(self):
        eq = self.assertEqual

        with self.assertRaisesRegex(EGEError, 'fields', msg='no fields'):
            t = Table(None) #test seems to be useless because python throw exception if positional argument is missed
        t = Table(['a', 'b', 'c'], name='table')
        eq(t.name, 'table', 'table name')

    def test_SelectInsertHash(self):
        eq = self.assertEqual
        tab = Table('id name'.split())

        self.assertDictEqual(tab._row_hash([ 2, 3 ]), { 'id': 2, 'name': 3 }, 'row hash')
        tab.insert_rows([ 1, 'aaa' ], [ 2, 'bbb' ])
        eq(pack_table(tab.select([ 'id', 'name' ])), 'id name|1 aaa|2 bbb', 'all fields')
        tab.insert_row(3, 'ccc')
        eq(pack_table(tab.select('id')), 'id|1|2|3', 'field 1')

        self.assertListEqual(tab.column_array('id'), [ 1, 2, 3 ], 'column_array')
        self.assertListEqual(tab.column_array(1), [ 1, 2, 3 ], 'column_array by number')
        with self.assertRaisesRegex(EGEError, 'zzz', msg='column_array none'):
            tab.column_array('zzz')
        with self.assertRaisesRegex(EGEError, '77', msg='column_array by number none'):
            tab.column_array(77)

        self.assertDictEqual(tab.column_hash('name'), { 'aaa': 1, 'bbb': 1, 'ccc': 1 }, 'column_hash')
        self.assertDictEqual(tab.column_hash(2), { 'aaa': 1, 'bbb': 1, 'ccc': 1 }, 'column_hash by number')
        with self.assertRaisesRegex(EGEError, 'xxx', msg='column_hash none'):
            tab.column_hash('xxx')

        eq(pack_table(tab.select('name')), 'name|aaa|bbb|ccc', 'field 2')
        eq(pack_table(tab.select([ 'id', 'id' ])), 'id id|1 1|2 2|3 3', 'duplicate field')
        #TODO exception used to be raised from Prog::Var::run, but it removed from there. Need to restore it or choose new place to raise
        # with self.assertRaisesRegex(EGEError, 'zzz', msg='bad field'):
        #     tab.select('zzz')

        r = tab.random_row(rnd)[0]
        self.assertTrue(r == 1 or r == 2 or r == 3, 'random_row')


if __name__ == '__main__':
    unittest.main(verbosity=1)
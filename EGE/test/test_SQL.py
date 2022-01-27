import unittest

from EGE.GenBase import EGEError
from EGE.Random import Random
from EGE.Prog import make_expr
from EGE.Utils import nrange

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

#TODO reorganize tests to multiple test cases to simplify structure of complex test_methods
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

        with self.subTest(msg='test _row_hash'):
            self.assertDictEqual(tab._row_hash([ 2, 3 ]), { 'id': 2, 'name': 3 })

        tab.insert_rows([ 1, 'aaa' ], [ 2, 'bbb' ])
        with self.subTest(msg='select all fields'):
            eq('id name|1 aaa|2 bbb', pack_table(tab.select([ 'id', 'name' ])))

        tab.insert_row(3, 'ccc')
        with self.subTest(msg='test select field id'):
            eq('id|1|2|3', pack_table(tab.select('id')))

        with self.subTest(msg='test column_array (str arg)'):
            self.assertListEqual([ 1, 2, 3 ], tab.column_array('id'))

        with self.subTest(msg='test column_array (number arg)'):
            self.assertListEqual([ 1, 2, 3 ], tab.column_array(1))

        with self.subTest(msg='test column_array none (str arg)'):
            with self.assertRaisesRegex(EGEError, 'zzz', msg='column_array none'):
                tab.column_array('zzz')

        with self.subTest(msg='test column_array none (number arg)'):
            with self.assertRaisesRegex(EGEError, '77', msg='column_array by number none'):
                tab.column_array(77)

        with self.subTest(msg='test column_hash (str arg)'):
            self.assertDictEqual({ 'aaa': 1, 'bbb': 1, 'ccc': 1 }, tab.column_hash('name'))

        with self.subTest(msg='test column_hash (number arg)'):
            self.assertDictEqual({ 'aaa': 1, 'bbb': 1, 'ccc': 1 }, tab.column_hash(2))

        with self.subTest(msg='test column_hash none (str argument)'):
            with self.assertRaisesRegex(EGEError, 'xxx'):
                tab.column_hash('xxx')

        with self.subTest(msg='test column_hash none (number argument)'):
            with self.assertRaisesRegex(EGEError, '42'):
                tab.column_hash(42)

        with self.subTest(msg='test select field name'):
            eq('name|aaa|bbb|ccc', pack_table(tab.select('name')))

        with self.subTest(msg='test select two same fields'):
            eq('id id|1 1|2 2|3 3', pack_table(tab.select([ 'id', 'id' ])))

        with self.subTest(msg='test select non existing field'):
            with self.assertRaisesRegex(EGEError, 'zzz'):
                tab.select('zzz')

        r = tab.random_row(rnd)[0]
        with self.subTest(msg='test random row'):
            self.assertTrue(r == 1 or r == 2 or r == 3)

    def test_select_where(self):
        eq = self.assertEqual

        tab = Table('id name city'.split())
        tab.insert_rows([ 1, 'aaa', 3 ], [ 2, 'bbb', 2 ], [ 3, 'ccc', 1 ], [ 4, 'bbn', 2 ])
        e = make_expr([ '==', 'city', 2 ])

        with self.subTest(msg='test where city == 2'):
            eq('id name city|2 bbb 2|4 bbn 2', pack_table(tab.where(e)))

        with self.subTest(msg='test count_where city == 2'):
            eq(2, tab.count_where(e))

        with self.subTest(msg='select id, name where city == 2'):
            eq('id name|2 bbb|4 bbn', pack_table(tab.select(['id', 'name'], e)))

        with self.subTest(msg='test select where city == 2'):
            eq('||', pack_table(tab.select([], e)))

        with self.subTest(msg='test count rows'):
            eq(4, tab.count())

        with self.subTest(msg='test where false'):
            eq(0, tab.where(make_expr(0)).count())

        with self.subTest(msg='test count_where false'):
            eq(0, tab.count_where(make_expr(0)))

    def test_where_copy_ref(self):
        eq = self.assertEqual

        tab = Table([ 'id' ])
        tab.insert_rows(*[ [i] for i in range(1, 6) ])
        e = make_expr([ '==', 'id', '3' ])

        w2 = tab.where(e)
        w2.data[0][0] = 9
        with self.subTest(msg='test where copy'):
            eq('id|1|2|3|4|5', pack_table(tab))

        w1 = tab.where(e, True)
        w1.data[0][0] = 9
        with self.subTest(msg='test where ref'):
            eq('id|1|2|9|4|5', pack_table(tab))

    # def test_update_var(self):


if __name__ == '__main__':
    unittest.main(verbosity=1)
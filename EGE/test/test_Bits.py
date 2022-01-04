import unittest

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from Bits import *
else:
    from ..Bits import *

class Test_Bits(unittest.TestCase):
    def test_Bits(self):
        eq = self.assertEqual

        b = Bits()
        eq(b.get_size(), 0, 'empty')
        b.set_size(6)
        eq(b.get_size(), 6, 'size')
        eq(b.is_empty(), True, 'empty is_empty')
        eq(b.get_bin(), '000000', '0 bin')
        eq(b.get_oct(), '00', '0 oct')
        eq(b.get_hex(), '00', '0 hex')
        b.set_bin('1111111')
        eq(b.get_bin(), '111111', '1 bin size')
        eq(b.is_empty(), False, 'non-empty is_empty')

        b = Bits().set_size(4, 1)
        eq(b.get_bin(), '1111', 'set_size 1')

    def test_get_bin(self):
        eq = self.assertEqual

        b = Bits().set_bin([ 1, 0, 1, 0 ])
        eq(b.get_size(), 4, 'set_bin array size')
        eq(b.get_bin(), '1010', 'set_bin array bin init')
        b.set_bin([ 1, 1, 1, 0, 1 ])
        eq(b.get_bin(), '1101', 'set_bin array bin')

    def test_copy(self):
        eq = self.assertEqual

        b1 = Bits().set_bin('1010')
        b2 = Bits().copy(b1)
        eq(b2.get_bin(), '1010', 'copy')
        b1.set_bit(0, 1)
        eq(b2.get_bin(), '1010', 'copy by val')
        b2.copy(b1)

    def test_set_bin(self):
        eq = self.assertEqual

        b = Bits().set_bin('1011')
        eq(b.get_size(), 4, 'set_bin size')
        eq(b.get_bin(), '1011', 'set_bin bin')
        eq(b.get_oct(), '13', 'set_bin oct')
        eq(b.get_hex(), 'B', 'set_bin hex')
        eq(b.get_dec(), 11, 'set_bin dec')

    def test_set_oct(self):
        eq = self.assertEqual

        b = Bits().set_oct('76')
        eq(b.get_size(), 6, 'set_oct size')
        eq(b.get_bin(), '111110', 'set_oct bin')
        eq(b.get_oct(), '76', 'set_oct oct')
        eq(b.get_hex(), '3E', 'set_oct hex')
        eq(b.get_dec(), 62, 'set_oct dec')

    def test_set_hex(self):
        eq = self.assertEqual

        b = Bits().set_hex('AC')
        eq(b.get_size(), 8, 'set_hex size')
        eq(b.get_bin(), '10101100', 'set_hex bin')
        eq(b.get_oct(), '254', 'set_hex oct')
        eq(b.get_hex(), 'AC', 'set_hex hex')
        eq(b.get_dec(), 172, 'set_hex dec')

    def test_set_size(self):
        eq = self.assertEqual

        b = Bits().set_size(7).set_dec(100)
        eq(b.get_hex(), '64', 'set_dec hex')
        eq(b.get_dec(), 100, 'set_dec dec')

    def test_set_long_bin(self):
        eq = self.assertEqual

        b = Bits().set_size(40).set_dec(2**33 + 2**15)
        eq(b.get_bin(), '0000001000000000000000001000000000000000', 'set_dec 2^33')

    def test_inc(self):
        b = Bits().set_size(3).set_dec(3)
        ok = True
        i = 4
        while ok and i != 3:
            i = (i + 1) % 8
            b.inc()
            ok ^= b.get_dec() == i
        self.assertTrue(ok, 'inc')

    def test_get_bit(self):
        eq = self.assertEqual

        b = Bits().set_bin('0100')
        eq(b.get_bit(1), 0, 'get 1')
        eq(b.set_bit(1, 1).get_bit(1), 1, 'set/get 1')
        eq(b.get_bit(2), 1, 'get 2')
        eq(b.flip([2]).get_bit(2), 0, 'flip 1')
        eq(b.set_bin('1010').flip([0, 2]).get_bin(), '1111', 'flip 2')

    def test_reverse(self):
        eq = self.assertEqual

        b = Bits().set_bin('01010111')
        eq(b.reverse_().get_bin(), '11101010', 'reverse')

    def test_scan_left(self):
        eq = self.assertEqual

        b = Bits().set_bin('01110000')
        eq(b.scan_left(0), 4, 'scan_left 1')
        eq(b.scan_left(4), 7, 'scan_left 2')
        eq(b.scan_left(7), 8, 'scan_left 3')

    def test_logic_op(self):
        eq = self.assertEqual

        def _logic_op_test(arg1, op, arg2, idx_from=0, idx_to=None):
            b = Bits().set_bin(arg1)
            r1 = b.dup().logic_op(op, int(arg2, 2) if arg2 != '' else None, idx_from, idx_to).get_bin()
            r2 = b.logic_op(op, Bits().set_bin(arg2), idx_from, idx_to).get_bin()
            eq(r1, r2, 'logic_op_test')
            return r1

        eq(_logic_op_test('0101', 'and', '1100'), '0100', 'and 1')
        eq(_logic_op_test('0101', 'or', '1100'), '1101', 'or 1')
        eq(_logic_op_test('0101', 'xor', '1100'), '1001', 'xor 1')
        eq(_logic_op_test('0101', 'not', ''), '1010', 'not 1')

        eq(_logic_op_test('1111111', 'and', '010', 2, 5), '1101011', 'and 2')
        eq(_logic_op_test('0000000', 'or', '101', 1, 4), '0101000', 'or 2')
        eq(_logic_op_test('0', 'xor', '1', 0, 1), '1', 'xor 2')
        eq(_logic_op_test('0101', 'not', '', 1, 3), '0011', 'not 2')

    def xor_bits(self):
        eq = self.assertEqual

        eq(Bits().set_bin('00').xor_bits(), 0, 'xor_bits 1')
        eq(Bits().set_bin('1').xor_bits(), 1, 'xor_bits 2')
        eq(Bits().set_bin('010101').xor_bits(), 1, 'xor_bits 3')
        eq(Bits().set_bin('111001').xor_bits(), 0, 'xor_bits 4')

    def test_indexes(self):
        b = Bits().set_bin('101010')

        self.assertListEqual(b.indexes(), [ 1, 3, 5 ], 'indexes')

    def test_count_ones(self):
        eq = self.assertEqual

        eq(Bits().set_bin('00000').count_ones(), 0, 'count_one (all zero)')
        eq(Bits().set_bin('11111').count_ones(), 5, 'count_one (all one)')
        eq(Bits().set_bin('101010').count_ones(), 3, 'count_one (3)')

    def test_inc_autosize(self):
        eq = self.assertEqual

        b = Bits()
        b.set_size(5)
        b.set_dec(30)
        b.inc_autosize()
        eq(b.get_dec(), 31, 'inc_autosize 30')
        b.inc_autosize()
        eq(b.get_dec(), 32, 'inc_autosize 31')

    def test_scan(self):
        eq = self.assertEqual

        def chk(hex, f, r, n):
            b = Bits().set_hex(hex)
            eq(b.scan_forward(), f, "scan_forward $n")
            eq(b.scan_reverse(), r, "scan_reverse $n")

        chk('0', -1, -1, -1)
        chk('1', 0, 0, 1)
        chk('469E', 1, 14, 2)
        chk('6D64690', 4, 26, 3)
        chk('86D64691', 0, 31, 4)

    def test_get_bits(self):
        b = Bits().set_bin('10110')
        self.assertListEqual(b.get_bits(), [ 1, 0, 1, 1, 0 ], 'get_bits')

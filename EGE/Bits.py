class Bits:
    b: list = []

    def get_size(self):
        return len(self.b)

    def set_size(self, new_size: int, val: int = 0):
        self.b = [ val for _ in range(new_size) ]
        return self

    def set_bin(self, new_bin, by_ref: bool = False):
        if isinstance(new_bin, list):
            self.set_bin_array(new_bin, by_ref)
        else:
            if self.get_size() == 0:
                self.b = [ int(i) for i in new_bin ]
            else:
                for i in range(min(self.get_size(), len(new_bin))):
                    self.b[-i - 1] = int(new_bin[-i -1])
        return self

    def set_bin_array(self, new_bin: list, by_ref: bool = False):
        i = len(self.b)
        if i != 0:
            j = len(new_bin)
            while i > 0 and j > 0:
                i -= 1
                j -= 1
                self.b[i] = new_bin[j]
        else:
            self.b = new_bin if by_ref else new_bin[:]
        return self

    def copy(self, other):
        self.set_bin_array(other.b)
        return self

    def dup(self):
        return Bits().copy(self)

    def get_bin(self):
        return ''.join(map(str, self.b))

    def get_oct(self):
        return oct(self.get_dec())[2:].zfill((self.get_size() + 2) // 3)

    def set_oct(self, new_oct):
        self.set_bin(bin(int(new_oct, 8))[2:])
        return self

    def get_hex(self):
        return hex(self.get_dec())[2:].upper().zfill((self.get_size() + 3) // 4)

    def set_hex(self, new_hex):
        self.set_bin(bin(int(new_hex, 16))[2:])
        return self

    def get_dec(self):
        return int(''.join(str(i) for i in self.b), 2)

    def set_dec(self, new_dec):
        self.set_bin(bin(int(new_dec))[2:])
        return self

    def inc_autosize(self):
        for i in range(len(self.b) - 1, -1, -1):
            self.b[i] ^= 1
            if self.b[i] == 1:
                return self
        self.b.insert(0, 1)
        return self

    def inc(self):
        for i in range(len(self.b) - 1, -1, -1):
            self.b[i] ^= 1
            if self.b[i] == 1:
                break
        return self

    def get_bit(self, index: int):
        return self.b[-index - 1]

    def set_bit(self, index: int, bit: int):
        self.b[-index - 1] = bit
        return self

    def flip(self, indexes: list):
        for i in indexes:
            self.b[-i - 1] ^= 1
        return self

    def is_empty(self):
        return 1 not in self.b

    def reverse_(self):
        self.b.reverse()
        return self

    def shift_(self, d: int, idx_from, idx_to, fill_value: int = 0):
        if idx_from is None:
            idx_from = 0
        if idx_to is None:
            idx_to = len(self.b)
        if d > 0:  # вправо
            j = idx_to
            i = idx_to - d
            while j > idx_from:
                i -= 1
                j -= 1
                self.b[j] = self.b[i] if i + 1 > idx_from else fill_value
        elif d < 0:  # влево
            j = idx_from
            i = idx_from - d
            while j < idx_to:
                i += 1
                j += 1
                self.b[j] = self.b[i] if i - 1 < idx_to else fill_value
        return self

    def scan_left(self, pos: int):
        bit = self.get_bit(pos)
        while pos < self.get_size() and self.get_bit(pos) == bit:
            pos += 1
        return pos

    def logic_op(self, opname: str, val, idx_from=0, idx_to=None):
        if idx_to is None:
            idx_to = self.get_size()
        l = idx_to - idx_from
        if val is None or val == '':
            right = []
        elif isinstance(val, Bits):
            right = val.b
        else:
            right = Bits().set_size(l).set_dec(val).b

        ops = {
            'and': lambda x1, x2: x1 & x2,
            'or': lambda x1, x2: x1 | x2,
            'xor': lambda x1, x2: x1 ^ x2,
            'not': lambda x1, x2: x1 ^ 1,
        }
        if opname in ops:
            op = ops[opname]
        else:
            raise EOFError(f'Unknown op {opname}')

        for i in range(l):
            self.b[idx_from + i] = op(self.b[idx_from + i], right[i] if len(right) == l else None)
        return self

    def xor_bits(self):
        r = 0
        for i in self.b:
            r ^= i
        return r

    def indexes(self):
        return [i for i in range(self.get_size()) if self.get_bit(i) == 1]

    def count_ones(self):
        return self.b.count(1)

    def get_bits(self):
        return self.b

    def _scan(self, start, end):
        step = -1 if start > end else 1
        for pos in range(start, end, step):
            if self.b[-pos - 1] == 1:
                return pos
        return -1

    def scan(self, reverse: bool = False):
        return self._scan(self.get_size() - 1, -1) if reverse else self._scan(0, self.get_size())

    def scan_forward(self):
        return self.scan()

    def scan_reverse(self):
        return self.scan(True)

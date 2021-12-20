class Bits:
    b = []

    def set_size(self, new_size, val=0):
        self.b = [val for _ in range(new_size)]
        return self

    def set_bin(self, new_bin):
        if new_bin is list:
            self.set_bin_array(new_bin)
        else:
            self.b = [int(i) for i in new_bin]
        return self

    def set_bin_array(self, new_bin):
        i = len(self.b)
        if i != 0:
            j = len(new_bin)
            while i > 0 and j > 0:
                i -= 1
                j -= 1
                self.b[i] = new_bin[j]
        else:
            self.b = new_bin
        return self

    def flip(self, indexes):
        for i in indexes:
            self.b[-i - 1] ^= 1
        return self

    def get_dec(self):
        return int(''.join(str(i) for i in self.b), 2)

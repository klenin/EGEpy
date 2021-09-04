
# Permuted congruential generator, http://www.pcg-random.org/
class Random:
    mask_32 = 0xffffffff
    mask_64 = (mask_32 << 32) + mask_32

    def __init__(self, seed: int, seq: int = None):
        self.seed(seed, seq)

    def seed(self, seed: int, seq: int = None):
        self.state = 0
        self.inc = (seq or 1) * 2 + 1
        self.get(1)
        self.state = (self.state + seed) & Random.mask_64
        self.get(1)

    def get(self, max_: int) -> int:
        oldstate = self.state
        self.state = (oldstate * 6364136223846793005 + self.inc) & Random.mask_64
        xorshifted = (((oldstate >> 18) ^ oldstate) >> 27) & Random.mask_32
        rotate = oldstate >> 59
        return ((xorshifted >> rotate) | (xorshifted << (32 - rotate)) & Random.mask_32) % max_

    def coin(self) -> int:
        return self.get(2)

    def in_range(self, lo: int, hi: int) -> int:
        if hi < lo:
            raise ValueError('hi < lo')
        return self.get(hi - lo + 1) + lo

    def in_range_except(self, lo: int, hi: int, exclude) -> int:
        if isinstance(exclude, list):
            exclude = frozenset(exclude)
            r = self.in_range(lo, hi - len(exclude))
            for e in exclude:
                if e > r:
                    break
                r += 1
            return r
        else:
            r = self.in_range(lo, hi - 1)
            return r if r < exclude else r + 1

    def pick(self, array):
        if len(array) == 0:
            raise ValueError('pick from empty array');
        return array[self.get(len(array))]

    # Не проверяя, предполагает, что exclude элементом array.
    def pick_except(self, exclude, array):
        if len(array) <= 1:
            raise ValueError('except nothing')
        a = array[self.get(len(array) - 1)]
        return array[-1] if a == exclude else a

    def pick_n(self, n: int, array):
        if n > len(array):
            raise ValueError(f"pick_n: {n} of {len(array)}")
        a = array[:]
        for i in range(n):
            pos = self.in_range(i, len(array) - 1)
            a[i], a[pos] = a[pos], a[i]
        return a[:n]

    def shuffle(self, array):
        return self.pick_n(len(array), array)


if __name__ == '__main__':
    import unittest
    unittest.main()

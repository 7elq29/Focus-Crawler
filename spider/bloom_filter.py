import math, time


class BloomFilter:


    def __init__(self, set_size, bits_per_element):
        self.filter_size = set_size * bits_per_element
        self.k = int(math.log(2 * self.filter_size / set_size))
        self.value = bytearray(chr(0) * (int(self.filter_size/8)+1), 'ascii')
        self.data_size = 0
        self.exec_time = 0
        self.test = 0

    def set(self, text: str):
        start = time.time()
        hashes = [self._hash(text, x) for x in range(self.k+1)]
        if self._contains(hashes):
            return False
        self.data_size += 1
        for h in hashes:
            self._add(h)
        self.exec_time += (time.time() - start)
        return True

    def contains(self, text: str):
        for i in range(self.k+1):
            if not self._has(self._hash(text, i)):
                return False
        return True

    def _contains(self, hashes):
        for h in hashes:
            if not self._has(h):
                return False
        return True

    def avg_exec_time(self):
        return self.exec_time / self.data_size

    def _hash(self, text: str, k):
        h1 = 2166136261
        h2 = 2166136261
        prime = 16777619
        for c in text:
            h1 ^= (ord(c) * k + (prime ^ ord(c)) % 255)
            h1 = (h1 * prime) % (1 << 32)
            h2 ^= ord(c)
        return abs((h1 ^ h2) % self.filter_size)

    def _add(self, number):
        self._set_bit(number)

    def _has(self, number):
        return True if self._get_bit(number) else False

    def _get_bit(self, index):
        return self.value[int(index / 8)] & (1 << (index % 8))

    def _set_bit(self, index):
        self.value[int(index / 8)] |= (1 << (index % 8))


if __name__ == '__main__':
    bf = BloomFilter(1000, 10)
    t = "bcbbabedcbbgcbc"
    bf.set(t)
    print(bf.avg_exec_time())





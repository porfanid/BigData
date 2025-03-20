import random

from section_3.ex_1.a.hash_function import HashFunction


class BloomFilter:
    def __init__(self, N_bits, k_hashes, p=1048583):
        self.N = N_bits
        self.k = k_hashes
        self.p = p
        self.bits = [0] * self.N
        self.hash_functions = [HashFunction(
            alpha=random.randint(1, p - 1),
            beta=random.randint(0, p - 1),
            p=p,
            N=self.N
        ) for _ in range(self.k)]

    def add(self, item):
        for h in self.hash_functions:
            index = h.hash(item)
            self.bits[index] = 1

    def check(self, item):
        return all(self.bits[h.hash(item)] for h in self.hash_functions)

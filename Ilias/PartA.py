#Onoma: ILIAS DIMOPOULOS AM: 4869
#Onoma: ANTREAS KARAPEDIS AM: 4693

import random
import numpy as np
from collections import Counter, defaultdict
import re



import random
import numpy as np
from collections import Counter, defaultdict
import re

# ------------------------- ask1 -------------------------
# ask1: Heavy Hitters
# Briskoume ta heavy hitters se mia roh me 1M stoixeia
# Xrisimopoioyme ton vasiko kai ton epektasmeno (2os metritis) algorithmo

def create_stream():
    A = list(range(1, 10_000_001))
    for i in range(9482):
        j = random.randint(i, len(A) - 1)
        A[i], A[j] = A[j], A[i]

    B = []
    for i in range(9480):
        B.extend([A[i]] * 100)
    B.extend([A[9481]] * 2000)
    B.extend([A[9482]] * 50000)
    random.shuffle(B)
    return B, A[9481], A[9482]

def deterministic_heavy_hitters(stream, k):
    # Klassikos nueteterministikos algorithmos gia f-heavy hitters
    L = {}
    for item in stream:
        if item in L:
            L[item] += 1
        elif len(L) < k:
            L[item] = 1
        else:
            to_remove = []
            for key in L:
                L[key] -= 1
                if L[key] == 0:
                    to_remove.append(key)
            for key in to_remove:
                del L[key]
    return L

def extended_heavy_hitters(stream, k):
    # Epektasi me deutero metriti gia katagrafi pliroforias
    L = {}
    for item in stream:
        if item in L:
            L[item] = (L[item][0] + 1, L[item][1] + 1)
        elif len(L) < k:
            L[item] = (1, 1)
        else:
            to_remove = []
            for key in L:
                L[key] = (L[key][0] - 1, L[key][1])
                if L[key][0] == 0:
                    to_remove.append(key)
            for key in to_remove:
                del L[key]
    return L



# ------------------------- ask2 -------------------------
# ask2: CountMinSketch
#  CountMin Sketch me duoadikous arithmous kai Vec277
# Ektymisi syxnothtas kai epilogi Top-3
def bitstring_to_base277_vector(bitstring, length=13):
    num = int(bitstring[::-1], 2)
    base277_vector = []
    for _ in range(length):
        base277_vector.append(num % 277)
        num //= 277
    return base277_vector

def estimate_frequency_from_sketch(x, hash_functions, sketch):
    # Ektymisi syxnothtas gia ena x me olous tous CountMin
    bitstring = bin(x)[2:][::-1].ljust(100, '0')
    estimates = []
    for cm_index in range(100):
        prefix = bitstring[:cm_index + 1]
        base277_vector = bitstring_to_base277_vector(prefix)
        current_min = float('inf')
        for row in range(15):
            h_idx = cm_index * 15 + row
            h_f = hash_functions[h_idx]
            h_val = sum(a * b for a, b in zip(h_f, base277_vector)) % 277
            current_min = min(current_min, sketch[h_idx][h_val])
        estimates.append(current_min)
    return min(estimates)

def find_top_3_from_sketch(hash_functions, sketch):
# Vriskoume ta 3 stoixeia me megalyteri ektimisi   
    frequencies = {}
    for x in range(2100):
        frequencies[x] = estimate_frequency_from_sketch(x, hash_functions, sketch)
    top_3 = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:3]
    return top_3

# ------------------------- ask3 -------------------------
# ask3: CountMinFInfinity
class CountMinFInfinity:
    # CountMinFInfinity gia f-infinity
    # Xrisimopoioume 2 hash functions
    # kai 2 hash tables
    # to 1 gia f-infinity kai to 2o gia f-0
    def __init__(self, epsilon, delta):
        self.epsilon = epsilon
        self.delta = delta
        self.w = int(np.ceil(np.e / epsilon))
        self.d = int(np.ceil(np.log(1 / delta)))
        self.p = 10**9 + 7
        self.table = np.zeros((self.d, self.w), dtype=int)
        self.hash_params = [(random.randint(1, self.p - 1), random.randint(0, self.p - 1)) for _ in range(self.d)]
        self.items_observed = set()

    def _hash(self, x, i):
        # Hash function gia CountMinFInfinity
        a, b = self.hash_params[i]
        return ((a * x + b) % self.p) % self.w

    def update(self, x, delta):
        # Ektimisi f-infinity
        self.items_observed.add(x)
        for i in range(self.d):
            idx = self._hash(x, i)
            self.table[i, idx] += delta

    def estimate(self, x):
        # Ektimisi f-0
        return min(self.table[i, self._hash(x, i)] for i in range(self.d))

    def estimate_f_infty(self):
        
        # Ektimisi f-infinity gia ola ta stoixeia pou exoume parakolouthei
        return max(self.estimate(x) for x in self.items_observed)

# -------------------------ask4 -------------------------
# ask4: CountMinSketch for words
def extract_words(text):
    # Ektimisi lekseon apo keimeno
    raw_tokens = text.split()
    words = []
    for token in raw_tokens:
        token = token.lower()
        token = re.sub(r'[^a-z]', '', token)
        if 0 < len(token) <= 15:
            words.append(token)
    return words

class CountMinSketch:
    # CountMinSketch gia lekseis
    def __init__(self, epsilon, delta):
        self.epsilon = epsilon
        self.delta = delta
        self.w = int(np.ceil(np.e / epsilon))
        self.d = int(np.ceil(np.log(1 / delta)))
        self.p = 2**61 - 1
        self.table = np.zeros((self.d, self.w), dtype=int)
        self.hash_functions = [(random.randint(1, self.p - 1), random.randint(0, self.p - 1)) for _ in range(self.d)]

    def _hash(self, word, i):
        # Hash function gia CountMinSketch
        value = 0
        for c in word:
            value = value * 26 + (ord(c) - ord('a'))
        a, b = self.hash_functions[i]
        return ((a * value + b) % self.p) % self.w

    def update(self, word):
        # Ektimisi syxnothtas lekseos
        for i in range(self.d):
            idx = self._hash(word, i)
            self.table[i, idx] += 1

    def estimate(self, word):
        # Ektimisi syxnothtas lekseos
        return min(self.table[i, self._hash(word, i)] for i in range(self.d))

def track_top_k(stream, cms, k):
    # Dinamiki lista top-k me sygkrisi ektimiseon
    top_k_list = []
    for word in stream:
        cms.update(word)
        if word in top_k_list:
            continue
        if len(top_k_list) < k:
            top_k_list.append(word)
        else:
            current_est = cms.estimate(word)
            estimates = [(w, cms.estimate(w)) for w in top_k_list]
            min_word, min_val = min(estimates, key=lambda x: x[1])
            if current_est > min_val:
                top_k_list.remove(min_word)
                top_k_list.append(word)
    top_k_list.sort(key=lambda w: cms.estimate(w), reverse=True)
    return [(w, cms.estimate(w)) for w in top_k_list]
# ------------------------- main -------------------------
# main function to run the code
if __name__ == "__main__":
    print("----- ask1 -----")
    stream, hitter1, hitter2 = create_stream()
    k = 999
    res_basic = deterministic_heavy_hitters(stream, k)
    res_extended = extended_heavy_hitters(stream, k)
    print(f"vrethikan {len(res_basic)} stoixeia me vasiko algorithmo")
    print(f"vrethikan {len(res_extended)} stoixeia me 2o metriti")
    
    print(f"to stoixeio {hitter1} {'vrethike' if hitter1 in res_basic else 'den brethike'} basic")
    print(f"to stoixeio {hitter2} {'vrethike' if hitter2 in res_extended else 'den brethike'} (me 2o metriti)")

    print("\n----- ask 2 -----")
    try:
        with open("CountMinSketch/hash_functions.txt") as f:
            hash_functions = [list(map(int, line.split())) for line in f.readlines()]
        with open("CountMinSketch/sketch.txt") as f:
            sketch = [list(map(int, line.split())) for line in f.readlines()]
        top_3 = find_top_3_from_sketch(hash_functions, sketch)
        print("top 3 sketch:")
        for x, est in top_3:
            print(f"{x}: ~{est}")
    except FileNotFoundError:
        print("arxeia hash_functions.txt h sketch.txt den vrethikan. no aks2.")

    print("\n----- ask 3 -----")
    stream_ops = [(1, +1), (1, +1), (2, +1), (1, -1), (3, +1), (3, +1), (3, +1)]
    cms_finf = CountMinFInfinity(epsilon=0.01, delta=0.01)
    for item, delta in stream_ops:
        cms_finf.update(item, delta)
    print(f"ektimisi F apoiro apo CountMin: {cms_finf.estimate_f_infty()}")

    print("\n----- ask 4 -----")
    try:
        with open("vilfredo.txt", "r", encoding="utf-8") as f:
            text = f.read()
        stream_words = extract_words(text)
        word_counts = Counter(stream_words)
        real_top10 = word_counts.most_common(10)
        print("top 10 lekseis (real):")
        for w, c in real_top10:
            print(f"{w}: {c}")

        cms = CountMinSketch(epsilon=0.001, delta=1e-5)
        top10_est = track_top_k(stream_words, cms, 10)
        print("\nTop-10 CountMin ektimiseis:")
        for w, est in top10_est:
            print(f"{w}: ~{est}")
    except FileNotFoundError:
        print("arxeio vilfredo.txt den brethike. no aks 4.")

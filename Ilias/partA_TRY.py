import random
import numpy as np
from collections import Counter, defaultdict
import re

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

class CountMinSketch:
    def __init__(self, epsilon, delta):
        self.epsilon = epsilon
        self.delta = delta
        self.w = int(np.ceil(np.e / epsilon))
        self.d = int(np.ceil(np.log(1 / delta)))
        
        self.p = 10_000_019
        
        self.table = np.zeros((self.d, self.w), dtype=int)
        
        self.hash_functions = []
        for _ in range(self.d):
            a = random.randint(1, self.p - 1)
            b = random.randint(0, self.p - 1)
            self.hash_functions.append((a, b))
        
        self.total_count = 0
        
    def _hash(self, item, row):
        a, b = self.hash_functions[row]
        return ((a * item + b) % self.p) % self.w
    
    def update(self, item):
        for i in range(self.d):
            col = self._hash(item, i)
            self.table[i, col] += 1
        self.total_count += 1
    
    def estimate(self, item):
        estimates = []
        for i in range(self.d):
            col = self._hash(item, i)
            estimates.append(self.table[i, col])
        return min(estimates)
    
    def get_heavy_hitters(self, phi):
        threshold = phi * self.total_count
        heavy_hitters = []
        
        print(f"anazhto {phi*100}%-hitters (katofli: {threshold})...")
        
        candidates_to_check = []
        for _ in range(1000):
            candidates_to_check.append(random.randint(1, 10_000_000))
        
        for item in candidates_to_check:
            estimated_freq = self.estimate(item)
            if estimated_freq >= threshold:
                heavy_hitters.append((item, estimated_freq))
        
        heavy_hitters.sort(key=lambda x: x[1], reverse=True)
        return heavy_hitters

def find_heavy_hitters_with_countmin():
    print("=== euresi Heavy Hitters me CountMin ===")
    
    print("dimioyrgo roi dedomenon...")
    stream, hitter1, hitter2 = create_stream()
    stream_size = len(stream)
    print(f"megethos  rois: {stream_size}")
    print(f"pragmatikoi 0.1%-hitters: {hitter1} (2000 fores), {hitter2} (50000 fores)")
    
    phi = 0.001
    
    epsilon = 0.0001
    delta = 0.01
    
    print(f"parametroi CountMin: e={epsilon}, d={delta}")
    
    cms = CountMinSketch(epsilon, delta)
    print(f"diastaseis  pinaka: {cms.d} x {cms.w}")
    
    print("trofodoto to CountMin me ti roi...")
    for item in stream:
        cms.update(item)
    
    print(f"sunolika stoixeia epeksergasmena: {cms.total_count}")
    
    print("anazito heavy hitters...")
    
    candidates_to_check = [hitter1, hitter2]
    for _ in range(100):
        candidates_to_check.append(random.randint(1, 10_000_000))
    
    threshold = phi * cms.total_count
    found_hitters = []
    
    for item in candidates_to_check:
        estimated_freq = cms.estimate(item)
        if estimated_freq >= threshold:
            found_hitters.append((item, estimated_freq))
    
    found_hitters.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n apotelesmata CountMin gia 0.1%-hitters (katofli: {threshold}):")
    print("=" * 60)
    
    if found_hitters:
        for item, freq in found_hitters:
            actual_freq = stream.count(item)
            percentage = (freq / cms.total_count) * 100
            actual_percentage = (actual_freq / cms.total_count) * 100
            print(f"stoixeio {item:>8}: ektimomeni sucnotita={freq:>6} ({percentage:>5.2f}%), "
                  f"pragmatiki={actual_freq:>6} ({actual_percentage:>5.2f}%)")
    else:
        print("den vrethikan heavy hitters!")
    
    print(f"\neleghos akrivias :")
    print("=" * 40)
    
    for hitter in [hitter1, hitter2]:
        estimated = cms.estimate(hitter)
        actual = stream.count(hitter)
        error = abs(estimated - actual)
        error_percentage = (error / actual) * 100 if actual > 0 else 0
        
        print(f"stoixeio {hitter}:")
        print(f"  ektimomeni suxnotita: {estimated}")
        print(f"  pragmatiki suxnotita: {actual}")
        print(f"  sfalma: {error} ({error_percentage:.2f}%)")
        print(f"  sfalma <= e*||a||1: {error} <= {epsilon * cms.total_count:.2f} -> {error <= epsilon * cms.total_count}")
        print()

def compare_methods():
    print("=== sugkrisi methodon ===")
    
    stream, hitter1, hitter2 = create_stream()
    
    actual_counts = Counter(stream)
    actual_heavy_hitters = [(item, count) for item, count in actual_counts.items() 
                           if count >= 0.001 * len(stream)]
    actual_heavy_hitters.sort(key=lambda x: x[1], reverse=True)
    
    print("pragmatikoi 0.1%-hitters:")
    for item, count in actual_heavy_hitters:
        percentage = (count / len(stream)) * 100
        print(f"  {item}: {count} fores ({percentage:.3f}%)")
    
    cms = CountMinSketch(epsilon=0.0001, delta=0.01)
    for item in stream:
        cms.update(item)
    
    print(f"\nCountMin ektimiseis:")
    for item, actual_count in actual_heavy_hitters:
        estimated = cms.estimate(item)
        error = abs(estimated - actual_count)
        print(f"  {item}: ektimomeni={estimated}, pragmatiki={actual_count}, sfalma={error}")

def bitstring_to_base277_vector(bitstring, length=13):
    num = int(bitstring[::-1], 2)
    base277_vector = []
    for _ in range(length):
        base277_vector.append(num % 277)
        num //= 277
    return base277_vector

def estimate_frequency_from_sketch(x, hash_functions, sketch):
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
    frequencies = {}
    for x in range(2100):
        frequencies[x] = estimate_frequency_from_sketch(x, hash_functions, sketch)
    top_3 = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:3]
    return top_3

class CountMinFInfinity:
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
        a, b = self.hash_params[i]
        return ((a * x + b) % self.p) % self.w

    def update(self, x, delta):
        self.items_observed.add(x)
        for i in range(self.d):
            idx = self._hash(x, i)
            self.table[i, idx] += delta

    def estimate(self, x):
        return min(self.table[i, self._hash(x, i)] for i in range(self.d))

    def estimate_f_infty(self):
        return max(self.estimate(x) for x in self.items_observed)

def extract_words(text):
    raw_tokens = text.split()
    words = []
    for token in raw_tokens:
        token = token.lower()
        token = re.sub(r'[^a-z]', '', token)
        if 0 < len(token) <= 15:
            words.append(token)
    return words

class CountMinSketchWords:
    def __init__(self, epsilon, delta):
        self.epsilon = epsilon
        self.delta = delta
        self.w = int(np.ceil(np.e / epsilon))
        self.d = int(np.ceil(np.log(1 / delta)))
        self.p = 2**61 - 1
        self.table = np.zeros((self.d, self.w), dtype=int)
        self.hash_functions = [(random.randint(1, self.p - 1), random.randint(0, self.p - 1)) for _ in range(self.d)]

    def _hash(self, word, i):
        value = 0
        for c in word:
            value = value * 26 + (ord(c) - ord('a'))
        a, b = self.hash_functions[i]
        return ((a * value + b) % self.p) % self.w

    def update(self, word):
        for i in range(self.d):
            idx = self._hash(word, i)
            self.table[i, idx] += 1

    def estimate(self, word):
        return min(self.table[i, self._hash(word, i)] for i in range(self.d))

def track_top_k(stream, cms, k):
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

def run_all_exercises():
    print("="*80)
    print("enotita a: ypologismos HEAVY HITTERS se roes dedomenon")
    print("="*80)
    
    print("\n" + "-"*50)
    print("ASKISI   1: Heavy Hitters")
    print("-"*50)
    
    stream, hitter1, hitter2 = create_stream()
    k = 999
    
    res_basic = deterministic_heavy_hitters(stream, k)
    res_extended = extended_heavy_hitters(stream, k)
    
    print(f"vrethikan {len(res_basic)} stoixeia me vasiko algorithmo ")
    print(f"vrethikan {len(res_extended)} stoixeia me 2o metriti")
    print(f"to stoixeio {hitter1} {'vrethike' if hitter1 in res_basic else 'den vrethike'} (vasikos)")
    print(f"to stoixeio {hitter2} {'vrethike' if hitter2 in res_extended else 'den vrethike'} (me 2o metrhths)")
    
    print("\n" + "="*60)
    find_heavy_hitters_with_countmin()
    print("\n" + "="*60)
    compare_methods()
    
    print("\n" + "-"*50)
    print("askisi  2: anaktisi apo  CountMin Sketch")
    print("-"*50)
    
    try:
        with open("CountMinSketch/hash_functions.txt") as f:
            hash_functions = [list(map(int, line.split())) for line in f.readlines()]
        with open("CountMinSketch/sketch.txt") as f:
            sketch = [list(map(int, line.split())) for line in f.readlines()]
        
        top_3 = find_top_3_from_sketch(hash_functions, sketch)
        print("Top-3 apo sketch:")
        for x, est in top_3:
            print(f"  {x}: ~{est}")
    except FileNotFoundError:
        print("arxeia  hash_functions.txt h sketch.txt den  vrethiakan.")
        print("paraleipsis  asksis 2.")
    
    print("\n" + "-"*50)
    print("askisi  3: CountMinFInfinity")
    print("-"*50)
    
    stream_ops = [(1, +1), (1, +1), (2, +1), (1, -1), (3, +1), (3, +1), (3, +1)]
    cms_finf = CountMinFInfinity(epsilon=0.01, delta=0.01)
    
    for item, delta in stream_ops:
        cms_finf.update(item, delta)
    
    f_infinity_estimate = cms_finf.estimate_f_infty()
    print(f"ektimisi F APOIRO apo CountMinFInfinity: {f_infinity_estimate}")
    
    actual_counts = {}
    for item, delta in stream_ops:
        actual_counts[item] = actual_counts.get(item, 0) + delta
    actual_f_infinity = max(actual_counts.values())
    print(f"pragmatiki timi F APOIRO: {actual_f_infinity}")
    
    print("\n" + "-"*50)
    print("askisi 4: Top-k se katanomes Zipf")
    print("-"*50)
    
    try:
        with open("vilfredo.txt", "r", encoding="utf-8") as f:
            text = f.read()
        
        stream_words = extract_words(text)
        word_counts = Counter(stream_words)
        real_top10 = word_counts.most_common(10)
        
        print("Top-10 lekseis (pragmatikes):")
        for w, c in real_top10:
            print(f"  {w}: {c}")
        
        cms_words = CountMinSketchWords(epsilon=0.001, delta=1e-5)
        top10_est = track_top_k(stream_words, cms_words, 10)
        
        print("\nTop-10 CountMin ektimiseis:")
        for w, est in top10_est:
            actual_count = word_counts[w]
            print(f"  {w}: ektimomeni={est}, pragmatiki={actual_count}")
            
    except FileNotFoundError:
        print("arxeio vilfredo.txt den vrethike.")
        print("paraleipsi asksiis 4.")
    
    print("\n" + "="*80)
    print("oloklirosi enotitas a")
    print("="*80)

if __name__ == "__main__":
    run_all_exercises()
# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr
import random                                   # Για παραγωγή τυχαίων αριθμών
import heapq                                    # Για υλοποίηση ουράς προτεραιότητας (min-heap)
import numpy as np                              # Για υπολογισμό διαμέσου (median)
from tqdm import tqdm                           # Για γραμμή προόδου στην κονσόλα
from tabulate import tabulate                   # Για όμορφη μορφοποίηση πίνακα αποτελεσμάτων

# TrieNode: βασικός κόμβος για το δυαδικό Trie
class TrieNode:
    def __init__(self):
        self.children = {}                      # Παιδιά κόμβου για bits '0' και '1'
        self.is_end = False                     # Αντιπροσωπεύει τέλος διαδρομής (πλήρης αριθμός)

# Δομή BinaryTrie για καταμέτρηση μοναδικών αριθμών
class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()                  # Αρχικοποιούμε τη ρίζα
        self.distinct_count = 0                 # Μετρητής διακριτών αριθμών

    def insert(self, x):
        binary = bin(x)[2:].zfill(20)           # Μετατροπή x σε δυαδική συμβολοσειρά 20-bit
        node = self.root
        for bit in binary:
            if bit not in node.children:
                node.children[bit] = TrieNode() # Δημιουργία νέου κόμβου αν δεν υπάρχει
            node = node.children[bit]
        if not node.is_end:                     # Αν ο αριθμός εμφανίζεται για πρώτη φορά
            node.is_end = True
            self.distinct_count += 1            # Αυξάνουμε το πλήθος μοναδικών
            return True
        return False

# BJKST αλγόριθμος εκτίμησης πληθυσμού μοναδικών στοιχείων
class BJKST:
    def __init__(self, m=2**20, epsilon=0.1):
        self.m = m                              # Μέγεθος του σύμπαντος των εισαγόμενων τιμών
        self.M = 2 ** 60                         # Πλήθος πιθανών hash τιμών (πρέπει να είναι μεγάλο)
        self.epsilon = epsilon                  # Παράμετρος ακρίβειας
        self.t = int(96 / (epsilon ** 2))       # Αριθμός στοιχείων που κρατάμε (θεωρητικά)
        self.hash_values = []                   # Max-heap με αρνητικά hash

        # Σχόλιο 1: Θέτουμε μεγάλο καθολικό p ώστε να είναι p > M
        self.p = 1048583 ** 3                   # Μεγάλος πρώτος αριθμός για hashing

        # Σχόλιο 2: Χρήση καθολικής hash με τυχαίες παραμέτρους a, b
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

    def hash_function(self, x):
        # Σχόλιο 3: Η hash επιστρέφει τιμή modulo M
        return ((self.a * x + self.b) % self.p) % self.M

    def insert(self, x):
        hx = self.hash_function(x)
        if len(self.hash_values) < self.t:
            heapq.heappush(self.hash_values, -hx)      # Προσθήκη στο heap (αρνητικό για max-heap)
        elif hx < -self.hash_values[0]:                # Αν είναι μικρότερο από το μέγιστο
            heapq.heappop(self.hash_values)            # Αφαίρεση του μεγαλύτερου
            heapq.heappush(self.hash_values, -hx)      # Προσθήκη νέου μικρότερου

    def query(self):
        if len(self.hash_values) < self.t:
            return len(self.hash_values)               # Επιστροφή μεγέθους αν έχουμε λίγα στοιχεία
        r = -self.hash_values[0]                       # Μεγαλύτερο αποθηκευμένο hash
        return (self.t * self.M) / r                   # Εκτίμηση πληθυσμού με βάση BJKST

# Δημιουργεί ομοιόμορφη ροή από 20-bit αριθμούς
def simple_form(N):
    return [random.randint(0, 2**20 - 1) for _ in range(N)]

# Δημιουργεί skewed (μη ομοιόμορφη) ροή με διαφορετικές πιθανότητες ανά περιοχή
def use_of_probabilities_20bit(N):
    ranges = [
        (0, 2**5 - 1, 1/4),                     # Πιο πιθανά μικρά νούμερα
        (2**5, 2**10 - 1, 1/8),
        (2**10, 2**15 - 1, 1/16),
        (2**15, 2**20 - 1, 1/32),               # Λιγότερο πιθανά μεγάλα νούμερα
    ]
    probs = [r[2] for r in ranges]
    stream = []
    for _ in range(N):
        low, high, _ = random.choices(ranges, weights=probs, k=1)[0]
        stream.append(random.randint(low, high))
    return stream

# Όπως το παραπάνω αλλά με hash για διάχυση τιμών
def use_of_probabilities_hashed(N):
    raw_stream = use_of_probabilities_20bit(N)
    a = random.randint(1, 2**20 - 1)
    b = random.randint(0, 2**20 - 1)
    p = 1048583 ** 3
    return [((a * x + b) % p) for x in raw_stream]

# Εκτελεί τον BJKST k φορές και παίρνει τη διάμεσο των εκτιμήσεων
def run_bjkst_with_median(stream, k=101, step=100000):
    bjksts = [BJKST() for _ in range(k)]      # Δημιουργία k ανεξάρτητων εκτιμητών
    trie = BinaryTrie()                       # Trie για ακριβή υπολογισμό μοναδικών
    results = []

    print(f"Running BJKST with median of {k} estimators...")
    for i, x in enumerate(tqdm(stream), 1):
        for bjkst in bjksts:
            bjkst.insert(x)                   # Εισαγωγή κάθε στοιχείου σε όλους τους εκτιμητές
        trie.insert(x)                        # Εισαγωγή στο Trie
        if i % step == 0:
            estimates = [bjkst.query() for bjkst in bjksts]
            median_estimate = int(np.median(estimates))          # Διάμεσος όλων των εκτιμήσεων
            results.append((i, trie.distinct_count, median_estimate))

    return results

# Εκτελεί τη δοκιμή σε ροή και εκτυπώνει πίνακα με τα αποτελέσματα
def run_and_print(stream_name, stream):
    results = run_bjkst_with_median(stream)
    headers = ["N", "True Count", "Median Estimate"]
    table = tabulate(results, headers=headers, tablefmt="fancy_grid", numalign="right")
    print(f"\n Results for {stream_name} stream:")
    print(table)

# Κεντρική συνάρτηση που εκτελεί το σύνολο των δοκιμών
def main():
    N = 1_000_000
    stream_u = simple_form(N)                     # Ομοιόμορφη ροή
    stream_s = use_of_probabilities_20bit(N)      # Skewed ροή
    stream_sh = use_of_probabilities_hashed(N)    # Skewed + hash ροή

    run_and_print("simple form", stream_u)
    run_and_print("use of probabilities", stream_s)
    run_and_print("use of probabilities + Hash", stream_sh)

# Εκκίνηση του προγράμματος
if __name__ == "__main__":
    main()

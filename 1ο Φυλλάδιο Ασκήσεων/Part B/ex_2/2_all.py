# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

import random                                  # Χρησιμοποιείται για παραγωγή τυχαίων αριθμών
import heapq                                   # Υλοποιεί ουρές προτεραιότητας (min-heap)
from tabulate import tabulate                  # Για όμορφη εμφάνιση πίνακα αποτελεσμάτων

class TrieNode:
    def __init__(self):
        self.children = {}                     # Λεξικό παιδιών για τα bits '0' και '1'
        self.is_end = False                    # Δηλώνει αν αυτός ο κόμβος είναι το τέλος ενός αριθμού

class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()                 # Ριζικός κόμβος του trie
        self.distinct_count = 0                # Πλήθος μοναδικών αριθμών που έχουν εισαχθεί

    def insert(self, x):
        binary = bin(x)[2:].zfill(20)          # Μετατροπή του x σε 20-bit δυαδική συμβολοσειρά
        node = self.root                       # Εκκίνηση από τη ρίζα
        for bit in binary:                     # Για κάθε bit της δυαδικής αναπαράστασης
            if bit not in node.children:       # Αν δεν υπάρχει ήδη το παιδί
                node.children[bit] = TrieNode()# Δημιουργία νέου κόμβου
            node = node.children[bit]          # Μετακίνηση στον επόμενο κόμβο
        if not node.is_end:                    # Αν ο αριθμός δεν έχει εισαχθεί ξανά
            node.is_end = True                 # Ορίζουμε ότι τώρα εισήχθη
            self.distinct_count += 1           # Αυξάνουμε τον μετρητή μοναδικών
            return True                        # Επιστρέφουμε ότι ήταν νέος αριθμός
        return False                           # Αν υπήρχε ήδη, επιστρέφουμε False

class BJKST:
    def __init__(self, m=2**20, epsilon=0.1):
        self.m = m                             # Μέγεθος του universe των στοιχείων
        self.M = 2 ** 60                       # Εύρος κατακερματισμένων τιμών (μεγαλύτερο από p)
        self.epsilon = epsilon                 # Παράμετρος σφάλματος
        self.t = int((96 / (epsilon ** 2)))    # Πλήθος στοιχείων που διατηρούμε
        self.hash_values = []                  # Λίστα με τα t μικρότερα hash

        self.p = 1048583 ** 3                  # Πολύ μεγάλος πρώτος αριθμός ώστε p > M
        self.a = random.randint(1, self.p - 1) # Τυχαίος πολλαπλασιαστής για universal hashing
        self.b = random.randint(0, self.p - 1) # Τυχαία σταθερά πρόσθεσης

    def hash_function(self, x):
        return ((self.a * x + self.b) % self.p) % self.M  # Καθολική συνάρτηση κατακερματισμού mod M

    def insert(self, x):
        hx = self.hash_function(x)             # Υπολογισμός του hash του x
        if len(self.hash_values) < self.t:     # Αν δεν έχουμε γεμίσει ακόμη
            heapq.heappush(self.hash_values, -hx)  # Εισαγωγή του -hx (max heap)
        elif hx < -self.hash_values[0]:        # Αν το νέο hash είναι μικρότερο από το μεγαλύτερο αποθηκευμένο
            heapq.heappop(self.hash_values)    # Αφαίρεση του μεγαλύτερου
            heapq.heappush(self.hash_values, -hx)  # Εισαγωγή του νέου

    def query(self):
        if len(self.hash_values) < self.t:     # Αν δεν έχουμε αρκετά δεδομένα
            return len(self.hash_values)       # Επιστρέφουμε απλώς το μέγεθος
        r = -self.hash_values[0]               # Το μέγιστο από τα μικρότερα hash
        return (self.t * self.M) / r           # Εκτίμηση με βάση την εξίσωση BJKST

def simple_form(N):
    return [random.randint(0, 2**20 - 1) for _ in range(N)]  # Δημιουργία N τυχαίων 20-bit αριθμών

def use_of_probabilities_20bit(N):
    ranges = [
        (0, 2**5 - 1, 1/4),                    # Πιο συχνοί αριθμοί: 5 bits
        (2**5, 2**10 - 1, 1/8),                # 10-bit περιοχή
        (2**10, 2**15 - 1, 1/16),              # 15-bit περιοχή
        (2**15, 2**20 - 1, 1/32),              # 20-bit περιοχή (σπάνια)
    ]
    probs = [r[2] for r in ranges]             # Λίστα πιθανοτήτων
    stream = []
    for _ in range(N):                         # Για κάθε στοιχείο της ροής
        low, high, _ = random.choices(ranges, weights=probs, k=1)[0]
        stream.append(random.randint(low, high))
    return stream

def use_of_probabilities_hash(N):
    raw_stream = use_of_probabilities_20bit(N) # Δημιουργία skewed ροής
    a = random.randint(1, 2**20 - 1)           # Συντελεστής για hash
    b = random.randint(0, 2**20 - 1)           # Προσθετέος όρος
    p = 1048583                                # Πρώτος αριθμός > 2^20
    return [((a * x + b) % p) for x in raw_stream]  # Hashάρισμα για ισοκατανομή

def run_bjkst(stream, step=100000):
    bjkst = BJKST()                            # Δημιουργία αντικειμένου BJKST
    seen = BinaryTrie()                        # Trie για πραγματικό count
    distinct_count = 0                         # Αριθμός διακριτών
    results = []

    for i, x in enumerate(stream, 1):          # Για κάθε στοιχείο της ροής
        bjkst.insert(x)                        # Εισαγωγή στον αλγόριθμο
        if seen.insert(x):                     # Εισαγωγή στο trie
            distinct_count += 1                # Αν είναι νέος, αυξάνουμε τον μετρητή
        if i % step == 0:                      # Αν φτάσαμε στο επόμενο βήμα
            est = int(bjkst.query())           # Εκτίμηση πλήθους από BJKST
            results.append((i, distinct_count, est))  # Καταγραφή αποτελεσμάτων

    return results

def main():
    N = 1_000_000                              # Μέγεθος ροής

    print("Δημιουργία ροών...")
    s_uniform = simple_form(N)                # Ομοιόμορφη κατανομή
    s_skewed = use_of_probabilities_20bit(N)  # Skewed χωρίς hash
    s_skewed_hashed = use_of_probabilities_hash(N)  # Skewed με hash

    print("Εκτέλεση BJKST σε Ομοιόμορφη ροή...")
    res_uniform = run_bjkst(s_uniform)
    print("Εκτέλεση BJKST σε Skewed ροή...")
    res_skewed = run_bjkst(s_skewed)
    print("Εκτέλεση BJKST σε Skewed + Hash ροή...")
    res_skewed_hash = run_bjkst(s_skewed_hashed)

    table = []                                 # Πίνακας αποτελεσμάτων
    for i in range(len(res_uniform)):
        n = res_uniform[i][0]                  # Πλήθος στοιχείων μέχρι το βήμα i
        u_act, u_est = res_uniform[i][1], res_uniform[i][2]
        s_act, s_est = res_skewed[i][1], res_skewed[i][2]
        sh_act, sh_est = res_skewed_hash[i][1], res_skewed_hash[i][2]
        table.append([n, u_act, u_est, s_act, s_est, sh_est])

    headers = ["N", "Actual number", "Simple form", "prob actual number", "prob", "prob + Hash"]
    print("\n Αποτελέσματα:")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid", numalign="right"))

if __name__ == "__main__":
    main()

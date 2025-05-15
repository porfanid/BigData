# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

import random
from tabulate import tabulate  # Βιβλιοθήκη για την όμορφη εκτύπωση πινάκων

# -------- Σταθερές --------
P = 1048583  # Ένας πρώτος αριθμός μεγαλύτερος του 2^20 (για χρήση στη hash function)
a = random.randint(1, P - 1)  # Συντελεστής a για τη hash function (τυχαίος)
b = random.randint(0, P - 1)  # Συντελεστής b για τη hash function (τυχαίος)

# -------- Κατανομή εισόδου --------
# Δημιουργεί τυχαίους 20-bit αριθμούς με μη ομοιόμορφη κατανομή
def custom_random_20bit():
    ranges = [
        (0,       2**5  - 1, 1/4),   # Τιμές 0–31: πολύ συχνές (0–4 bits)
        (2**5,    2**10 - 1, 1/8),   # Τιμές 32–1023: συχνές (5–9 bits)
        (2**10,   2**15 - 1, 1/16),  # Τιμές 1024–32767: λιγότερο συχνές (10–14 bits)
        (2**15,   2**20 - 1, 1/32),  # Τιμές 32768–1048575: σπάνιες (15–19 bits)
    ]
    probs = [r[2] for r in ranges]  # Πιθανότητες εμφάνισης για κάθε περιοχή
    selected = random.choices(ranges, weights=probs, k=1)[0]  # Επιλογή περιοχής με βάση τις πιθανότητες
    return random.randint(selected[0], selected[1])  # Τυχαίος αριθμός μέσα στην επιλεγμένη περιοχή

# -------- Συνάρτηση κατακερματισμού (hash function) --------
# Εφαρμόζει την hash: h(x) = (a * x + b) mod P
def hash_function(x):
    return (a * x + b) % P

# -------- Καταμέτρηση αριθμού μηδενικών στο τέλος του δυαδικού --------
def count_trailing_zeros(x):
    binary = bin(x)[2:]  # Δυαδική αναπαράσταση του x
    return len(binary) - len(binary.rstrip('0'))  # Αφαιρεί τα μηδενικά από το τέλος και μετράει πόσα υπήρχαν

# -------- Πιθανοτικός Εκτιμητής Flajolet-Martin --------
class DistinctCounter:
    def __init__(self):
        self.R = 0  # Μέγιστο πλήθος μηδενικών που έχουμε δει

    def insert(self, x):
        h = hash_function(x)         # Υπολογισμός hash του x
        r = count_trailing_zeros(h)  # Καταμέτρηση των τελικών μηδενικών στο δυαδικό του hash
        if r > self.R:               # Ενημέρωση του μέγιστου αν βρέθηκε μεγαλύτερο
            self.R = r

    def query(self):
        return 2 ** self.R  # Εκτίμηση πλήθους μοναδικών στοιχείων: 2^R

# -------- Trie για αποθήκευση μοναδικών δυαδικών ακολουθιών --------
class TrieNode:
    def __init__(self):
        self.children = {}  # Παιδιά κόμβου (0 ή 1)
        self.is_end = False  # Τέλος έγκυρης ακολουθίας

class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()
        self.count = 0  # Καταμέτρηση μοναδικών στοιχείων

    def insert(self, x):
        binary = format(x, '020b')  # Αναπαράσταση 20-bit του αριθμού
        node = self.root
        is_new = False

        for bit in binary:  # Εισαγωγή χαρακτήρα-χαρακτήρα (bit-bit)
            if bit not in node.children:
                node.children[bit] = TrieNode()
                is_new = True  # Νέα διαδρομή = νέο στοιχείο
            node = node.children[bit]

        if not node.is_end:
            node.is_end = True
            is_new = True  # Νέο τέλος λέξης = νέο στοιχείο

        if is_new:
            self.count += 1  # Αύξηση πλήθους μοναδικών στοιχείων

# -------- Κύρια Συνάρτηση --------
def main():
    print(f"Χρησιμοποιείται hash: h(x) = ({a} * x + {b}) mod {P}")

    N = 1_000_000  # Πλήθος εισόδων προς επεξεργασία
    counter = DistinctCounter()  # Εκτιμητής Flajolet-Martin
    trie = BinaryTrie()          # Trie για καταμέτρηση πραγματικών μοναδικών
    true_set = set()             # Set για σύγκριση (πραγματικά μοναδικά)
    results = []                 # Λίστα για αποθήκευση ενδιάμεσων αποτελεσμάτων

    # Εισαγωγή στοιχείων και ενημέρωση εκτιμητών
    for i in range(1, N + 1):
        x = custom_random_20bit()  # Δημιουργία στοιχείου
        counter.insert(x)         # Εισαγωγή στον Flajolet-Martin
        trie.insert(x)            # Εισαγωγή στο Trie
        true_set.add(x)           # Εισαγωγή στο σύνολο (για ακριβή μέτρηση)

        # Ανά 100.000 στοιχεία, εκτυπώνουμε τις ενδιάμεσες εκτιμήσεις
        if i % 100000 == 0:
            approx = counter.query()       # Εκτίμηση FM
            actual_set = len(true_set)     # Πραγματικά μοναδικά από set
            actual_trie = trie.count       # Πραγματικά μοναδικά από Trie
            results.append([i, actual_set, actual_trie, approx])  # Αποθήκευση αποτελεσμάτων

    # Εκτύπωση αποτελεσμάτων σε μορφή πίνακα
    headers = ["Στοιχεία μέχρι τώρα", "Πραγματικά μοναδικά set", "Πραγματικά μοναδικά trie", "Εκτίμηση Flajolet-Martin"]
    print(tabulate(results, headers=headers, tablefmt="fancy_grid", numalign="right"))

# -------- Εκκίνηση προγράμματος --------
if __name__ == "__main__":
    main()

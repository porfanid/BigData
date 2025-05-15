# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

import random
from tabulate import tabulate  # type: ignore # Χρήση βιβλιοθήκης για εκτύπωση πίνακα σε όμορφη μορφή

# --------------------------------------------------
# Συνάρτηση count_trailing_zeros(x):
# Υπολογίζει πόσα συνεχόμενα μηδενικά υπάρχουν στο τέλος
# της δυαδικής αναπαράστασης του ακέραιου x.
# Παράδειγμα: bin(12) = '1100' => έχει 2 trailing zeros.
def count_trailing_zeros(x):
    binary = bin(x)[2:]  # Μετατροπή σε δυαδική αναπαράσταση, αφαίρεση του '0b' προθέματος
    return len(binary) - len(binary.rstrip('0'))  # Υπολογισμός αριθμού διαδοχικών μηδενικών στο τέλος

# --------------------------------------------------
# Συνάρτηση κατακερματισμού (hash function).
# Στη συγκεκριμένη απλή υλοποίηση, ο hash είναι απλά το ίδιο το x.
def hash_function(x):
    return x

# --------------------------------------------------
# Κλάση DistinctCounter που υλοποιεί τον Flajolet-Martin αλγόριθμο.
# Κρατά μόνο μία μεταβλητή R, που αντιστοιχεί στο μέγιστο αριθμό trailing zeros
# που έχουν παρατηρηθεί σε hash τιμές μέχρι στιγμής.
class DistinctCounter:
    def __init__(self):
        self.R = 0  # Αρχική τιμή: κανένα μηδενικό στο τέλος

    def insert(self, x):
        h = hash_function(x)               # Εφαρμογή συνάρτησης κατακερματισμού
        r = count_trailing_zeros(h)       # Υπολογισμός trailing zeros στο h(x)
        if r > self.R:                    # Αν αυτός ο αριθμός είναι μεγαλύτερος απ’ ό,τι έχουμε δει μέχρι τώρα
            self.R = r                    # Τότε ενημερώνουμε την τιμή του R

    def query(self):
        return 2 ** self.R  # Η εκτίμηση βασίζεται στο 2^R, σύμφωνα με τη θεωρία του Flajolet-Martin

# -----------------------------
# Κόμβος του Trie
class TrieNode:
    def __init__(self):
        self.children = {}  # Παιδιά κόμβου (0 ή 1)
        self.is_end = False  # Αν αυτό το μονοπάτι αποτελεί ολοκληρωμένο αριθμό

# Trie για αποθήκευση δυαδικών αναπαραστάσεων και καταμέτρηση μοναδικών τιμών
class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()
        self.count = 0  # Πλήθος διαφορετικών αριθμών

    def insert(self, x):
        binary = bin(x)[2:]  # Μετατροπή σε δυαδική μορφή
        node = self.root
        is_new = False  # Flag για να δούμε αν το μονοπάτι είναι καινούριο

        for bit in binary:
            if bit not in node.children:
                node.children[bit] = TrieNode()
                is_new = True  # Εντοπίστηκε νέα διαδρομή
            node = node.children[bit]

        if not node.is_end:
            node.is_end = True
            is_new = True  # Νέα μοναδική αλυσίδα

        if is_new:
            self.count += 1  # Αυξάνουμε το πλήθος μοναδικών τιμών

# -----------------------------
# Κύρια συνάρτηση εκτέλεσης
def main():
    N = 1_000_000  # Πλήθος στοιχείων που θα εισαχθούν
    counter = DistinctCounter()  # Πιθανοτικός εκτιμητής (Flajolet-Martin)
    trie = BinaryTrie()  # Ακριβής καταμέτρηση με Trie
    results = []  # Πίνακας αποτελεσμάτων για την εκτύπωση

    for i in range(1, N + 1):
        x = random.randint(0, 1_000_000)  # Τυχαίος ακέραιος αριθμός
        counter.insert(x)  # Εισαγωγή στον εκτιμητή
        trie.insert(x)     # Εισαγωγή στο Trie

        if i % 100000 == 0:  # Κάθε 100.000 στοιχεία, καταγράφουμε αποτελέσματα
            approx = counter.query()  # Εκτίμηση μοναδικών από FM
            actual = trie.count       # Πραγματικό πλήθος μοναδικών από Trie
            results.append([i, actual, approx])  # Προσθήκη στο αποτέλεσμα

    # Εκτύπωση των αποτελεσμάτων σε μορφή πίνακα (με τίτλους στηλών)
    headers = ["Στοιχεία μέχρι τώρα", "Πραγματικά μοναδικά", "Εκτίμηση Flajolet-Martin"]
    print(tabulate(results, headers=headers, tablefmt="fancy_grid", numalign="right"))

# Εκκίνηση προγράμματος
if __name__ == "__main__":
    main()

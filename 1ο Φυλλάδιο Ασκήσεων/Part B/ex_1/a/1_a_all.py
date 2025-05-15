# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

import random
from tabulate import tabulate  # type: ignore # Χρήση βιβλιοθήκης για εκτύπωση πίνακα σε όμορφη μορφή

# Συνάρτηση που υπολογίζει πόσα μηδενικά υπάρχουν στο τέλος της δυαδικής αναπαράστασης ενός αριθμού.
# Για παράδειγμα: 8 -> '1000' έχει 3 trailing zeros.
def count_trailing_zeros(x):
    binary = bin(x)[2:]  # Αφαίρεση του '0b' από την αρχή της δυαδικής μορφής
    return len(binary) - len(binary.rstrip('0'))  # Αφαιρούμε τα δεξιά μηδενικά και υπολογίζουμε πόσα αφαιρέθηκαν

# Συνάρτηση κατακερματισμού (hash). Εδώ απλώς επιστρέφει την ίδια τιμή,
# αλλά μπορεί να αλλαχτεί για χρήση π.χ. με hash(x) ή κάποιο universal hash.
def hash_function(x):
    return x

# Κλάση που υλοποιεί τον βασικό πιθανοτικό εκτιμητή τύπου Flajolet-Martin.
class DistinctCounter:
    def __init__(self):
        self.R = 0  # Αποθηκεύει τη μέγιστη παρατηρούμενη τιμή trailing zeros

    def insert(self, x):
        h = hash_function(x)             # Εφαρμογή συνάρτησης κατακερματισμού
        r = count_trailing_zeros(h)      # Υπολογισμός trailing zeros στο hash
        if r > self.R:                   # Αν η τιμή είναι μεγαλύτερη από τη μέχρι τώρα μέγιστη
            self.R = r                   # την αποθηκεύουμε

    def query(self):
        return 2 ** self.R               # Η εκτίμηση του πλήθους μοναδικών στοιχείων είναι 2^R

# Κλάση για κόμβο του δυαδικού trie (κάθε κόμβος έχει 0 ή 1 ως παιδιά)
class TrieNode:
    def __init__(self):
        self.children = {}              # Παιδιά (bit -> κόμβος)
        self.is_end = False             # Σηματοδοτεί αν είναι τέλος αριθμού

# Δυαδικό trie για αποθήκευση αριθμών σε δυαδική μορφή, χρησιμοποιείται ως ground truth για πλήθος μοναδικών.
class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()          # Ριζικός κόμβος
        self.count = 0                  # Πλήθος μοναδικών αριθμών που εισήχθησαν

    def insert(self, x):
        binary = bin(x)[2:]             # Μετατροπή του αριθμού σε δυαδική μορφή χωρίς το '0b'
        node = self.root
        is_new = False                  # Αν είναι καινούργια διαδρομή/αριθμός

        for bit in binary:
            if bit not in node.children:
                node.children[bit] = TrieNode()
                is_new = True
            node = node.children[bit]

        if not node.is_end:
            node.is_end = True
            is_new = True

        if is_new:
            self.count += 1             # Αυξάνουμε το πλήθος μόνο αν προστέθηκε νέος αριθμός

# Κύρια ροή προγράμματος
def main():
    N = 1_000_000                          # Συνολικά στοιχεία προς εισαγωγή
    counter = DistinctCounter()           # Δημιουργία του πιθανοτικού εκτιμητή (Flajolet-Martin)
    trie = BinaryTrie()                   # Trie για αποθήκευση μοναδικών τιμών
    true_set = set()                      # Χρήση συνόλου Python για "πραγματικά" μοναδικά
    results = []                          # Αποτελέσματα για εμφάνιση

    for i in range(1, N + 1):
        x = random.randint(0, 1_000_000)   # Τυχαίος ακέραιος αριθμός

        counter.insert(x)                 # Εισαγωγή στον εκτιμητή
        trie.insert(x)                    # Εισαγωγή στο trie
        true_set.add(x)                   # Εισαγωγή στο σύνολο (set)

        # Ανά 100.000 στοιχεία, καταγράφουμε την πρόοδο
        if i % 100000 == 0:
            approx = counter.query()      # Εκτίμηση με τον Flajolet-Martin
            actual_set = len(true_set)    # Ακριβές πλήθος μέσω set
            actual_trie = trie.count      # Ακριβές πλήθος μέσω trie
            results.append([i, actual_set, actual_trie, approx])

    # Εκτύπωση αποτελεσμάτων με μορφοποίηση πίνακα
    headers = ["Στοιχεία μέχρι τώρα", "Πραγματικά μοναδικά set", "Πραγματικά μοναδικά trie", "Εκτίμηση Flajolet-Martin"]
    print(tabulate(results, headers=headers, tablefmt="fancy_grid", numalign="right"))

if __name__ == "__main__":
    main()

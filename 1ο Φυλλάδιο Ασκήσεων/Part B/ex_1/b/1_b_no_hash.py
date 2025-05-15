# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

import random
from tabulate import tabulate  # type: ignore # Χρήση βιβλιοθήκης για εκτύπωση πίνακα σε όμορφη μορφή

# -------- Προσαρμοσμένη Πιθανοτική Κατανομή για 20-bit Αριθμούς --------
# Γεννά 20-bit ακέραιους με μια ασύμμετρη κατανομή πιθανοτήτων.
# Ορισμένες περιοχές bit εμφανίζονται πιο συχνά από άλλες.
def custom_random_20bit():
    # Περιοχές τιμών με τις αντίστοιχες πιθανότητες εμφάνισης
    ranges = [
        (0,       2**5  - 1, 1/4),   # Τιμές με 0–4 bits (πιο συχνές)
        (2**5,    2**10 - 1, 1/8),   # Τιμές με 5–9 bits
        (2**10,   2**15 - 1, 1/16),  # Τιμές με 10–14 bits
        (2**15,   2**20 - 1, 1/32),  # Τιμές με 15–19 bits (πιο σπάνιες)
    ]
    # Εξαγωγή των πιθανοτήτων από κάθε περιοχή
    probs = [r[2] for r in ranges]
    # Επιλογή μιας περιοχής βάσει πιθανοτήτων
    selected = random.choices(ranges, weights=probs, k=1)[0]
    low, high = selected[0], selected[1]
    return random.randint(low, high)

# -------- Συνάρτηση Κατακερματισμού --------
# Προσωρινή συνάρτηση hash — προς το παρόν επιστρέφει τον ίδιο τον αριθμό.
def hash_function(x):
    return x

# -------- Συνάρτηση Μέτρησης Τερματικών Μηδενικών --------
# Μετρά πόσα συνεχόμενα μηδενικά υπάρχουν στο τέλος της δυαδικής μορφής του x.
def count_trailing_zeros(x):
    binary = bin(x)[2:]  # Μετατροπή σε δυαδικό χωρίς το '0b'
    return len(binary) - len(binary.rstrip('0'))

# -------- Κλάση Εκτιμητή Flajolet-Martin --------
# Πιθανοτικός αλγόριθμος για εκτίμηση πλήθους μοναδικών στοιχείων.
class DistinctCounter:
    def __init__(self):
        self.R = 0  # Μέγιστος αριθμός τερματικών μηδενικών που έχουμε δει

    def insert(self, x):
        h = hash_function(x)
        r = count_trailing_zeros(h)
        if r > self.R:
            self.R = r  # Ενημέρωση του R αν βρέθηκε μεγαλύτερη τιμή

    def query(self):
        return 2 ** self.R  # Εκτίμηση μοναδικών στοιχείων: 2^R

# -------- Trie για Ακριβή Καταμέτρηση --------
# Κόμβος του δυαδικού Trie
class TrieNode:
    def __init__(self):
        self.children = {}  # Παιδιά του κόμβου: '0' ή '1'
        self.is_end = False  # Αντιπροσωπεύει τέλος μιας αριθμητικής αλυσίδας

# Δομή Trie που αποθηκεύει δυαδικές αναπαραστάσεις 20-bit αριθμών
class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()
        self.count = 0  # Πλήθος διαφορετικών αριθμών που έχουν εισαχθεί

    def insert(self, x):
        binary = format(x, '020b')  # Δυαδική αναπαράσταση 20 bit
        node = self.root
        is_new = False  # Σημαία για να εντοπίσουμε αν είναι νέα διαδρομή

        for bit in binary:
            if bit not in node.children:
                node.children[bit] = TrieNode()
                is_new = True  # Δημιουργήθηκε νέο μονοπάτι
            node = node.children[bit]

        if not node.is_end:
            node.is_end = True
            is_new = True  # Τέλος νέου μοναδικού αριθμού

        if is_new:
            self.count += 1  # Αύξηση μετρητή για νέο διαφορετικό στοιχείο

# -------- Κύρια Συνάρτηση Εκτέλεσης --------
def main():
    N = 1_000_000  # Πλήθος αριθμών που θα δημιουργηθούν
    counter = DistinctCounter()  # Πιθανοτικός εκτιμητής (FM)
    trie = BinaryTrie()          # Trie για ακριβή μέτρηση
    true_set = set()             # Επίσης χρησιμοποιούμε Python set για έλεγχο
    results = []
    for i in range(1, N + 1):
        x = custom_random_20bit()  # Δημιουργία αριθμού από την ειδική κατανομή
        counter.insert(x)          # Εισαγωγή στον FM εκτιμητή
        trie.insert(x)             # Εισαγωγή στο Trie
        true_set.add(x)            # Εισαγωγή στο set (για ακρίβεια)

        if i % 100000 == 0:
            approx = counter.query()        # Εκτίμηση FM
            actual_set = len(true_set)      # Πραγματικό πλήθος από set
            actual_trie = trie.count        # Πραγματικό πλήθος από Trie
            results.append([i, actual_set, actual_trie, approx])

    # Εκτύπωση των αποτελεσμάτων σε μορφή πίνακα (με τίτλους στηλών)
    headers = ["Στοιχεία μέχρι τώρα", "Πραγματικά μοναδικά set", "Πραγματικά μοναδικά trie", "Εκτίμηση Flajolet-Martin"]
    print(tabulate(results, headers=headers, tablefmt="fancy_grid", numalign="right"))
    
# Σημείο εκκίνησης του προγράμματος
if __name__ == "__main__":
    main()

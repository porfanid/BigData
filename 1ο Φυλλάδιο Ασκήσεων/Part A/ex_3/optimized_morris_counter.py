# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

import numpy as np                        # Για αριθμητικούς υπολογισμούς (δεν χρησιμοποιείται πολύ εδώ)
import matplotlib.pyplot as plt           # Για δημιουργία γραφημάτων
import random                             # Για παραγωγή τυχαίων αριθμών (για την εισαγωγή στον μετρητή)
import math                               # Για μαθηματικές συναρτήσεις όπως log2 και ceil

# Ορισμός της κλάσης για τον βελτιστοποιημένο μετρητή Morris
class OptimizedMorrisCounter:
    """
    Κλάση που υλοποιεί έναν βελτιωμένο Morris counter με ρυθμιζόμενο alpha.
    """

    def __init__(self, alpha, bits=8):
        """
        Αρχικοποίηση μεταβλητών για τον μετρητή.

        alpha: η βάση του εκθετικού βήματος (σχετίζεται με την πιθανότητα αύξησης).
        bits: το πλήθος των bits που περιορίζουν τη μέγιστη τιμή του μετρητή.
        """
        self.alpha = alpha                        # Ρυθμιζόμενο alpha για ακρίβεια/εύρος
        self.C = 0                                # Αρχική εσωτερική τιμή του μετρητή
        self.max_C = 2 ** bits - 1                # Ανώτατο όριο για C βάσει των διαθέσιμων bits

    def insert(self):
        """
        Εισάγει ένα στοιχείο στον μετρητή με πιθανότητα 1 / alpha^C.
        """
        if self.C < self.max_C and random.random() < 1 / pow(self.alpha, self.C):
            self.C += 1                           # Αυξάνουμε C μόνο με την κατάλληλη πιθανότητα

    def query(self):
        """
        Υπολογίζει την εκτίμηση πλήθους με βάση την εσωτερική τιμή C.

        Επιστρέφει:
            float: η εκτιμώμενη τιμή του πλήθους των εισαγωγών.
        """
        return (pow(self.alpha, self.C) - 1) / (self.alpha - 1)  # Τύπος εκτίμησης του Morris counter

# Συνάρτηση που βρίσκει το κατάλληλο alpha ώστε ο μετρητής να καλύπτει έως max_n με τα δεδομένα bits
def find_optimal_alpha(bits, max_n):
    max_C = 2 ** bits - 1                      # Μέγιστη τιμή που μπορεί να πάρει το C
    alpha = 1.1                                # Ξεκινάμε από μικρή τιμή του alpha
    step = 0.01                                # Βήμα αύξησης του alpha για δοκιμές

    while alpha <= 2:
        max_count = (pow(alpha, max_C) - 1) / (alpha - 1)  # Υπολογισμός μέγιστης εκτίμησης για το τρέχον alpha
        if max_count >= max_n:
            return alpha                       # Επιστρέφουμε το alpha που καλύπτει την απαίτηση
        alpha += step

    return 2                                   # Επιστρέφουμε 2 αν δεν βρεθεί καταλληλότερο alpha

# Προσομοίωση της λειτουργίας του μετρητή Morris
def simulate_morris_counter(alpha, max_n, runs=1):
    counter = OptimizedMorrisCounter(alpha)    # Δημιουργία του μετρητή με το δοσμένο alpha
    real_counts = []                           # Πραγματικός αριθμός στοιχείων
    estimated_counts = []                      # Εκτιμήσεις του μετρητή

    for i in range(1, max_n + 1):
        counter.insert()                       # Εισαγωγή στοιχείου
        if i % (max_n // 1000) == 0 or i == max_n:
            real_counts.append(i)              # Καταγραφή πραγματικής τιμής
            estimated_counts.append(counter.query())  # Καταγραφή εκτίμησης

    return real_counts, estimated_counts

# Ορισμός παραμέτρων
bits = 8                                       # Bits που χρησιμοποιούνται για τον μετρητή
max_n = 1_000_000                              # Μέγιστος αριθμός εισαγωγών

# Εύρεση του βέλτιστου alpha για τα συγκεκριμένα bits ώστε να καλύψει το εύρος μέχρι το max_n
optimal_alpha = find_optimal_alpha(bits, max_n)
print(f"Βέλτιστο alpha για {bits} bits και μέγιστο count {max_n}: {optimal_alpha:.4f}")

# Υπολογισμός των ελάχιστων bits που θα απαιτούνταν για standard Morris με alpha = 2
bits_needed = math.ceil(math.log2(math.log2(max_n + 1) + 1))
print(f"Ελάχιστα bits που χρειαζόμαστε για standard Morris counter (με α=2): {bits_needed}")

# Εκτέλεση της προσομοίωσης με το optimal alpha
real_counts, estimated_counts = simulate_morris_counter(optimal_alpha, max_n)

# Δημιουργία γραφήματος αποτελεσμάτων
plt.figure(figsize=(12, 8))                                              # Μέγεθος γραφήματος
plt.plot(real_counts, real_counts, 'r--', label='Πραγματικές τιμές')    # Γραμμή αναφοράς
plt.plot(real_counts, estimated_counts, 'b-', label=f'Εκτιμήσεις μετρητή Morris (alpha={optimal_alpha:.4f})')  # Εκτιμήσεις
plt.xscale('log')                                                        # Λογαριθμική κλίμακα στον x-άξονα
plt.yscale('log')                                                        # Λογαριθμική κλίμακα στον y-άξονα
plt.xlabel('Πλήθος εισαγωγών (n)')
plt.ylabel('Εκτίμηση')
plt.title(f'Βελτιστοποιημένος μετρητής Morris με alpha={optimal_alpha:.4f}')
plt.legend()
plt.grid(True)
plt.savefig('optimized_morris_counter.png')                              # Αποθήκευση του γραφήματος
plt.show()

# Υπολογισμός του μέσου σχετικού σφάλματος για τον optimized μετρητή
rel_errors = [abs(est - real) / real for real, est in zip(real_counts, estimated_counts)]
avg_rel_error = sum(rel_errors) / len(rel_errors)
print(f"Μέσο σχετικό σφάλμα: {avg_rel_error:.4f}")

# Σύγκριση με τον κλασικό μετρητή Morris (alpha = 2)
standard_counter = OptimizedMorrisCounter(2.0)
standard_real_counts = []
standard_estimated_counts = []

for i in range(1, max_n + 1):
    standard_counter.insert()
    if i % (max_n // 1000) == 0 or i == max_n:
        standard_real_counts.append(i)
        standard_estimated_counts.append(standard_counter.query())

# Υπολογισμός σχετικού σφάλματος για τον τυπικό Morris counter
standard_rel_errors = [abs(est - real) / real for real, est in zip(standard_real_counts, standard_estimated_counts)]
standard_avg_rel_error = sum(standard_rel_errors) / len(standard_rel_errors)
print(f"Μέσο σχετικό σφάλμα με τυπικό μετρητή Morris (alpha=2): {standard_avg_rel_error:.4f}")

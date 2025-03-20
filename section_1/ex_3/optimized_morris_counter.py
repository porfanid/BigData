import numpy as np
import matplotlib.pyplot as plt
import random
import math


class OptimizedMorrisCounter:
    def __init__(self, alpha, bits=8):
        self.alpha = alpha
        self.C = 0
        self.max_C = 2 ** bits - 1  # Μέγιστη τιμή που μπορεί να πάρει το C με bits bits

    def insert(self):
        # Αυξάνουμε το C με πιθανότητα 1/alpha^C
        if self.C < self.max_C and random.random() < 1 / pow(self.alpha, self.C):
            self.C += 1

    def query(self):
        # Επιστρέφουμε την εκτίμηση (alpha^C - 1)/(alpha - 1)
        return (pow(self.alpha, self.C) - 1) / (self.alpha - 1)


def find_optimal_alpha(bits, max_n):
    """
    Βρίσκει το βέλτιστο alpha για να αξιοποιηθούν πλήρως τα διαθέσιμα bits,
    ώστε να μπορεί να μετρήσει μέχρι max_n.
    """
    max_C = 2 ** bits - 1

    # Για να μετρήσει μέχρι max_n, θα πρέπει:
    # (alpha^max_C - 1)/(alpha - 1) >= max_n
    # Λύνοντας ως προς alpha:
    # alpha^max_C >= max_n * (alpha - 1) + 1
    # Επειδή είναι δύσκολο να λυθεί αναλυτικά, θα χρησιμοποιήσουμε αριθμητική προσέγγιση

    # Ξεκινάμε με alpha = 1.1 και αυξάνουμε μέχρι να βρούμε το κατάλληλο
    alpha = 1.1
    step = 0.01
    while alpha <= 2:
        max_count = (pow(alpha, max_C) - 1) / (alpha - 1)
        if max_count >= max_n:
            return alpha
        alpha += step

    return 2  # Αν δεν βρέθηκε κατάλληλο alpha, επιστρέφουμε 2


def simulate_morris_counter(alpha, max_n, runs=1):
    """
    Προσομοιώνει τη λειτουργία του βελτιστοποιημένου μετρητή Morris για max_n εισαγωγές.
    """
    counter = OptimizedMorrisCounter(alpha)
    real_counts = []
    estimated_counts = []

    for i in range(1, max_n + 1):
        counter.insert()

        if i % (max_n // 1000) == 0 or i == max_n:  # Κρατάμε περίπου 1000 σημεία για το γράφημα
            real_counts.append(i)
            estimated_counts.append(counter.query())

    return real_counts, estimated_counts


# Παράμετροι
bits = 8
max_n = 1000000

# Υπολογισμός του βέλτιστου alpha
optimal_alpha = find_optimal_alpha(bits, max_n)
print(f"Βέλτιστο alpha για {bits} bits και μέγιστο count {max_n}: {optimal_alpha:.4f}")

# Τεκμηρίωση ότι 8 bits είναι περισσότερα από όσα χρειαζόμαστε
bits_needed = math.ceil(math.log2(math.log2(max_n + 1) + 1))
print(f"Ελάχιστα bits που χρειαζόμαστε για standard Morris counter (με α=2): {bits_needed}")

# Εκτέλεση προσομοίωσης
real_counts, estimated_counts = simulate_morris_counter(optimal_alpha, max_n)

# Δημιουργία γραφήματος
plt.figure(figsize=(12, 8))
plt.plot(real_counts, real_counts, 'r--', label='Πραγματικές τιμές')
plt.plot(real_counts, estimated_counts, 'b-', label='Εκτιμήσεις μετρητή Morris (alpha={:.4f})'.format(optimal_alpha))
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Πλήθος εισαγωγών (n)')
plt.ylabel('Εκτίμηση')
plt.title('Βελτιστοποιημένος μετρητής Morris με alpha={:.4f}'.format(optimal_alpha))
plt.legend()
plt.grid(True)
plt.savefig('optimized_morris_counter.png')
plt.show()

# Υπολογισμός σχετικού σφάλματος
rel_errors = [abs(est - real) / real for real, est in zip(real_counts, estimated_counts)]
avg_rel_error = sum(rel_errors) / len(rel_errors)
print(f"Μέσο σχετικό σφάλμα: {avg_rel_error:.4f}")

# Σύγκριση με τον τυπικό μετρητή Morris (alpha = 2)
standard_counter = OptimizedMorrisCounter(2.0)
standard_real_counts = []
standard_estimated_counts = []

for i in range(1, max_n + 1):
    standard_counter.insert()

    if i % (max_n // 1000) == 0 or i == max_n:
        standard_real_counts.append(i)
        standard_estimated_counts.append(standard_counter.query())

standard_rel_errors = [abs(est - real) / real for real, est in zip(standard_real_counts, standard_estimated_counts)]
standard_avg_rel_error = sum(standard_rel_errors) / len(standard_rel_errors)
print(f"Μέσο σχετικό σφάλμα με τυπικό μετρητή Morris (alpha=2): {standard_avg_rel_error:.4f}")
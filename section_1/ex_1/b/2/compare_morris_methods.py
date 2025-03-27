import sys
import os

# Προσθήκη του καταλόγου ../1 στη διαδρομή συστήματος
# Επιτρέπει την εισαγωγή λειτουργιών από άλλον φάκελο
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../1')))

import numpy as np
import matplotlib.pyplot as plt
import random
import math

# Εισαγωγή της βελτιωμένης κλάσης MorrisCounter
from improved_morris_counter import ImprovedMorrisCounter


# Συνάρτηση σύγκρισης μεθόδων του Morris Counter
def compare_morris_methods(n=1000000, num_counters=5, num_runs=10):
    # Λίστες για αποθήκευση σφαλμάτων από κάθε μέθοδο
    mean_errors = []
    median_errors = []

    # Επανάληψη πολλαπλών εκτελέσεων για στατιστική αξιοπιστία
    for run in range(num_runs):
        # Δημιουργία νέου στιγμιότυπου μετρητή
        counter = ImprovedMorrisCounter(num_counters)

        # Λίστες για αποθήκευση σφαλμάτων σε κάθε εκτέλεση
        mean_run_errors = []
        median_run_errors = []

        # Προσομοίωση εισαγωγής στοιχείων
        for i in range(1, n + 1):
            # Εισαγωγή στοιχείου
            counter.insert()

            # Υπολογισμός εκτιμήσεων με δύο διαφορετικές μεθόδους
            mean_estimate = counter.query_mean()
            median_estimate = counter.query_median()

            # Υπολογισμός σχετικού σφάλματος
            # |πραγματική τιμή - εκτιμώμενη τιμή| / πραγματική τιμή
            mean_rel_error = abs(mean_estimate - i) / i
            median_rel_error = abs(median_estimate - i) / i

            # Αποθήκευση σφαλμάτων
            mean_run_errors.append(mean_rel_error)
            median_run_errors.append(median_rel_error)

        # Προσθήκη των σφαλμάτων κάθε εκτέλεσης
        mean_errors.append(mean_run_errors)
        median_errors.append(median_run_errors)

    # Υπολογισμός μέσου όρου σφαλμάτων από όλες τις εκτελέσεις
    avg_mean_errors = np.mean(mean_errors, axis=0)
    avg_median_errors = np.mean(median_errors, axis=0)

    return avg_mean_errors, avg_median_errors


# Συνάρτηση ανάλυσης χρήσης μνήμης
def memory_analysis():
    # Υπολογισμός απαιτούμενων bits για αναπαράσταση ενός αριθμού
    def bits_needed(n):
        # Χρησιμοποιούμε την ελάχιστη δυνατή bit αναπαράσταση
        return math.ceil(math.log2(n + 1))

    # Επιλέγουμε ένα μεγάλο δείγμα για ανάλυση (1,000,000)
    n = 1000000

    # Υπολογισμός bits για τον απλό Morris Counter
    bits_for_morris = bits_needed(n)

    # Υπολογισμός bits για βελτιωμένο Counter με 5 μεταβλητές
    bits_for_improved = 5 * bits_needed(math.ceil(math.log2(n + 1)))

    # Εύρεση του μέγιστου n όπου η βελτιωμένη μέθοδος είναι αποδοτική
    max_n = 0
    for n_test in range(100, 10 ** 20, 10 ** 5):
        if bits_needed(n_test) <= 5 * bits_needed(math.ceil(math.log2(n_test + 1))):
            continue
        else:
            max_n = n_test - 10 ** 5
            break

    return bits_for_morris, bits_for_improved, max_n


# Ορισμός σταθερού seed για αναπαραγωγιμότητα
random.seed(42)

# Μείωση του n για ταχύτερη εκτέλεση
n = 100000

# Εκτέλεση σύγκρισης μεθόδων
avg_mean_errors, avg_median_errors = compare_morris_methods(n, num_counters=5, num_runs=5)

# Δημιουργία γραφικής παράστασης σφαλμάτων
plt.figure(figsize=(10, 6))
# Γράφημα σφαλμάτων μέσου όρου
plt.plot(range(1, n + 1), avg_mean_errors, color='blue', label='Mean Method Error')
# Γράφημα σφαλμάτων διαμέσου
plt.plot(range(1, n + 1), avg_median_errors, color='green', label='Median Method Error')
# Λογαριθμική κλίμακα για καλύτερη απεικόνιση
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of Elements (n)')
plt.ylabel('Average Relative Error')
plt.title('Comparison of Mean vs Median Methods')
plt.legend()
plt.grid(True)
# Αποθήκευση γραφήματος
plt.savefig('morris_comparison_1b2.png')
plt.close()

# Εκτέλεση ανάλυσης μνήμης
bits_morris, bits_improved, max_useful_n = memory_analysis()

# Εκτύπωση αποτελεσμάτων ανάλυσης
print(f"Bits needed for basic Morris counter to count up to 1,000,000: {bits_morris}")
print(f"Bits needed for improved Morris counter with 5 variables: {bits_improved}")
print(f"Maximum n where using 5 variables is memory-efficient: {max_useful_n}")
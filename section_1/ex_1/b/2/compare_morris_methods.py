import sys
import os

# Add the ../1 directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../1')))

import numpy as np
import matplotlib.pyplot as plt
import random
import math

from improved_morris_counter import ImprovedMorrisCounter


# Συνάρτηση για την άσκηση 1β2
def compare_morris_methods(n=1000000, num_counters=5, num_runs=10):
    mean_errors = []
    median_errors = []

    for run in range(num_runs):
        counter = ImprovedMorrisCounter(num_counters)
        mean_run_errors = []
        median_run_errors = []

        for i in range(1, n + 1):
            counter.insert()

            # Υπολογίζουμε σχετικό σφάλμα
            mean_estimate = counter.query_mean()
            median_estimate = counter.query_median()

            mean_rel_error = abs(mean_estimate - i) / i
            median_rel_error = abs(median_estimate - i) / i

            mean_run_errors.append(mean_rel_error)
            median_run_errors.append(median_rel_error)

        mean_errors.append(mean_run_errors)
        median_errors.append(median_run_errors)

    # Υπολογίζουμε μέσους όρους των σφαλμάτων από όλα τα runs
    avg_mean_errors = np.mean(mean_errors, axis=0)
    avg_median_errors = np.mean(median_errors, axis=0)

    return avg_mean_errors, avg_median_errors


# Ανάλυση για τη χρήση μνήμης
def memory_analysis():
    # Για να αποθηκεύσουμε έναν αριθμό n χρειαζόμαστε log2(n+1) bits
    def bits_needed(n):
        return math.ceil(math.log2(n + 1))

    # Για τον αρχικό μετρητή Morris
    n = 1000000
    bits_for_morris = bits_needed(n)

    # Για τον βελτιωμένο μετρητή με 5 μεταβλητές
    bits_for_improved = 5 * bits_needed(math.ceil(math.log2(n + 1)))

    # Μέχρι ποιο n έχει νόημα να χρησιμοποιούμε 5 μεταβλητές
    # Λύνουμε την εξίσωση: bits_needed(n) = 5 * bits_needed(math.ceil(math.log2(n+1)))
    max_n = 0
    for n_test in range(100, 10 ** 20, 10 ** 5):
        if bits_needed(n_test) <= 5 * bits_needed(math.ceil(math.log2(n_test + 1))):
            continue
        else:
            max_n = n_test - 10 ** 5
            break

    return bits_for_morris, bits_for_improved, max_n


# Εκτέλεση συγκρίσεων
random.seed(42)
n = 100000  # Μειώσαμε το n για ταχύτερη εκτέλεση
avg_mean_errors, avg_median_errors = compare_morris_methods(n, num_counters=5, num_runs=5)

# Γραφική παράσταση με σύγκριση σφαλμάτων
plt.figure(figsize=(10, 6))
plt.plot(range(1, n + 1), avg_mean_errors, color='blue', label='Mean Method Error')
plt.plot(range(1, n + 1), avg_median_errors, color='green', label='Median Method Error')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of Elements (n)')
plt.ylabel('Average Relative Error')
plt.title('Comparison of Mean vs Median Methods')
plt.legend()
plt.grid(True)
plt.savefig('morris_comparison_1b2.png')
plt.close()

# Ανάλυση μνήμης
bits_morris, bits_improved, max_useful_n = memory_analysis()
print(f"Bits needed for basic Morris counter to count up to 1,000,000: {bits_morris}")
print(f"Bits needed for improved Morris counter with 5 variables: {bits_improved}")
print(f"Maximum n where using 5 variables is memory-efficient: {max_useful_n}")
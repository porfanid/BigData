import numpy as np
import matplotlib.pyplot as plt
import random
from fractions import Fraction
import math


# Μετρητής Morris για την άσκηση 1α
class MorrisCounter:
    def __init__(self):
        self.C = 0

    def insert(self):
        # Με πιθανότητα 1/2^C αυξάνουμε το C κατά 1
        if random.random() < 1 / (2 ** self.C):
            self.C += 1

    def query(self):
        # Επιστρέφουμε 2^C - 1 ως εκτίμηση
        return 2 ** self.C - 1


# Υλοποίηση για την άσκηση 1α
def morris_test(n=1000000):
    counter = MorrisCounter()
    estimates = []

    for i in range(1, n + 1):
        counter.insert()
        estimates.append(counter.query())

    return estimates


# Εκτέλεση και δημιουργία γραφικής παράστασης
random.seed(42)  # Για αναπαραγωγή αποτελεσμάτων
n = 1000000
estimates = morris_test(n)

# Γραφική παράσταση
plt.figure(figsize=(10, 6))
plt.plot(range(1, n + 1), estimates, color='blue', label='Morris Counter Estimate')
plt.plot(range(1, n + 1), range(1, n + 1), color='red', linestyle='--', label='Actual Count')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Actual Count (n)')
plt.ylabel('Estimated Count')
plt.title('Morris Counter Estimate vs Actual Count')
plt.legend()
plt.grid(True)
plt.savefig('morris_counter_1a.png')
plt.close()

print("Υλοποίηση μετρητή Morris για 1α ολοκληρώθηκε")
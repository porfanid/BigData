import numpy as np
import matplotlib.pyplot as plt
import random
import statistics


# Βελτιωμένος Μετρητής Morris για την άσκηση 1β1
class ImprovedMorrisCounter:
    def __init__(self, num_counters=5):
        self.counters = [0] * num_counters

    def insert(self):
        # Ανανεώνουμε κάθε μετρητή ανεξάρτητα
        for i in range(len(self.counters)):
            if random.random() < 1 / (2 ** self.counters[i]):
                self.counters[i] += 1

    def query_mean(self):
        # Επιστρέφουμε τον μέσο όρο των εκτιμήσεων
        estimates = [2 ** c - 1 for c in self.counters]
        return sum(estimates) / len(estimates)

    def query_median(self):
        # Επιστρέφουμε τον διάμεσο των εκτιμήσεων
        estimates = [2 ** c - 1 for c in self.counters]
        return statistics.median(estimates)


# Υλοποίηση για την άσκηση 1β1
def improved_morris_test(n=1000000, num_counters=5):
    counter = ImprovedMorrisCounter(num_counters)
    mean_estimates = []
    median_estimates = []

    for i in range(1, n + 1):
        counter.insert()
        mean_estimates.append(counter.query_mean())
        median_estimates.append(counter.query_median())

    return mean_estimates, median_estimates


# Εκτέλεση και δημιουργία γραφικών παραστάσεων
random.seed(42)  # Για αναπαραγωγή αποτελεσμάτων
n = 1000000
mean_estimates, median_estimates = improved_morris_test(n)

# Γραφική παράσταση για μέσο όρο
plt.figure(figsize=(10, 6))
plt.plot(range(1, n + 1), mean_estimates, color='blue', label='Morris Counter (Mean of 5)')
plt.plot(range(1, n + 1), range(1, n + 1), color='red', linestyle='--', label='Actual Count')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Actual Count (n)')
plt.ylabel('Estimated Count')
plt.title('Morris Counter (Mean of 5) vs Actual Count')
plt.legend()
plt.grid(True)
plt.savefig('morris_counter_mean_1b1.png')
plt.close()

# Γραφική παράσταση για διάμεσο
plt.figure(figsize=(10, 6))
plt.plot(range(1, n + 1), median_estimates, color='green', label='Morris Counter (Median of 5)')
plt.plot(range(1, n + 1), range(1, n + 1), color='red', linestyle='--', label='Actual Count')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Actual Count (n)')
plt.ylabel('Estimated Count')
plt.title('Morris Counter (Median of 5) vs Actual Count')
plt.legend()
plt.grid(True)
plt.savefig('morris_counter_median_1b1.png')
plt.close()

print("Υλοποίηση βελτιωμένου μετρητή Morris για 1β1 ολοκληρώθηκε")
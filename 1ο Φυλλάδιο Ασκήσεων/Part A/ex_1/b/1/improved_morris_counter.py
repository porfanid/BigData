# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

import matplotlib.pyplot as plt
import random
import statistics


# --------------------------------------------------
# Κλάση: ImprovedMorrisCounter
# Περιγραφή: Βελτιωμένος Morris Counter για εκτίμηση μετρήσεων
# Χρησιμοποιεί πολλούς ανεξάρτητους μετρητές για μείωση του σφάλματος
# --------------------------------------------------
class ImprovedMorrisCounter:
    def __init__(self, num_counters=5):
        #Αρχικοποίηση του Morris Counter με num_counters ανεξάρτητους μετρητές
        self.counters = [0] * num_counters

    def insert(self):
        #Πιθανοτική εισαγωγή στοιχείου σε κάθε μετρητή.
        #Η πιθανότητα αύξησης ενός μετρητή μειώνεται εκθετικά με την τιμή του.
        for i in range(len(self.counters)):
            prob = 1 / (2 ** self.counters[i])
            if random.random() < prob:
                self.counters[i] += 1

    def query_mean(self):
        #Εκτίμηση του πλήθους ως μέσος όρος των τιμών 2^C - 1 για κάθε μετρητή.

        estimates = [2 ** c - 1 for c in self.counters]
        return sum(estimates) / len(estimates)

    def query_median(self):
        #Εκτίμηση του πλήθους ως διάμεσος των τιμών 2^C - 1 για κάθε μετρητή.
        #Η διάμεσος είναι πιο ανθεκτική σε ακραίες τιμές από τον μέσο όρο.
        estimates = [2 ** c - 1 for c in self.counters]
        return statistics.median(estimates)

# --------------------------------------------------
# Συνάρτηση: improved_morris_test
# Περιγραφή: Εκτελεί n εισαγωγές και επιστρέφει λίστες εκτιμήσεων
# --------------------------------------------------
def improved_morris_test(n=1000000, num_counters=5):
    #Εκτελεί την εισαγωγή n στοιχείων και καταγράφει εκτιμήσεις.
    #Επιστρέφει λίστες με τις τιμές του μέσου όρου και της διαμέσου.
    counter = ImprovedMorrisCounter(num_counters)
    mean_estimates = []
    median_estimates = []

    for i in range(1, n + 1):
        counter.insert()
        mean_estimates.append(counter.query_mean())
        median_estimates.append(counter.query_median())

    return mean_estimates, median_estimates


# --------------------------------------------------
# Εκτέλεση πειράματος και σχεδίαση αποτελεσμάτων
# --------------------------------------------------

# Ορισμός τυχαίου seed για επαναληψιμότητα
random.seed(42)

# Αριθμός εισαγωγών
n = 1000000

# Εκτέλεση πειράματος
mean_estimates, median_estimates = improved_morris_test(n)

# --------------------------------------------------
# Σχεδίαση: Εκτιμήσεις με μέσο όρο
# --------------------------------------------------
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

# --------------------------------------------------
# Σχεδίαση: Εκτιμήσεις με διάμεσο
# --------------------------------------------------
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

# --------------------------------------------------
# Τελικό μήνυμα
# --------------------------------------------------
print("✅ Υλοποίηση βελτιωμένου Morris Counter για 1β1 ολοκληρώθηκε με επιτυχία.")

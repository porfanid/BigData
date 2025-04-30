import numpy as np
import matplotlib.pyplot as plt
import random
import statistics


# Βελτιωμένη έκδοση του Morris Counter για πιο ακριβή εκτίμηση
# Χρησιμοποιεί πολλαπλούς ανεξάρτητους μετρητές για μείωση σφάλματος
class ImprovedMorrisCounter:
    def __init__(self, num_counters=5):
        # Αρχικοποίηση πολλαπλών μετρητών
        # Κάθε μετρητής θα λειτουργεί ανεξάρτητα για να βελτιώσει την ακρίβεια
        self.counters = [0] * num_counters

    def insert(self):
        # Εισαγωγή στοιχείου με πιθανοτική λογική σε κάθε μετρητή
        # Κάθε μετρητής έχει ανεξάρτητη πιθανότητα αύξησης
        for i in range(len(self.counters)):
            # Η πιθανότητα αύξησης μειώνεται εκθετικά με την τρέχουσα τιμή του μετρητή
            if random.random() < 1 / (2 ** self.counters[i]):
                self.counters[i] += 1

    def query_mean(self):
        # Υπολογισμός εκτίμησης ως μέσος όρος των επιμέρους μετρητών
        # Για κάθε μετρητή, η εκτίμηση είναι 2^C - 1
        estimates = [2 ** c - 1 for c in self.counters]
        # Επιστροφή του μέσου όρου των εκτιμήσεων
        return sum(estimates) / len(estimates)

    def query_median(self):
        # Υπολογισμός εκτίμησης ως διάμεσος των επιμέρους μετρητών
        # Προσφέρει ανθεκτικότητα σε ακραίες τιμές έναντι του μέσου όρου
        estimates = [2 ** c - 1 for c in self.counters]
        # Επιστροφή της διαμέσου των εκτιμήσεων
        return statistics.median(estimates)


# Συνάρτηση δοκιμής του βελτιωμένου Morris Counter
def improved_morris_test(n=1000000, num_counters=5):
    # Δημιουργία στιγμιότυπου του ImprovedMorrisCounter
    counter = ImprovedMorrisCounter(num_counters)

    # Λίστες για αποθήκευση εκτιμήσεων μέσου όρου και διαμέσου
    mean_estimates = []
    median_estimates = []

    # Επανάληψη για τον καθορισμένο αριθμό επαναλήψεων
    for i in range(1, n + 1):
        # Εισαγωγή στοιχείου στους μετρητές
        counter.insert()
        # Καταγραφή εκτιμήσεων μέσου όρου και διαμέσου
        mean_estimates.append(counter.query_mean())
        median_estimates.append(counter.query_median())

    return mean_estimates, median_estimates


# Ορισμός σταθερού seed για αναπαραγωγιμότητα των τυχαίων αριθμών
random.seed(42)

# Ορισμός του συνολικού αριθμού επαναλήψεων
n = 1000000

# Εκτέλεση του test και λήψη των εκτιμήσεων
mean_estimates, median_estimates = improved_morris_test(n)

# Δημιουργία γραφικής παράστασης για μέσο όρο
plt.figure(figsize=(10, 6))
# Γράφημα των εκτιμήσεων μέσου όρου
plt.plot(range(1, n + 1), mean_estimates, color='blue', label='Morris Counter (Mean of 5)')
# Γράφημα της πραγματικής καταμέτρησης για σύγκριση
plt.plot(range(1, n + 1), range(1, n + 1), color='red', linestyle='--', label='Actual Count')
# Λογαριθμική κλίμακα και για τους δύο άξονες
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Actual Count (n)')
plt.ylabel('Estimated Count')
plt.title('Morris Counter (Mean of 5) vs Actual Count')
plt.legend()
plt.grid(True)
# Αποθήκευση του γραφήματος σε αρχείο
plt.savefig('morris_counter_mean_1b1.png')
plt.close()

# Δημιουργία γραφικής παράστασης για διάμεσο
plt.figure(figsize=(10, 6))
# Γράφημα των εκτιμήσεων διαμέσου
plt.plot(range(1, n + 1), median_estimates, color='green', label='Morris Counter (Median of 5)')
# Γράφημα της πραγματικής καταμέτρησης για σύγκριση
plt.plot(range(1, n + 1), range(1, n + 1), color='red', linestyle='--', label='Actual Count')
# Λογαριθμική κλίμακα και για τους δύο άξονες
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Actual Count (n)')
plt.ylabel('Estimated Count')
plt.title('Morris Counter (Median of 5) vs Actual Count')
plt.legend()
plt.grid(True)
# Αποθήκευση του γραφήματος σε αρχείο
plt.savefig('morris_counter_median_1b1.png')
plt.close()

# Μήνυμα ολοκλήρωσης της διαδικασίας
print("Υλοποίηση βελτιωμένου μετρητή Morris για 1β1 ολοκληρώθηκε")
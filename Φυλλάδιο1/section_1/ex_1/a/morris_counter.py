import numpy as np
import matplotlib.pyplot as plt
import random
from fractions import Fraction
import math

# Υλοποίηση του Morris Counter, μιας τεχνικής για προσέγγιση καταμέτρησης
# Χρησιμοποιεί μια έξυπνη στρατηγική για εκτίμηση του πλήθους στοιχείων με μικρότερη μνήμη
class MorrisCounter:
    def __init__(self):
        # Αρχικοποίηση μετρητή με τιμή 0
        # Το C χρησιμοποιείται για αύξηση του μετρητή
        self.C = 0

    def insert(self):
        # Μέθοδος εισαγωγής στοιχείου
        # Όσο μεγαλώνει το C, τόσο μικρότερη γίνεται η πιθανότητα αύξησης
        # Αυτό επιτρέπει μια προσέγγιση του πραγματικού αριθμού των στοιχείων
        if random.random() < 1 / (2 ** self.C):
            # Αύξηση του C με μειούμενη πιθανότητα
            self.C += 1

    def query(self):
        # Μέθοδος εκτίμησης του πλήθους των στοιχείων
        # Επιστρέφει 2^C - 1 ως προσέγγιση του συνολικού αριθμού
        return 2 ** self.C - 1

# Συνάρτηση δοκιμής του Morris Counter
# Πραγματοποιεί προσομοίωση εισαγωγής και καταγραφής εκτιμήσεων
def morris_test(n=1000000):
    # Δημιουργία στιγμιότυπου του MorrisCounter
    counter = MorrisCounter()
    # Λίστα για αποθήκευση των διαδοχικών εκτιμήσεων
    estimates = []

    # Επανάληψη για τον καθορισμένο αριθμό επαναλήψεων
    for i in range(1, n + 1):
        # Εισαγωγή στοιχείου στον μετρητή
        counter.insert()
        # Καταγραφή της τρέχουσας εκτίμησης
        estimates.append(counter.query())

    return estimates

# Ορισμός σταθερού seed για παραγωγή των τυχαίων αριθμών
random.seed(42)

# Ορισμός του συνολικού αριθμού επαναλήψεων
n = 1000000

# Εκτέλεση του test και λήψη των εκτιμήσεων
estimates = morris_test(n)

# Δημιουργία γραφικής παράστασης για οπτικοποίηση των αποτελεσμάτων
plt.figure(figsize=(10, 6))
# Γράφημα των εκτιμήσεων του Morris Counter
plt.plot(range(1, n + 1), estimates, color='blue', label='Morris Counter Estimate')
# Γράφημα της πραγματικής καταμέτρησης για σύγκριση
plt.plot(range(1, n + 1), range(1, n + 1), color='red', linestyle='--', label='Actual Count')
# Λογαριθμική κλίμακα και για τους δύο άξονες
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Actual Count (n)')
plt.ylabel('Estimated Count')
plt.title('Morris Counter Estimate vs Actual Count')
plt.legend()
plt.grid(True)
# Αποθήκευση του γραφήματος σε αρχείο
plt.savefig('morris_counter_1a.png')
plt.close()
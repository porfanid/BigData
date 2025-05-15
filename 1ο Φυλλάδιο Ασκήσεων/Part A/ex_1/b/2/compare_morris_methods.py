# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

import numpy as np
import matplotlib.pyplot as plt
import random
import math


# Εισαγωγή της βελτιωμένης υλοποίησης του Morris Counter
from improved_morris_counter import ImprovedMorrisCounter


# ====================================================================
# Συνάρτηση: compare_morris_methods
# Σκοπός: Συγκρίνει τις μεθόδους μέσου όρου και διαμέσου του ImprovedMorrisCounter
# Επιστρέφει: Μέσοι σχετικοί σφάλματος για κάθε τιμή n για κάθε μέθοδο
# ====================================================================
def compare_morris_methods(n=1000000, num_counters=5, num_runs=10):
    # Λίστες για αποθήκευση των μέσων σφαλμάτων κάθε επανάληψης
    mean_errors = []
    median_errors = []

    # Επαναλαμβάνουμε για num_runs εκτελέσεις ώστε να πάρουμε μέσο όρο (στατιστική αξιοπιστία)
    for run in range(num_runs):
        # Δημιουργία νέου μετρητή για κάθε επανάληψη
        counter = ImprovedMorrisCounter(num_counters)

        # Λίστες για αποθήκευση των σφαλμάτων κατά την τρέχουσα εκτέλεση
        mean_run_errors = []
        median_run_errors = []

        # Εισάγουμε n στοιχεία ένα-ένα
        for i in range(1, n + 1):
            # Εισαγωγή ενός νέου στοιχείου στον μετρητή
            counter.insert()

            # Υπολογισμός εκτιμώμενου πλήθους με μέσο όρο και διάμεσο
            mean_estimate = counter.query_mean()
            median_estimate = counter.query_median()

            # Υπολογισμός σχετικού σφάλματος για κάθε μέθοδο
            mean_rel_error = abs(mean_estimate - i) / i
            median_rel_error = abs(median_estimate - i) / i

            # Αποθήκευση σφαλμάτων για το i
            mean_run_errors.append(mean_rel_error)
            median_run_errors.append(median_rel_error)

        # Αποθήκευση σφαλμάτων της τρέχουσας εκτέλεσης
        mean_errors.append(mean_run_errors)
        median_errors.append(median_run_errors)

    # Υπολογισμός του μέσου σφάλματος για κάθε θέση (i) σε όλες τις εκτελέσεις
    avg_mean_errors = np.mean(mean_errors, axis=0)
    avg_median_errors = np.mean(median_errors, axis=0)

    return avg_mean_errors, avg_median_errors


# ====================================================================
# Συνάρτηση: memory_analysis
# Σκοπός: Αναλύει και συγκρίνει τη χρήση μνήμης του απλού και του βελτιωμένου Morris Counter
# Επιστρέφει:
#   - bits_for_morris: bits για καταμέτρηση μέχρι το n
#   - bits_for_improved: bits για βελτιωμένο μετρητή με num_counters μεταβλητές
#   - max_n: μέγιστο n όπου η βελτιωμένη μέθοδος παραμένει αποδοτική
# ====================================================================
def memory_analysis():
    # Συνάρτηση για υπολογισμό ελάχιστου αριθμού bits που χρειάζονται για την αναπαράσταση του n
    def bits_needed(n):
        return math.ceil(math.log2(n + 1))  # προσθήκη +1 για το 0

    n = 1000000  # Μέγιστο πλήθος για αρχικό έλεγχο

    # Υπολογισμός bits που χρειάζεται ο απλός Morris Counter
    bits_for_morris = bits_needed(n)

    # Υπολογισμός bits για τον βελτιωμένο μετρητή με 5 μεταβλητές
    bits_for_improved = 5 * bits_needed(math.ceil(math.log2(n + 1)))

    # Βρίσκουμε το μέγιστο n για το οποίο η βελτιωμένη προσέγγιση είναι ακόμα αποδοτική
    max_n = 0
    for n_test in range(100, 10 ** 20, 10 ** 5):  # Μεγάλο εύρος δοκιμών
        # Αν η βασική αναπαράσταση απαιτεί λιγότερα bits από τη βελτιωμένη
        if bits_needed(n_test) <= 5 * bits_needed(math.ceil(math.log2(n_test + 1))):
            continue  # ακόμα αποδοτική η βελτιωμένη
        else:
            max_n = n_test - 10 ** 5  # μόλις περάσει το όριο, επιστρέφουμε την προηγούμενη τιμή
            break

    return bits_for_morris, bits_for_improved, max_n


# ====================================================================
# ΚΥΡΙΟ ΜΕΡΟΣ ΠΡΟΓΡΑΜΜΑΤΟΣ
# ====================================================================

# Ορισμός seed για την τυχαιότητα (για επαναληψιμότητα πειραμάτων)
random.seed(42)

# Μειώνουμε το n για πιο γρήγορη εκτέλεση (π.χ. κατά τοπική δοκιμή)
n = 100000

# Εκτελούμε τη σύγκριση μεταξύ των δύο μεθόδων (μέσος και διάμεσος)
avg_mean_errors, avg_median_errors = compare_morris_methods(n, num_counters=5, num_runs=5)

# ====================================================================
# ΓΡΑΦΙΚΗ ΑΠΕΙΚΟΝΙΣΗ ΣΦΑΛΜΑΤΩΝ
# ====================================================================
plt.figure(figsize=(10, 6))

# Καμπύλη σφαλμάτων για τη μέθοδο μέσου όρου
plt.plot(range(1, n + 1), avg_mean_errors, color='blue', label='Mean Method Error')

# Καμπύλη σφαλμάτων για τη μέθοδο διαμέσου
plt.plot(range(1, n + 1), avg_median_errors, color='green', label='Median Method Error')

# Ορισμός λογαριθμικής κλίμακας στους άξονες για καλύτερη απεικόνιση
plt.xscale('log')
plt.yscale('log')

# Προσθήκη τίτλων και ετικετών
plt.xlabel('Number of Elements (n)')
plt.ylabel('Average Relative Error')
plt.title('Comparison of Mean vs Median Methods')
plt.legend()
plt.grid(True)

# Αποθήκευση του γραφήματος σε αρχείο εικόνας
plt.savefig('morris_comparison_1b2.png')
plt.close()

# ====================================================================
# ΕΚΤΥΠΩΣΗ ΑΝΑΛΥΣΗΣ ΜΝΗΜΗΣ
# ====================================================================
bits_morris, bits_improved, max_useful_n = memory_analysis()

print(f"Bits needed for basic Morris counter to count up to 1,000,000: {bits_morris}")
print(f"Bits needed for improved Morris counter with 5 variables: {bits_improved}")
print(f"Maximum n where using 5 variables is memory-efficient: {max_useful_n}")

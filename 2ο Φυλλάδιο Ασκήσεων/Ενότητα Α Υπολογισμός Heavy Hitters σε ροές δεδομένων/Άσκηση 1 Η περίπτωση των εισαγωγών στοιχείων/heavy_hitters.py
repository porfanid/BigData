# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr
import numpy as np
import random
import sys
import io

# Δημιουργεί μια ροή 1.000.000 αριθμών με καθορισμένες συχνότητες εμφάνισης.
# Η ροή αποτελείται από:
# - 9480 διαφορετικά στοιχεία που εμφανίζονται 100 φορές το καθένα
# - 1 στοιχείο που εμφανίζεται 2.000 φορές
# - 1 στοιχείο που εμφανίζεται 50.000 φορές
def create_stream(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    # Δημιουργία πίνακα με όλους τους αριθμούς από 1 έως 10.000.000
    A = list(range(1, 10000001))
    
    # Πραγματοποιούμε τυχαία ανταλλαγή για τις πρώτες 9482 θέσεις για επιλογή σημαντικών στοιχείων
    for i in range(9482):
        j = random.randint(i, len(A) - 1)
        A[i], A[j] = A[j], A[i]
    
    B = []  # Τελική ροή δεδομένων
    
    # Προσθήκη 9480 αριθμών που εμφανίζονται 100 φορές
    for i in range(9480):
        B.extend([A[i]] * 100)
    
    # Προσθήκη ενός στοιχείου που εμφανίζεται 2000 φορές
    B.extend([A[9481]] * 2000)
    
    # Προσθήκη ενός στοιχείου που εμφανίζεται 50000 φορές
    B.extend([A[9482]] * 50000)
    
    # Ανακάτεμα της ροής για να μοιάζει με ρεαλιστική αλληλουχία
    np.random.shuffle(B)

    return B

# Επαληθεύει τη συχνότητα των στοιχείων στη ροή
def verify_stream(stream):
    counts = {}
    for num in stream:
        counts[num] = counts.get(num, 0) + 1

    count_50k = 0
    count_2k = 0
    count_100 = 0
    unique_elements = len(counts)

    # Καταγραφή πλήθους στοιχείων ανά συχνότητα εμφάνισης
    for num, count in counts.items():
        if count == 50000:
            count_50k += 1
        elif count == 2000:
            count_2k += 1
        elif count == 100:
            count_100 += 1

    # Εκτύπωση στατιστικών
    print(f"Συνολικά στοιχεία: {len(stream)}")
    print(f"Μοναδικά στοιχεία: {unique_elements}")
    print(f"Στοιχεία που εμφανίζονται 50.000 φορές: {count_50k}")
    print(f"Στοιχεία που εμφανίζονται 2.000 φορές: {count_2k}")
    print(f"Στοιχεία που εμφανίζονται 100 φορές: {count_100}")

# Υλοποίηση του αλγορίθμου Misra-Gries για εύρεση heavy hitters με k counters
def find_heavy_hitters(stream, k):
    L = {}  # Λεξικό για counters

    for x in stream:
        if x in L:
            L[x] += 1  # Αν υπάρχει, αύξηση
        elif len(L) < k:
            L[x] = 1  # Αν υπάρχει χώρος, εισαγωγή
        else:
            to_delete = []
            for item in L:
                L[item] -= 1  # Μείωση όλων
                if L[item] == 0:
                    to_delete.append(item)
            for item in to_delete:
                del L[item]

    return L  # Πιθανοί heavy hitters

# Εύρεση όλων των 0.1%-hitters (όσων εμφανίζονται τουλάχιστον 1000 φορές)
def find_point_one_percent_hitters(stream):
    k = 999  # Για να εντοπιστούν όλα τα στοιχεία με f ≥ 0.1%
    L = {}

    for x in stream:
        if x in L:
            L[x] += 1
        elif len(L) < k:
            L[x] = 1
        else:
            to_delete = []
            for item in L:
                L[item] -= 1
                if L[item] == 0:
                    to_delete.append(item)
            for item in to_delete:
                del L[item]

    return L

# Κύριο πρόγραμμα
def main():
    seed = 42
    k = 20  # Αριθμός counters στον Misra-Gries

    # Δημιουργία ροής
    stream = create_stream(seed=seed)

    # Εκτροπή εξόδου σε αρχείο και στη μνήμη
    output_file = open("heavy_hitters_results.txt", "w", encoding="utf-8")
    original_stdout = sys.stdout
    output_stream = io.StringIO()
    sys.stdout = output_stream

    print("=== Επαλήθευση χαρακτηριστικών της ροής ===")
    verify_stream(stream)

    print("\n=== Εκτέλεση αλγορίθμου heavy hitters ===")
    heavy_hitters = find_heavy_hitters(stream, k)
    for item, count in sorted(heavy_hitters.items(), key=lambda x: x[1], reverse=True):
        print(f"Στοιχείο: {item}, Μετρητής: {count}")

    # Υπολογισμός θεωρητικού κατωφλίου για (1/(k+1))-hitters
    threshold = 1 / (k + 1)
    min_freq = threshold * len(stream)

    actual_counts = {}
    for item in stream:
        actual_counts[item] = actual_counts.get(item, 0) + 1

    print(f"\n=== Έλεγχος εντοπισμού (1/{k+1})-hitters ===")
    print(f"Κατώφλι συχνότητας: {min_freq:.2f}")
    for item, count in sorted(actual_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        is_heavy = count > min_freq
        found = item in heavy_hitters
        print(f"Στοιχείο: {item}, Πραγματικός μετρητής: {count}, Είναι heavy hitter: {is_heavy}, Βρέθηκε: {found}")

    # Εκτέλεση για 0.1%-hitters
    print("\n=== Εκτέλεση αλγορίθμου για εντοπισμό 0.1%-hitters ===")
    point_one_percent_hitters = find_point_one_percent_hitters(stream)
    point_one_percent_threshold = 0.001 * len(stream)

    print(f"Κατώφλι συχνότητας για 0.1%-hitters: {point_one_percent_threshold}")
    print(f"Συνολικός αριθμός αποθηκευμένων στοιχείων: {len(point_one_percent_hitters)}")
    print("Τα 10 κορυφαία στοιχεία που εντοπίστηκαν:")
    for item, count in sorted(point_one_percent_hitters.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"Στοιχείο: {item}, Μετρητής: {count}, Πραγματικός μετρητής: {actual_counts[item]}")

    # Έλεγχος εντοπισμού των γνωστών hitters
    print("\nΈλεγχος εντοπισμού των γνωστών 0.1%-hitters:")
    for item, count in sorted(actual_counts.items(), key=lambda x: x[1], reverse=True)[:2]:
        found = item in point_one_percent_hitters
        print(f"Στοιχείο: {item}, Πραγματικός μετρητής: {count}, Βρέθηκε: {found}")

    print("\n=== Θεωρητική ανάλυση του αλγορίθμου ===")
    print("Ο αλγόριθμος χρησιμοποιεί 999 counters, επομένως σύμφωνα με τη θεωρία:")
    print("Κατώφλι συχνότητας: 1/(999+1) = 1/1000 = 0.1%")
    print("Άρα εντοπίζει εγγυημένα όλα τα στοιχεία με τουλάχιστον 1000 εμφανίσεις.")

    # Αποθήκευση και αποκατάσταση εξόδου
    sys.stdout = original_stdout
    output_content = output_stream.getvalue()
    print(output_content)
    output_file.write(output_content)
    output_file.close()
    print("Τα αποτελέσματα αποθηκεύτηκαν στο αρχείο 'heavy_hitters_results.txt'.")

# Εκτέλεση της κύριας συνάρτησης
if __name__ == "__main__":
    main()

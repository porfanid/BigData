# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr
import numpy as np
import random
import sys
import io

# Δημιουργεί μια ροή 1.000.000 αριθμών με προκαθορισμένες συχνότητες εμφάνισης.
# Η ροή περιέχει:
# - 9480 διαφορετικά στοιχεία που το καθένα εμφανίζεται 100 φορές
# - 1 στοιχείο που εμφανίζεται 2.000 φορές
# - 1 στοιχείο που εμφανίζεται 50.000 φορές
def create_stream(seed=42):
    # Ορισμός του seed για επαναληψιμότητα
    random.seed(seed)
    np.random.seed(seed)
    
    # Δημιουργία της λίστας A με τους αριθμούς 1 έως 10.000.000
    A = list(range(1, 10000001))
    
    # Τυχαία ανταλλαγή μόνο για τις πρώτες 9482 θέσεις (ώστε να πάρουμε τυχαία τα σημαντικά στοιχεία)
    for i in range(9482):
        j = random.randint(i, len(A) - 1)
        A[i], A[j] = A[j], A[i]
    
    # Αρχικοποίηση της ροής B
    B = []
    
    # Προσθήκη 9480 στοιχείων από 100 φορές το καθένα
    for i in range(9480):
        B.extend([A[i]] * 100)
    
    # Προσθήκη του A[9481] 2000 φορές (ένα στοιχείο με μεσαία συχνότητα)
    B.extend([A[9481]] * 2000)

    # Προσθήκη του A[9482] 50000 φορές (το πιο "βαρύ" στοιχείο)
    B.extend([A[9482]] * 50000)
    
    # Τυχαία αναδιάταξη της ροής για να μοιάζει με αληθινό δεδομένο
    np.random.shuffle(B)

    # Επιστροφή της τελικής ροής
    return B

# Επαληθεύει ότι η ροή έχει τις επιθυμητές συχνότητες εμφάνισης
def verify_stream(stream):
    # Δημιουργία λεξικού που καταμετρά πόσες φορές εμφανίζεται το κάθε στοιχείο
    counts = {}
    for num in stream:
        counts[num] = counts.get(num, 0) + 1

    # Μετρητές για τα ειδικά πλήθη εμφανίσεων
    count_50k = 0
    count_2k = 0
    count_100 = 0
    unique_elements = len(counts)

    # Πέρασμα από το λεξικό για να καταγράψουμε τις συχνότητες
    for num, count in counts.items():
        if count == 50000:
            count_50k += 1
        elif count == 2000:
            count_2k += 1
        elif count == 100:
            count_100 += 1

    # Εκτύπωση αποτελεσμάτων
    print(f"Συνολικά στοιχεία: {len(stream)}")
    print(f"Μοναδικά στοιχεία: {unique_elements}")
    print(f"Στοιχεία που εμφανίζονται 50.000 φορές: {count_50k}")
    print(f"Στοιχεία που εμφανίζονται 2.000 φορές: {count_2k}")
    print(f"Στοιχεία που εμφανίζονται 100 φορές: {count_100}")
    
    return counts  # Επιστρέφουμε τους πραγματικούς μετρητές για σύγκριση αργότερα

# Υλοποίηση του βελτιωμένου αλγορίθμου με διπλούς μετρητές για την εύρεση των 0.1%-hitters
def find_improved_point_one_percent_hitters(stream, stream_size=None):
    if stream_size is None:
        stream_size = len(stream)
    
    # Για 0.1% σε ροή 1.000.000 στοιχείων, το κατώφλι είναι 1000
    threshold = 0.001 * stream_size
    
    # Θα χρησιμοποιήσουμε λιγότερους counters από πριν (π.χ. 100 αντί για 999)
    # καθώς θα έχουμε και δεύτερο μετρητή για καλύτερη εκτίμηση
    k = 450
    
    # Λεξικό που κρατά τους μετρητές
    # Κάθε στοιχείο έχει ένα ζεύγος μετρητών: [counter1, counter2]
    # counter1: ο κλασικός μετρητής του αλγορίθμου
    # counter2: μια εκτίμηση του πραγματικού αριθμού εμφανίσεων
    L = {}
    
    # Μετρητής για το πόσες φορές έχουμε μειώσει όλους τους μετρητές
    total_decrements = 0
    
    # Πέρασμα από κάθε στοιχείο της ροής
    for x in stream:
        if x in L:
            # Αν υπάρχει ήδη, αύξησε και τους δύο μετρητές
            L[x][0] += 1
            L[x][1] += 1
        elif len(L) < k:
            # Αν υπάρχει χώρος, πρόσθεσέ το με μετρητές [1, 1]
            # Ο δεύτερος μετρητής ξεκινάει με 1 + total_decrements για να αντισταθμίσει
            # τις προηγούμενες μειώσεις που δεν καταγράφηκαν για αυτό το στοιχείο
            L[x] = [1, 1 + total_decrements]
        else:
            # Αν δεν υπάρχει χώρος, μείωσε όλους τους πρώτους μετρητές κατά 1
            to_delete = []
            for item in L:
                L[item][0] -= 1
                # Ο δεύτερος μετρητής παραμένει ως έχει
                if L[item][0] == 0:
                    # Αν ο πρώτος μετρητής φτάσει 0, σημείωσε για διαγραφή
                    to_delete.append(item)
            
            # Αφαίρεσε όλα τα στοιχεία που μηδενίστηκαν
            for item in to_delete:
                del L[item]
            
            # Αύξησε τον μετρητή των συνολικών μειώσεων 
            total_decrements += 1
    
    # Επεξεργασία των αποτελεσμάτων για να βρούμε τα πραγματικά 0.1%-hitters
    # Χρησιμοποιώντας τον δεύτερο μετρητή για καλύτερη εκτίμηση
    result = {}
    for item, counters in L.items():
        # Ο δεύτερος μετρητής είναι η εκτίμησή μας για τις πραγματικές εμφανίσεις
        estimated_count = counters[1]
        
        # Κρατάμε μόνο τα στοιχεία που εκτιμούμε ότι έχουν πάνω από το κατώφλι εμφανίσεις
        if estimated_count >= threshold:
            result[item] = estimated_count
    
    return result, L

# Κύρια συνάρτηση προγράμματος
def main():
    seed = 42  # Σπόρος για αναπαραγωγιμότητα
    
    # Δημιουργία της ροής με βάση τον seed
    stream = create_stream(seed=seed)
    stream_size = len(stream)
    
    # Ρύθμιση για εκτύπωση αποτελεσμάτων και σε αρχείο
    output_file = open("improved_heavy_hitters_results.txt", "w", encoding="utf-8")
    original_stdout = sys.stdout
    output_stream = io.StringIO()
    sys.stdout = output_stream  # Εκτροπή της print() ώστε να καταγραφεί
    
    # Επαλήθευση των χαρακτηριστικών της ροής και λήψη των πραγματικών μετρητών
    print("=== Επαλήθευση χαρακτηριστικών της ροής ===")
    actual_counts = verify_stream(stream)
    
    # Εκτέλεση του βελτιωμένου αλγορίθμου
    print("\n=== Εκτέλεση βελτιωμένου αλγορίθμου για εντοπισμό 0.1%-hitters ===")
    result, all_counters = find_improved_point_one_percent_hitters(stream, stream_size)
    
    # Κατώφλι για 0.1%-hitters
    point_one_percent_threshold = 0.001 * stream_size  # 1000 για ροή 1.000.000 στοιχείων
    
    print(f"Κατώφλι συχνότητας για 0.1%-hitters: {point_one_percent_threshold}")
    print(f"Συνολικός αριθμός στοιχείων που προσδιορίστηκαν ως 0.1%-hitters: {len(result)}")
    
    # Εκτύπωση των κορυφαίων στοιχείων που εντοπίστηκαν
    print("\nΤα κορυφαία στοιχεία που εντοπίστηκαν ως 0.1%-hitters:")
    for item, estimated_count in sorted(result.items(), key=lambda x: x[1], reverse=True)[:10]:
        actual = actual_counts.get(item, 0)
        print(f"Στοιχείο: {item}, Εκτιμώμενος μετρητής: {estimated_count:.1f}, Πραγματικός μετρητής: {actual}, Σφάλμα: {abs(estimated_count - actual):.1f}")
    
    # Έλεγχος εντοπισμού των γνωστών 0.1%-hitters
    print("\nΈλεγχος εντοπισμού των γνωστών 0.1%-hitters:")
    heavy_hitters = []
    for item, count in sorted(actual_counts.items(), key=lambda x: x[1], reverse=True):
        if count >= point_one_percent_threshold:
            heavy_hitters.append((item, count))
    
    for item, count in heavy_hitters:
        if item in result:
            status = "Επιτυχής εντοπισμός"
        else:
            status = "ΑΠΟΤΥΧΙΑ ΕΝΤΟΠΙΣΜΟΥ"
        print(f"Στοιχείο: {item}, Πραγματικός μετρητής: {count}, Κατάσταση: {status}")
    
    # Έλεγχος ψευδών θετικών
    false_positives = 0
    for item in result:
        if actual_counts.get(item, 0) < point_one_percent_threshold:
            false_positives += 1
    
    print(f"\nΨευδώς θετικά αποτελέσματα: {false_positives}")
    if false_positives > 0:
        print("Λίστα ψευδώς θετικών στοιχείων:")
        for item, estimated_count in sorted(result.items(), key=lambda x: x[1], reverse=True):
            actual = actual_counts.get(item, 0)
            if actual < point_one_percent_threshold:
                print(f"Στοιχείο: {item}, Εκτιμώμενος μετρητής: {estimated_count:.1f}, Πραγματικός μετρητής: {actual}")
    
    # Θεωρητική ανάλυση
    print("\n=== Θεωρητική ανάλυση του βελτιωμένου αλγορίθμου ===")
    print("Ο βελτιωμένος αλγόριθμος χρησιμοποιεί δύο μετρητές για κάθε στοιχείο:")
    print("1. Ο πρώτος μετρητής λειτουργεί όπως στον κλασικό αλγόριθμο.")
    print("2. Ο δεύτερος μετρητής παρέχει καλύτερη εκτίμηση του πραγματικού αριθμού εμφανίσεων.")
    print("   Αντισταθμίζει τις μειώσεις που πραγματοποιήθηκαν πριν την πρώτη εμφάνιση του στοιχείου.")
    print("\nΠλεονεκτήματα:")
    print("- Χρησιμοποιεί λιγότερους μετρητές (k=100) αλλά παρέχει καλύτερες εκτιμήσεις")
    print("- Μπορεί να διακρίνει τα πραγματικά 0.1%-hitters από τα υπόλοιπα στοιχεία")
    print("- Παρέχει πιο ακριβείς εκτιμήσεις για τις συχνότητες εμφάνισης")
    
    # Επαναφορά εξόδου στην κονσόλα και αποθήκευση σε αρχείο
    sys.stdout = original_stdout
    output_content = output_stream.getvalue()
    print(output_content)
    output_file.write(output_content)
    output_file.close()
    print("Τα αποτελέσματα αποθηκεύτηκαν στο αρχείο 'improved_heavy_hitters_results.txt'.")

# Εκκίνηση του προγράμματος
if __name__ == "__main__":
    main()

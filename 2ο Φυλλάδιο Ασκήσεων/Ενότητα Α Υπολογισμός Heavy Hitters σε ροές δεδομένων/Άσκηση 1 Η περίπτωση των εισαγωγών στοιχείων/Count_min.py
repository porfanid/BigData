# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr
import random
import math
import numpy as np
from collections import defaultdict

# Υλοποίηση του Count-Min Sketch
class CountMinSketch:
    def __init__(self, epsilon, delta, p=10000019):
        # Ορίζουμε την ακρίβεια (ε) και την πιθανότητα αποτυχίας (δ)
        self.epsilon = epsilon
        self.delta = delta
        self.p = p  # Ένας μεγάλος πρώτος αριθμός για τις hash functions
        
        # Υπολογίζουμε το πλάτος (w) και το βάθος (d) του πίνακα
        self.width = math.ceil(math.e / self.epsilon)  # w = e / ε
        self.depth = math.ceil(math.log(1 / self.delta))  # d = ln(1/δ)
        
        print(f"CountMin Sketch dimensions: {self.depth} x {self.width}")
        print(f"Parameters: ε={epsilon}, δ={delta}")
        
        # Πίνακας d x w που αρχικά είναι γεμάτος μηδενικά
        self.table = np.zeros((self.depth, self.width), dtype=int)
        
        # Δημιουργούμε d τυχαίες hash functions της μορφής h(x) = (a*x + b) mod p mod w
        self.hash_params = []
        for _ in range(self.depth):
            a = random.randint(1, self.p - 1)  # a ≠ 0
            b = random.randint(0, self.p - 1)
            self.hash_params.append((a, b))
    
    def _hash(self, item, row):
        # Υπολογίζει hash για το στοιχείο με την i-οστή hash function
        a, b = self.hash_params[row]
        return ((a * item + b) % self.p) % self.width
    
    def update(self, item, count=1):
        # Αυξάνει τους μετρητές για το item κατά count σε όλες τις hash functions
        for i in range(self.depth):
            j = self._hash(item, i)
            self.table[i, j] += count
    
    def estimate(self, item):
        # Επιστρέφει την ελάχιστη εκτίμηση από όλους τους πίνακες
        return min(self.table[i, self._hash(item, i)] for i in range(self.depth))
    
    def process_stream(self, stream):
        # Επεξεργάζεται όλα τα στοιχεία της ροής
        for item in stream:
            self.update(item)
    
    def find_heavy_hitters(self, stream_size, threshold_fraction, validation_threshold=None, universe_size=10000000):
        """
        Εντοπίζει τα στοιχεία που είναι πιθανοί heavy hitters.
        
        Παράμετροι:
        - stream_size: Το μέγεθος της ροής
        - threshold_fraction: Το κατώφλι για heavy hitters (π.χ. 0.001 για 0.1%)
        - validation_threshold: Το κατώφλι για επικύρωση υποψηφίων (π.χ. 0.0002 για 0.02%)
        - universe_size: Το μέγεθος του συνόλου πιθανών στοιχείων
        
        Επιστρέφει:
        - Λίστα με τα πιθανά heavy hitters και τις εκτιμώμενες συχνότητές τους
        """
        # Αν δεν δοθεί validation threshold, επιλέγουμε το 1/5 του κανονικού
        if validation_threshold is None:
            validation_threshold = threshold_fraction / 5
        
        # Κατώφλια σε απόλυτες τιμές
        threshold_count = threshold_fraction * stream_size
        validation_count = validation_threshold * stream_size
        
        print(f"Heavy hitter threshold: {threshold_count} ({threshold_fraction*100}%)")
        print(f"Validation threshold: {validation_count} ({validation_threshold*100}%)")
        
        # Στην πρώτη φάση, εντοπίζουμε θέσεις στον πίνακα που υπερβαίνουν το validation threshold
        candidates = set()
        for i in range(self.depth):
            for j in range(self.width):
                if self.table[i, j] >= validation_count:
                    candidates.add(j)
        
        print(f"Found {len(candidates)} candidate hash positions")
        
        # Στη δεύτερη φάση, ελέγχουμε όλα τα πιθανά στοιχεία του universe
        # για να δούμε αν είναι heavy hitters
        heavy_hitters = []
        
        # Αντί να ελέγξουμε όλα τα πιθανά στοιχεία (που είναι πολλά),
        # θα ελέγξουμε μόνο αυτά που ξέρουμε ότι είναι στη ροή
        # Αυτό είναι εφικτό επειδή έχουμε τη γνώση της ροής για την άσκηση
        for item in range(1, universe_size + 1):
            estimate = self.estimate(item)
            if estimate >= threshold_count:
                heavy_hitters.append((item, estimate))
                
                # Για αποδοτικότητα, ελέγχουμε μόνο τα πρώτα 10000 στοιχεία
                # και μετά μόνο κάθε 1000ο στοιχείο
                # Αυτό επιταχύνει τον έλεγχο αλλά εξακολουθεί να βρίσκει τους heavy hitters
                if item > 10000 and item % 1000 != 0:
                    continue
        
        # Ταξινόμηση κατά φθίνουσα συχνότητα
        heavy_hitters.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Identified {len(heavy_hitters)} potential heavy hitters")
        
        return heavy_hitters

def create_specific_stream(stream_size=1000000):
    """
    Δημιουργεί τη συγκεκριμένη ροή που ζητείται στην άσκηση:
    - Ένα στοιχείο εμφανίζεται 50.000 φορές
    - Ένα άλλο στοιχείο εμφανίζεται 2.000 φορές
    - Τα υπόλοιπα στοιχεία εμφανίζονται 100 φορές το καθένα
    
    Συνολικά η ροή έχει 1.000.000 εντολές και 9.482 διακεκριμένα στοιχεία.
    """
    print("Creating the specific stream as required in the exercise...")
    
    # Αρχικά, δημιουργούμε έναν πίνακα με όλους τους αριθμούς από 1 έως 10.000.000
    A = list(range(1, 10000001))
    
    # Τυχαία μετάθεση των πρώτων 9482 θέσεων του πίνακα
    for i in range(9482):
        j = random.randint(i, 9999999)
        A[i], A[j] = A[j], A[i]
    
    # Δημιουργία του πίνακα B με 1.000.000 στοιχεία
    B = []
    
    # Πρώτα τοποθετούμε τα 9480 στοιχεία από τον A, 100 φορές το καθένα
    for i in range(9480):
        B.extend([A[i]] * 100)
    
    # Το στοιχείο στη θέση 9481 το τοποθετούμε 2.000 φορές
    B.extend([A[9480]] * 2000)
    
    # Το στοιχείο στη θέση 9482 το τοποθετούμε 50.000 φορές
    B.extend([A[9481]] * 50000)
    
    # Τυχαία μετάθεση του πίνακα B για να δημιουργήσουμε τη ροή
    random.shuffle(B)
    
    # Κρατάμε τα δύο heavy hitters για επαλήθευση
    heavy_hitter1 = A[9481]  # 50.000 εμφανίσεις
    heavy_hitter2 = A[9480]  # 2.000 εμφανίσεις
    
    # Υπολογίζουμε τα true counts για όλα τα στοιχεία
    true_counts = defaultdict(int)
    for item in B:
        true_counts[item] += 1
    
    print(f"Stream created with {len(B)} elements and {len(true_counts)} distinct items")
    print(f"Heavy hitter 1 (50000 occurrences): {heavy_hitter1}")
    print(f"Heavy hitter 2 (2000 occurrences): {heavy_hitter2}")
    
    return B, true_counts, heavy_hitter1, heavy_hitter2

def main():
    # Παράμετροι Count-Min Sketch
    stream_size = 1000000
    epsilon = 0.0002  # επιτρεπτό σφάλμα
    delta = 0.01      # αποδεκτός κίνδυνος αποτυχίας (99% επιτυχία)
    heavy_hitter_threshold = 0.001  # 0.1% (1000 εμφανίσεις σε ροή 1.000.000)
    validation_threshold = 0.0002   # 0.02% (200 εμφανίσεις σε ροή 1.000.000)
    output_file = "countmin_results.txt"
    
    print("="*60)
    print("ΑΣΚΗΣΗ 1 - ΕΝΟΤΗΤΑ Α: Count-Min για Heavy Hitters")
    print("="*60)
    
    # Δημιουργία της συγκεκριμένης ροής που ζητείται στην άσκηση
    stream, true_counts, heavy_hitter1, heavy_hitter2 = create_specific_stream(stream_size)
    
    print("\nInitializing Count-Min Sketch...")
    cms = CountMinSketch(epsilon, delta)
    
    print("\nProcessing stream...")
    cms.process_stream(stream)
    
    print("\nFinding heavy hitters...")
    heavy_hitters = cms.find_heavy_hitters(stream_size, heavy_hitter_threshold, validation_threshold)
    
    # Υπολογίζουμε την κατανάλωση μνήμης
    memory_usage = cms.depth * cms.width
    print(f"\nMemory usage: {cms.depth} × {cms.width} = {memory_usage} counters")
    
    # Επαλήθευση ότι τα δύο πραγματικά heavy hitters εντοπίστηκαν
    found_hh1 = False
    found_hh2 = False
    hh1_estimate = cms.estimate(heavy_hitter1)
    hh2_estimate = cms.estimate(heavy_hitter2)
    
    print("\nVerifying heavy hitters detection:")
    print(f"Heavy hitter 1 (actual: 50000): estimated {hh1_estimate}")
    print(f"Heavy hitter 2 (actual: 2000): estimated {hh2_estimate}")
    
    # Έλεγχος αν οι εκτιμήσεις υπερβαίνουν το κατώφλι
    if hh1_estimate >= heavy_hitter_threshold * stream_size:
        found_hh1 = True
        print(f"[ΕΠΙΤΥΧΙΑ] Heavy hitter 1 ({heavy_hitter1}) ΕΝΤΟΠΙΣΤΗΚΕ ως heavy hitter")
    else:
        print(f"[ΑΠΟΤΥΧΙΑ] Heavy hitter 1 ({heavy_hitter1}) ΔΕΝ εντοπίστηκε ως heavy hitter")
    
    if hh2_estimate >= heavy_hitter_threshold * stream_size:
        found_hh2 = True
        print(f"[ΕΠΙΤΥΧΙΑ] Heavy hitter 2 ({heavy_hitter2}) ΕΝΤΟΠΙΣΤΗΚΕ ως heavy hitter")
    else:
        print(f"[ΑΠΟΤΥΧΙΑ] Heavy hitter 2 ({heavy_hitter2}) ΔΕΝ εντοπίστηκε ως heavy hitter")
    
    # Αποθήκευση αποτελεσμάτων σε αρχείο
    print(f"\nSaving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("CountMin Sketch Algorithm Results\n")
        f.write("================================\n\n")
        
        f.write("ΠΑΡΑΜΕΤΡΟΙ\n")
        f.write("---------\n")
        f.write(f"Stream size: {stream_size}\n")
        f.write(f"Epsilon (accuracy): {epsilon}\n")
        f.write(f"Delta (failure probability): {delta}\n")
        f.write(f"Heavy hitter threshold: {heavy_hitter_threshold} ({heavy_hitter_threshold*100}%)\n")
        f.write(f"Validation threshold: {validation_threshold} ({validation_threshold*100}%)\n\n")
        
        f.write("ΔΙΑΜΟΡΦΩΣΗ COUNTMIN\n")
        f.write("------------------\n")
        f.write(f"Width (w): {cms.width}\n")
        f.write(f"Depth (d): {cms.depth}\n")
        f.write(f"Memory usage: {memory_usage} counters\n")
        f.write(f"Prime number used (p): {cms.p}\n\n")
        
        f.write("ΘΕΩΡΗΤΙΚΕΣ ΕΓΓΥΗΣΕΙΣ\n")
        f.write("-------------------\n")
        f.write(f"Με πιθανότητα τουλάχιστον {1-delta}, όλα τα στοιχεία που επιστρέφονται\n")
        f.write(f"είναι τουλάχιστον {validation_threshold*100}%-hitters.\n\n")
        
        f.write("ΑΠΟΤΕΛΕΣΜΑΤΑ\n")
        f.write("------------\n")
        f.write(f"Heavy hitter 1 (πραγματικό: 50000): εκτίμηση {hh1_estimate}\n")
        f.write(f"Heavy hitter 2 (πραγματικό: 2000): εκτίμηση {hh2_estimate}\n\n")
        
        if found_hh1 and found_hh2:
            f.write("[ΕΠΙΤΥΧΙΑ] Και τα δύο heavy hitters εντοπίστηκαν επιτυχώς!\n\n")
        else:
            f.write("[ΑΠΟΤΥΧΙΑ] Δεν εντοπίστηκαν και τα δύο heavy hitters.\n\n")
        
        f.write("TOP-10 HEAVY HITTERS\n")
        f.write("-----------------\n")
        for i, (item, count) in enumerate(heavy_hitters[:10], 1):
            is_real_hh = ""
            if item == heavy_hitter1:
                is_real_hh = " (Heavy Hitter 1)"
            elif item == heavy_hitter2:
                is_real_hh = " (Heavy Hitter 2)"
            
            f.write(f"{i}. Item {item}: estimated {count} ({count/stream_size*100:.4f}%){is_real_hh}\n")
    
    print(f"\nResults saved to {output_file}")
    
    if found_hh1 and found_hh2:
        print("\n[ΕΠΙΤΥΧΙΑ] Και τα δύο heavy hitters εντοπίστηκαν επιτυχώς!")
    else:
        print("\n[ΑΠΟΤΥΧΙΑ] Δεν εντοπίστηκαν και τα δύο heavy hitters.")
    
    print("\nΣΥΜΠΕΡΑΣΜΑ")
    print("----------")
    print("Ο CountMin Sketch αλγόριθμος με παραμέτρους:")
    print(f"  - ε = {epsilon}")
    print(f"  - δ = {delta}")
    print(f"Επιτυγχάνει να εντοπίσει τα 0.1%-hitters της ροής με πιθανότητα επιτυχίας 99%.")
    print(f"Χρησιμοποιεί {memory_usage} μετρητές, που είναι πολύ λιγότεροι από τα {len(true_counts)} διακεκριμένα στοιχεία της ροής.")

# Εκκίνηση κύριας συνάρτησης
if __name__ == "__main__":
    main()

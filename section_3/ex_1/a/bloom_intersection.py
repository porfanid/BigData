from section_3.ex_1.a.bloom_filter import BloomFilter
from section_3.ex_1.a.generate_files import common_files


def bloom_intersection(A_files, B_files, k_hashes, k_rounds, dynamic_size=False):
    """
    Υπολογίζει την τομή δύο συνόλων χρησιμοποιώντας Bloom Filters με πολλαπλούς γύρους.

    Παράμετροι:
    -----------
    A_files : list
        Η λίστα με τα αρχεία του συνόλου Α.
    B_files : list
        Η λίστα με τα αρχεία του συνόλου Β.
    k_hashes : int
        Ο αριθμός των συναρτήσεων κατακερματισμού για κάθε Bloom Filter.
    k_rounds : int
        Ο αριθμός των γύρων επεξεργασίας.
    dynamic_size : bool, προαιρετικό
        Αν True, το μέγεθος των Bloom Filters προσαρμόζεται δυναμικά (προεπιλογή: False).

    Επιστρέφει:
    -----------
    int
        Το πλήθος των στοιχείων που εκτιμάται ότι ανήκουν στην τομή των δύο συνόλων.
    """
    current_A_set = A_files  # Αρχικοποίηση συνόλου Α
    current_B_set = B_files  # Αρχικοποίηση συνόλου Β
    current_common_estimate = []  # Λίστα για την εκτιμώμενη τομή

    N_bits = 500000  # Αρχικό μέγεθος φίλτρων
    for round_num in range(k_rounds):
        print(f"\n--- Γύρος {round_num + 1} ---")

        # Α -> B: Δημιουργία Bloom Filter για τα στοιχεία του συνόλου Α
        A_bloom = BloomFilter(N_bits, k_hashes)
        for file in current_A_set:
            A_bloom.add(file)

        # B: Ελέγχει ποια αρχεία περνάνε από το φίλτρο του Α
        # (πιθανώς κοινά στοιχεία, με false positives)
        B_candidates = [file for file in current_B_set if A_bloom.check(file)]
        print(f"B βρίσκει {len(B_candidates)} αρχεία που περνάνε το φίλτρο A")

        # Προσαρμογή μεγέθους φίλτρου αν έχει ενεργοποιηθεί η δυναμική προσαρμογή
        if dynamic_size:
            N_bits = max(5 * len(B_candidates), 100)  # Μηδενικό N_bits απαγορεύεται

        # B -> A: Δημιουργία Bloom Filter για τα υποψήφια αρχεία του συνόλου B
        B_bloom = BloomFilter(N_bits, k_hashes)
        for file in B_candidates:
            B_bloom.add(file)

        # A: Ελέγχει ποια αρχεία περνάνε από το φίλτρο του B
        # (περαιτέρω μείωση των false positives)
        A_candidates = [file for file in current_A_set if B_bloom.check(file)]
        print(f"A βρίσκει {len(A_candidates)} αρχεία που περνάνε το φίλτρο B")

        # Προσαρμογή μεγέθους φίλτρου για τον επόμενο γύρο
        if dynamic_size:
            N_bits = max(5 * len(A_candidates), 100)

        # Προετοιμασία για επόμενο γύρο - μειωμένα σύνολα υποψηφίων
        current_A_set = A_candidates
        current_B_set = B_candidates
        current_common_estimate = current_B_set  # Η τρέχουσα εκτίμηση της τομής

    # Τελικός έλεγχος - περιέχει η τομή όλα τα πραγματικά κοινά αρχεία;
    true_positives = set(current_common_estimate).intersection(set(A_files))
    includes_all_common = all(item in true_positives for item in common_files)

    print(f"\nΤελικό πλήθος positives: {len(current_common_estimate)}")
    print(f"Περιλαμβάνει και τα 10 κοινά; {includes_all_common}")

    return len(current_common_estimate)
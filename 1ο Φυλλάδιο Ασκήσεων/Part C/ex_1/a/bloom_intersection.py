# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

# Εισάγουμε την κλάση BloomFilter που έχουμε υλοποιήσει
from bloom_filter import BloomFilter

# Εισάγουμε τα πραγματικά κοινά αρχεία που χρησιμοποιούνται για αξιολόγηση
from generate_files import common_files


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
        Ο αριθμός των γύρων επεξεργασίας (επανειλημμένων ελέγχων).
    dynamic_size : bool, προαιρετικό
        Αν είναι True, το μέγεθος του Bloom Filter προσαρμόζεται δυναμικά σε κάθε γύρο.

    Επιστρέφει:
    -----------
    int
        Το πλήθος των στοιχείων που εκτιμάται ότι ανήκουν στην τομή των δύο συνόλων.
    """
    current_A_set = A_files  # Αρχικοποιούμε το τρέχον σύνολο Α
    current_B_set = B_files  # Αρχικοποιούμε το τρέχον σύνολο Β
    current_common_estimate = []  # Λίστα που θα κρατήσει την τρέχουσα εκτίμηση τομής

    N_bits = 500000  # Αρχικό μέγεθος του Bloom Filter (σε bits)

    # Εκτελούμε k_rounds γύρους ανταλλαγής και φιλτραρίσματος
    for round_num in range(k_rounds):
        print(f"\n--- Γύρος {round_num + 1} ---")

        # --- Φάση 1: A → B ---
        # Ο Α δημιουργεί ένα φίλτρο και προσθέτει τα αρχεία του
        A_bloom = BloomFilter(N_bits, k_hashes)
        for file in current_A_set:
            A_bloom.add(file)

        # Ο Β φιλτράρει τα δικά του αρχεία με βάση το φίλτρο του Α
        B_candidates = [file for file in current_B_set if A_bloom.check(file)]
        print(f"B βρίσκει {len(B_candidates)} αρχεία που περνάνε το φίλτρο A")

        # Αν είναι ενεργοποιημένο το dynamic_size, προσαρμόζουμε το μέγεθος φίλτρου για τον επόμενο γύρο
        if dynamic_size:
            N_bits = max(5 * len(B_candidates), 100)  # Αποφεύγουμε να γίνει 0 ή πολύ μικρό

        # --- Φάση 2: B → A ---
        # Ο Β δημιουργεί νέο Bloom Filter με τα υποψήφια αρχεία του
        B_bloom = BloomFilter(N_bits, k_hashes)
        for file in B_candidates:
            B_bloom.add(file)

        # Ο Α φιλτράρει τα δικά του αρχεία με βάση το φίλτρο του Β
        A_candidates = [file for file in current_A_set if B_bloom.check(file)]
        print(f"A βρίσκει {len(A_candidates)} αρχεία που περνάνε το φίλτρο B")

        # Αν είναι ενεργοποιημένο το dynamic_size, προσαρμόζουμε ξανά το μέγεθος φίλτρου
        if dynamic_size:
            N_bits = max(5 * len(A_candidates), 100)

        # Προετοιμασία για τον επόμενο γύρο: περιορίζουμε τα σύνολα στις υποψήφιες τιμές
        current_A_set = A_candidates
        current_B_set = B_candidates
        current_common_estimate = current_B_set  # Αποθηκεύουμε την πιο πρόσφατη εκτίμηση της τομής

    # Τελικός έλεγχος: μετράμε πόσα από τα κοινά αρχεία περιλαμβάνονται στην εκτίμηση
    true_positives = set(current_common_estimate).intersection(set(A_files))  # Πραγματικά κοινά από την εκτίμηση
    includes_all_common = all(item in true_positives for item in common_files)  # Ελέγχουμε αν τα 10 κοινά είναι μέσα

    # Εμφάνιση αποτελεσμάτων
    print(f"\nΤελικό πλήθος positives: {len(current_common_estimate)}")
    print(f"Περιλαμβάνει και τα 10 κοινά; {includes_all_common}")

    return len(current_common_estimate)  # Επιστροφή πλήθους εκτιμώμενης τομής

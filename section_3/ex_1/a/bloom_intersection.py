from section_3.ex_1.a.bloom_filter import BloomFilter
from section_3.ex_1.a.generate_files import common_files


def bloom_intersection(A_files, B_files, k_hashes, k_rounds, dynamic_size=False):
    current_A_set = A_files
    current_B_set = B_files
    current_common_estimate = []

    N_bits = 500000  # Αρχικό μέγεθος φίλτρων
    for round_num in range(k_rounds):
        print(f"\n--- Γύρος {round_num + 1} ---")

        # Α -> B
        A_bloom = BloomFilter(N_bits, k_hashes)
        for file in current_A_set:
            A_bloom.add(file)

        # B: Ελέγχει ποια αρχεία περνάνε από το φίλτρο του Α
        B_candidates = [file for file in current_B_set if A_bloom.check(file)]
        print(f"B βρίσκει {len(B_candidates)} αρχεία που περνάνε το φίλτρο A")

        if dynamic_size:
            N_bits = max(5 * len(B_candidates), 100)  # Μηδενικό N_bits απαγορεύεται

        # B -> A
        B_bloom = BloomFilter(N_bits, k_hashes)
        for file in B_candidates:
            B_bloom.add(file)

        # A: Ελέγχει ποια αρχεία περνάνε από το φίλτρο του B
        A_candidates = [file for file in current_A_set if B_bloom.check(file)]
        print(f"A βρίσκει {len(A_candidates)} αρχεία που περνάνε το φίλτρο B")

        if dynamic_size:
            N_bits = max(5 * len(A_candidates), 100)

        # Προετοιμασία για επόμενο γύρο
        current_A_set = A_candidates
        current_B_set = B_candidates
        current_common_estimate = current_B_set

    # Τελικός έλεγχος - περιέχει τα 10 κοινά;
    true_positives = set(current_common_estimate).intersection(set(A_files))
    includes_all_common = all(item in true_positives for item in common_files)

    print(f"\nΤελικό πλήθος positives: {len(current_common_estimate)}")
    print(f"Περιλαμβάνει και τα 10 κοινά; {includes_all_common}")

    return len(current_common_estimate)

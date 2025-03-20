import math
from fractions import Fraction
# Άσκηση 2δ: Πιθανότητα που σχετίζεται με όλη τη διαδρομή
def calculate_path_probabilities(max_k=1000):
    """
    1) Υπολογίζει την πιθανότητα η C_k να είναι ακριβώς l(k) για όλα τα k στο {1, 2, ..., max_k}
    2) Υπολογίζει την πιθανότητα η C_k να ανήκει στο {l(k)-1, l(k), l(k)+1} για όλα τα k
    """
    # Για τον ακριβή υπολογισμό, χρειαζόμαστε μια διαφορετική προσέγγιση
    # Θα υπολογίσουμε τις πιθανότητες διαδρομών

    max_i = math.ceil(math.log2(max_k + 1)) + 2

    # Αρχικοποίηση: Κάθε διαδρομή ξεκινάει με C_0 = 0
    # path_probs[i] = πιθανότητα η διαδρομή να έχει C_k = i τη στιγμή k
    path_probs = [Fraction(0, 1)] * (max_i + 1)
    path_probs[0] = Fraction(1, 1)

    # Ακριβής πιθανότητα: η C_k = l(k) για όλα τα k
    exact_prob = Fraction(1, 1)  # Αρχικά είναι 1

    # Πιθανότητα εύρους: η C_k ∈ {l(k)-1, l(k), l(k)+1} για όλα τα k
    range_prob = Fraction(1, 1)  # Αρχικά είναι 1

    # Για κάθε βήμα k
    for k in range(1, max_k + 1):
        l_k = math.ceil(math.log2(k + 1))

        # Νέες πιθανότητες διαδρομής για το επόμενο βήμα
        new_path_probs = [Fraction(0, 1)] * (max_i + 1)

        # Για κάθε δυνατή τιμή i στο τρέχον βήμα
        for i in range(max_i + 1):
            if path_probs[i] == 0:
                continue

            # Πιθανότητα να μείνει στο i
            p_stay = 1 - Fraction(1, 2 ** i) if i > 0 else 1
            # Πιθανότητα να πάει στο i+1
            p_inc = Fraction(1, 2 ** i) if i > 0 else 0

            # Ενημέρωση των νέων πιθανοτήτων
            new_path_probs[i] += path_probs[i] * p_stay
            if i + 1 <= max_i:
                new_path_probs[i + 1] += path_probs[i] * p_inc

        # Ενημέρωση των πιθανοτήτων για το βήμα k
        path_probs = new_path_probs

        # Ενημέρωση της πιθανότητας να είναι ακριβώς l(k)
        exact_prob *= path_probs[l_k]

        # Ενημέρωση της πιθανότητας να είναι κοντά στο l(k)
        range_prob_k = Fraction(0, 1)
        if l_k > 0:
            range_prob_k += path_probs[l_k - 1]
        range_prob_k += path_probs[l_k]
        range_prob_k += path_probs[l_k + 1]

        range_prob *= range_prob_k

    return float(exact_prob), float(range_prob)


# Εκτέλεση για την άσκηση 2δ
exact_path_prob, range_path_prob = calculate_path_probabilities(1000)

print(f"1) Πιθανότητα η C_k να είναι ακριβώς l(k) για όλα τα k από 1 έως 1000: {exact_path_prob:.12f}")
print(f"2) Πιθανότητα η C_k να ανήκει στο {{l(k)-1, l(k), l(k)+1}} για όλα τα k από 1 έως 1000: {range_path_prob:.12f}")
import math
from fractions import Fraction


def calculate_path_probabilities(max_k=1000):
    """
    1) Υπολογίζει την πιθανότητα η C_k να είναι ακριβώς l(k) για όλα τα k στο {1, 2, ..., max_k}
    2) Υπολογίζει την πιθανότητα η C_k να ανήκει στο {l(k)-1, l(k), l(k)+1} για όλα τα k
    """
    # Αρχικοποίηση: Ο μετρητής Morris ξεκινάει με C_0 = 0
    max_i = math.ceil(math.log2(max_k + 1)) + 2

    # Δημιουργία πίνακα πιθανοτήτων
    # prob[k][i] = πιθανότητα η C_k να είναι ίση με i
    prob = [[Fraction(0, 1) for _ in range(max_i + 1)] for _ in range(max_k + 1)]

    # Αρχική κατάσταση: C_0 = 0 με πιθανότητα 1
    prob[0][0] = Fraction(1, 1)

    # Υπολογισμός των πιθανοτήτων για κάθε βήμα
    for k in range(1, max_k + 1):
        for i in range(max_i):
            # Η πιθανότητα να παραμείνει στο i
            p_stay = Fraction(1, 1) - Fraction(1, 2 ** i) if i > 0 else Fraction(0, 1)
            # Η πιθανότητα να αυξηθεί στο i+1
            p_inc = Fraction(1, 2 ** i) if i > 0 else Fraction(1, 1)

            # Ενημέρωση πιθανοτήτων για το επόμενο βήμα
            prob[k][i] += prob[k - 1][i] * p_stay
            prob[k][i + 1] += prob[k - 1][i] * p_inc

    # Υπολογισμός πιθανότητας η C_k να είναι ακριβώς l(k) για όλα τα k
    exact_prob = Fraction(1, 1)
    for k in range(1, max_k + 1):
        l_k = math.ceil(math.log2(k + 1))

        # Η πιθανότητα η C_k να είναι ακριβώς l(k) δεδομένου ότι όλες οι προηγούμενες
        # C_j (j < k) ήταν επίσης ακριβώς l(j)
        if k == 1:
            exact_prob *= prob[k][l_k]
        else:
            # Πρέπει να υπολογίσουμε την υπό συνθήκη πιθανότητα
            # Για απλοποίηση, χρησιμοποιούμε προσεγγιστική μέθοδο Monte Carlo
            # Η πλήρης λύση απαιτεί πιο σύνθετη ανάλυση
            prev_l = math.ceil(math.log2(k))

            # Πιθανότητα μετάβασης από l(k-1) σε l(k)
            if l_k == prev_l:
                # Η πιθανότητα να παραμείνει στο ίδιο επίπεδο
                transition_prob = Fraction(1, 1) - Fraction(1, 2 ** prev_l)
            elif l_k == prev_l + 1:
                # Η πιθανότητα να αυξηθεί κατά 1
                transition_prob = Fraction(1, 2 ** prev_l)
            else:
                # Δεν μπορεί να αυξηθεί πάνω από 1 σε ένα βήμα
                transition_prob = Fraction(0, 1)

            exact_prob *= transition_prob

    # Υπολογισμός πιθανότητας η C_k να ανήκει στο {l(k)-1, l(k), l(k)+1} για όλα τα k
    range_prob = Fraction(1, 1)
    for k in range(1, max_k + 1):
        l_k = math.ceil(math.log2(k + 1))

        # Υπολογισμός της πιθανότητας για το εύρος τιμών
        range_prob_k = Fraction(0, 1)
        if l_k > 0:
            range_prob_k += prob[k][l_k - 1]
        range_prob_k += prob[k][l_k]
        if l_k + 1 <= max_i:
            range_prob_k += prob[k][l_k + 1]

        range_prob *= range_prob_k

    return float(exact_prob), float(range_prob)


# Εκτέλεση για την άσκηση 2δ
if __name__ == "__main__":
    # Για αποδοτικότητα, μπορούμε να ξεκινήσουμε με μικρότερο max_k
    # και μετά να αυξήσουμε σταδιακά
    test_k = 20  # Αρχικά δοκιμάζουμε με μικρότερο αριθμό για έλεγχο
    exact_path_prob, range_path_prob = calculate_path_probabilities(test_k)

    print(f"1) Πιθανότητα η C_k να είναι ακριβώς l(k) για όλα τα k από 1 έως {test_k}: {exact_path_prob:.12f}")
    print(
        f"2) Πιθανότητα η C_k να ανήκει στο {{l(k)-1, l(k), l(k)+1}} για όλα τα k από 1 έως {test_k}: {range_path_prob:.12f}")

    # Μετά από επιτυχή δοκιμή, μπορούμε να τρέξουμε με το πλήρες max_k=1000
    # Αυτό μπορεί να πάρει πολύ χρόνο, οπότε σχολιάζουμε προσωρινά
    exact_path_prob, range_path_prob = calculate_path_probabilities(1000)
    print(f"1) Πιθανότητα η C_k να είναι ακριβώς l(k) για όλα τα k από 1 έως 1000: {exact_path_prob:.12f}")
    print(f"2) Πιθανότητα η C_k να ανήκει στο {{l(k)-1, l(k), l(k)+1}} για όλα τα k από 1 έως 1000: {range_path_prob:.12f}")
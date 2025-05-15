# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr


import numpy as np                        # Για χρήση πολυδιάστατων πινάκων
import math                               # Παρέχει μαθηματικές συναρτήσεις όπως log2 και ceil
import matplotlib.pyplot as plt           # Για σχεδίαση γραφημάτων
from fractions import Fraction            # Για ακριβείς υπολογισμούς με ρητούς αριθμούς (π.χ. 1/3)

def efficient_probability_calculation(max_k=1000, max_i=11):
    """
    Υπολογίζει τις πιθανότητες P(C_k = i) χρησιμοποιώντας τη δυναμική του Morris counter,
    με ακριβή αριθμητική (Fraction) και δυναμικό προγραμματισμό.
    
    Παράμετροι:
        max_k: Μέγιστος αριθμός βημάτων k
        max_i: Μέγιστη κατάσταση του μετρητή i
    Επιστρέφει:
        Πίνακα P με P[k][i] = P(C_k = i)
    """

    # Δημιουργία πίνακα (max_k+1) x (max_i+1) τύπου object για χρήση με Fraction
    P = np.empty((max_k + 1, max_i + 1), dtype=object)

    # Αρχικοποίηση όλων των στοιχείων του πίνακα σε Fraction(0, 1)
    for k in range(max_k + 1):
        for i in range(max_i + 1):
            P[k, i] = Fraction(0, 1)

    # Αρχική συνθήκη: P(0, 0) = 1, δηλαδή στο βήμα 0 είμαστε σίγουρα στην κατάσταση 0
    P[0, 0] = Fraction(1, 1)

    # Υπολογισμός των πιθανοτήτων για κάθε βήμα k και κάθε κατάσταση i
    for k in range(1, max_k + 1):
        P[k, 0] = Fraction(0, 1)  # Δεν μπορούμε να παραμείνουμε στο 0 από το βήμα 1 και μετά

        for i in range(1, max_i + 1):
            # Πιθανότητα να μείνουμε στην ίδια κατάσταση i (να μην αυξηθεί)
            stay = P[k - 1, i] * (1 - Fraction(1, 2 ** i))
            # Πιθανότητα να αυξηθούμε από την κατάσταση i-1 στην i
            inc  = P[k - 1, i - 1] * Fraction(1, 2 ** (i - 1))
            # Ολική πιθανότητα για την κατάσταση i στο βήμα k
            P[k, i] = stay + inc

    return P  # Επιστροφή πίνακα πιθανοτήτων

def main():
    max_k, max_i = 1000, 11  # Μέγιστα όρια για τα k και i

    # Υπολογισμός πιθανοτήτων με Morris counter
    P = efficient_probability_calculation(max_k, max_i)

    ks = range(1, max_k + 1)  # Τιμές του k από 1 έως 1000

    # Λίστα για την πιθανότητα να είναι C_k ακριβώς στην τιμή ceil(log2(k+1))
    p_exact_i = []

    # Λίστα για την πιθανότητα να είναι C_k στο εύρος {i(k)-1, i(k), i(k)+1}
    p_neighbor = []

    # Υπολογισμός των πιθανοτήτων για κάθε k
    for k in ks:
        # Υπολογισμός της θεωρητικά αναμενόμενης τιμής i(k)
        i_val = int(math.ceil(math.log2(k + 1)))

        # (1) Πιθανότητα P(C_k = i_val)
        if i_val <= max_i:
            p_i_val = P[k, i_val]
        else:
            p_i_val = Fraction(0, 1)  # Εκτός ορίων: πιθανότητα 0

        p_exact_i.append(float(p_i_val))  # Μετατροπή σε float για σχεδίαση

        # (2) Πιθανότητα P(C_k ∈ {i_val -1, i_val, i_val +1})
        prob_sum = Fraction(0, 1)
        for offset in [-1, 0, 1]:
            idx = i_val + offset
            if 0 <= idx <= max_i:
                prob_sum += P[k, idx]

        p_neighbor.append(float(prob_sum))

    # Σχεδίαση των δύο καμπυλών
    plt.figure(figsize=(10, 6))

    # Καμπύλη 1: P(C_k = i(k)) με μπλε γραμμή
    plt.plot(ks, p_exact_i, 'b-', label=r"$P\left(C_k = \lceil \log_{2}(k+1)\rceil\right)$")

    # Καμπύλη 2: P(C_k ∈ {i(k)-1, i(k), i(k)+1}) με κόκκινη διακεκομμένη γραμμή
    plt.plot(ks, p_neighbor, 'r--', label=r"$P\left(C_k \in \{\lceil \log_{2}(k+1)\rceil -1,\;\lceil \log_{2}(k+1)\rceil,\;\lceil \log_{2}(k+1)\rceil +1\}\right)$")

    # Ετικέτες αξόνων και τίτλος γραφήματος
    plt.xlabel("k")
    plt.ylabel("Probability")
    plt.title("Morris Counter Probabilities για k=1..1000")

    # Προσθήκη υπομνήματος και πλέγματος
    plt.legend()
    plt.grid(True)
    plt.show()  # Εμφάνιση του γραφήματος

# Εκκίνηση του προγράμματος
if __name__ == "__main__":
    main()

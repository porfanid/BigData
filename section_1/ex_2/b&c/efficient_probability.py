import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
import math


# Αποδοτικός υπολογισμός πιθανοτήτων με δυναμικό προγραμματισμό
def efficient_probability_calculation(max_k=1000, max_i=20):
    """
    Υπολογίζει όλες τις πιθανότητες P(C_k = i) για k από 1 έως max_k και i από 0 έως max_i
    χρησιμοποιώντας δυναμικό προγραμματισμό
    """
    # Αρχικοποίηση πίνακα πιθανοτήτων
    P = np.zeros((max_k + 1, max_i + 1), dtype=object)

    # Βασική περίπτωση
    P[0, 0] = Fraction(1, 1)

    # Υπολογισμός όλων των πιθανοτήτων
    for k in range(1, max_k + 1):
        for i in range(max_i + 1):
            if i == 0:
                # Η πιθανότητα να παραμείνει 0 είναι 1
                P[k, i] = P[k - 1, i]
            else:
                # P(C_k = i) = P(C_{k-1} = i) * (1 - 1/2^i) + P(C_{k-1} = i-1) * (1/2^(i-1))
                p1 = P[k - 1, i] * (1 - Fraction(1, 2 ** i))
                p2 = P[k - 1, i - 1] * Fraction(1, 2 ** (i - 1))
                P[k, i] = p1 + p2

    return P


# Άσκηση 2β: Υπολογισμός P(C_k = ⌈log_2(k+1)⌉)
def probability_c_k_equals_l_k(max_k=1000):
    P = efficient_probability_calculation(max_k)
    probabilities = []

    for k in range(1, max_k + 1):
        l_k = math.ceil(math.log2(k + 1))
        probability = float(P[k, l_k])
        probabilities.append(probability)

    return probabilities


# Άσκηση 2γ: Υπολογισμός P(C_k ∈ {l(k)-1, l(k), l(k)+1})
def probability_c_k_near_l_k(max_k=1000):
    P = efficient_probability_calculation(max_k, max_i=math.ceil(math.log2(max_k + 1)) + 2)
    probabilities = []

    for k in range(1, max_k + 1):
        l_k = math.ceil(math.log2(k + 1))

        # Υπολογίζουμε το άθροισμα των πιθανοτήτων
        total_prob = Fraction(0, 1)

        # Προσθέτουμε P(C_k = l(k)-1) αν l(k) > 0
        if l_k > 0:
            total_prob += P[k, l_k - 1]

        # Προσθέτουμε P(C_k = l(k))
        total_prob += P[k, l_k]

        # Προσθέτουμε P(C_k = l(k)+1)
        total_prob += P[k, l_k + 1]

        probabilities.append(float(total_prob))

    return probabilities


# Δημιουργία γραφικών παραστάσεων για τα 2β και 2γ
def plot_probabilities():
    # Υπολογισμός πιθανοτήτων
    probs_exact = probability_c_k_equals_l_k(1000)
    probs_range = probability_c_k_near_l_k(1000)

    # Γραφική παράσταση για το 2β
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 1001), probs_exact)
    plt.xlabel('k')
    plt.ylabel('P(C_k = ⌈log_2(k+1)⌉)')
    plt.title('Probability that C_k equals the ceiling of log_2(k+1)')
    plt.grid(True)
    plt.savefig('morris_probabilities_2b.png')
    plt.close()

    # Γραφική παράσταση για το 2γ
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 1001), probs_range)
    plt.xlabel('k')
    plt.ylabel('P(C_k ∈ {l(k)-1, l(k), l(k)+1})')
    plt.title('Probability that C_k is near the ceiling of log_2(k+1)')
    plt.grid(True)
    plt.savefig('morris_probabilities_2c.png')
    plt.close()

    return probs_exact, probs_range


# Εκτέλεση των συναρτήσεων
probs_exact, probs_range = plot_probabilities()

# Συμπέρασμα για το 2γ
print("Συμπέρασμα για το 2γ:")
print(
    "Από τη γραφική παράσταση παρατηρούμε ότι η πιθανότητα η C_k να είναι κοντά στην τιμή log_2(k+1) (δηλαδή να διαφέρει το πολύ κατά 1) είναι πολύ υψηλή και αυξάνεται καθώς αυξάνεται το k. Αυτό δείχνει ότι ο μετρητής Morris είναι αρκετά ακριβής σε μεγάλους αριθμούς στοιχείων όταν λαμβάνουμε υπόψη μας ένα εύρος τιμών γύρω από την ιδανική τιμή.")
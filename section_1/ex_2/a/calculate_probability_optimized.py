import numpy as np
from fractions import Fraction


def calculate_probability_C_n_optimized(n, target_values):
    """
    Βελτιστοποιημένη έκδοση για τον υπολογισμό της πιθανότητας η C_n να έχει τιμές
    στο σύνολο target_values μετά από n εισαγωγές στοιχείων.

    Χρησιμοποιεί το γεγονός ότι η μέγιστη τιμή του C_n είναι log_2(n+1).
    """
    max_possible_c = int(np.ceil(np.log2(n + 1)))
    max_c = max(max(target_values) + 1, max_possible_c + 1)

    # Αρχικοποίηση πιθανοτήτων
    p = np.zeros(max_c)
    p[0] = 1  # Αρχικά, C = 0 με πιθανότητα 1

    # Δυναμικός προγραμματισμός για τον υπολογισμό των πιθανοτήτων
    for k in range(1, n + 1):
        new_p = np.zeros(max_c)

        for i in range(max_c):
            # Η πιθανότητα να παραμείνει στο i
            if i > 0:  # C δεν μπορεί να είναι αρνητικό
                new_p[i] += p[i] * (1 - 1 / pow(2, i))

            # Η πιθανότητα να αυξηθεί από i-1 σε i
            if i > 0:
                new_p[i] += p[i - 1] * (1 / pow(2, i - 1))

        p = new_p

    # Αθροίζουμε τις πιθανότητες για τις τιμές που μας ενδιαφέρουν
    total_prob = sum(p[i] for i in target_values)

    # Μετατροπή σε κλάσμα για ακριβή αναπαράσταση
    fraction_prob = Fraction(total_prob).limit_denominator()

    return fraction_prob, float(fraction_prob)


# Υπολογισμός για C_1000 να έχει τιμές στο σύνολο {8, 9, 10, 11}
target_values = [8, 9, 10, 11]
n = 1000

fraction_prob, decimal_prob = calculate_probability_C_n_optimized(n, target_values)

print(f"Η πιθανότητα η C_{n} να έχει τιμές στο σύνολο {target_values} είναι:")
print(f"Ως κλάσμα: {fraction_prob}")
print(f"Ως δεκαδικός: {decimal_prob:.6f}")
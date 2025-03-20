import numpy as np
from fractions import Fraction


def calculate_probability_c_n(n, target_values):
    """
    Υπολογίζει την πιθανότητα η μεταβλητή C_n να έχει τιμές στο σύνολο target_values
    μετά από n εισαγωγές στοιχείων.

    Args:
        n: Αριθμός εισαγωγών στοιχείων
        target_values: Σύνολο τιμών που μας ενδιαφέρουν

    Returns:
        Η πιθανότητα σε μορφή κλάσματος και σε δεκαδική μορφή
    """
    # Αρχικοποίηση πιθανοτήτων
    # p[i] = πιθανότητα η C να είναι i μετά από k βήματα
    max_c = max(target_values) + 1  # Χρειαζόμαστε αρκετό χώρο για όλες τις πιθανές τιμές
    p = [0] * max_c
    p[0] = 1  # Αρχικά, C = 0 με πιθανότητα 1

    # Για κάθε βήμα, υπολογίζουμε τις νέες πιθανότητες
    for k in range(1, n + 1):
        new_p = [0] * max_c

        for i in range(max_c - 1):
            # Η πιθανότητα να παραμείνει στο i
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

fraction_prob, decimal_prob = calculate_probability_c_n(n, target_values)

print(f"Η πιθανότητα η C_{n} να έχει τιμές στο σύνολο {target_values} είναι:")
print(f"Ως κλάσμα: {fraction_prob}")
print(f"Ως δεκαδικός: {decimal_prob:.6f}")
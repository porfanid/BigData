import random

def random_bitstring(length=100):
    """
    Δημιουργεί τυχαίες συμβολοσειρές από bits (0 και 1).

    Παράμετροι:
    -----------
    length : int, προαιρετικό
        Το μήκος της συμβολοσειράς (προεπιλογή: 100).

    Επιστρέφει:
    -----------
    str
        Μια τυχαία συμβολοσειρά από '0' και '1' χαρακτήρες.
    """
    return ''.join(random.choice('01') for _ in range(length))

# Δημιουργία των 10 κοινών αρχείων
common_files = [random_bitstring() for _ in range(10)]

# Δημιουργία των υπόλοιπων αρχείων για κάθε server
# Κάθε σύνολο περιέχει τα κοινά αρχεία συν 99990 μοναδικά αρχεία
A_files = common_files + [random_bitstring() for _ in range(99990)]
B_files = common_files + [random_bitstring() for _ in range(99990)]
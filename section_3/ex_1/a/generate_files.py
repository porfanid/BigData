import random

def random_bitstring(length=100):
    return ''.join(random.choice('01') for _ in range(length))

# Δημιουργία των 10 κοινών αρχείων
common_files = [random_bitstring() for _ in range(10)]

# Δημιουργία των υπόλοιπων αρχείων για κάθε server
A_files = common_files + [random_bitstring() for _ in range(99990)]
B_files = common_files + [random_bitstring() for _ in range(99990)]

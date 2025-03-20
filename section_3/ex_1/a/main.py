# Πίνακας για αποθήκευση αποτελεσμάτων
from section_3.ex_1.a.bloom_intersection import bloom_intersection
from section_3.ex_1.a.generate_files import A_files, B_files

results = {}

# Παράμετροι δοκιμών
hash_values = [1, 2, 3, 5, 10]
round_values = [1, 2, 3, 4, 5]

# Εκτέλεση όλων των συνδυασμών
for k_hashes in hash_values:
    for k_rounds in round_values:
        print(f"\n### Δοκιμή με {k_hashes} hash functions και {k_rounds} γύρους ###")
        count = bloom_intersection(
            A_files=A_files,
            B_files=B_files,
            k_hashes=k_hashes,
            k_rounds=k_rounds,
            dynamic_size=True  # μπορείς να δοκιμάσεις και False
        )
        results[(k_hashes, k_rounds)] = count

print("\n\n===== ΑΠΟΤΕΛΕΣΜΑΤΑ =====")
for (k_hashes, k_rounds), count in results.items():
    print(f"{k_hashes} hash functions, {k_rounds} γύροι => {count} τελικά positives")


# Εισαγωγή των απαραίτητων μονάδων
from section_3.ex_1.a.bloom_intersection import bloom_intersection
from section_3.ex_1.a.generate_files import A_files, B_files

# Πίνακας για αποθήκευση αποτελεσμάτων
results = {}

# Παράμετροι δοκιμών
hash_values = [1, 2, 3, 5, 10]      # Διαφορετικοί αριθμοί συναρτήσεων κατακερματισμού
round_values = [1, 2, 3, 4, 5]      # Διαφορετικοί αριθμοί γύρων

# Εκτέλεση όλων των συνδυασμών παραμέτρων
for k_hashes in hash_values:
    for k_rounds in round_values:
        print(f"\n### Δοκιμή με {k_hashes} hash functions και {k_rounds} γύρους ###")
        count = bloom_intersection(
            A_files=A_files,         # Το σύνολο αρχείων του Α
            B_files=B_files,         # Το σύνολο αρχείων του Β
            k_hashes=k_hashes,       # Αριθμός συναρτήσεων κατακερματισμού
            k_rounds=k_rounds,       # Αριθμός γύρων
            dynamic_size=True        # Δυναμική προσαρμογή του μεγέθους του Bloom Filter
        )
        results[(k_hashes, k_rounds)] = count  # Αποθήκευση του αποτελέσματος

# Εμφάνιση των συγκεντρωτικών αποτελεσμάτων
print("\n\n===== ΑΠΟΤΕΛΕΣΜΑΤΑ =====")
for (k_hashes, k_rounds), count in results.items():
    print(f"{k_hashes} hash functions, {k_rounds} γύροι => {count} τελικά positives")
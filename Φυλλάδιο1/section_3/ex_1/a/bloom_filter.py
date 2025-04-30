import random

from section_3.ex_1.a.hash_function import HashFunction


class BloomFilter:
    """
    Υλοποίηση του αλγορίθμου Bloom Filter.
    Το Bloom Filter είναι μια πιθανοτική δομή δεδομένων που χρησιμοποιείται για να ελέγχει
    αν ένα στοιχείο ανήκει σε ένα σύνολο.
    """

    def __init__(self, N_bits, k_hashes, p=1048583):
        """
        Αρχικοποίηση του Bloom Filter.

        Παράμετροι:
        -----------
        N_bits : int
            Ο αριθμός των bits στο φίλτρο.
        k_hashes : int
            Ο αριθμός των συναρτήσεων κατακερματισμού (hash functions).
        p : int, προαιρετικό
            Ο πρώτος αριθμός που χρησιμοποιείται στις συναρτήσεις κατακερματισμού (προεπιλογή: 1048583).
        """
        self.N = N_bits  # Μέγεθος του φίλτρου σε bits
        self.k = k_hashes  # Αριθμός συναρτήσεων κατακερματισμού
        self.p = p  # Πρώτος αριθμός για τις hash functions
        self.bits = [0] * self.N  # Αρχικοποίηση του πίνακα bits με μηδενικά
        # Δημιουργία k τυχαίων συναρτήσεων κατακερματισμού
        self.hash_functions = [HashFunction(
            alpha=random.randint(1, p - 1),  # Τυχαία παράμετρος alpha
            beta=random.randint(0, p - 1),  # Τυχαία παράμετρος beta
            p=p,  # Πρώτος αριθμός
            N=self.N  # Μέγεθος φίλτρου
        ) for _ in range(self.k)]

    def add(self, item):
        """
        Προσθέτει ένα στοιχείο στο Bloom Filter.

        Παράμετροι:
        -----------
        item : any
            Το στοιχείο προς προσθήκη στο φίλτρο.
        """
        for h in self.hash_functions:
            index = h.hash(item)  # Υπολογισμός του δείκτη με την hash function
            self.bits[index] = 1  # Θέτει το αντίστοιχο bit σε 1

    def check(self, item):
        """
        Ελέγχει αν ένα στοιχείο πιθανώς υπάρχει στο Bloom Filter.

        Παράμετροι:
        -----------
        item : any
            Το στοιχείο προς έλεγχο.

        Επιστρέφει:
        -----------
        bool
            True αν το στοιχείο πιθανώς υπάρχει στο φίλτρο, False αν σίγουρα δεν υπάρχει.
            Προσοχή: Μπορεί να επιστρέψει ψευδώς θετικά αποτελέσματα (false positives),
            αλλά ποτέ ψευδώς αρνητικά (false negatives).
        """
        return all(self.bits[h.hash(item)] for h in self.hash_functions)
# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

# Εισάγουμε τη βιβλιοθήκη random για τη δημιουργία τυχαίων αριθμών
import random

# Εισάγουμε την κλάση HashFunction που χρησιμοποιείται για την υλοποίηση των hash functions
from hash_function import HashFunction


class BloomFilter:
    """
    Υλοποίηση του αλγορίθμου Bloom Filter.
    Το Bloom Filter είναι μια πιθανοτική δομή δεδομένων που χρησιμοποιείται για να ελέγχει
    αν ένα στοιχείο ανήκει σε ένα σύνολο, με πιθανότητα εμφάνισης false positives.
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
            Ο πρώτος αριθμός που χρησιμοποιείται στις hash functions (default: 1048583).
        """
        self.N = N_bits  # Αποθηκεύουμε τον συνολικό αριθμό των bits του Bloom filter
        self.k = k_hashes  # Αποθηκεύουμε τον αριθμό των hash functions που θα χρησιμοποιηθούν
        self.p = p  # Ο πρώτος αριθμός που θα χρησιμοποιείται στις hash functions

        self.bits = [0] * self.N  # Δημιουργούμε έναν πίνακα με N μηδενικά (αρχικά όλα τα bits είναι 0)

        # Δημιουργούμε μια λίστα με k διαφορετικές hash functions
        self.hash_functions = [HashFunction(
            alpha=random.randint(1, p - 1),  # Τυχαία τιμή alpha από το [1, p-1]
            beta=random.randint(0, p - 1),  # Τυχαία τιμή beta από το [0, p-1]
            p=p,  # Ο πρώτος αριθμός που χρησιμοποιείται στη hash function
            N=self.N  # Το N είναι το μέγεθος του πίνακα bits (χρησιμοποιείται για mod)
        ) for _ in range(self.k)]  # Επαναλαμβάνεται k φορές για να δημιουργήσουμε k hash functions

    def add(self, item):
        """
        Προσθέτει ένα στοιχείο στο Bloom Filter.

        Παράμετροι:
        -----------
        item : any
            Το στοιχείο προς προσθήκη στο φίλτρο.
        """
        for h in self.hash_functions:  # Για κάθε hash function στη λίστα
            index = h.hash(item)  # Υπολογίζουμε τον δείκτη μέσω της hash function για το στοιχείο
            self.bits[index] = 1  # Θέτουμε το bit στη θέση index σε 1 (δηλ. "ενεργοποιούμε" το bit)

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
            Προσοχή: Μπορεί να επιστρέψει false positives, αλλά ποτέ false negatives.
        """
        # Επιστρέφει True μόνο αν για όλες τις hash functions το αντίστοιχο bit είναι 1
        # Δηλαδή, αν υπάρχει έστω μία hash function που οδηγεί σε bit=0, τότε σίγουρα το στοιχείο δεν υπάρχει
        return all(self.bits[h.hash(item)] for h in self.hash_functions)

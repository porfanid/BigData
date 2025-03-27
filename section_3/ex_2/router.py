from section_3.ex_1.a.bloom_filter import BloomFilter


class Router:
    """
    Αναπαράσταση ενός δρομολογητή (router) που χρησιμοποιεί Bloom Filter για
    την καταγραφή μηνυμάτων που έχει επεξεργαστεί.
    """
    def __init__(self, router_id, N_bits=10000, k_hashes=1):
        """
        Αρχικοποίηση ενός δρομολογητή.

        Παράμετροι:
        -----------
        router_id : int
            Το αναγνωριστικό του δρομολογητή στο δίκτυο.
        N_bits : int, προαιρετικό
            Το μέγεθος του Bloom Filter σε bits (προεπιλογή: 10000).
        k_hashes : int, προαιρετικό
            Ο αριθμός των συναρτήσεων κατακερματισμού (προεπιλογή: 1).
        """
        self.id = router_id                          # Αναγνωριστικό του router
        self.bloom_filter = BloomFilter(N_bits, k_hashes)  # Δημιουργία Bloom Filter
        self.received_messages = set()               # Για debugging/ιχνηλάτηση αν χρειαστεί

    def receive_message(self, message):
        """
        Καταγράφει την παραλαβή ενός μηνύματος από τον router.

        Παράμετροι:
        -----------
        message : str
            Το μήνυμα που παραλαμβάνεται.
        """
        self.bloom_filter.add(message)      # Προσθήκη στο Bloom Filter
        self.received_messages.add(message) # Αποθήκευση στο σύνολο μηνυμάτων

    def has_message(self, message):
        """
        Ελέγχει αν ο router έχει επεξεργαστεί ένα συγκεκριμένο μήνυμα.

        Παράμετροι:
        -----------
        message : str
            Το μήνυμα προς έλεγχο.

        Επιστρέφει:
        -----------
        bool
            True αν το μήνυμα έχει πιθανώς επεξεργαστεί από τον router,
            False αν σίγουρα δεν έχει επεξεργαστεί.
            Σημείωση: Μπορεί να επιστρέψει false positives λόγω της φύσης του Bloom Filter.
        """
        return self.bloom_filter.check(message)
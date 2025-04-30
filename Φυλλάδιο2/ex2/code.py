import numpy as np
import random


class SparseVectorRecovery:
    def __init__(self, n=10000, p=20011, T=1):
        """
        Μηχανισμός ανάκτησης 1-αραιού διανύσματος

        Παράμετροι:
        - n: μέγεθος του διανύσματος (10000)
        - p: πρώτος αριθμός (20011)
        - T: πλήθος τυχαίων αριθμών r_i
        """
        self.n = n
        self.p = p
        self.T = T

        # Διάνυσμα που παρακολουθούμε
        self.x = np.zeros(n + 1)  # Αριθμούμε από 1 έως n

        # Τυχαίοι αριθμοί r_i από {1, 2, ..., p-1}
        self.r = [random.randint(1, p - 1) for _ in range(T)]

        # Διανύσματα για τον μηχανισμό ανάκτησης
        self.a = [0] * T
        self.b = [0] * T

    def process_command(self, i, c):
        """
        Επεξεργάζεται μια εντολή (i,c) που προσθέτει την τιμή c στη συντεταγμένη i
        και ενημερώνει τα διανύσματα a και b
        """
        # Ενημέρωση του διανύσματος x
        self.x[i] += c

        # Ενημέρωση των διανυσμάτων a και b
        for t in range(self.T):
            r_i_power = pow(self.r[t], i, self.p)
            self.a[t] = (self.a[t] + c * r_i_power) % self.p
            self.b[t] = (self.b[t] + c) % self.p

    def is_1_sparse(self):
        """
        Ελέγχει αν το διάνυσμα είναι 1-αραιό, δηλαδή
        αν περιέχει ακριβώς μία μη-μηδενική συντεταγμένη

        Επιστρέφει:
        - True αν το διάνυσμα φαίνεται να είναι 1-αραιό
        - False διαφορετικά
        """
        # Αν το b είναι 0, τότε το διάνυσμα είναι 0-αραιό (δεν έχει μη-μηδενικές συντεταγμένες)
        if all(b_t == 0 for b_t in self.b):
            return False

        # Έλεγχος για 1-αραιό διάνυσμα
        for t in range(self.T):
            # Αν το b_t είναι 0, πρέπει και το a_t να είναι 0
            if self.b[t] == 0 and self.a[t] != 0:
                return False

            # Αν το b_t δεν είναι 0, ελέγχουμε αν a_t/b_t = r_i^j για κάποιο j
            if self.b[t] != 0:
                # Υπολογισμός του a_t / b_t mod p
                # Χρειαζόμαστε τον πολλαπλασιαστικό αντίστροφο του b_t mod p
                b_inv = pow(self.b[t], -1, self.p)
                result = (self.a[t] * b_inv) % self.p

                # Αν κάποιο t δεν επαληθεύει τον κανόνα, τότε το διάνυσμα δεν είναι 1-αραιό
                found = False
                for j in range(1, self.n + 1):
                    if pow(self.r[t], j, self.p) == result:
                        found = True
                        break

                if not found:
                    return False

        # Αν όλοι οι έλεγχοι περάσουν, το διάνυσμα είναι 1-αραιό
        return True

    def get_non_zero_coordinate(self):
        """
        Επιστρέφει τη μη-μηδενική συντεταγμένη και την τιμή της,
        υπό την προϋπόθεση ότι το διάνυσμα είναι 1-αραιό
        """
        if not self.is_1_sparse():
            return None, None

        # Αν το b[0] είναι 0, όλες οι συντεταγμένες είναι 0
        if self.b[0] == 0:
            return None, None

        # Υπολογισμός του a[0]/b[0] mod p
        b_inv = pow(self.b[0], -1, self.p)
        result = (self.a[0] * b_inv) % self.p

        # Εύρεση του i τέτοιο ώστε r[0]^i = result
        for i in range(1, self.n + 1):
            if pow(self.r[0], i, self.p) == result:
                return i, self.b[0]  # Η τιμή της συντεταγμένης είναι το b[0]

        return None, None  # Δεν θα πρέπει να φτάσουμε εδώ αν το is_1_sparse() επέστρεψε True


def run_simulation(T=1, n_commands=10_000_000):
    """
    Εκτελεί την προσομοίωση με τον μηχανισμό ανάκτησης 1-αραιού διανύσματος

    Παράμετροι:
    - T: Αριθμός τυχαίων αριθμών r_i
    - n_commands: Πλήθος εντολών
    """
    # Δημιουργία των εντολών
    from Φυλλάδιο2.ex1.code import generate_commands
    print(f"Παράγονται {n_commands} εντολές...")
    commands = generate_commands(n_commands)
    print("Ολοκληρώθηκε η παραγωγή εντολών.")

    # Δημιουργία του μηχανισμού ανάκτησης
    recovery = SparseVectorRecovery(n=10000, p=20011, T=T)

    # Μετρητής σφαλμάτων (false positives)
    errors = 0

    # Διάνυσμα x που παρακολουθούμε για επαλήθευση
    x = np.zeros(10001)

    print(f"Εκτέλεση προσομοίωσης με T={T}...")
    for idx, (i, c) in enumerate(commands, 1):
        # Εφαρμογή της εντολής στο διάνυσμα x για επαλήθευση
        x[i] += c

        # Εφαρμογή της εντολής στον μηχανισμό ανάκτησης
        recovery.process_command(i, c)

        # Έλεγχος αν το διάνυσμα είναι 1-αραιό
        is_1_sparse_algorithm = recovery.is_1_sparse()

        # Έλεγχος της πραγματικής κατάστασης του διανύσματος
        non_zero_count = np.count_nonzero(x)
        is_1_sparse_actual = (non_zero_count == 1)

        # Έλεγχος για false positive
        if is_1_sparse_algorithm and not is_1_sparse_actual:
            errors += 1

        # Εκτύπωση της προόδου και των σφαλμάτων
        if idx % 100000 == 0 or idx == n_commands:
            print(f"{idx}: {errors}")

    return errors


# Εκτέλεση της προσομοίωσης για διαφορετικές τιμές του T
def run_multiple_simulations(max_T=10, n_commands=10_000_000):
    """
    Εκτελεί την προσομοίωση για διαφορετικές τιμές του T

    Παράμετροι:
    - max_T: Μέγιστη τιμή του T που θα δοκιμαστεί
    - n_commands: Πλήθος εντολών
    """
    results = {}
    for T in range(1, max_T + 1):
        print(f"\nΠροσομοίωση με T={T}")
        errors = run_simulation(T=T, n_commands=n_commands)
        results[T] = errors
        print(f"Αποτέλεσμα για T={T}: {errors} σφάλματα")

    return results


# Για την εκτέλεση της προσομοίωσης, χρησιμοποιήστε:
# results = run_multiple_simulations(max_T=10, n_commands=10_000_000)
# ή για μια μόνο τιμή του T:
# errors = run_simulation(T=2, n_commands=10_000_000)

# Για δοκιμαστική εκτέλεση με λιγότερες εντολές:
if __name__ == "__main__":
    errors = run_simulation(T=2, n_commands=1000)
    print(f"Συνολικά σφάλματα: {errors}")
import numpy as np
import random


def generate_commands(n=10_000_000):
    """
    Παράγει n εντολές σύμφωνα με τις προδιαγραφές της άσκησης.
    Κάθε εντολή έχει τη μορφή (i, c) όπου:
    - i είναι μια συντεταγμένη (1-10000)
    - c είναι η τιμή που θα προστεθεί στη συντεταγμένη
    """
    # Αρχικοποίηση του διανύσματος x
    x = np.zeros(10001)  # Αριθμούμε 1-10000, αγνοούμε το x[0]

    commands = []
    phase = 'O'  # Ξεκινάμε από τη φάση O
    s = 0  # Ειδική συντεταγμένη

    i = 0
    while i < n:
        if phase == 'O':  # Φάση 0
            s = random.randint(1, 10000)  # Επιλογή τυχαίας συντεταγμένης s
            commands.append((s, 1))  # Προσθήκη 1 στη συντεταγμένη s
            x[s] += 1
            phase = 'A'  # Μετάβαση στη φάση A
            i += 1

        elif phase == 'A':  # Κανονική εξέλιξη
            # Φάση A1: Μηδενισμός μη-μηδενικής συντεταγμένης διάφορης της s
            non_zero_indices = [idx for idx in range(1, 10001) if idx != s and x[idx] != 0]
            if non_zero_indices and random.random() < 1 / 3:
                idx = random.choice(non_zero_indices)
                commands.append((idx, -int(x[idx])))
                x[idx] = 0
                i += 1

            # Φάση A2: Προσθήκη τιμής σε συντεταγμένη διάφορη της s
            if random.random() < 1 / 3:
                idx = random.choice([j for j in range(1, 10001) if j != s])
                c = random.choice([j for j in range(-10, 11) if j != 0])
                commands.append((idx, c))
                x[idx] += c
                i += 1

            # Φάση A3: Τροποποίηση της συντεταγμένης s
            if random.random() < 1 / 2:
                c = random.choice([-2, 2])
                commands.append((s, c))
                x[s] += c
                i += 1

            # Απόφαση για την επόμενη φάση
            r = random.random()
            if r < 0.95:
                phase = 'A'  # Παραμένουμε στη φάση A (95%)
            elif r < 0.99:
                phase = 'B'  # Μεταβαίνουμε στη φάση B (4%)
            else:
                phase = 'Γ'  # Μεταβαίνουμε στη φάση Γ (1%)

        elif phase == 'B':  # Επιστροφή στο 0
            non_zero_indices = [idx for idx in range(1, 10001) if x[idx] != 0]
            if non_zero_indices:
                idx = random.choice(non_zero_indices)
                commands.append((idx, -int(x[idx])))
                x[idx] = 0
                i += 1
            else:
                phase = 'O'  # Μόλις μηδενιστεί το διάνυσμα, πάμε στη φάση O

        elif phase == 'Γ':  # Ξαφνική έκρηξη
            count_explosion = 0
            while count_explosion < 100 and i < n:
                idx = random.choice([j for j in range(1, 10001) if j != s])
                c = random.choice([j for j in range(-10, 11) if j != 0])
                commands.append((idx, c))
                x[idx] += c
                count_explosion += 1
                i += 1
            phase = 'A'  # Μετάβαση στη φάση A μετά την έκρηξη

    return commands[:n]  # Επιστρέφουμε ακριβώς n εντολές


def save_commands_to_file(commands, filename="commands.txt"):
    """Αποθηκεύει τις εντολές σε αρχείο"""
    with open(filename, "w") as f:
        for i, c in commands:
            f.write(f"{i} {c}\n")


# Παράδειγμα χρήσης
if __name__ == "__main__":
    # Για λόγους επίδειξης, παράγουμε λιγότερες εντολές
    commands = generate_commands(1000)
    save_commands_to_file(commands)
    print(f"Παράχθηκαν {len(commands)} εντολές")

# Για την πλήρη άσκηση, χρησιμοποιήστε:
    commands = generate_commands(10_000_000)
    save_commands_to_file(commands)
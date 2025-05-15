# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr

# Εισάγουμε τη βιβλιοθήκη random για επιλογές και τυχαιότητα
import random

# Χρήση συνάρτησης για δημιουργία τυχαίων bitstrings
from generate_files import random_bitstring

# Εισάγουμε την κλάση Router για την προσομοίωση των δρομολογητών
from router import Router


def load_graph(filepath):
    """
    Φορτώνει το γράφημα δικτύου από αρχείο.
    Το αρχείο περιέχει στην πρώτη γραμμή τον αριθμό κόμβων και ακμών,
    και στη συνέχεια ζεύγη ακμών (x, y) ανά γραμμή.

    Επιστρέφει:
    -----------
    dict (graph), int (n): το γράφημα και τον αριθμό των κόμβων.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    n, m = map(int, lines[0].strip().split())  # Πρώτη γραμμή: αριθμός κόμβων και ακμών
    graph = {i: [] for i in range(1, n + 1)}   # Αρχικοποίηση άδειου γράφου με κλειδιά από 1 έως n

    for line in lines[1:]:  # Για κάθε γραμμή-ακμή
        x, y = map(int, line.strip().split())  # Παίρνουμε τα δύο άκρα της ακμής
        graph[x].append(y)  # Προσθέτουμε τον y ως γείτονα του x

    return graph, n


def create_routers(graph, n_bits=10000, k_hashes=1):
    """
    Δημιουργεί router αντικείμενα για κάθε κόμβο του γράφου.

    Επιστρέφει:
    -----------
    dict με router_id → Router instance.
    """
    routers = {}
    for node_id in graph.keys():  # Για κάθε κόμβο του γράφου
        routers[node_id] = Router(node_id, n_bits, k_hashes)  # Δημιουργούμε router με τις κατάλληλες παραμέτρους
    return routers


def generate_messages(num_messages=100000, message_size=100):
    """
    Δημιουργεί μια λίστα από τυχαία bitstring μηνύματα.

    Επιστρέφει:
    -----------
    list με τυχαία μηνύματα.
    """
    messages = []
    for _ in range(num_messages):
        msg = random_bitstring(message_size)  # Δημιουργία bitstring μήκους 100
        messages.append(msg)
    return messages


def forward_messages(graph, routers, messages):
    """
    Προωθεί κάθε μήνυμα μέσα στο δίκτυο ξεκινώντας από τυχαίο κόμβο (1 έως 10)
    μέχρι να φτάσει στον τελευταίο κόμβο ή να "κολλήσει".

    Ενημερώνει τα Bloom Filters κάθε router.
    """
    for msg in messages:
        source = random.randint(1, 10)  # Τυχαίος αρχικός κόμβος από τους 10 πρώτους
        routers[source].receive_message(msg)  # Ο αρχικός router καταγράφει το μήνυμα

        current = source
        while current != max(graph.keys()):  # Συνεχίζουμε μέχρι τον τελικό router
            next_hops = graph[current]  # Επόμενοι γείτονες
            if not next_hops:
                break  # Αν δεν έχει επόμενους, σταματάμε
            next_router = random.choice(next_hops)  # Τυχαία επιλογή επομένου router
            routers[next_router].receive_message(msg)  # Ο επόμενος router λαμβάνει το μήνυμα
            current = next_router  # Προχωράμε


def trace_message(graph, routers, message, current_router_id, sources):
    """
    Αναζητά αναδρομικά την πηγή ενός μηνύματος μέσω Bloom Filters.

    Επιστρέφει:
    -----------
    True αν βρεθεί μοναδική πηγή στο σύνολο των sources.
    """
    stack = [current_router_id]  # Χρήση στοίβας για DFS
    visited = set()              # Κόμβοι που έχουμε επισκεφθεί
    candidates = set()           # Πιθανοί source routers

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        router = routers[node]
        if router.has_message(message):  # Αν ο router "έχει" το μήνυμα
            if node in sources:  # Αν είναι στους αρχικούς κόμβους
                candidates.add(node)
            else:
                # Βρίσκουμε "γονείς" (κόμβους που δείχνουν σε αυτόν)
                for parent in [n for n in graph if node in graph[n]]:
                    stack.append(parent)  # Προσθέτουμε τον γονέα για εξερεύνηση

    return len(candidates) == 1  # Επιτυχία αν υπάρχει μόνο ένας υποψήφιος


def packet_tracing_simulation(filepath, k_hashes=1):
    """
    Εκτελεί το συνολικό πείραμα προώθησης & ιχνηλάτησης για ένα δίκτυο.

    Επιστρέφει:
    -----------
    int: Πλήθος επιτυχημένων ιχνηλατήσεων.
    """
    graph, n = load_graph(filepath)  # Φόρτωση γραφήματος
    routers = create_routers(graph, n_bits=10000, k_hashes=k_hashes)  # Δημιουργία routers

    sources = set(range(1, 11))  # Οι 10 αρχικοί source routers
    messages = generate_messages(num_messages=100000)  # Τυχαία μηνύματα

    forward_messages(graph, routers, messages)  # Προώθηση μέσα στο δίκτυο

    successful_traces = 0
    receiver_id = n  # Ο τελευταίος κόμβος είναι ο παραλήπτης

    for msg in messages:
        success = trace_message(graph, routers, msg, receiver_id, sources)
        if success:
            successful_traces += 1

    print(f"Με {k_hashes} hash functions, επιτυχημένες ιχνηλατήσεις: {successful_traces} / {len(messages)}")
    return successful_traces


# --- Εκτέλεση πειραμάτων με διαφορετικό αριθμό hash functions ---

hash_values = [1, 2, 3, 5, 10]  # Διαφορετικές τιμές για k_hashes
results = {}

# Δοκιμή με κάθε τιμή
for k_hashes in hash_values:
    success_count = packet_tracing_simulation('Networks/graphA1.txt', k_hashes=k_hashes)
    results[k_hashes] = success_count  # Αποθήκευση αποτελέσματος

# Εμφάνιση συγκεντρωτικών αποτελεσμάτων
print("\nΑΠΟΤΕΛΕΣΜΑΤΑ:")
for k, success in results.items():
    print(f"{k} hash functions => {success} επιτυχημένες ιχνηλατήσεις")

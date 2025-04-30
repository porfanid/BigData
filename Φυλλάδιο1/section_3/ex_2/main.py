import random

from section_3.ex_1.a.generate_files import random_bitstring
from section_3.ex_2.router import Router


def load_graph(filepath):
    """
    Φορτώνει το γράφημα δικτύου από αρχείο.

    Παράμετροι:
    -----------
    filepath : str
        Η διαδρομή του αρχείου που περιέχει το γράφημα.

    Επιστρέφει:
    -----------
    tuple
        Το γράφημα ως λεξικό και τον αριθμό κόμβων.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    n, m = map(int, lines[0].strip().split())  # Αριθμός κόμβων και ακμών
    graph = {i: [] for i in range(1, n + 1)}   # Αρχικοποίηση γραφήματος
    for line in lines[1:]:
        x, y = map(int, line.strip().split())  # Ανάγνωση κάθε ακμής
        graph[x].append(y)                    # Προσθήκη γειτονικού κόμβου

    return graph, n

def create_routers(graph, n_bits=10000, k_hashes=1):
    """
    Δημιουργεί τους routers του δικτύου.

    Παράμετροι:
    -----------
    graph : dict
        Το γράφημα του δικτύου.
    n_bits : int, προαιρετικό
        Μέγεθος του Bloom Filter (προεπιλογή: 10000).
    k_hashes : int, προαιρετικό
        Αριθμός συναρτήσεων κατακερματισμού (προεπιλογή: 1).

    Επιστρέφει:
    -----------
    dict
        Λεξικό με τους routers του δικτύου.
    """
    routers = {}
    for node_id in graph.keys():
        routers[node_id] = Router(node_id, n_bits, k_hashes)
    return routers

def generate_messages(num_messages=100000, message_size=100):
    """
    Δημιουργεί τυχαία μηνύματα για την προσομοίωση.

    Παράμετροι:
    -----------
    num_messages : int, προαιρετικό
        Αριθμός μηνυμάτων (προεπιλογή: 100000).
    message_size : int, προαιρετικό
        Μέγεθος κάθε μηνύματος σε bits (προεπιλογή: 100).

    Επιστρέφει:
    -----------
    list
        Λίστα με τα τυχαία μηνύματα.
    """
    messages = []
    for _ in range(num_messages):
        msg = random_bitstring(message_size)
        messages.append(msg)
    return messages

def forward_messages(graph, routers, messages):
    """
    Προωθεί τα μηνύματα στο δίκτυο και ενημερώνει τα Bloom Filters.

    Παράμετροι:
    -----------
    graph : dict
        Το γράφημα του δικτύου.
    routers : dict
        Οι routers του δικτύου.
    messages : list
        Τα μηνύματα προς προώθηση.
    """
    for msg in messages:
        # Διάλεξε τυχαίο router από τα 1-10 για προέλευση
        source = random.randint(1, 10)
        routers[source].receive_message(msg)

        current = source
        while current != max(graph.keys()):
            next_hops = graph[current]
            if not next_hops:
                break
            # Τυχαία επιλογή επόμενου router
            next_router = random.choice(next_hops)
            routers[next_router].receive_message(msg)
            current = next_router

def trace_message(graph, routers, message, current_router_id, sources):
    """
    Εκτελεί ιχνηλάτηση ενός μηνύματος για εύρεση της πηγής του.

    Παράμετροι:
    -----------
    graph : dict
        Το γράφημα του δικτύου.
    routers : dict
        Οι routers του δικτύου.
    message : str
        Το μήνυμα προς ιχνηλάτηση.
    current_router_id : int
        Ο router που έχει λάβει το μήνυμα και ξεκινά την ιχνηλάτηση.
    sources : set
        Το σύνολο των πιθανών πηγών μηνυμάτων.

    Επιστρέφει:
    -----------
    bool
        True αν η ιχνηλάτηση είναι επιτυχής (μοναδική πηγή βρέθηκε).
    """
    stack = [current_router_id]  # Στοίβα για διάσχιση γραφήματος
    visited = set()              # Κόμβοι που έχουν επισκεφθεί

    candidates = set()           # Υποψήφιες πηγές του μηνύματος

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        router = routers[node]
        if router.has_message(message):
            if node in sources:
                candidates.add(node)  # Αν είναι πηγή, τον προσθέτουμε στους υποψήφιους
            else:
                # Εξετάζουμε τους "γονείς" που συνδέονται με αυτόν
                for parent in [n for n in graph if node in graph[n]]:
                    stack.append(parent)

    # Επιτυχία αν υπάρχει ΜΟΝΟ ένα μοναδικό source router που το έχει
    return len(candidates) == 1

def packet_tracing_simulation(filepath, k_hashes=1):
    """
    Εκτελεί την προσομοίωση ιχνηλάτησης πακέτων στο δίκτυο.

    Παράμετροι:
    -----------
    filepath : str
        Η διαδρομή του αρχείου που περιέχει το γράφημα.
    k_hashes : int, προαιρετικό
        Αριθμός συναρτήσεων κατακερματισμού (προεπιλογή: 1).

    Επιστρέφει:
    -----------
    int
        Το πλήθος των επιτυχημένων ιχνηλατήσεων.
    """
    graph, n = load_graph(filepath)  # Φόρτωση γραφήματος
    routers = create_routers(graph, n_bits=10000, k_hashes=k_hashes)  # Δημιουργία routers

    sources = set(range(1, 11))  # Οι 10 αρχικοί κόμβοι
    messages = generate_messages(num_messages=100000)  # Δημιουργία μηνυμάτων

    forward_messages(graph, routers, messages)  # Προώθηση μηνυμάτων στο δίκτυο

    successful_traces = 0
    receiver_id = n  # Ο τελευταίος router είναι ο παραλήπτης

    for msg in messages:
        success = trace_message(graph, routers, msg, receiver_id, sources)
        if success:
            successful_traces += 1

    print(f"Με {k_hashes} hash functions, επιτυχημένες ιχνηλατήσεις: {successful_traces} / {len(messages)}")
    return successful_traces


# Παράδειγμα εκτέλεσης σε ένα γράφημα
hash_values = [1, 2, 3, 5, 10]  # Διαφορετικές τιμές αριθμού hash functions
results = {}

# Δοκιμή με διαφορετικό αριθμό hash functions
for k_hashes in hash_values:
    success_count = packet_tracing_simulation('../../Networks/graphA1.txt', k_hashes=k_hashes)
    results[k_hashes] = success_count

# Εμφάνιση συγκεντρωτικών αποτελεσμάτων
print("\nΑΠΟΤΕΛΕΣΜΑΤΑ:")
for k, success in results.items():
    print(f"{k} hash functions => {success} επιτυχημένες ιχνηλατήσεις")
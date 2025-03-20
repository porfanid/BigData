import random

from section_3.ex_1.a.generate_files import random_bitstring
from section_3.ex_2.router import Router


def load_graph(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    n, m = map(int, lines[0].strip().split())
    graph = {i: [] for i in range(1, n + 1)}
    for line in lines[1:]:
        x, y = map(int, line.strip().split())
        graph[x].append(y)

    return graph, n

def create_routers(graph, n_bits=10000, k_hashes=1):
    routers = {}
    for node_id in graph.keys():
        routers[node_id] = Router(node_id, n_bits, k_hashes)
    return routers

def generate_messages(num_messages=100000, message_size=100):
    messages = []
    for _ in range(num_messages):
        msg = random_bitstring(message_size)
        messages.append(msg)
    return messages

def forward_messages(graph, routers, messages):
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
    stack = [current_router_id]
    visited = set()

    candidates = set()

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        router = routers[node]
        if router.has_message(message):
            if node in sources:
                candidates.add(node)
            else:
                # Εξετάζουμε τους "γονείς" που συνδέονται με αυτόν
                for parent in [n for n in graph if node in graph[n]]:
                    stack.append(parent)

    # Επιτυχία αν υπάρχει ΜΟΝΟ ένα μοναδικό source router που το έχει
    return len(candidates) == 1

def packet_tracing_simulation(filepath, k_hashes=1):
    graph, n = load_graph(filepath)
    routers = create_routers(graph, n_bits=10000, k_hashes=k_hashes)

    sources = set(range(1, 11))  # Οι 10 αρχικοί κόμβοι
    messages = generate_messages(num_messages=100000)

    forward_messages(graph, routers, messages)

    successful_traces = 0
    receiver_id = n

    for msg in messages:
        success = trace_message(graph, routers, msg, receiver_id, sources)
        if success:
            successful_traces += 1

    print(f"Με {k_hashes} hash functions, επιτυχημένες ιχνηλατήσεις: {successful_traces} / {len(messages)}")
    return successful_traces


# Παράδειγμα εκτέλεσης σε ένα γράφημα
hash_values = [1, 2, 3, 5, 10]
results = {}

for k_hashes in hash_values:
    success_count = packet_tracing_simulation('../../Networks/graphA1.txt', k_hashes=k_hashes)
    results[k_hashes] = success_count

print("\nΑΠΟΤΕΛΕΣΜΑΤΑ:")
for k, success in results.items():
    print(f"{k} hash functions => {success} επιτυχημένες ιχνηλατήσεις")

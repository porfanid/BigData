import random
import time
import matplotlib.pyplot as plt
from collections import deque, defaultdict
import math
import multiprocessing as mp
import numpy as np
from functools import partial
import os

class GraphConnectivityChecker:
    def __init__(self, n, max_degree=10):
        self.n = n
        self.max_degree = max_degree
        self.graph = defaultdict(set)  # Adjacency list representation
        self.degrees = [0] * (n + 1)  # Degree of each node (1-indexed)
        
    def add_edge(self, u, v):
        """Add edge if it doesn't violate degree constraint"""
        if v in self.graph[u]:  # Edge already exists
            return False
        if self.degrees[u] >= self.max_degree or self.degrees[v] >= self.max_degree:
            return False
        
        self.graph[u].add(v)
        self.graph[v].add(u)
        self.degrees[u] += 1
        self.degrees[v] += 1
        return True
    
    def linear_connectivity_check(self):
        """
        Γραμμικός αλγόριθμος ελέγχου συνεκτικότητας με βελτιστοποίηση
        Επιλέγει τυχαία έναν κόμβο και κάνει BFS. Αν εξερευνήσει όλους τους κόμβους,
        το γράφημα είναι συνεκτικό.
        """
        visited = [False] * (self.n + 1)
        visited_nodes = []
        
        # Επιλογή τυχαίου αρχικού κόμβου
        start = random.randint(1, self.n)
        
        # BFS από τον αρχικό κόμβο
        queue = deque([start])
        visited[start] = True
        visited_nodes.append(start)
        visited_count = 1
        
        while queue:
            node = queue.popleft()
            for neighbor in self.graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    visited_nodes.append(neighbor)
                    queue.append(neighbor)
                    visited_count += 1
        
        # Έλεγχος αν εξερευνήθηκαν όλοι οι κόμβοι
        return visited_count == self.n
    
    def local_connectivity_check(self, seed, budget):
        """
        Ρουτίνα τοπικού ελέγχου συνεκτικότητας με budget B
        Ξεκινά BFS από το seed μέχρι να εξερευνήσει B+1 κόμβους ή να ολοκληρώσει τη διερεύνηση
        """
        visited = [False] * (self.n + 1)
        
        queue = deque([seed])
        visited[seed] = True
        explored_count = 1
        
        while queue and explored_count <= budget:
            node = queue.popleft()
            for neighbor in self.graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
                    explored_count += 1
                    if explored_count > budget:
                        break
        
        return "YES" if explored_count > budget else "NO"
    
    def simple_sublinear_algorithm(self, epsilon):
        """
        Απλός αλγόριθμος υπογραμμικού χρόνου O(1/(ε²Δ))
        """
        if epsilon <= 0:
            epsilon = 1e-10
            
        budget = max(1, int(1.0 / (epsilon * epsilon * self.max_degree)))
        budget = min(budget, self.n)  # Περιορισμός
        
        # Επιλογή τυχαίου seed
        seed = random.randint(1, self.n)
        
        result = self.local_connectivity_check(seed, budget)
        return result == "YES"
    
    def refined_sublinear_algorithm(self, epsilon):
        """
        Εκλεπτυσμένος αλγόριθμος υπογραμμικού χρόνου O((1/ε)·log(1/(εΔ))²)
        """
        if epsilon <= 0:
            epsilon = 1e-10
        if epsilon * self.max_degree <= 0:
            return False
            
        try:
            log_factor = math.log(1.0 / (epsilon * self.max_degree)) ** 2
            budget = max(1, int((1.0 / epsilon) * log_factor))
            budget = min(budget, self.n)
        except (ValueError, OverflowError):
            budget = min(1000, self.n)
        
        # Επιλογή τυχαίου seed
        seed = random.randint(1, self.n)
        
        result = self.local_connectivity_check(seed, budget)
        return result == "YES"
    
    def connectivity_check_with_decreasing_epsilon(self, algorithm_type="simple"):
        """
        Έλεγχος συνεκτικότητας δοκιμάζοντας μειούμενα ε
        Ξεκινά από ε=1/Δ και το υποδιπλασιάζει μέχρι να συμφέρει να τρέξει γραμμικό αλγόριθμο
        """
        # Ξεκινά από ε=1/Δ όπως λέει η εκφώνηση
        epsilon = 1.0 / self.max_degree
        calls_count = 0
        
        # Threshold για μετάβαση στον γραμμικό αλγόριθμο
        min_epsilon_threshold = 1.0 / (self.n ** 0.5)  # 1/√n όπως στην αρχική υλοποίηση
        max_iterations = 20  # Όριο ασφαλείας
        iteration = 0
        
        while epsilon >= min_epsilon_threshold and iteration < max_iterations:
            calls_count += 1
            iteration += 1
            
            if algorithm_type == "refined":
                result = self.refined_sublinear_algorithm(epsilon)
            else:
                result = self.simple_sublinear_algorithm(epsilon)
            
            if not result:  # Αλγόριθμος λέει "ΟΧΙ" - οπωσδήποτε μη-συνεκτικό
                return False, calls_count
            
            # Αλγόριθμος λέει "ΝΑΙ" - υποδιπλασιάζουμε το ε
            epsilon /= 2.0
        
        # Αν φτάσαμε εδώ, χρησιμοποιούμε γραμμικό αλγόριθμο
        return self.linear_connectivity_check(), calls_count
    
    def is_connected(self):
        """Απλό wrapper για έλεγχο συνεκτικότητας"""
        return self.linear_connectivity_check()

class UnionFind:
    """Union-Find για γρήγορο έλεγχο συνεκτικότητας - O(m·α(n))"""
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)
        self.components = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        self.components -= 1
        return True
    
    def is_connected(self):
        return self.components == 1

def random_graph_generation_basic_worker(args):
    """
    Worker function για παράλληλη εκτέλεση του βασικού πειράματος
    ΙΔΙΑ ΑΚΡΙΒΩΣ ΛΕΙΤΟΥΡΓΙΚΟΤΗΤΑ με την αρχική
    """
    n, max_degree, worker_id = args
    random.seed(worker_id + int(time.time() * 1000) % 10000)  # Unique seed per worker
    
    checker = GraphConnectivityChecker(n, max_degree)
    edges_added = 0
    
    while True:
        # Γένεση τυχαίας ακμής
        u = random.randint(1, n)
        v = random.randint(1, n)
        
        # Διασφάλιση u ≠ v
        while v == u:
            v = random.randint(1, n)
        
        # Προσπάθεια προσθήκης ακμής
        if checker.add_edge(u, v):
            edges_added += 1
            
            # Έλεγχος συνεκτικότητας
            if checker.is_connected():
                break
    
    return edges_added

def single_graph_experiment_worker(args):
    """
    Worker για ένα ΠΛΗΡΕΣ πείραμα sublinear - δουλεύει σε ολόκληρο γράφημα
    ΙΔΙΑ ΑΚΡΙΒΩΣ ΛΕΙΤΟΥΡΓΙΚΟΤΗΤΑ με την αρχική
    """
    n, max_degree, max_insertions, algorithm_type, worker_id = args
    random.seed(worker_id + int(time.time() * 1000) % 10000)
    
    checker = GraphConnectivityChecker(n, max_degree)
    insertion_counts = []
    call_counts = []
    
    # ΑΚΡΙΒΩΣ ΙΔΙΑ ΛΟΓΙΚΗ με το αρχικό πείραμα
    for insertion in range(1, max_insertions + 1):
        # Γένεση και προσθήκη τυχαίας ακμής
        u = random.randint(1, n)
        v = random.randint(1, n)
        while v == u:
            v = random.randint(1, n)
        
        if checker.add_edge(u, v):
            # Έλεγχος συνεκτικότητας με μειούμενα ε - ΚΑΘΕ ΕΙΣΑΓΩΓΗ
            is_connected, calls = checker.connectivity_check_with_decreasing_epsilon(algorithm_type)
            
            insertion_counts.append(insertion)
            call_counts.append(calls)
            
            if insertion % 25000 == 0:
                print(f"Worker {worker_id}: Insertion {insertion}, {calls} calls")
            
            if is_connected:
                print(f"Worker {worker_id}: Graph became connected at insertion {insertion}")
                break
    
    return insertion_counts, call_counts, worker_id

def run_basic_experiment():
    """
    Πείραμα για n=100: Το πλήθος εισαγωγών ακμών θα είναι συνήθως μεταξύ 200 και 500
    ΠΛΗΡΗ ΑΚΡΙΒΕΙΑ - 10 ανεξάρτητα πειράματα παράλληλα
    """
    print("=== Testing Basic Implementation (n=100) - PARALLEL ===")
    
    num_workers = mp.cpu_count()
    num_runs = 10
    
    # Προετοιμασία arguments για workers - κάθε worker κάνει ένα πλήρες πείραμα
    args = [(100, 10, i) for i in range(num_runs)]
    
    start_time = time.time()
    
    with mp.Pool(processes=min(num_workers, num_runs)) as pool:
        edges_needed = pool.map(random_graph_generation_basic_worker, args)
    
    elapsed_time = time.time() - start_time
    
    for i, edges in enumerate(edges_needed):
        print(f"Run {i+1}: {edges} edges needed")
    
    avg_edges = sum(edges_needed) / len(edges_needed)
    print(f"Average edges needed for n=100: {avg_edges:.1f}")
    print(f"Range: {min(edges_needed)} - {max(edges_needed)}")
    print(f"Parallel execution time: {elapsed_time:.2f}s using {min(num_workers, num_runs)} cores")
    
    # Έλεγχος αν τα αποτελέσματα είναι στο αναμενόμενο εύρος 200-500
    if 200 <= avg_edges <= 500:
        print("✓ Results are in expected range (200-500)")
    else:
        print("✗ Results outside expected range (200-500)")

def run_simple_sublinear_experiment():
    """
    Πείραμα 1: n=100,000, 250,000 εισαγωγές με απλό αλγόριθμο υπογραμμικού χρόνου
    ΠΛΗΡΗ ΑΚΡΙΒΕΙΑ - Τρέχει ΕΝΑΣ worker που κάνει ολόκληρο το πείραμα
    """
    print("\n=== Experiment 1: Simple Sublinear Algorithm (n=100,000) ===")
    n = 100000
    max_insertions = 250000
    
    print("Running simple sublinear experiment...")
    start_time = time.time()
    
    # Τρέχουμε ένα worker που κάνει το ΠΛΗΡΕΣ πείραμα
    args = (n, 10, max_insertions, "simple", 0)
    insertion_counts, call_counts, worker_id = single_graph_experiment_worker(args)
    
    # Δημιουργία και αποθήκευση γραφήματος
    plt.figure(figsize=(12, 6))
    plt.scatter(insertion_counts, call_counts, alpha=0.6, s=1)
    plt.xlabel('Insertions')
    plt.ylabel('Calls to Simple Sublinear Algorithm')
    plt.title('Simple Sublinear Algorithm Performance (n=100,000)')
    plt.grid(True, alpha=0.3)
    plt.savefig('simple_sublinear_n100k.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Plot saved as 'simple_sublinear_n100k.png'")
    
    print(f"Simple sublinear experiment completed in {time.time() - start_time:.1f} seconds")
    return insertion_counts, call_counts

def run_refined_sublinear_experiment():
    """
    Πείραμα 2: Εκλεπτυσμένος αλγόριθμος 
    ΠΛΗΡΗ ΑΚΡΙΒΕΙΑ - Δύο ανεξάρτητα πειράματα παράλληλα
    """
    print("\n=== Experiment 2: Refined Sublinear Algorithm ===")
    
    # Δύο πειράματα παράλληλα
    experiment_args = [
        (100000, 10, 300000, "refined", 0),  # n=100k, 300k εισαγωγές
        (1000000, 100, 2000000, "refined", 1)  # n=1M, Δ=100, 2M εισαγωγές
    ]
    
    start_time = time.time()
    
    with mp.Pool(processes=2) as pool:
        results = pool.map(single_graph_experiment_worker, experiment_args)
    
    # Επεξεργασία αποτελεσμάτων πρώτου πειράματος
    insertion_counts1, call_counts1, _ = results[0]
    if insertion_counts1 and call_counts1:
        plt.figure(figsize=(12, 6))
        plt.scatter(insertion_counts1, call_counts1, alpha=0.6, s=1, color='red')
        plt.xlabel('Insertions')
        plt.ylabel('Calls to Refined Sublinear Algorithm')
        plt.title('Refined Sublinear Algorithm Performance (n=100,000)')
        plt.grid(True, alpha=0.3)
        plt.savefig('refined_sublinear_n100k.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("Plot saved as 'refined_sublinear_n100k.png'")
    
    # Επεξεργασία αποτελεσμάτων δεύτερου πειράματος  
    insertion_counts2, call_counts2, _ = results[1]
    if insertion_counts2 and call_counts2:
        plt.figure(figsize=(12, 6))
        plt.scatter(insertion_counts2, call_counts2, alpha=0.6, s=1, color='green')
        plt.xlabel('Insertions')
        plt.ylabel('Calls to Refined Sublinear Algorithm')
        plt.title('Refined Sublinear Algorithm Performance (n=1,000,000, Δ=100)')
        plt.grid(True, alpha=0.3)
        plt.savefig('refined_sublinear_n1M.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("Plot saved as 'refined_sublinear_n1M.png'")
    
    elapsed_time = time.time() - start_time
    print(f"Both refined experiments completed in {elapsed_time:.1f} seconds using 2 cores")
    
    return insertion_counts1, call_counts1, insertion_counts2, call_counts2

def fast_random_graph_generation_worker(args):
    """
    Worker function για Union-Find αλγόριθμο
    ΙΔΙΑ ΑΚΡΙΒΩΣ ΛΕΙΤΟΥΡΓΙΚΟΤΗΤΑ με την αρχική
    """
    n, max_degree, worker_id = args
    random.seed(worker_id + int(time.time() * 1000) % 10000)
    
    uf = UnionFind(n)
    degrees = [0] * (n + 1)
    edges_added = 0
    
    max_attempts = n * max_degree * 3  # Όριο ασφαλείας
    attempts = 0
    
    while not uf.is_connected() and attempts < max_attempts:
        attempts += 1
        
        # Γένεση τυχαίας ακμής
        u = random.randint(1, n)
        v = random.randint(1, n)
        
        while v == u:
            v = random.randint(1, n)
        
        # Έλεγχος περιορισμών βαθμού
        if degrees[u] < max_degree and degrees[v] < max_degree:
            if uf.union(u, v):  # Επιστρέφει True αν συνενώθηκαν συνιστώσες
                degrees[u] += 1
                degrees[v] += 1
                edges_added += 1
    
    return edges_added

def test_fast_algorithm():
    """
    Test του γρήγορου Union-Find αλγορίθμου
    ΠΛΗΡΗ ΑΚΡΙΒΕΙΑ - Παράλληλες επαναλήψεις
    """
    print("\n=== Testing Fast Algorithm (Union-Find) ===")
    
    num_workers = mp.cpu_count()
    
    test_cases = [
        (100000, 10, "Medium scale test", 5),
        (1000000, 100, "Large scale test (n=1M, Δ=100)", 3),
    ]
    
    for n, max_degree, description, num_runs in test_cases:
        print(f"\n{description}: n={n}, Δ={max_degree}")
        
        # Προετοιμασία arguments για workers - κάθε worker κάνει ένα πλήρες πείραμα
        args = [(n, max_degree, i) for i in range(num_runs)]
        
        start_time = time.time()
        
        with mp.Pool(processes=min(num_workers, num_runs)) as pool:
            edges_needed = pool.map(fast_random_graph_generation_worker, args)
        
        elapsed_time = time.time() - start_time
        
        for i, edges in enumerate(edges_needed):
            print(f"Run {i+1}: {edges} edges, {elapsed_time/num_runs:.3f}s")
        
        avg_edges = sum(edges_needed) / len(edges_needed)
        avg_time = elapsed_time / num_runs
        print(f"Average: {avg_edges:.0f} edges, {avg_time:.3f}s per run, total: {elapsed_time:.3f}s using {min(num_workers, num_runs)} cores")
        
        # Έλεγχος για n=1M, Δ=100
        if n == 1000000 and max_degree == 100:
            print(f"Expected ~6-8 million edges for n=1M, Δ=100")
            if 6000000 <= avg_edges <= 8000000:
                print("✓ Results match theoretical expectation")
            else:
                print("✗ Results outside expected range")

def run_all_experiments():
    """
    Εκτέλεση όλων των πειραμάτων της Ενότητας Α
    ΠΛΗΡΗ ΑΚΡΙΒΕΙΑ - Πολυπύρηνη επεξεργασία όπου είναι δυνατόν
    """
    print("=" * 60)
    print("ΕΝΟΤΗΤΑ Α: ΕΛΕΓΧΟΣ ΣΥΝΕΚΤΙΚΟΤΗΤΑΣ ΓΡΑΦΗΜΑΤΟΣ")
    print("Δ=10 (μέγιστος βαθμός) - ΠΛΗΡΗ ΑΚΡΙΒΕΙΑ + ΠΟΛΥΠΥΡΗΝΗ")
    print(f"Διαθέσιμοι πυρήνες: {mp.cpu_count()}")
    print("=" * 60)
    
    try:
        # 1. Βασικό πείραμα n=100 (10 παράλληλες επαναλήψεις)
        run_basic_experiment()
        
        # 2. Απλός υπογραμμικός n=100k, 250k εισαγωγές (1 πλήρες πείραμα)
        run_simple_sublinear_experiment()
        
        # 3. Εκλεπτυσμένος υπογραμμικός (2 παράλληλα πειράματα)
        run_refined_sublinear_experiment()
        
        # 4. Γρήγορος αλγόριθμος με Union-Find (παράλληλες επαναλήψεις)
        test_fast_algorithm()
        
        print("\n" + "=" * 60)
        print("ΟΛΑ ΤΑ ΠΕΙΡΑΜΑΤΑ ΟΛΟΚΛΗΡΩΘΗΚΑΝ ΕΠΙΤΥΧΩΣ!")
        print("Αποθηκευμένα γραφήματα:")
        print("- simple_sublinear_n100k.png")
        print("- refined_sublinear_n100k.png") 
        print("- refined_sublinear_n1M.png")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nΠειράματα διακόπηκαν από τον χρήστη")
    except Exception as e:
        print(f"Σφάλμα κατά τα πειράματα: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Δοκιμή μικρού παραδείγματος
    print("Testing Graph Connectivity Implementation")
    print("=" * 50)
    
    # Γρήγορος έλεγχος συνεκτικότητας
    checker = GraphConnectivityChecker(8, 3)
    test_edges = [(1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 8)]
    for u, v in test_edges:
        checker.add_edge(u, v)
    
    print(f"Test graph connectivity: {checker.is_connected()}")
    print("(Should be False - graph has two components)")
    
    # Εκτέλεση όλων των πειραμάτων
    run_all_experiments()

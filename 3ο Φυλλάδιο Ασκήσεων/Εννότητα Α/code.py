import random
import time
import matplotlib.pyplot as plt
from collections import deque, defaultdict
import math

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
        if not hasattr(self, '_visited_array'):
            self._visited_array = [False] * (self.n + 1)
            self._visited_nodes = []
        
        # Επιλογή τυχαίου αρχικού κόμβου
        start = random.randint(1, self.n)
        
        # BFS από τον αρχικό κόμβο
        queue = deque([start])
        self._visited_array[start] = True
        self._visited_nodes.append(start)
        visited_count = 1
        
        while queue:
            node = queue.popleft()
            for neighbor in self.graph[node]:
                if not self._visited_array[neighbor]:
                    self._visited_array[neighbor] = True
                    self._visited_nodes.append(neighbor)
                    queue.append(neighbor)
                    visited_count += 1
        
        # Έλεγχος αν εξερευνήθηκαν όλοι οι κόμβοι
        is_connected = (visited_count == self.n)
        
        # Καθαρισμός μόνο των επισκεπτεί κόμβων (βελτιστοποίηση)
        for node in self._visited_nodes:
            self._visited_array[node] = False
        self._visited_nodes.clear()
        
        return is_connected
    
    def local_connectivity_check(self, seed, budget):
        """
        Ρουτίνα τοπικού ελέγχου συνεκτικότητας με budget B
        Ξεκινά BFS από το seed μέχρι να εξερευνήσει B+1 κόμβους ή να ολοκληρώσει τη διερεύνηση
        """
        if not hasattr(self, '_local_visited'):
            self._local_visited = [False] * (self.n + 1)
            self._local_visited_nodes = []
        
        queue = deque([seed])
        self._local_visited[seed] = True
        self._local_visited_nodes.append(seed)
        explored_count = 1
        
        while queue and explored_count <= budget:
            node = queue.popleft()
            for neighbor in self.graph[node]:
                if not self._local_visited[neighbor]:
                    self._local_visited[neighbor] = True
                    self._local_visited_nodes.append(neighbor)
                    queue.append(neighbor)
                    explored_count += 1
                    if explored_count > budget:
                        break
        
        # Καθαρισμός
        for node in self._local_visited_nodes:
            self._local_visited[node] = False
        self._local_visited_nodes.clear()
        
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

def random_graph_generation_basic(n, max_degree=10):
    """
    Βασικό πείραμα: γενετούρα τυχαίου γραφήματος μέχρι συνεκτικότητα
    Χρησιμοποιεί γραμμικό αλγόριθμο για έλεγχο
    """
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

def run_basic_experiment():
    """
    Πείραμα για n=100: Το πλήθος εισαγωγών ακμών θα είναι συνήθως μεταξύ 200 και 500
    """
    print("=== Testing Basic Implementation (n=100) ===")
    edges_needed = []
    for i in range(10):
        edges = random_graph_generation_basic(100)
        edges_needed.append(edges)
        print(f"Run {i+1}: {edges} edges needed")
    
    avg_edges = sum(edges_needed) / len(edges_needed)
    print(f"Average edges needed for n=100: {avg_edges:.1f}")
    print(f"Range: {min(edges_needed)} - {max(edges_needed)}")
    
    # Έλεγχος αν τα αποτελέσματα είναι στο αναμενόμενο εύρος 200-500
    if 200 <= avg_edges <= 500:
        print("✓ Results are in expected range (200-500)")
    else:
        print("✗ Results outside expected range (200-500)")

def run_simple_sublinear_experiment():
    """
    Πείραμα 1: n=100,000, 250,000 εισαγωγές με απλό αλγόριθμο υπογραμμικού χρόνου
    """
    print("\n=== Experiment 1: Simple Sublinear Algorithm (n=100,000) ===")
    n = 100000
    max_insertions = 250000
    
    insertion_counts = []
    call_counts = []
    
    print("Running simple sublinear experiment...")
    start_time = time.time()
    
    checker = GraphConnectivityChecker(n, max_degree=10)
    
    for insertion in range(1, max_insertions + 1):
        # Γένεση και προσθήκη τυχαίας ακμής
        u = random.randint(1, n)
        v = random.randint(1, n)
        while v == u:
            v = random.randint(1, n)
        
        if checker.add_edge(u, v):
            # Έλεγχος συνεκτικότητας με μειούμενα ε
            is_connected, calls = checker.connectivity_check_with_decreasing_epsilon("simple")
            
            insertion_counts.append(insertion)
            call_counts.append(calls)
            
            if insertion % 25000 == 0:
                elapsed = time.time() - start_time
                print(f"Insertion {insertion}: {calls} calls, {elapsed:.1f}s elapsed")
            
            if is_connected:
                print(f"Graph became connected at insertion {insertion}")
                break
    
    # Δημιουργία και αποθήκευση γραφήματος
    plt.figure(figsize=(12, 6))
    plt.scatter(insertion_counts, call_counts, alpha=0.6, s=1)
    plt.xlabel('Insertions')
    plt.ylabel('Calls to Simple Sublinear Algorithm')
    plt.title('Simple Sublinear Algorithm Performance (n=100,000)')
    plt.grid(True, alpha=0.3)
    plt.savefig('simple_sublinear_n100k.png', dpi=150, bbox_inches='tight')
    plt.close()  # Κλείνει το plot χωρίς εμφάνιση
    print("Plot saved as 'simple_sublinear_n100k.png'")
    
    print(f"Simple sublinear experiment completed in {time.time() - start_time:.1f} seconds")
    return insertion_counts, call_counts

def run_refined_sublinear_experiment():
    """
    Πείραμα 2: Εκλεπτυσμένος αλγόριθμος 
    - n=100,000, 300,000 εισαγωγές
    - n=1,000,000, Δ=100, 2,000,000 εισαγωγές
    """
    print("\n=== Experiment 2: Refined Sublinear Algorithm ===")
    
    # Πρώτο πείραμα: n=100,000, 300,000 εισαγωγές
    print("Testing refined algorithm with n=100,000, 300,000 insertions...")
    n = 100000
    max_insertions = 300000
    
    insertion_counts = []
    call_counts = []
    
    start_time = time.time()
    checker = GraphConnectivityChecker(n, max_degree=10)
    
    for insertion in range(1, max_insertions + 1):
        u = random.randint(1, n)
        v = random.randint(1, n)
        while v == u:
            v = random.randint(1, n)
        
        if checker.add_edge(u, v):
            is_connected, calls = checker.connectivity_check_with_decreasing_epsilon("refined")
            
            insertion_counts.append(insertion)
            call_counts.append(calls)
            
            if insertion % 30000 == 0:
                elapsed = time.time() - start_time
                print(f"Insertion {insertion}: {calls} calls, {elapsed:.1f}s elapsed")
            
            if is_connected:
                print(f"Graph became connected at insertion {insertion}")
                break
    
    # Γραφική παράσταση για n=100k
    plt.figure(figsize=(12, 6))
    plt.scatter(insertion_counts, call_counts, alpha=0.6, s=1, color='red')
    plt.xlabel('Insertions')
    plt.ylabel('Calls to Refined Sublinear Algorithm')
    plt.title('Refined Sublinear Algorithm Performance (n=100,000)')
    plt.grid(True, alpha=0.3)
    plt.savefig('refined_sublinear_n100k.png', dpi=150, bbox_inches='tight')
    plt.close()  # Κλείνει το plot χωρίς εμφάνιση
    print("Plot saved as 'refined_sublinear_n100k.png'")
    
    print(f"Refined algorithm (n=100k) completed in {time.time() - start_time:.1f} seconds")
    
    # Δεύτερο πείραμα: n=1,000,000, Δ=100, 2,000,000 εισαγωγές
    print("\nTesting refined algorithm with n=1,000,000, Δ=100, 2,000,000 insertions...")
    n = 1000000
    max_degree = 100
    max_insertions = 2000000
    
    insertion_counts_large = []
    call_counts_large = []
    
    start_time = time.time()
    checker = GraphConnectivityChecker(n, max_degree)
    
    for insertion in range(1, max_insertions + 1):
        u = random.randint(1, n)
        v = random.randint(1, n)
        while v == u:
            v = random.randint(1, n)
        
        if checker.add_edge(u, v):
            is_connected, calls = checker.connectivity_check_with_decreasing_epsilon("refined")
            
            insertion_counts_large.append(insertion)
            call_counts_large.append(calls)
            
            if insertion % 200000 == 0:
                elapsed = time.time() - start_time
                print(f"Insertion {insertion}: {calls} calls, {elapsed:.1f}s elapsed")
            
            if is_connected:
                print(f"Large graph became connected at insertion {insertion}")
                break
    
    # Γραφική παράσταση για n=1M
    plt.figure(figsize=(12, 6))
    plt.scatter(insertion_counts_large, call_counts_large, alpha=0.6, s=1, color='green')
    plt.xlabel('Insertions')
    plt.ylabel('Calls to Refined Sublinear Algorithm')
    plt.title('Refined Sublinear Algorithm Performance (n=1,000,000, Δ=100)')
    plt.grid(True, alpha=0.3)
    plt.savefig('refined_sublinear_n1M.png', dpi=150, bbox_inches='tight')
    plt.close()  # Κλείνει το plot χωρίς εμφάνιση
    print("Plot saved as 'refined_sublinear_n1M.png'")
    
    print(f"Refined algorithm (n=1M) completed in {time.time() - start_time:.1f} seconds")
    
    return insertion_counts, call_counts, insertion_counts_large, call_counts_large

def fast_random_graph_generation(n, max_degree=10):
    """
    Γρήγορος αλγόριθμος με Union-Find για μεγάλα n
    Χρόνος: σχεδόν γραμμικός O(m·α(n))
    """
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
    Για n=1,000,000 και Δ=100 αναμένουμε ~6-8 εκατομμύρια ακμές
    """
    print("\n=== Testing Fast Algorithm (Union-Find) ===")
    
    test_cases = [
        (100000, 10, "Medium scale test"),
        (1000000, 100, "Large scale test (n=1M, Δ=100)"),
    ]
    
    for n, max_degree, description in test_cases:
        print(f"\n{description}: n={n}, Δ={max_degree}")
        edges_needed = []
        times = []
        
        num_runs = 3 if n >= 1000000 else 5
        
        for i in range(num_runs):
            start_time = time.time()
            edges = fast_random_graph_generation(n, max_degree)
            elapsed = time.time() - start_time
            
            edges_needed.append(edges)
            times.append(elapsed)
            print(f"Run {i+1}: {edges} edges, {elapsed:.3f}s")
        
        avg_edges = sum(edges_needed) / len(edges_needed)
        avg_time = sum(times) / len(times)
        print(f"Average: {avg_edges:.0f} edges, {avg_time:.3f}s")
        
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
    """
    print("=" * 60)
    print("ΕΝΟΤΗΤΑ Α: ΕΛΕΓΧΟΣ ΣΥΝΕΚΤΙΚΟΤΗΤΑΣ ΓΡΑΦΗΜΑΤΟΣ")
    print("Δ=10 (μέγιστος βαθμός)")
    print("=" * 60)
    
    try:
        # 1. Βασικό πείραμα n=100
        run_basic_experiment()
        
        # 2. Απλός υπογραμμικός n=100k, 250k εισαγωγές  
        run_simple_sublinear_experiment()
        
        # 3. Εκλεπτυσμένος υπογραμμικός (δύο πειράματα)
        run_refined_sublinear_experiment()
        
        # 4. Γρήγορος αλγόριθμος με Union-Find
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

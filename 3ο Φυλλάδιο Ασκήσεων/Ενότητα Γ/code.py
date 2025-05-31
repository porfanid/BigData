import random
import matplotlib.pyplot as plt
from collections import deque, defaultdict
import time
import numpy as np

class BipartiteGraphChecker:
    """Κλάση για έλεγχο διμερότητας γραφημάτων με γραμμικούς και υπογραμμικούς αλγορίθμους"""
    
    def __init__(self):
        pass
    
    def generate_random_graph_erdos_renyi(self, num_nodes, edge_probability):
        """
        Δημιουργεί τυχαίο γράφημα Erdős-Rényi με num_nodes κόμβους 
        και πιθανότητα ακμής edge_probability
        """
        adjacency_list = defaultdict(list)
        
        # Για κάθε πιθανό ζευγάρι κόμβων
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if random.random() < edge_probability:
                    adjacency_list[i].append(j)
                    adjacency_list[j].append(i)
        
        return adjacency_list
    
    def is_bipartite_linear_time(self, graph, num_nodes):
        """
        Έλεγχος διμερότητας σε γραμμικό χρόνο O(V+E)
        Χρησιμοποιεί BFS για χρωματισμό με 2 χρώματα
        
        Args:
            graph: λεξικό με λίστες γειτνίασης
            num_nodes: αριθμός κόμβων
            
        Returns:
            bool: True αν το γράφημα είναι διμερές, False αλλιώς
        """
        node_colors = [-1] * num_nodes  # -1 = μη επισκεπτόμενος, 0/1 = χρώματα
        
        # Ελέγχουμε κάθε συνεκτική συνιστώσα
        for start_node in range(num_nodes):
            if node_colors[start_node] == -1:  # Αν δεν έχει επισκεφτεί
                # BFS από αυτόν τον κόμβο
                bfs_queue = deque([start_node])
                node_colors[start_node] = 0
                
                while bfs_queue:
                    current_node = bfs_queue.popleft()
                    
                    for neighbor in graph[current_node]:
                        if node_colors[neighbor] == -1:
                            # Χρωματίζουμε με το αντίθετο χρώμα
                            node_colors[neighbor] = 1 - node_colors[current_node]
                            bfs_queue.append(neighbor)
                        elif node_colors[neighbor] == node_colors[current_node]:
                            # Δύο γειτονικοί κόμβοι με το ίδιο χρώμα → όχι διμερές
                            return False
        
        return True
    
    def sample_nodes_without_replacement(self, total_nodes, sample_size):
        """
        Δειγματοληψία sample_size κόμβων από {0,1,...,total_nodes-1} χωρίς επανάθεση
        
        Args:
            total_nodes: συνολικός αριθμός κόμβων
            sample_size: μέγεθος δείγματος
            
        Returns:
            list: λίστα με τους επιλεγμένους κόμβους
        """
        if sample_size > total_nodes:
            sample_size = total_nodes
        
        selected_nodes = set()
        while len(selected_nodes) < sample_size:
            random_node = random.randint(0, total_nodes - 1)
            selected_nodes.add(random_node)
        
        return list(selected_nodes)
    
    def is_bipartite_sublinear_time(self, graph, num_nodes, epsilon, max_iterations=None):
        """
        Αλγόριθμος υπογραμμικού χρόνου για έλεγχο διμερότητας
        
        Args:
            graph: το γράφημα (λεξικό λιστών γειτνίασης)
            num_nodes: αριθμός κόμβων
            epsilon: παράμετρος που καθορίζει το μέγεθος δείγματος
            max_iterations: μέγιστος αριθμός επαναλήψεων
            
        Returns:
            str: "NOT_BIPARTITE" αν βρήκαμε μη-διμερότητα, "POSSIBLY_BIPARTITE" αλλιώς
        """
        # Μέγεθος δείγματος βάσει ε
        sample_size = min(num_nodes, max(1, int(1 / (epsilon**2))))
        
        if max_iterations is None:
            max_iterations = int(1 / epsilon)
        
        for iteration in range(max_iterations):
            # Δειγματοληψία κόμβων
            sampled_nodes = self.sample_nodes_without_replacement(num_nodes, sample_size)
            
            # Δημιουργία υπογραφήματος από το δείγμα με επαναδημιουργία ευρετηρίων
            sampled_nodes_set = set(sampled_nodes)
            node_mapping = {old_node: new_node for new_node, old_node in enumerate(sampled_nodes)}
            
            induced_subgraph = defaultdict(list)
            for old_node in sampled_nodes:
                new_node = node_mapping[old_node]
                for neighbor in graph[old_node]:
                    if neighbor in sampled_nodes_set:
                        new_neighbor = node_mapping[neighbor]
                        induced_subgraph[new_node].append(new_neighbor)
            
            # Έλεγχος διμερότητας στο υπογράφημα
            if not self.is_bipartite_linear_time(induced_subgraph, len(sampled_nodes)):
                return "NOT_BIPARTITE"  # Βρήκαμε μη-διμερότητα
        
        return "POSSIBLY_BIPARTITE"  # Δεν βρήκαμε μη-διμερότητα
    
    def run_monte_carlo_experiment(self, num_nodes, probability_values, num_trials=100, use_sublinear_algorithm=False):
        """
        Πείραμα Monte Carlo για εκτίμηση πιθανότητας διμερότητας
        
        Args:
            num_nodes: αριθμός κόμβων
            probability_values: λίστα με τιμές πιθανότητας p
            num_trials: αριθμός επαναλήψεων για κάθε p
            use_sublinear_algorithm: αν θα χρησιμοποιήσουμε υπογραμμικό αλγόριθμο
            
        Returns:
            list: πιθανότητες διμερότητας για κάθε p
        """
        bipartite_probabilities = []
        
        for p in probability_values:
            bipartite_count = 0
            
            for trial in range(num_trials):
                # Δημιουργία τυχαίου γραφήματος
                random_graph = self.generate_random_graph_erdos_renyi(num_nodes, p)
                
                if use_sublinear_algorithm:
                    # Χρήση αλγορίθμου υπογραμμικού χρόνου
                    is_bipartite = self.test_bipartite_with_adaptive_sublinear(random_graph, num_nodes)
                else:
                    # Χρήση αλγορίθμου γραμμικού χρόνου
                    is_bipartite = self.is_bipartite_linear_time(random_graph, num_nodes)
                
                if is_bipartite:
                    bipartite_count += 1
            
            probability = bipartite_count / num_trials
            bipartite_probabilities.append(probability)
            print(f"p = {p:.6f}, Bipartite probability = {probability:.3f}")
        
        return bipartite_probabilities
    
    def test_bipartite_with_adaptive_sublinear(self, graph, num_nodes):
        """
        Ελέγχει διμερότητα χρησιμοποιώντας πρώτα αλγόριθμο υπογραμμικού χρόνου
        με προσαρμοστικό ε, και αν χρειαστεί, τον γραμμικό
        
        Args:
            graph: το γράφημα
            num_nodes: αριθμός κόμβων
            
        Returns:
            bool: True αν το γράφημα είναι διμερές
        """
        # Ξεκινάμε με ε = 1/2 και το υποδιπλασιάζουμε
        epsilon = 0.5
        min_epsilon = 0.001  # Όριο κάτω για το ε
        
        while epsilon >= min_epsilon:
            result = self.is_bipartite_sublinear_time(graph, num_nodes, epsilon)
            
            if result == "NOT_BIPARTITE":
                return False  # Σίγουρα όχι διμερές
            
            # Υποδιπλασιάζουμε το ε για περισσότερη ακρίβεια
            epsilon /= 2
        
        # Αν φτάσαμε εδώ, τρέχουμε τον γραμμικό αλγόριθμο
        return self.is_bipartite_linear_time(graph, num_nodes)
    
    def create_probability_plots(self, p_values, probabilities, title="Bipartite Probability vs p"):
        """Δημιουργεί γραφικές παραστάσεις για τα αποτελέσματα"""
        plt.figure(figsize=(15, 6))
        
        # Γραφική με κανονικό άξονα x (p values)
        plt.subplot(1, 2, 1)
        plt.plot(p_values, probabilities, 'ro-', markersize=4, linewidth=2)
        plt.xlabel('Edge Probability (p)', fontsize=12)
        plt.ylabel('Probability of being bipartite', fontsize=12)
        plt.title(f'{title} (Linear scale)', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.ylim(-0.05, 1.05)
        
        # Γραφική με sequential index στον άξονα x
        plt.subplot(1, 2, 2)
        plt.plot(range(len(p_values)), probabilities, 'bo-', markersize=4, linewidth=2)
        plt.xlabel('Iteration Index', fontsize=12)
        plt.ylabel('Probability of being bipartite', fontsize=12)
        plt.title(f'{title} (Sequential scale)', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.ylim(-0.05, 1.05)
        
        plt.tight_layout()
        plt.show()

def run_exercise_1_linear_algorithm():
    """
    Άσκηση 1: Αλγόριθμος γραμμικού χρόνου
    n=100, p values: 1, 1/1.1, 1/1.1^2, ..., μέχρι p > 0.001
    """
    print("=== ΆΣΚΗΣΗ 1: Αλγόριθμος Γραμμικού Χρόνου ===")
    
    checker = BipartiteGraphChecker()
    num_nodes = 100
    
    # Δημιουργία p values: 1, 1/1.1, 1/1.1^2, ..., μέχρι p > 0.001
    p_values = []
    p = 1.0
    while p > 0.001:
        p_values.append(p)
        p /= 1.1
    
    print(f"Τρέχουμε πείραμα με n={num_nodes}, {len(p_values)} διαφορετικά p values")
    print("Αυτό μπορεί να πάρει λίγα λεπτά...")
    
    start_time = time.time()
    probabilities = checker.run_monte_carlo_experiment(num_nodes, p_values, num_trials=100)
    end_time = time.time()
    
    print(f"Ολοκληρώθηκε σε {end_time - start_time:.2f} δευτερόλεπτα")
    
    # Γραφικές παραστάσεις
    checker.create_probability_plots(p_values, probabilities, f"n={num_nodes}, Linear Time Algorithm")
    
    return p_values, probabilities

def run_exercise_2_sublinear_algorithm():
    """
    Άσκηση 2: Αλγόριθμος υπογραμμικού χρόνου
    n=1000, p values: 1, 1/2, 1/4, 1/8, ..., μέχρι p > 0.0009
    """
    print("\n=== ΆΣΚΗΣΗ 2: Αλγόριθμος Υπογραμμικού Χρόνου ===")
    
    checker = BipartiteGraphChecker()
    num_nodes = 1000
    
    # p values: 1, 1/2, 1/4, 1/8, ..., μέχρι p > 0.0009
    p_values = []
    p = 1.0
    while p > 0.0009:
        p_values.append(p)
        p /= 2
    
    print(f"Τρέχουμε πείραμα με n={num_nodes}, {len(p_values)} διαφορετικά p values")
    print("Χρησιμοποιούμε αλγόριθμο υπογραμμικού χρόνου...")
    
    start_time = time.time()
    probabilities = checker.run_monte_carlo_experiment(num_nodes, p_values, num_trials=100, use_sublinear_algorithm=True)
    end_time = time.time()
    
    print(f"Ολοκληρώθηκε σε {end_time - start_time:.2f} δευτερόλεπτα")
    
    # Γραφικές παραστάσεις
    checker.create_probability_plots(p_values, probabilities, f"n={num_nodes}, Sublinear Time Algorithm")
    
    return p_values, probabilities

def run_large_scale_experiments():
    """
    Δοκιμές για μεγάλα n (n=10000) με επιλεγμένες τιμές p
    """
    print("\n=== ΔΟΚΙΜΕΣ ΜΕΓΑΛΗΣ ΚΛΙΜΑΚΑΣ (n=10000) ===")
    
    checker = BipartiteGraphChecker()
    num_nodes = 10000
    
    # Επιλεγμένες τιμές p για μεγάλο n
    p_values = [1.0, 0.5, 0.25, 0.125]
    
    print(f"Τρέχουμε πείραμα με n={num_nodes} για p ∈ {p_values}")
    print("Χρησιμοποιούμε αλγόριθμο υπογραμμικού χρόνου...")
    
    start_time = time.time()
    probabilities = checker.run_monte_carlo_experiment(num_nodes, p_values, num_trials=50, use_sublinear_algorithm=True)
    end_time = time.time()
    
    print(f"Ολοκληρώθηκε σε {end_time - start_time:.2f} δευτερόλεπτα")
    
    for p, prob in zip(p_values, probabilities):
        print(f"p = {p:.3f}: Bipartite probability = {prob:.3f}")
    
    return p_values, probabilities

def run_algorithm_validation_tests():
    """Δοκιμαστικές εκτελέσεις για επαλήθευση των αλγορίθμων"""
    print("=== ΔΟΚΙΜΕΣ ΕΠΑΛΗΘΕΥΣΗΣ ΑΛΓΟΡΙΘΜΩΝ ===")
    
    checker = BipartiteGraphChecker()
    
    # Δοκιμή 1: Μικρό διμερές γράφημα (K_{2,2})
    print("Δοκιμή 1: Πλήρες διμερές γράφημα K_{2,2}")
    bipartite_graph = {0: [2, 3], 1: [2, 3], 2: [0, 1], 3: [0, 1]}
    result1 = checker.is_bipartite_linear_time(bipartite_graph, 4)
    print(f"Αποτέλεσμα: {result1} (αναμενόμενο: True)")
    
    # Δοκιμή 2: Τρίγωνο (μη-διμερές)
    print("\nΔοκιμή 2: Τρίγωνο (μη-διμερές γράφημα)")
    triangle_graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    result2 = checker.is_bipartite_linear_time(triangle_graph, 3)
    print(f"Αποτέλεσμα: {result2} (αναμενόμενο: False)")
    
    # Δοκιμή 3: Κύκλος μήκους 4 (διμερές)
    print("\nΔοκιμή 3: Κύκλος μήκους 4 (διμερές)")
    cycle4_graph = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
    result3 = checker.is_bipartite_linear_time(cycle4_graph, 4)
    print(f"Αποτέλεσμα: {result3} (αναμενόμενο: True)")
    
    # Δοκιμή 4: Κύκλος μήκους 5 (μη-διμερές)
    print("\nΔοκιμή 4: Κύκλος μήκους 5 (μη-διμερές)")
    cycle5_graph = {0: [1, 4], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [3, 0]}
    result4 = checker.is_bipartite_linear_time(cycle5_graph, 5)
    print(f"Αποτέλεσμα: {result4} (αναμενόμενο: False)")
    
    # Δοκιμή 5: Σύγκριση γραμμικού και υπογραμμικού αλγορίθμου
    print("\nΔοκιμή 5: Σύγκριση αλγορίθμων σε τυχαία γραφήματα")
    test_cases = [(10, 0.1), (10, 0.5), (10, 0.8)]
    
    for n, p in test_cases:
        graph = checker.generate_random_graph_erdos_renyi(n, p)
        linear_result = checker.is_bipartite_linear_time(graph, n)
        sublinear_result = checker.test_bipartite_with_adaptive_sublinear(graph, n)
        match = "✓" if linear_result == sublinear_result else "✗"
        print(f"n={n}, p={p}: Linear={linear_result}, Sublinear={sublinear_result} {match}")

def main():
    """Κύρια συνάρτηση που εκτελεί όλες τις ασκήσεις"""
    print("Έλεγχος Διμερότητας Γραφημάτων - Ενότητα Γ")
    print("=" * 60)
    
    # Εκτέλεση δοκιμών επαλήθευσης
    run_algorithm_validation_tests()
    
    print("\n" + "=" * 60)
    
    try:
        # Άσκηση 1: Γραμμικός αλγόριθμος
        p_vals_1, probs_1 = run_exercise_1_linear_algorithm()
        
        # Άσκηση 2: Υπογραμμικός αλγόριθμος  
        p_vals_2, probs_2 = run_exercise_2_sublinear_algorithm()
        
        # Δοκιμές μεγάλης κλίμακας
        print("\nΘέλετε να τρέξετε δοκιμές για n=10000; (y/n)")
        large_response = input().lower().strip()
        if large_response in ['y', 'yes', 'ναι', 'ν']:
            p_vals_large, probs_large = run_large_scale_experiments()
        
        # Σύγκριση αποτελεσμάτων
        print("\n" + "=" * 60)
        print("=== ΣΥΓΚΡΙΣΗ ΚΑΙ ΣΥΜΠΕΡΑΣΜΑΤΑ ===")
        print("Παρατηρήσεις:")
        print("1. Για μεγάλα p: Τα γραφήματα είναι πυκνά → σπάνια διμερή")
        print("2. Για μικρά p: Τα γραφήματα είναι αραιά → συχνά διμερή") 
        print("3. Υπάρχει απότομη μετάβαση γύρω από ένα κρίσιμο p (phase transition)")
        print("4. Ο αλγόριθμος υπογραμμικού χρόνου είναι ταχύτερος για μεγάλα n και μεγάλα p")
        print("5. Το κρίσιμο p μικραίνει καθώς το n αυξάνεται")
        
    except KeyboardInterrupt:
        print("\nΠρόγραμμα διακόπηκε από τον χρήστη.")
    except Exception as e:
        print(f"\nΣφάλμα κατά την εκτέλεση: {e}")

if __name__ == "__main__":
    # Ρύθμιση τυχαιότητας για αναπαραγωγιμότητα (προαιρετικό)
    random.seed(42)
    np.random.seed(42)
    
    main()

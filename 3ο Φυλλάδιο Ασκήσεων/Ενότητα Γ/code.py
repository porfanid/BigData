import random  # Εισαγωγή βιβλιοθήκης για τυχαία αριθμό
import matplotlib.pyplot as plt  # Εισαγωγή βιβλιοθήκης για γραφικές παραστάσεις
from collections import deque, defaultdict  # Εισαγωγή δομών δεδομένων για ουρά και προεπιλεγμένο λεξικό
import time  # Εισαγωγή βιβλιοθήκης για μέτρηση χρόνου
import numpy as np  # Εισαγωγή βιβλιοθήκης NumPy για μαθηματικές πράξεις

class BipartiteGraphChecker:
    """
    Κλάση που υλοποιεί αλγορίθμους ελέγχου διμερότητας γραφημάτων.
    
    Περιλαμβάνει:
    - Αλγόριθμο γραμμικού χρόνου O(V+E) με BFS
    - Αλγόριθμο υπογραμμικού χρόνου με δειγματοληψία
    - Δημιουργία τυχαίων γραφημάτων Erdős-Rényi
    - Πειράματα Monte Carlo για στατιστική ανάλυση
    """
    
    def __init__(self):
        """
        Κατασκευαστής της κλάσης BipartiteGraphChecker.
        Δεν χρειάζεται αρχικοποίηση παραμέτρων.
        """
        pass  # Κενή υλοποίηση - δεν χρειάζεται αρχικοποίηση
    
    def generate_random_graph_erdos_renyi(self, num_nodes, edge_probability):
        """
        Δημιουργεί τυχαίο γράφημα βάσει του μοντέλου Erdős-Rényi.
        
        Το μοντέλο Erdős-Rényi δημιουργεί γράφημα όπου κάθε πιθανή ακμή
        μεταξύ δύο κόμβων εμφανίζεται με πιθανότητα p.
        
        Args:
            num_nodes (int): Αριθμός κόμβων του γραφήματος
            edge_probability (float): Πιθανότητα ύπαρξης ακμής μεταξύ δύο κόμβων
            
        Returns:
            defaultdict: Λεξικό που αναπαριστά το γράφημα με λίστες γειτνίασης
        """
        adjacency_list = defaultdict(list)  # Δημιουργία κενού λεξικού για λίστες γειτνίασης
        
        # Εξέταση κάθε πιθανού ζεύγους κόμβων (i, j) με i < j
        for i in range(num_nodes):  # Επανάληψη για κάθε κόμβο i
            for j in range(i + 1, num_nodes):  # Επανάληψη για κάθε κόμβο j > i
                if random.random() < edge_probability:  # Έλεγχος αν θα δημιουργηθεί ακμή
                    adjacency_list[i].append(j)  # Προσθήκη του j στη λίστα γειτνίασης του i
                    adjacency_list[j].append(i)  # Προσθήκη του i στη λίστα γειτνίασης του j (μη κατευθυνόμενο γράφημα)
        
        return adjacency_list  # Επιστροφή του γραφήματος
    
    def is_bipartite_linear_time(self, graph, num_nodes):
        """
        Ελέγχει αν ένα γράφημα είναι διμερές σε γραμμικό χρόνο O(V+E).
        
        Χρησιμοποιεί αλγόριθμο BFS για να προσπαθήσει να χρωματίσει το γράφημα
        με δύο χρώματα. Αν είναι δυνατό, το γράφημα είναι διμερές.
        
        Args:
            graph (dict): Το γράφημα ως λεξικό λιστών γειτνίασης
            num_nodes (int): Αριθμός κόμβων του γραφήματος
            
        Returns:
            bool: True αν το γράφημα είναι διμερές, False αλλιώς
        """
        node_colors = [-1] * num_nodes  # Πίνακας χρωμάτων: -1=μη επισκεπτόμενος, 0/1=χρώματα
        
        # Έλεγχος κάθε συνεκτικής συνιστώσας του γραφήματος
        for start_node in range(num_nodes):  # Επανάληψη για κάθε κόμβο
            if node_colors[start_node] == -1:  # Αν ο κόμβος δεν έχει επισκεφτεί
                # Εκκίνηση BFS από τον τρέχοντα κόμβο
                bfs_queue = deque([start_node])  # Δημιουργία ουράς BFS με αρχικό κόμβο
                node_colors[start_node] = 0  # Χρωματισμός αρχικού κόμβου με χρώμα 0
                
                while bfs_queue:  # Όσο η ουρά δεν είναι κενή
                    current_node = bfs_queue.popleft()  # Εξαγωγή κόμβου από την αρχή της ουράς
                    
                    # Εξέταση όλων των γειτόνων του τρέχοντος κόμβου
                    for neighbor in graph[current_node]:  # Επανάληψη για κάθε γείτονα
                        if node_colors[neighbor] == -1:  # Αν ο γείτονας δεν έχει επισκεφτεί
                            # Χρωματισμός γείτονα με αντίθετο χρώμα από τον τρέχοντα κόμβο
                            node_colors[neighbor] = 1 - node_colors[current_node]  # 0->1 ή 1->0
                            bfs_queue.append(neighbor)  # Προσθήκη γείτονα στην ουρά
                        elif node_colors[neighbor] == node_colors[current_node]:  # Αν γείτονας έχει ίδιο χρώμα
                            # Βρέθηκε σύγκρουση χρωμάτων - το γράφημα δεν είναι διμερές
                            return False  # Επιστροφή False
        
        return True  # Αν δεν βρέθηκε σύγκρουση, το γράφημα είναι διμερές
    
    def sample_nodes_without_replacement(self, total_nodes, sample_size):
        """
        Επιλέγει τυχαία δείγμα κόμβων χωρίς επανάθεση.
        
        Χρησιμοποιεί μέθοδο rejection sampling για να εξασφαλίσει
        ότι κάθε κόμβος επιλέγεται το πολύ μία φορά.
        
        Args:
            total_nodes (int): Συνολικός αριθμός διαθέσιμων κόμβων
            sample_size (int): Μέγεθος επιθυμητού δείγματος
            
        Returns:
            list: Λίστα με τους επιλεγμένους κόμβους
        """
        if sample_size > total_nodes:  # Έλεγχος αν το δείγμα είναι μεγαλύτερο από το σύνολο
            sample_size = total_nodes  # Περιορισμός μεγέθους δείγματος
        
        selected_nodes = set()  # Σύνολο για αποθήκευση επιλεγμένων κόμβων (αποφυγή διπλότυπων)
        while len(selected_nodes) < sample_size:  # Όσο δεν έχουμε επιλέξει αρκετούς κόμβους
            random_node = random.randint(0, total_nodes - 1)  # Επιλογή τυχαίου κόμβου
            selected_nodes.add(random_node)  # Προσθήκη στο σύνολο (αυτόματα αποφεύγει διπλότυπα)
        
        return list(selected_nodes)  # Μετατροπή συνόλου σε λίστα και επιστροφή
    
    def is_bipartite_sublinear_time(self, graph, num_nodes, epsilon, max_iterations=None):
        """
        Αλγόριθμος υπογραμμικού χρόνου για έλεγχο διμερότητας.
        
        Δειγματοληπτεί υπογραφήματα και ελέγχει τη διμερότητά τους.
        Αν βρει μη-διμερές υπογράφημα, το αρχικό γράφημα είναι μη-διμερές.
        Αν δεν βρει τίποτα, το γράφημα μπορεί να είναι διμερές.
        
        Args:
            graph (dict): Το γράφημα προς έλεγχο
            num_nodes (int): Αριθμός κόμβων
            epsilon (float): Παράμετρος που καθορίζει το μέγεθος δείγματος
            max_iterations (int, optional): Μέγιστος αριθμός επαναλήψεων
            
        Returns:
            str: "NOT_BIPARTITE" αν βρέθηκε μη-διμερότητα, "POSSIBLY_BIPARTITE" αλλιώς
        """
        # Υπολογισμός μεγέθους δείγματος βάσει παραμέτρου epsilon
        sample_size = min(num_nodes, max(1, int(1 / (epsilon**2))))  # Μέγεθος ανάλογο του 1/ε²
        
        if max_iterations is None:  # Αν δεν δόθηκε μέγιστος αριθμός επαναλήψεων
            max_iterations = int(1 / epsilon)  # Ορισμός βάσει του epsilon
        
        # Εκτέλεση πολλαπλών επαναλήψεων δειγματοληψίας
        for iteration in range(max_iterations):  # Επανάληψη για κάθε iteration
            # Δειγματοληψία κόμβων χωρίς επανάθεση
            sampled_nodes = self.sample_nodes_without_replacement(num_nodes, sample_size)
            
            # Δημιουργία mapping από παλιούς σε νέους δείκτες κόμβων
            sampled_nodes_set = set(sampled_nodes)  # Μετατροπή σε σύνολο για γρήγορη αναζήτηση
            node_mapping = {old_node: new_node for new_node, old_node in enumerate(sampled_nodes)}  # Δημιουργία χάρτη αντιστοίχισης
            
            # Κατασκευή επαγόμενου υπογραφήματος από το δείγμα
            induced_subgraph = defaultdict(list)  # Δημιουργία κενού υπογραφήματος
            for old_node in sampled_nodes:  # Για κάθε κόμβο στο δείγμα
                new_node = node_mapping[old_node]  # Λήψη νέου δείκτη
                for neighbor in graph[old_node]:  # Για κάθε γείτονα του κόμβου
                    if neighbor in sampled_nodes_set:  # Αν ο γείτονας είναι επίσης στο δείγμα
                        new_neighbor = node_mapping[neighbor]  # Λήψη νέου δείκτη γείτονα
                        induced_subgraph[new_node].append(new_neighbor)  # Προσθήκη ακμής στο υπογράφημα
            
            # Έλεγχος διμερότητας του επαγόμενου υπογραφήματος
            if not self.is_bipartite_linear_time(induced_subgraph, len(sampled_nodes)):  # Αν το υπογράφημα δεν είναι διμερές
                return "NOT_BIPARTITE"  # Το αρχικό γράφημα δεν είναι διμερές
        
        return "POSSIBLY_BIPARTITE"  # Δεν βρέθηκε απόδειξη μη-διμερότητας
    
    def run_monte_carlo_experiment(self, num_nodes, probability_values, num_trials=100, use_sublinear_algorithm=False):
        """
        Εκτελεί πείραμα Monte Carlo για εκτίμηση πιθανότητας διμερότητας.
        
        Για κάθε τιμή πιθανότητας p, δημιουργεί πολλά τυχαία γραφήματα
        και υπολογίζει το ποσοστό αυτών που είναι διμερή.
        
        Args:
            num_nodes (int): Αριθμός κόμβων των γραφημάτων
            probability_values (list): Λίστα τιμών πιθανότητας ακμής
            num_trials (int): Αριθμός επαναλήψεων για κάθε p
            use_sublinear_algorithm (bool): Αν θα χρησιμοποιηθεί υπογραμμικός αλγόριθμος
            
        Returns:
            list: Πιθανότητες διμερότητας για κάθε p
        """
        bipartite_probabilities = []  # Λίστα για αποθήκευση αποτελεσμάτων
        
        # Επανάληψη για κάθε τιμή πιθανότητας
        for p in probability_values:  # Για κάθε πιθανότητα ακμής p
            bipartite_count = 0  # Μετρητής διμερών γραφημάτων
            
            # Εκτέλεση πολλαπλών δοκιμών για την τρέχουσα πιθανότητα
            for trial in range(num_trials):  # Για κάθε δοκιμή
                # Δημιουργία τυχαίου γραφήματος Erdős-Rényi
                random_graph = self.generate_random_graph_erdos_renyi(num_nodes, p)
                
                # Επιλογή αλγορίθμου ελέγχου διμερότητας
                if use_sublinear_algorithm:  # Αν επιλέχθηκε υπογραμμικός αλγόριθμος
                    # Χρήση προσαρμοστικού υπογραμμικού αλγορίθμου
                    is_bipartite = self.test_bipartite_with_adaptive_sublinear(random_graph, num_nodes)
                else:  # Αλλιώς
                    # Χρήση κλασικού γραμμικού αλγορίθμου
                    is_bipartite = self.is_bipartite_linear_time(random_graph, num_nodes)
                
                if is_bipartite:  # Αν το γράφημα είναι διμερές
                    bipartite_count += 1  # Αύξηση μετρητή
            
            # Υπολογισμός πιθανότητας διμερότητας για την τρέχουσα p
            probability = bipartite_count / num_trials  # Ποσοστό διμερών γραφημάτων
            bipartite_probabilities.append(probability)  # Προσθήκη στα αποτελέσματα
            print(f"p = {p:.6f}, Bipartite probability = {probability:.3f}")  # Εκτύπωση αποτελέσματος
        
        return bipartite_probabilities  # Επιστροφή όλων των πιθανοτήτων
    
    def test_bipartite_with_adaptive_sublinear(self, graph, num_nodes):
        """
        Ελέγχει διμερότητα με προσαρμοστικό υπογραμμικό αλγόριθμο.
        
        Ξεκινά με μεγάλο epsilon και το μειώνει σταδιακά μέχρι να βρει
        σίγουρη απάντηση ή να φτάσει στο όριο ακρίβειας.
        
        Args:
            graph (dict): Το γράφημα προς έλεγχο
            num_nodes (int): Αριθμός κόμβων
            
        Returns:
            bool: True αν το γράφημα είναι διμερές
        """
        # Αρχικοποίηση παραμέτρων προσαρμοστικού αλγορίθμου
        epsilon = 0.5  # Αρχική τιμή epsilon
        min_epsilon = 0.001  # Ελάχιστη επιτρεπτή τιμή epsilon
        
        # Σταδιακή μείωση epsilon μέχρι να βρεθεί σίγουρη απάντηση
        while epsilon >= min_epsilon:  # Όσο το epsilon είναι πάνω από το όριο
            # Εκτέλεση υπογραμμικού αλγορίθμου με τρέχον epsilon
            result = self.is_bipartite_sublinear_time(graph, num_nodes, epsilon)
            
            if result == "NOT_BIPARTITE":  # Αν βρέθηκε σίγουρη απόδειξη μη-διμερότητας
                return False  # Το γράφημα δεν είναι διμερές
            
            # Υποδιπλασιασμός epsilon για αυξημένη ακρίβεια
            epsilon /= 2  # Μείωση epsilon κατά το ήμισυ
        
        # Αν δεν βρέθηκε σίγουρη απάντηση, χρήση γραμμικού αλγορίθμου
        return self.is_bipartite_linear_time(graph, num_nodes)  # Οριστικός έλεγχος
    
    def create_probability_plots(self, p_values, probabilities, title="Bipartite Probability vs p"):
        """
        Δημιουργεί γραφικές παραστάσεις των αποτελεσμάτων.
        
        Παράγει δύο γραφήματα: ένα με γραμμικό άξονα p και ένα με
        σειριακούς δείκτες για καλύτερη οπτικοποίηση της μετάβασης φάσης.
        
        Args:
            p_values (list): Τιμές πιθανότητας ακμής
            probabilities (list): Αντίστοιχες πιθανότητες διμερότητας
            title (str): Τίτλος των γραφημάτων
        """
        plt.figure(figsize=(15, 6))  # Δημιουργία παραθύρου γραφημάτων με καθορισμένο μέγεθος
        
        # Πρώτο γράφημα: Γραμμικός άξονας p
        plt.subplot(1, 2, 1)  # Δημιουργία πρώτου υπογραφήματος
        plt.plot(p_values, probabilities, 'ro-', markersize=4, linewidth=2)  # Σχεδίαση γραμμής με κόκκινα σημεία
        plt.xlabel('Edge Probability (p)', fontsize=12)  # Ετικέτα άξονα x
        plt.ylabel('Probability of being bipartite', fontsize=12)  # Ετικέτα άξονα y
        plt.title(f'{title} (Linear scale)', fontsize=14)  # Τίτλος γραφήματος
        plt.grid(True, alpha=0.3)  # Προσθήκη πλέγματος με διαφάνεια
        plt.ylim(-0.05, 1.05)  # Ορισμός ορίων άξονα y
        
        # Δεύτερο γράφημα: Σειριακός άξονας
        plt.subplot(1, 2, 2)  # Δημιουργία δεύτερου υπογραφήματος
        plt.plot(range(len(p_values)), probabilities, 'bo-', markersize=4, linewidth=2)  # Σχεδίαση με μπλε σημεία
        plt.xlabel('Iteration Index', fontsize=12)  # Ετικέτα άξονα x
        plt.ylabel('Probability of being bipartite', fontsize=12)  # Ετικέτα άξονα y
        plt.title(f'{title} (Sequential scale)', fontsize=14)  # Τίτλος γραφήματος
        plt.grid(True, alpha=0.3)  # Προσθήκη πλέγματος
        plt.ylim(-0.05, 1.05)  # Ορισμός ορίων άξονα y
        
        plt.tight_layout()  # Αυτόματη ρύθμιση διάταξης
        plt.show()  # Εμφάνιση γραφημάτων

def run_exercise_1_linear_algorithm():
    """
    Εκτελεί την Άσκηση 1: Αλγόριθμος γραμμικού χρόνου.
    
    Δημιουργεί γραφήματα με n=100 κόμβους και τιμές p που ακολουθούν
    τη σειρά 1, 1/1.1, 1/1.1², ... μέχρι p > 0.001.
    Χρησιμοποιεί τον κλασικό γραμμικό αλγόριθμο BFS.
    
    Returns:
        tuple: Τιμές p και αντίστοιχες πιθανότητες διμερότητας
    """
    print("=== ΆΣΚΗΣΗ 1: Αλγόριθμος Γραμμικού Χρόνου ===")  # Εκτύπωση τίτλου
    
    checker = BipartiteGraphChecker()  # Δημιουργία αντικειμένου ελέγχου
    num_nodes = 100  # Ορισμός αριθμού κόμβων
    
    # Δημιουργία σειράς τιμών p: 1, 1/1.1, 1/1.1², ...
    p_values = []  # Λίστα για τιμές p
    p = 1.0  # Αρχική τιμή p
    while p > 0.001:  # Όσο p > 0.001
        p_values.append(p)  # Προσθήκη τρέχουσας τιμής
        p /= 1.1  # Διαίρεση με 1.1
    
    print(f"Τρέχουμε πείραμα με n={num_nodes}, {len(p_values)} διαφορετικά p values")  # Πληροφορίες πειράματος
    print("Αυτό μπορεί να πάρει λίγα λεπτά...")  # Προειδοποίηση για χρόνο εκτέλεσης
    
    start_time = time.time()  # Καταγραφή χρόνου έναρξης
    # Εκτέλεση πειράματος Monte Carlo με γραμμικό αλγόριθμο
    probabilities = checker.run_monte_carlo_experiment(num_nodes, p_values, num_trials=100)
    end_time = time.time()  # Καταγραφή χρόνου λήξης
    
    print(f"Ολοκληρώθηκε σε {end_time - start_time:.2f} δευτερόλεπτα")  # Εκτύπωση χρόνου εκτέλεσης
    
    # Δημιουργία γραφικών παραστάσεων
    checker.create_probability_plots(p_values, probabilities, f"n={num_nodes}, Linear Time Algorithm")
    
    return p_values, probabilities  # Επιστροφή αποτελεσμάτων

def run_exercise_2_sublinear_algorithm():
    """
    Εκτελεί την Άσκηση 2: Αλγόριθμος υπογραμμικού χρόνου.
    
    Δημιουργεί γραφήματα με n=1000 κόμβους και τιμές p που ακολουθούν
    τη σειρά 1, 1/2, 1/4, 1/8, ... μέχρι p > 0.0009.
    Χρησιμοποιεί τον υπογραμμικό αλγόριθμο με δειγματοληψία.
    
    Returns:
        tuple: Τιμές p και αντίστοιχες πιθανότητες διμερότητας
    """
    print("\n=== ΆΣΚΗΣΗ 2: Αλγόριθμος Υπογραμμικού Χρόνου ===")  # Εκτύπωση τίτλου
    
    checker = BipartiteGraphChecker()  # Δημιουργία αντικειμένου ελέγχου
    num_nodes = 1000  # Ορισμός αριθμού κόμβων (μεγαλύτερος από Άσκηση 1)
    
    # Δημιουργία σειράς τιμών p: 1, 1/2, 1/4, 1/8, ...
    p_values = []  # Λίστα για τιμές p
    p = 1.0  # Αρχική τιμή p
    while p > 0.0009:  # Όσο p > 0.0009
        p_values.append(p)  # Προσθήκη τρέχουσας τιμής
        p /= 2  # Διαίρεση με 2
    
    print(f"Τρέχουμε πείραμα με n={num_nodes}, {len(p_values)} διαφορετικά p values")  # Πληροφορίες πειράματος
    print("Χρησιμοποιούμε αλγόριθμο υπογραμμικού χρόνου...")  # Ενημέρωση για αλγόριθμο
    
    start_time = time.time()  # Καταγραφή χρόνου έναρξης
    # Εκτέλεση πειράματος Monte Carlo με υπογραμμικό αλγόριθμο
    probabilities = checker.run_monte_carlo_experiment(num_nodes, p_values, num_trials=100, use_sublinear_algorithm=True)
    end_time = time.time()  # Καταγραφή χρόνου λήξης
    
    print(f"Ολοκληρώθηκε σε {end_time - start_time:.2f} δευτερόλεπτα")  # Εκτύπωση χρόνου εκτέλεσης
   
    # Δημιουργία γραφικών παραστάσεων
    checker.create_probability_plots(p_values, probabilities, f"n={num_nodes}, Sublinear Time Algorithm")
   
    return p_values, probabilities  # Επιστροφή αποτελεσμάτων

def run_large_scale_experiments():
   """
   Εκτελεί δοκιμές μεγάλης κλίμακας για n=10000 κόμβους.
   
   Χρησιμοποιεί επιλεγμένες τιμές p για να δοκιμάσει την απόδοση
   του υπογραμμικού αλγορίθμου σε μεγάλα γραφήματα.
   
   Returns:
       tuple: Τιμές p και αντίστοιχες πιθανότητες διμερότητας
   """
   print("\n=== ΔΟΚΙΜΕΣ ΜΕΓΑΛΗΣ ΚΛΙΜΑΚΑΣ (n=10000) ===")  # Εκτύπωση τίτλου
   
   checker = BipartiteGraphChecker()  # Δημιουργία αντικειμένου ελέγχου
   num_nodes = 10000  # Ορισμός μεγάλου αριθμού κόμβων
   
   # Επιλεγμένες τιμές p για δοκιμή σε μεγάλα γραφήματα
   p_values = [1.0, 0.5, 0.25, 0.125]  # Συγκεκριμένες τιμές p
   
   print(f"Τρέχουμε πείραμα με n={num_nodes} για p ∈ {p_values}")  # Πληροφορίες πειράματος
   print("Χρησιμοποιούμε αλγόριθμο υπογραμμικού χρόνου...")  # Ενημέρωση για αλγόριθμο
   
   start_time = time.time()  # Καταγραφή χρόνου έναρξης
   # Εκτέλεση πειράματος με λιγότερες δοκιμές λόγω μεγέθους
   probabilities = checker.run_monte_carlo_experiment(num_nodes, p_values, num_trials=50, use_sublinear_algorithm=True)
   end_time = time.time()  # Καταγραφή χρόνου λήξης
   
   print(f"Ολοκληρώθηκε σε {end_time - start_time:.2f} δευτερόλεπτα")  # Εκτύπωση χρόνου εκτέλεσης
   
   # Εκτύπωση αποτελεσμάτων
   for p, prob in zip(p_values, probabilities):  # Για κάθε ζεύγος (p, πιθανότητα)
       print(f"p = {p:.3f}: Bipartite probability = {prob:.3f}")  # Εκτύπωση αποτελέσματος
   
   return p_values, probabilities  # Επιστροφή αποτελεσμάτων

def run_algorithm_validation_tests():
   """
   Εκτελεί δοκιμές επαλήθευσης για τους αλγορίθμους.
   
   Δοκιμάζει τους αλγορίθμους σε γνωστά γραφήματα με προβλέψιμα
   αποτελέσματα για να επαληθεύσει την ορθότητά τους.
   """
   print("=== ΔΟΚΙΜΕΣ ΕΠΑΛΗΘΕΥΣΗΣ ΑΛΓΟΡΙΘΜΩΝ ===")  # Εκτύπωση τίτλου
   
   checker = BipartiteGraphChecker()  # Δημιουργία αντικειμένου ελέγχου
   
   # Δοκιμή 1: Πλήρες διμερές γράφημα K_{2,2}
   print("Δοκιμή 1: Πλήρες διμερές γράφημα K_{2,2}")  # Περιγραφή δοκιμής
   # Δημιουργία K_{2,2}: κόμβοι {0,1} συνδέονται με κόμβους {2,3}
   bipartite_graph = {0: [2, 3], 1: [2, 3], 2: [0, 1], 3: [0, 1]}  # Λίστες γειτνίασης
   result1 = checker.is_bipartite_linear_time(bipartite_graph, 4)  # Έλεγχος διμερότητας
   print(f"Αποτέλεσμα: {result1} (αναμενόμενο: True)")  # Εκτύπωση αποτελέσματος
   
   # Δοκιμή 2: Τρίγωνο (μη-διμερές γράφημα)
   print("\nΔοκιμή 2: Τρίγωνο (μη-διμερές γράφημα)")  # Περιγραφή δοκιμής
   # Δημιουργία τριγώνου: κάθε κόμβος συνδέεται με τους άλλους δύο
   triangle_graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}  # Λίστες γειτνίασης
   result2 = checker.is_bipartite_linear_time(triangle_graph, 3)  # Έλεγχος διμερότητας
   print(f"Αποτέλεσμα: {result2} (αναμενόμενο: False)")  # Εκτύπωση αποτελέσματος
   
   # Δοκιμή 3: Κύκλος μήκους 4 (διμερές)
   print("\nΔοκιμή 3: Κύκλος μήκους 4 (διμερές)")  # Περιγραφή δοκιμής
   # Δημιουργία τετραγώνου: 0-1-2-3-0
   cycle4_graph = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}  # Λίστες γειτνίασης
   result3 = checker.is_bipartite_linear_time(cycle4_graph, 4)  # Έλεγχος διμερότητας
   print(f"Αποτέλεσμα: {result3} (αναμενόμενο: True)")  # Εκτύπωση αποτελέσματος
   
   # Δοκιμή 4: Κύκλος μήκους 5 (μη-διμερές)
   print("\nΔοκιμή 4: Κύκλος μήκους 5 (μη-διμερές)")  # Περιγραφή δοκιμής
   # Δημιουργία πενταγώνου: 0-1-2-3-4-0
   cycle5_graph = {0: [1, 4], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [3, 0]}  # Λίστες γειτνίασης
   result4 = checker.is_bipartite_linear_time(cycle5_graph, 5)  # Έλεγχος διμερότητας
   print(f"Αποτέλεσμα: {result4} (αναμενόμενο: False)")  # Εκτύπωση αποτελέσματος
   
   # Δοκιμή 5: Σύγκριση γραμμικού και υπογραμμικού αλγορίθμου
   print("\nΔοκιμή 5: Σύγκριση αλγορίθμων σε τυχαία γραφήματα")  # Περιγραφή δοκιμής
   test_cases = [(10, 0.1), (10, 0.5), (10, 0.8)]  # Περιπτώσεις δοκιμής (n, p)
   
   # Δοκιμή συμφωνίας αλγορίθμων σε τυχαία γραφήματα
   for n, p in test_cases:  # Για κάθε περίπτωση δοκιμής
       graph = checker.generate_random_graph_erdos_renyi(n, p)  # Δημιουργία τυχαίου γραφήματος
       linear_result = checker.is_bipartite_linear_time(graph, n)  # Αποτέλεσμα γραμμικού αλγορίθμου
       sublinear_result = checker.test_bipartite_with_adaptive_sublinear(graph, n)  # Αποτέλεσμα υπογραμμικού αλγορίθμου
       match = "✓" if linear_result == sublinear_result else "✗"  # Σύμβολο συμφωνίας
       print(f"n={n}, p={p}: Linear={linear_result}, Sublinear={sublinear_result} {match}")  # Εκτύπωση σύγκρισης

def main():
   """
   Κύρια συνάρτηση που ορχηστρώνει την εκτέλεση όλων των ασκήσεων.
   
   Εκτελεί με τη σειρά:
   1. Δοκιμές επαλήθευσης αλγορίθμων
   2. Άσκηση 1 με γραμμικό αλγόριθμο
   3. Άσκηση 2 με υπογραμμικό αλγόριθμο
   4. Προαιρετικές δοκιμές μεγάλης κλίμακας
   5. Ανάλυση και σύγκριση αποτελεσμάτων
   """
   print("Έλεγχος Διμερότητας Γραφημάτων - Ενότητα Γ")  # Τίτλος προγράμματος
   print("=" * 60)  # Διακοσμητική γραμμή
   
   # Εκτέλεση δοκιμών επαλήθευσης αλγορίθμων
   run_algorithm_validation_tests()  # Έλεγχος ορθότητας αλγορίθμων
   
   print("\n" + "=" * 60)  # Διαχωριστική γραμμή
   
   try:  # Χειρισμός εξαιρέσεων
       # Άσκηση 1: Αλγόριθμος γραμμικού χρόνου
       p_vals_1, probs_1 = run_exercise_1_linear_algorithm()  # Εκτέλεση πρώτης άσκησης
       
       # Άσκηση 2: Αλγόριθμος υπογραμμικού χρόνου  
       p_vals_2, probs_2 = run_exercise_2_sublinear_algorithm()  # Εκτέλεση δεύτερης άσκησης
       
       # Προαιρετικές δοκιμές μεγάλης κλίμακας
       print("\nΘέλετε να τρέξετε δοκιμές για n=10000; (y/n)")  # Ερώτηση για επιπλέον δοκιμές
       large_response = input().lower().strip()  # Λήψη απάντησης χρήστη
       if large_response in ['y', 'yes', 'ναι', 'ν']:  # Αν ο χρήστης συμφωνεί
           p_vals_large, probs_large = run_large_scale_experiments()  # Εκτέλεση δοκιμών μεγάλης κλίμακας
       
       # Σύγκριση και ανάλυση αποτελεσμάτων
       print("\n" + "=" * 60)  # Διαχωριστική γραμμή
       print("=== ΣΥΓΚΡΙΣΗ ΚΑΙ ΣΥΜΠΕΡΑΣΜΑΤΑ ===")  # Τίτλος ενότητας
       print("Παρατηρήσεις:")  # Εισαγωγή παρατηρήσεων
       print("1. Για μεγάλα p: Τα γραφήματα είναι πυκνά → σπάνια διμερή")  # Παρατήρηση 1
       print("2. Για μικρά p: Τα γραφήματα είναι αραιά → συχνά διμερή")  # Παρατήρηση 2
       print("3. Υπάρχει απότομη μετάβαση γύρω από ένα κρίσιμο p (phase transition)")  # Παρατήρηση 3
       print("4. Ο αλγόριθμος υπογραμμικού χρόνου είναι ταχύτερος για μεγάλα n και μεγάλα p")  # Παρατήρηση 4
       print("5. Το κρίσιμο p μικραίνει καθώς το n αυξάνεται")  # Παρατήρηση 5
       
   except KeyboardInterrupt:  # Αν ο χρήστης διακόψει το πρόγραμμα
       print("\nΠρόγραμμα διακόπηκε από τον χρήστη.")  # Μήνυμα διακοπής
   except Exception as e:  # Αν προκύψει άλλη εξαίρεση
       print(f"\nΣφάλμα κατά την εκτέλεση: {e}")  # Μήνυμα σφάλματος

if __name__ == "__main__":
   """
   Σημείο εκκίνησης του προγράμματος.
   
   Ρυθμίζει τις σπόρους τυχαιότητας για αναπαραγωγιμότητα
   και καλεί την κύρια συνάρτηση.
   """
   # Ρύθμιση σπόρων τυχαιότητας για αναπαραγωγιμότητα αποτελεσμάτων
   random.seed(42)  # Σπόρος για βιβλιοθήκη random
   np.random.seed(42)  # Σπόρος για NumPy
   
   main()  # Εκκίνηση κύριας συνάρτησης

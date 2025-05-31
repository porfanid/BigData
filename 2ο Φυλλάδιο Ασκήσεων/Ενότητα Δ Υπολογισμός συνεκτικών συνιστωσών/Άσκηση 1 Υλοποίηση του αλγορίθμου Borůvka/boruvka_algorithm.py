# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr
import random
import time
import matplotlib.pyplot as plt
from collections import defaultdict

class TrivialL0Sampler:
    """
    Κλάση που υλοποιεί έναν απλό L0 sampler για διανύσματα.
    Διατηρεί όλες τις μη-μηδενικές συντεταγμένες και επιτρέπει τυχαία δειγματοληψία.
    Χρησιμοποιείται για την αναπαράσταση διανυσμάτων πρόσπτωσης των κόμβων.
    """
    
    def __init__(self):
        """
        Αρχικοποίηση του sampler.
        Δημιουργεί λεξικό για αποθήκευση μη-μηδενικών συντεταγμένων.
        """
        # Λεξικό που αποθηκεύει συντεταγμένη -> τιμή για μη-μηδενικές συντεταγμένες
        self.non_zero_coords = {}
    
    def update(self, coord, value):
        """
        Ενημερώνει την τιμή μιας συντεταγμένης στο διάνυσμα.
        
        Args:
            coord: Η συντεταγμένη που θα ενημερωθεί
            value: Η τιμή που θα προστεθεί στη συντεταγμένη
        """
        # Έλεγχος αν η συντεταγμένη υπάρχει ήδη
        if coord in self.non_zero_coords:
            # Προσθήκη της νέας τιμής στην υπάρχουσα
            self.non_zero_coords[coord] += value
            # Αν η συνολική τιμή γίνει μηδέν, διαγράφουμε τη συντεταγμένη
            if self.non_zero_coords[coord] == 0:
                del self.non_zero_coords[coord]
        else:
            # Αν η συντεταγμένη δεν υπάρχει και η τιμή δεν είναι μηδέν, την προσθέτουμε
            if value != 0:
                self.non_zero_coords[coord] = value
    
    def sample(self):
        """
        Επιστρέφει μια τυχαία μη-μηδενική συντεταγμένη.
        
        Returns:
            Τυχαία συντεταγμένη ή None αν όλες οι συντεταγμένες είναι μηδέν
        """
        # Έλεγχος αν υπάρχουν μη-μηδενικές συντεταγμένες
        if not self.non_zero_coords:
            return None
        # Επιστροφή τυχαίας συντεταγμένης από τις διαθέσιμες
        return random.choice(list(self.non_zero_coords.keys()))
    
    def is_zero(self):
        """
        Ελέγχει αν το διάνυσμα είναι μηδενικό (όλες οι συντεταγμένες είναι μηδέν).
        
        Returns:
            True αν το διάνυσμα είναι μηδενικό, False αλλιώς
        """
        return len(self.non_zero_coords) == 0
    
    def copy(self):
        """
        Δημιουργεί και επιστρέφει ένα αντίγραφο του τρέχοντος sampler.
        
        Returns:
            Νέο TrivialL0Sampler που είναι αντίγραφο του τρέχοντος
        """
        # Δημιουργία νέου sampler
        new_sampler = TrivialL0Sampler()
        # Αντιγραφή του λεξικού με τις μη-μηδενικές συντεταγμένες
        new_sampler.non_zero_coords = self.non_zero_coords.copy()
        return new_sampler
    
    def add_sampler(self, other):
        """
        Προσθέτει άλλον sampler στον τρέχοντα (πρόσθεση διανυσμάτων).
        
        Args:
            other: Ο sampler που θα προστεθεί στον τρέχοντα
        """
        # Για κάθε συντεταγμένη του άλλου sampler
        for coord, value in other.non_zero_coords.items():
            # Ενημέρωση της αντίστοιχης συντεταγμένης στον τρέχοντα sampler
            self.update(coord, value)

def encode_edge(u, v, n):
    """
    Κωδικοποιεί μια ακμή (u,v) σε συντεταγμένη διανύσματος.
    Εξασφαλίζει ότι η κωδικοποίηση είναι συμμετρική (u,v) == (v,u).
    
    Args:
        u, v: Οι κόμβοι της ακμής
        n: Ο συνολικός αριθμός κόμβων (δεν χρησιμοποιείται εδώ)
    
    Returns:
        Tuple (u,v) με u <= v για συμμετρική αναπαράσταση
    """
    # Εξασφάλιση ότι u <= v για συνεπή κωδικοποίηση
    if u > v:
        u, v = v, u
    # Επιστροφή tuple αντί για μεγάλο αριθμό για αποφυγή overflow
    return (u, v)

def decode_edge(coord):
    """
    Αποκωδικοποιεί συντεταγμένη διανύσματος σε ακμή (u,v).
    
    Args:
        coord: Η κωδικοποιημένη συντεταγμένη (tuple)
    
    Returns:
        Tuple (u,v) που αναπαριστά την ακμή
    """
    # Η συντεταγμένη είναι ήδη tuple (u, v)
    return coord

class SimpleUnionFind:
    """
    Απλή υλοποίηση δομής Union-Find για επαλήθευση των αποτελεσμάτων.
    Χρησιμοποιείται για σύγκριση με τον αλγόριθμο Borůvka.
    """
    
    def __init__(self, n):
        """
        Αρχικοποίηση δομής Union-Find για n κόμβους.
        
        Args:
            n: Αριθμός κόμβων
        """
        # Κάθε κόμβος αρχικά είναι γονέας του εαυτού του
        self.parent = list(range(n + 1))
        # Rank κάθε κόμβου για βελτιστοποίηση union operations
        self.rank = [0] * (n + 1)
    
    def find(self, x):
        """
        Βρίσκει τον εκπρόσωπο της συνεκτικής συνιστώσας που ανήκει ο κόμβος x.
        Χρησιμοποιεί path compression για βελτιστοποίηση.
        
        Args:
            x: Ο κόμβος για τον οποίο ψάχνουμε τον εκπρόσωπο
        
        Returns:
            Ο εκπρόσωπος της συνεκτικής συνιστώσας
        """
        # Αν ο κόμβος δεν είναι γονέας του εαυτού του
        if self.parent[x] != x:
            # Path compression: κάνουμε τον κόμβο να δείχνει απευθείας στον εκπρόσωπο
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """
        Ενώνει τις συνεκτικές συνιστώσες που περιέχουν τους κόμβους x και y.
        
        Args:
            x, y: Οι κόμβοι των οποίων οι συνιστώσες θα ενωθούν
        """
        # Βρίσκουμε τους εκπροσώπους των δύο συνιστωσών
        px, py = self.find(x), self.find(y)
        # Αν ανήκουν ήδη στην ίδια συνιστώσα, δεν κάνουμε τίποτα
        if px == py:
            return
        # Union by rank: η συνιστώσα με μικρότερο rank γίνεται παιδί της άλλης
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        # Αν τα ranks είναι ίσα, αυξάνουμε το rank του νέου εκπροσώπου
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
    
    def get_components(self):
        """
        Επιστρέφει όλες τις συνεκτικές συνιστώσες.
        
        Returns:
            Λεξικό με εκπρόσωπο -> σύνολο κόμβων της συνιστώσας
        """
        # Λεξικό για ομαδοποίηση κόμβων ανά συνιστώσα
        components = defaultdict(set)
        # Για κάθε κόμβο, βρίσκουμε τον εκπρόσωπό του και τον προσθέτουμε στη συνιστώσα
        for i in range(1, len(self.parent)):
            if i < len(self.parent):
                components[self.find(i)].add(i)
        return dict(components)

class BoruvkaGraph:
    """
    Κλάση που αναπαριστά γράφο για τον αλγόριθμο Borůvka.
    Χρησιμοποιεί διανύσματα πρόσπτωσης για αποδοτική εύρεση συνεκτικών συνιστωσών.
    """
    
    def __init__(self, n):
        """
        Αρχικοποίηση γραφήματος με n κόμβους.
        
        Args:
            n: Αριθμός κόμβων στο γράφημα
        """
        # Αποθήκευση αριθμού κόμβων
        self.n = n
        # Λεξικό που αντιστοιχεί κάθε κόμβο σε διάνυσμα πρόσπτωσης
        self.incident_vectors = {}
        # Μετρητής για παράλληλες ακμές (ακμή -> πλήθος εμφανίσεων)
        self.edge_counts = defaultdict(int)
        
        # Αρχικοποίηση διανυσμάτων πρόσπτωσης για κάθε κόμβο
        for i in range(1, n + 1):
            self.incident_vectors[i] = TrivialL0Sampler()
    
    def add_edge(self, u, v):
        """
        Προσθέτει ακμή (u,v) στο γράφημα.
        Ενημερώνει τα διανύσματα πρόσπτωσης των αντίστοιχων κόμβων.
        
        Args:
            u, v: Οι κόμβοι της ακμής που προστίθεται
        """
        # Αγνοούμε self-loops (ακμές από κόμβο σε τον εαυτό του)
        if u == v:
            return
        
        # Δημιουργία συμμετρικής αναπαράστασης της ακμής
        edge = tuple(sorted([u, v]))
        # Αύξηση μετρητή για αυτήν την ακμή (υποστήριξη παράλληλων ακμών)
        self.edge_counts[edge] += 1
        
        # Κωδικοποίηση ακμής σε συντεταγμένη διανύσματος
        coord = encode_edge(u, v, self.n)
        
        # Ενημέρωση διανυσμάτων πρόσπτωσης μόνο την πρώτη φορά που βλέπουμε την ακμή
        if self.edge_counts[edge] == 1:
            # Προσθήκη της συντεταγμένης στα διανύσματα πρόσπτωσης των δύο κόμβων
            self.incident_vectors[u].update(coord, 1)
            self.incident_vectors[v].update(coord, 1)
    
    def remove_edge(self, u, v):
        """
        Αφαιρεί ακμή (u,v) από το γράφημα.
        Ενημερώνει τα διανύσματα πρόσπτωσης των αντίστοιχων κόμβων.
        
        Args:
            u, v: Οι κόμβοι της ακμής που αφαιρείται
        """
        # Δημιουργία συμμετρικής αναπαράστασης της ακμής
        edge = tuple(sorted([u, v]))
        # Έλεγχος αν η ακμή υπάρχει
        if edge not in self.edge_counts or self.edge_counts[edge] == 0:
            return
        
        # Μείωση μετρητή της ακμής
        self.edge_counts[edge] -= 1
        # Κωδικοποίηση ακμής σε συντεταγμένη διανύσματος
        coord = encode_edge(u, v, self.n)
        
        # Ενημέρωση διανυσμάτων πρόσπτωσης μόνο αν δεν υπάρχουν άλλες παράλληλες ακμές
        if self.edge_counts[edge] == 0:
            # Αφαίρεση της συντεταγμένης από τα διανύσματα πρόσπτωσης των δύο κόμβων
            self.incident_vectors[u].update(coord, -1)
            self.incident_vectors[v].update(coord, -1)
            # Διαγραφή της ακμής από τον μετρητή
            del self.edge_counts[edge]
    
    def get_incident_edges(self, node):
        """
        Επιστρέφει όλες τις ακμές που προσπίπτουν σε έναν κόμβο.
        
        Args:
            node: Ο κόμβος για τον οποίο θέλουμε τις προσπίπτουσες ακμές
        
        Returns:
            Λίστα με tuples (u,v) που αναπαριστούν τις προσπίπτουσες ακμές
        """
        # Λήψη όλων των μη-μηδενικών συντεταγμένων από το διάνυσμα πρόσπτωσης
        incident_coords = list(self.incident_vectors[node].non_zero_coords.keys())
        edges = []
        # Αποκωδικοποίηση κάθε συντεταγμένης σε ακμή
        for coord in incident_coords:
            u, v = decode_edge(coord)
            edges.append((u, v))
        return edges
    
    def get_all_edges(self):
        """
        Επιστρέφει όλες τις ακμές του γραφήματος για επαλήθευση.
        
        Returns:
            Λίστα με όλες τις ακμές του γραφήματος
        """
        return list(self.edge_counts.keys())
    
    def boruvka_connected_components(self):
        """
        Υπολογίζει τις συνεκτικές συνιστώσες χρησιμοποιώντας παραλλαγή του αλγορίθμου Borůvka.
        Ο αλγόριθμος λειτουργεί επαναληπτικά συγχωνεύοντας συνιστώσες μέσω εξερχόμενων ακμών.
        
        Returns:
            Λεξικό με component_id -> σύνολο κόμβων της συνιστώσας
        """
        # Αρχικοποίηση: κάθε κόμβος αποτελεί ξεχωριστή συνιστώσα
        components = {}
        node_to_component = {}
        component_vectors = {}
        
        # Δημιουργία αρχικών συνιστωσών
        for i in range(1, self.n + 1):
            # Κάθε κόμβος είναι μια συνιστώσα με τον εαυτό του
            components[i] = {i}
            # Αντιστοίχηση κόμβου σε ID συνιστώσας
            node_to_component[i] = i
            # Αντίγραφο του διανύσματος πρόσπτωσης για κάθε συνιστώσα
            component_vectors[i] = self.incident_vectors[i].copy()
        
        # Όριο επαναλήψεων για αποφυγή αέναων βρόχων
        max_iterations = 25
        iteration = 0
        
        # Επαναληπτική διαδικασία συγχώνευσης συνιστωσών
        while len(components) > 1 and iteration < max_iterations:
            iteration += 1
            # Λίστα συγχωνεύσεων που πρέπει να γίνουν
            merges_to_do = []
            
            # Για κάθε υπάρχουσα συνιστώσα
            for comp_id in list(components.keys()):
                # Έλεγχος ότι η συνιστώσα υπάρχει ακόμη
                if comp_id not in component_vectors:
                    continue
                    
                # Δειγματοληψία τυχαίας εξερχόμενης ακμής από τη συνιστώσα
                sampled_coord = component_vectors[comp_id].sample()
                # Αν δεν υπάρχει εξερχόμενη ακμή, συνέχισε στην επόμενη συνιστώσα
                if sampled_coord is None:
                    continue
                
                # Αποκωδικοποίηση της ακμής
                u, v = decode_edge(sampled_coord)
                
                # Εύρεση των συνιστωσών στις οποίες ανήκουν οι δύο κόμβοι
                comp_u = node_to_component.get(u)
                comp_v = node_to_component.get(v)
                
                # Αν οι κόμβοι ανήκουν σε διαφορετικές συνιστώσες
                if comp_u != comp_v and comp_u is not None and comp_v is not None:
                    # Εξασφάλιση συνεπούς σειράς για αποφυγή διπλών συγχωνεύσεων
                    if comp_u > comp_v:
                        comp_u, comp_v = comp_v, comp_u
                    # Προσθήκη στη λίστα συγχωνεύσεων
                    merges_to_do.append((comp_u, comp_v))
            
            # Εκτέλεση όλων των συγχωνεύσεων
            merges_done = set()
            for comp1, comp2 in merges_to_do:
                # Έλεγχος ότι η συγχώνευση δεν έχει ήδη γίνει και ότι οι συνιστώσες υπάρχουν
                if (comp1, comp2) in merges_done or comp1 not in components or comp2 not in components:
                    continue
                
                # Αποθήκευση των αρχικών κόμβων για μετέπειτα χρήση
                old_comp1_nodes = components[comp1].copy()
                old_comp2_nodes = components[comp2].copy()
                
                # Συγχώνευση της comp2 στην comp1
                components[comp1].update(components[comp2])
                
                # Ενημέρωση αντιστοίχησης κόμβων σε συνιστώσες
                for node in components[comp2]:
                    node_to_component[node] = comp1
                
                # Συγχώνευση διανυσμάτων πρόσπτωσης
                if comp1 in component_vectors and comp2 in component_vectors:
                    # Πρόσθεση του διανύσματος της comp2 στο διάνυσμα της comp1
                    component_vectors[comp1].add_sampler(component_vectors[comp2])
                    
                    # Αφαίρεση εσωτερικών ακμών (ακμές μεταξύ κόμβων της ίδιας νέας συνιστώσας)
                    new_component_nodes = components[comp1]
                    # Έλεγχος κάθε ακμής στο νέο διάνυσμα
                    for coord in list(component_vectors[comp1].non_zero_coords.keys()):
                        u, v = decode_edge(coord)
                        # Αν και οι δύο κόμβοι ανήκουν στη νέα συνιστώσα, η ακμή είναι εσωτερική
                        if u in new_component_nodes and v in new_component_nodes:
                            # Αφαίρεση εσωτερικής ακμής από το διάνυσμα
                            component_vectors[comp1].update(coord, -component_vectors[comp1].non_zero_coords[coord])
                    
                    # Διαγραφή του διανύσματος της comp2
                    del component_vectors[comp2]
                
                # Διαγραφή της comp2 από τις συνιστώσες
                del components[comp2]
                # Σημείωση ότι η συγχώνευση έγινε
                merges_done.add((comp1, comp2))
            
            # Αν δεν έγιναν συγχωνεύσεις, τερματισμός του αλγορίθμου
            if not merges_done:
                break
        
        return components
    
    def simple_connected_components(self):
        """
        Υπολογίζει τις συνεκτικές συνιστώσες χρησιμοποιώντας απλό Union-Find για επαλήθευση.
        
        Returns:
            Λεξικό με εκπρόσωπο -> σύνολο κόμβων της συνιστώσας
        """
        # Δημιουργία δομής Union-Find
        uf = SimpleUnionFind(self.n)
        # Για κάθε ακμή που υπάρχει
        for edge in self.edge_counts:
            if self.edge_counts[edge] > 0:
                u, v = edge
                # Ένωση των συνιστωσών των δύο κόμβων
                uf.union(u, v)
        # Επιστροφή των συνεκτικών συνιστωσών
        return uf.get_components()

def generate_random_edges(n, num_edges):
    """
    Generator function που παράγει τυχαίες ακμές.
    
    Args:
        n: Αριθμός κόμβων
        num_edges: Αριθμός ακμών που θα παραχθούν
    
    Yields:
        Tuple (u,v) που αναπαριστά τυχαία ακμή
    """
    for _ in range(num_edges):
        # Επιλογή τυχαίου πρώτου κόμβου
        u = random.randint(1, n)
        # Επιλογή τυχαίου δεύτερου κόμβου
        v = random.randint(1, n)
        # Εξασφάλιση ότι οι κόμβοι είναι διαφορετικοί (αποφυγή self-loops)
        while u == v:
            v = random.randint(1, n)
        yield (u, v)

def run_boruvka_experiment():
    """
    Εκτελεί το κύριο πείραμα: προσθήκη 500.000 τυχαίων ακμών και παρακολούθηση
    της εξέλιξης των συνεκτικών συνιστωσών.
    
    Returns:
        Tuple με λίστες (edge_counts, num_components, largest_component_sizes)
    """
    print("Ξεκινάμε το πείραμα με τον αλγόριθμο Borůvka...")
    
    # Παράμετροι πειράματος
    n = 100000  # αριθμός κόμβων
    num_edges = 500000  # αριθμός ακμών
    check_interval = 1000  # έλεγχος κάθε 1000 ακμές
    
    # Δημιουργία γραφήματος
    graph = BoruvkaGraph(n)
    
    # Λίστες για αποθήκευση αποτελεσμάτων
    edge_counts = []
    num_components = []
    largest_component_sizes = []
    
    print("Προσθήκη ακμών και υπολογισμός συνεκτικών συνιστωσών...")
    
    # Άνοιγμα αρχείου για αποθήκευση αποτελεσμάτων
    with open('partD1.txt', 'w', encoding='utf-8') as f:
        # Γραφή header στο αρχείο
        f.write("=== Πείραμα 1: 500.000 εισαγωγές τυχαίων ακμών ===\n")
        
        # Δημιουργία generator για τυχαίες ακμές
        edge_generator = generate_random_edges(n, num_edges)
        edges_added = 0
        
        # Προσθήκη ακμών μία προς μία
        for u, v in edge_generator:
            # Προσθήκη ακμής στο γράφημα
            graph.add_edge(u, v)
            edges_added += 1
            
            # Έλεγχος και καταγραφή κάθε check_interval ακμές
            if edges_added % check_interval == 0:
                # Υπολογισμός συνεκτικών συνιστωσών με Borůvka
                components_boruvka = graph.boruvka_connected_components()
                
                # Επαλήθευση με απλό αλγόριθμο Union-Find
                components_simple = graph.simple_connected_components()
                
                # Υπολογισμός στατιστικών
                num_comp_boruvka = len(components_boruvka)
                num_comp_simple = len(components_simple)
                
                # Εύρεση μεγέθους μεγαλύτερης συνιστώσας
                largest_size_boruvka = max(len(comp) for comp in components_boruvka.values()) if components_boruvka else 0
                largest_size_simple = max(len(comp) for comp in components_simple.values()) if components_simple else 0
                
                # Έλεγχος ορθότητας των αποτελεσμάτων
                if num_comp_boruvka != num_comp_simple or largest_size_boruvka != largest_size_simple:
                    # Εκτύπωση μηνύματος σφάλματος αν τα αποτελέσματα διαφέρουν
                    error_msg = f"ΣΦΑΛΜΑ: Borůvka={num_comp_boruvka},{largest_size_boruvka} vs Simple={num_comp_simple},{largest_size_simple}"
                    print(error_msg)
                    f.write(error_msg + "\n")
                
                # Μορφοποίηση και εκτύπωση αποτελεσμάτων
                result_line = f"{edges_added}: {num_comp_boruvka} {largest_size_boruvka}"
                print(result_line)
                f.write(result_line + "\n")
                # Εξασφάλιση άμεσης εγγραφής στο αρχείο
                f.flush()
                
                # Αποθήκευση αποτελεσμάτων για γραφικές παραστάσεις
                edge_counts.append(edges_added)
                num_components.append(num_comp_boruvka)
                largest_component_sizes.append(largest_size_boruvka)
    
    # Επιστροφή των αποτελεσμάτων
    return edge_counts, num_components, largest_component_sizes

def run_deletion_experiment(p_delete):
    """
    Εκτελεί πείραμα με μίγμα εισαγωγών και διαγραφών ακμών.
    
    Args:
        p_delete: Πιθανότητα διαγραφής ακμής σε κάθε βήμα
    
    Returns:
        Tuple με λίστες (operation_counts, num_components, largest_component_sizes)
    """
    print(f"Ξεκινάμε πείραμα με διαγραφές (p={p_delete})...")
    
    # Παράμετροι πειράματος
    n = 100000  # αριθμός κόμβων
    num_operations = 5000000  # συνολικές εντολές
    check_interval = 10000  # έλεγχος κάθε 10000 εντολές
    
    # Δημιουργία γραφήματος
    graph = BoruvkaGraph(n)
    
    # Λίστες για αποθήκευση αποτελεσμάτων
    operation_counts = []
    num_components = []
    largest_component_sizes = []
    
    print("Εκτέλεση εντολών...")
    
    # Άνοιγμα αρχείου για προσθήκη αποτελεσμάτων
    with open('partD1.txt', 'a', encoding='utf-8') as f:
        # Γραφή header για το νέο πείραμα
        f.write(f"\n=== Πείραμα με διαγραφές p={p_delete} ===\n")
        
        # Εκτέλεση εντολών
        for op_count in range(1, num_operations + 1):
            # Απόφαση για το είδος της εντολής βάσει πιθανότητας
            if random.random() < p_delete:
                # Προσπάθεια διαγραφής ακμής
                # Επιλογή τυχαίου κόμβου
                node = random.randint(1, n)
                # Εύρεση προσπίπτουσων ακμών του κόμβου
                incident_edges = graph.get_incident_edges(node)
                
                # Αν υπάρχουν προσπίπτουσες ακμές
                if incident_edges:
                    # Επιλογή τυχαίας ακμής για διαγραφή
                    edge_to_remove = random.choice(incident_edges)
                    graph.remove_edge(edge_to_remove[0], edge_to_remove[1])
                else:
                    # Αν δεν υπάρχει προσπίπτουσα ακμή, κάνε εισαγωγή αντί για διαγραφή
                    u = random.randint(1, n)
                    v = random.randint(1, n)
                    # Εξασφάλιση ότι οι κόμβοι είναι διαφορετικοί
                    while u == v:
                        v = random.randint(1, n)
                    graph.add_edge(u, v)
            else:
                # Εισαγωγή νέας τυχαίας ακμής
                u = random.randint(1, n)
                v = random.randint(1, n)
                # Εξασφάλιση ότι οι κόμβοι είναι διαφορετικοί
                while u == v:
                    v = random.randint(1, n)
                graph.add_edge(u, v)
            
            # Έλεγχος και καταγραφή κάθε check_interval εντολές
            if op_count % check_interval == 0:
                # Υπολογισμός συνεκτικών συνιστωσών
                components = graph.boruvka_connected_components()
                num_comp = len(components)
                # Εύρεση μεγέθους μεγαλύτερης συνιστώσας
                largest_size = max(len(comp) for comp in components.values()) if components else 0
                
                # Μορφοποίηση και εκτύπωση αποτελεσμάτων
                result_line = f"{op_count}: {num_comp} {largest_size}"
                print(result_line)
                f.write(result_line + "\n")
                # Εξασφάλιση άμεσης εγγραφής στο αρχείο
                f.flush()
                
                # Αποθήκευση αποτελεσμάτων για γραφικές παραστάσεις
                operation_counts.append(op_count)
                num_components.append(num_comp)
                largest_component_sizes.append(largest_size)
    
    # Επιστροφή των αποτελεσμάτων
    return operation_counts, num_components, largest_component_sizes

def plot_results(edge_counts, num_components, largest_component_sizes, title="Εξέλιξη Συνεκτικών Συνιστωσών", filename=None):
    """
    Δημιουργεί γραφικές παραστάσεις των αποτελεσμάτων.
    
    Args:
        edge_counts: Λίστα με αριθμό ακμών/εντολών
        num_components: Λίστα με αριθμό συνεκτικών συνιστωσών
        largest_component_sizes: Λίστα με μέγεθος μεγαλύτερης συνιστώσας
        title: Τίτλος του γραφήματος
        filename: Όνομα αρχείου για αποθήκευση (προαιρετικό)
    """
    # Δημιουργία νέου γραφήματος με καθορισμένο μέγεθος
    plt.figure(figsize=(12, 8))
    
    # Σχεδίαση και των δύο μεγεθών στον ίδιο άξονα
    # Γραμμή για αριθμό συνεκτικών συνιστωσών
    plt.plot(edge_counts, num_components, 'b-', linewidth=2, label='Αριθμός συνεκτικών συνιστωσών')
    # Γραμμή για μέγεθος μεγαλύτερης συνιστώσας
    plt.plot(edge_counts, largest_component_sizes, 'r-', linewidth=2, label='Μέγεθος μεγαλύτερης συνιστώσας')
    
    # Ρύθμιση ετικετών αξόνων και τίτλου
    plt.xlabel('Αριθμός Ακμών/Εντολών')
    plt.ylabel('Πλήθος')
    plt.title(title)
    # Προσθήκη πλέγματος για καλύτερη αναγνωσιμότητα
    plt.grid(True)
    # Προσθήκη υπομνήματος
    plt.legend()
    
    # Αποθήκευση σε αρχείο αν δόθηκε όνομα
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    # Εμφάνιση του γραφήματος
    plt.show()

if __name__ == "__main__":
    # Ρύθμιση seed για αναπαραγωγιμότητα των αποτελεσμάτων
    random.seed(42)
    
    print("=== Πείραμα 1: 500.000 εισαγωγές τυχαίων ακμών ===")
    # Εκτέλεση κύριου πειράματος εισαγωγής ακμών
    edge_counts, num_components, largest_component_sizes = run_boruvka_experiment()
    
    print("\n=== Δημιουργία γραφικών παραστάσεων ===")
    # Δημιουργία γραφήματος για το πείραμα εισαγωγών
    plot_results(edge_counts, num_components, largest_component_sizes, 
                "Εξέλιξη Συνεκτικών Συνιστωσών - Εισαγωγές Ακμών",
                "boruvka_insertions.png")
    
    print("\n=== Πείραμα 2: Εισαγωγές/Διαγραφές με p=3/4 ===")
    # Εκτέλεση πειράματος με πιθανότητα διαγραφής 0.75
    op_counts_075, num_comp_075, largest_size_075 = run_deletion_experiment(0.75)
    # Δημιουργία γραφήματος για το πείραμα με p=0.75
    plot_results(op_counts_075, num_comp_075, largest_size_075,
                "Εξέλιξη Συνεκτικών Συνιστωσών - Εισαγωγές/Διαγραφές (p=0.75)",
                "boruvka_p075.png")
    
    print("\n=== Πείραμα 3: Εισαγωγές/Διαγραφές με p=9/10 ===")
    # Εκτέλεση πειράματος με πιθανότητα διαγραφής 0.9
    op_counts_090, num_comp_090, largest_size_090 = run_deletion_experiment(0.9)
    # Δημιουργία γραφήματος για το πείραμα με p=0.9
    plot_results(op_counts_090, num_comp_090, largest_size_090,
                "Εξέλιξη Συνεκτικών Συνιστωσών - Εισαγωγές/Διαγραφές (p=0.9)",
                "boruvka_p090.png")
    
    # Δημιουργία συγκριτικού γραφήματος για όλα τα πειράματα
    plt.figure(figsize=(14, 10))
    
    # Πρώτο subplot: Σύγκριση αριθμού συνιστωσών
    plt.subplot(2, 1, 1)
    # Γραμμή για πείραμα μόνο εισαγωγών
    plt.plot(edge_counts, num_components, 'b-', linewidth=2, label='p=0 (μόνο εισαγωγές)')
    # Γραμμή για πείραμα με p=0.75
    plt.plot(op_counts_075, num_comp_075, 'g-', linewidth=2, label='p=0.75')
    # Γραμμή για πείραμα με p=0.9
    plt.plot(op_counts_090, num_comp_090, 'r-', linewidth=2, label='p=0.9')
    plt.xlabel('Αριθμός Εντολών')
    plt.ylabel('Αριθμός Συνεκτικών Συνιστωσών')
    plt.title('Σύγκριση Αριθμού Συνεκτικών Συνιστωσών για Διαφορετικά p')
    plt.grid(True)
    plt.legend()
    
    # Δεύτερο subplot: Σύγκριση μεγέθους μεγαλύτερης συνιστώσας
    plt.subplot(2, 1, 2)
    # Γραμμή για πείραμα μόνο εισαγωγών
    plt.plot(edge_counts, largest_component_sizes, 'b-', linewidth=2, label='p=0 (μόνο εισαγωγές)')
    # Γραμμή για πείραμα με p=0.75
    plt.plot(op_counts_075, largest_size_075, 'g-', linewidth=2, label='p=0.75')
    # Γραμμή για πείραμα με p=0.9
    plt.plot(op_counts_090, largest_size_090, 'r-', linewidth=2, label='p=0.9')
    plt.xlabel('Αριθμός Εντολών')
    plt.ylabel('Μέγεθος Μεγαλύτερης Συνιστώσας')
    plt.title('Σύγκριση Μεγέθους Μεγαλύτερης Συνιστώσας για Διαφορετικά p')
    plt.grid(True)
    plt.legend()
    
    # Ρύθμιση διάταξης για αποφυγή επικάλυψης
    plt.tight_layout()
    # Αποθήκευση συγκριτικού γραφήματος
    plt.savefig("boruvka_comparison.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nΌλα τα πειράματα ολοκληρώθηκαν!")
    
    # Δημιουργία κειμένου εξήγησης των αποτελεσμάτων
    explanation = """
""" + "="*60 + """
ΕΞΗΓΗΣΗ ΤΟΥ ΦΑΙΝΟΜΕΝΟΥ PHASE TRANSITION:
""" + "="*60 + """

Το μοτίβο που παρατηρούμε εξηγείται από το φαινόμενο phase transition:

1. ΑΡΧΙΚΗ ΦΑΣΗ (σταθερότητα):
   - Όταν έχουμε λίγες ακμές, κάθε ακμή συνδέει διαφορετικούς κόμβους
   - Οι συνιστώσες είναι μικρές και πολλές
   - Η μεγαλύτερη συνιστώσα μεγαλώνει αργά

2. ΚΡΙΣΙΜΟ ΣΗΜΕΙΟ (~n/2 ακμές):
   - Όταν ο αριθμός ακμών φτάσει περίπου n/2, εμφανίζεται το critical threshold
   - Ξαφνικά σχηματίζεται μια "γιγαντιαία" συνεκτική συνιστώσα
   - Αυτό είναι γνωστό ως "phase transition" στη θεωρία γραφημάτων

3. ΤΕΛΙΚΗ ΦΑΣΗ (σταθεροποίηση):
   - Μετά το κρίσιμο σημείο, σχεδόν όλοι οι κόμβοι ανήκουν στη μεγαλύτερη συνιστώσα
   - Νέες ακμές απλώς συνδέουν την γιγαντιαία συνιστώσα με τις λίγες απομονωμένες
   - Ο αριθμός συνιστωσών μειώνεται γρήγορα προς 1

Αυτό το φαινόμενο είναι θεμελιώδες στη θεωρία τυχαίων γραφημάτων (Erdős-Rényi).
"""
    
    # Εκτύπωση εξήγησης στην κονσόλα
    print(explanation)
    
    # Αποθήκευση εξήγησης στο αρχείο αποτελεσμάτων
    with open('partD1.txt', 'a', encoding='utf-8') as f:
        f.write("\n" + explanation)

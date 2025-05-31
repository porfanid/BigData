# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr
import random
import time
import math
from collections import defaultdict

class NonZeroSampler:
    """
    Υλοποίηση Non-Zero Sampler με hierarchical sampling structure.
    Χρησιμοποιεί πολλαπλά επίπεδα δειγματοληψίας για αποδοτική εύρεση
    μη-μηδενικών συντεταγμένων σε αραιά διανύσματα.
    """
    
    def __init__(self, n, delta=0.00002):
        """
        Αρχικοποίηση του Non-Zero Sampler.
        
        Args:
            n: Μέγιστος αριθμός συντεταγμένων που μπορεί να χειριστεί
            delta: Πιθανότητα αποτυχίας ανά query (default: 0.00002)
        """
        # Αποθήκευση παραμέτρων εισόδου
        self.n = n
        self.delta = delta
        
        # Υπολογισμός αριθμού επιπέδων: log₂(n+1), με όριο 20 για απόδοση
        self.levels = min(20, math.ceil(math.log2(n + 1)))
        
        # Υπολογισμός αριθμού επαναλήψεων: log(1/δ), με όρια 1-5 για απόδοση
        self.T = min(5, max(1, math.ceil(math.log(1/delta))))
        
        # Πρώτος αριθμός για τις hash functions (σύμφωνα με την άσκηση)
        self.p = 20011
        
        # Λίστα παραμέτρων hash functions: [level][repetition] -> (a, b)
        self.hash_params = []
        
        # Λίστα TrivialL0Samplers: [level][repetition] -> TrivialL0Sampler
        self.level_samplers = []
        
        # Δημιουργία hash functions και samplers για κάθε επίπεδο
        for level in range(self.levels):
            # Παράμετροι hash functions για αυτό το επίπεδο
            level_hash_params = []
            # Samplers για αυτό το επίπεδο
            level_level_samplers = []
            
            # Δημιουργία T επαναλήψεων για κάθε επίπεδο
            for t in range(self.T):
                # Τυχαία παράμετρα για hash function: h(x) = (ax + b) mod p
                # a πρέπει να είναι μη-μηδενικό (1 ≤ a ≤ p-1)
                a = random.randint(1, self.p - 1)
                # b μπορεί να είναι οποιοδήποτε (0 ≤ b ≤ p-1)
                b = random.randint(0, self.p - 1)
                level_hash_params.append((a, b))
                
                # Δημιουργία νέου TrivialL0Sampler για αυτό το επίπεδο-επανάληψη
                level_level_samplers.append(TrivialL0Sampler())
            
            # Προσθήκη στις κύριες λίστες
            self.hash_params.append(level_hash_params)
            self.level_samplers.append(level_level_samplers)
    
    def get_params_info(self):
        """
        Επιστρέφει string με τις παραμέτρους του sampler για debugging.
        
        Returns:
            str: Πληροφορίες παραμέτρων σε μορφή "levels=X, T=Y, p=Z"
        """
        return f"levels={self.levels}, T={self.T}, p={self.p}"
    
    def _hash_to_level(self, coord, level, t):
        """
        Υπολογίζει την hash τιμή μιας συντεταγμένης για συγκεκριμένο επίπεδο και επανάληψη.
        
        Args:
            coord: Η συντεταγμένη (int ή tuple)
            level: Το επίπεδο (0 ≤ level < levels)
            t: Η επανάληψη (0 ≤ t < T)
            
        Returns:
            int: Hash τιμή mod 2^level
        """
        # Μετατροπή tuple συντεταγμένων σε integer
        if isinstance(coord, tuple):
            # Για ακμές (u,v), χρησιμοποιούμε u*p + v
            u, v = coord
            coord_int = u * self.p + v
        else:
            # Για απλές συντεταγμένες
            coord_int = coord
        
        # Παράμετροι hash function για αυτό το επίπεδο-επανάληψη
        a, b = self.hash_params[level][t]
        
        # Υπολογισμός hash: h(x) = (ax + b) mod p
        hash_val = (a * coord_int + b) % self.p
        
        # Επιστροφή του αποτελέσματος mod 2^level
        return hash_val % (2 ** level)
    
    def update(self, coord, value):
        """
        Ενημερώνει τον sampler με μια νέα συντεταγμένη και την τιμή της.
        Η συντεταγμένη προστίθεται σε όλα τα κατάλληλα επίπεδα βάσει hash functions.
        
        Args:
            coord: Η συντεταγμένη προς ενημέρωση
            value: Η τιμή που προστίθεται στη συντεταγμένη
        """
        # Ελέγχουμε όλα τα επίπεδα
        for level in range(self.levels):
            # Ελέγχουμε όλες τις επαναλήψεις στο επίπεδο
            for t in range(self.T):
                # Ελέγχουμε αν η συντεταγμένη "περνάει" το hash test
                # Δηλαδή αν hash_to_level(coord, level, t) == 0
                if self._hash_to_level(coord, level, t) == 0:
                    # Η συντεταγμένη επιλέγεται για αυτό το επίπεδο-επανάληψη
                    # Ενημερώνουμε τον αντίστοιχο TrivialL0Sampler
                    self.level_samplers[level][t].update(coord, value)
    
    def sample(self):
        """
        Επιστρέφει μια τυχαία μη-μηδενική συντεταγμένη από τον sampler.
        Χρησιμοποιεί τη στρατηγική του hierarchical sampling: ξεκινάει από
        τα υψηλότερα επίπεδα (πιο αραιά) και κατεβαίνει.
        
        Returns:
            Συντεταγμένη ή None αν δεν υπάρχει μη-μηδενική συντεταγμένη
        """
        # Ξεκινάμε από το υψηλότερο επίπεδο (πιο αραιό δείγμα)
        for level in range(self.levels - 1, -1, -1):
            # Ελέγχουμε όλες τις επαναλήψεις στο επίπεδο
            for t in range(self.T):
                # Παίρνουμε τον sampler για αυτό το επίπεδο-επανάληψη
                sampler = self.level_samplers[level][t]
                
                # Ελέγχουμε αν έχει ακριβώς 1 μη-μηδενική συντεταγμένη
                if len(sampler.non_zero_coords) == 1:
                    # Βρήκαμε το ιδανικό επίπεδο - επιστρέφουμε τη συντεταγμένη
                    coord = list(sampler.non_zero_coords.keys())[0]
                    return coord
        
        # Δεν βρήκαμε επίπεδο με ακριβώς 1 στοιχείο
        return None
    
    def is_zero(self):
        """
        Ελέγχει αν το διάνυσμα είναι μηδενικό (δεν έχει μη-μηδενικές συντεταγμένες).
        
        Returns:
            bool: True αν το διάνυσμα είναι μηδενικό, False αλλιώς
        """
        # Ελέγχουμε όλα τα επίπεδα και επαναλήψεις
        for level in range(self.levels):
            for t in range(self.T):
                # Αν οποιοσδήποτε sampler δεν είναι μηδενικός, το διάνυσμα δεν είναι μηδενικό
                if not self.level_samplers[level][t].is_zero():
                    return False
        
        # Όλοι οι samplers είναι μηδενικοί
        return True
    
    def copy(self):
        """
        Δημιουργεί ένα βαθύ αντίγραφο του sampler.
        
        Returns:
            NonZeroSampler: Αντίγραφο του τρέχοντος sampler
        """
        # Δημιουργία νέου αντικειμένου χωρίς κλήση __init__
        new_sampler = NonZeroSampler.__new__(NonZeroSampler)
        
        # Αντιγραφή των βασικών παραμέτρων
        new_sampler.n = self.n
        new_sampler.delta = self.delta
        new_sampler.levels = self.levels
        new_sampler.T = self.T
        new_sampler.p = self.p
        
        # Κοινή χρήση των hash functions (δεν χρειάζεται αντιγραφή)
        new_sampler.hash_params = self.hash_params
        
        # Αντιγραφή των level samplers
        new_sampler.level_samplers = []
        for level in range(self.levels):
            level_level_samplers = []
            for t in range(self.T):
                # Δημιουργία αντιγράφου για κάθε TrivialL0Sampler
                level_level_samplers.append(self.level_samplers[level][t].copy())
            new_sampler.level_samplers.append(level_level_samplers)
        
        return new_sampler
    
    def add_sampler(self, other):
        """
        Προσθέτει έναν άλλο sampler στον τρέχοντα (vector addition).
        
        Args:
            other: Άλλος NonZeroSampler προς πρόσθεση
        """
        # Για κάθε επίπεδο και επανάληψη
        for level in range(self.levels):
            for t in range(self.T):
                # Παίρνουμε όλες τις συντεταγμένες από τον άλλο sampler
                for coord, value in other.level_samplers[level][t].non_zero_coords.items():
                    # Προσθέτουμε τη συντεταγμένη στον τρέχοντα sampler
                    self.level_samplers[level][t].update(coord, value)

class TrivialL0Sampler:
    """
    Απλός L0 sampler που διατηρεί όλες τις μη-μηδενικές συντεταγμένες.
    Χρησιμοποιείται ως βασικό building block για τον NonZeroSampler.
    """
    
    def __init__(self):
        """
        Αρχικοποίηση του TrivialL0Sampler.
        """
        # Dictionary που κρατάει συντεταγμένη -> τιμή για όλες τις μη-μηδενικές
        self.non_zero_coords = {}
    
    def update(self, coord, value):
        """
        Ενημερώνει μια συντεταγμένη με νέα τιμή.
        
        Args:
            coord: Η συντεταγμένη προς ενημέρωση
            value: Η τιμή που προστίθεται στη συντεταγμένη
        """
        # Ελέγχουμε αν η συντεταγμένη υπάρχει ήδη
        if coord in self.non_zero_coords:
            # Προσθέτουμε την τιμή στην υπάρχουσα
            self.non_zero_coords[coord] += value
            
            # Αν η νέα τιμή γίνει 0, αφαιρούμε τη συντεταγμένη
            if self.non_zero_coords[coord] == 0:
                del self.non_zero_coords[coord]
        else:
            # Νέα συντεταγμένη - προσθήκη μόνο αν δεν είναι 0
            if value != 0:
                self.non_zero_coords[coord] = value
    
    def sample(self):
        """
        Επιστρέφει τυχαία μη-μηδενική συντεταγμένη.
        
        Returns:
            Τυχαία συντεταγμένη ή None αν όλες είναι μηδενικές
        """
        # Ελέγχουμε αν υπάρχουν μη-μηδενικές συντεταγμένες
        if not self.non_zero_coords:
            return None
        
        # Επιστρέφουμε τυχαία επιλογή από τις μη-μηδενικές
        return random.choice(list(self.non_zero_coords.keys()))
    
    def is_zero(self):
        """
        Ελέγχει αν το διάνυσμα είναι μηδενικό.
        
        Returns:
            bool: True αν δεν υπάρχουν μη-μηδενικές συντεταγμένες
        """
        return len(self.non_zero_coords) == 0
    
    def copy(self):
        """
        Δημιουργεί αντίγραφο του sampler.
        
        Returns:
            TrivialL0Sampler: Αντίγραφο του τρέχοντος sampler
        """
        # Δημιουργία νέου sampler
        new_sampler = TrivialL0Sampler()
        
        # Αντιγραφή του dictionary με τις συντεταγμένες
        new_sampler.non_zero_coords = self.non_zero_coords.copy()
        
        return new_sampler
    
    def add_sampler(self, other):
        """
        Προσθέτει έναν άλλο sampler στον τρέχοντα.
        
        Args:
            other: Άλλος TrivialL0Sampler προς πρόσθεση
        """
        # Για κάθε συντεταγμένη του άλλου sampler
        for coord, value in other.non_zero_coords.items():
            # Ενημερώνουμε τη συντεταγμένη στον τρέχοντα
            self.update(coord, value)

def encode_edge(u, v, n):
    """
    Κωδικοποιεί μια ακμή (u,v) σε συντεταγμένη διανύσματος.
    Εξασφαλίζει ότι u ≤ v για συνέπεια.
    
    Args:
        u, v: Οι κόμβοι της ακμής
        n: Συνολικός αριθμός κόμβων (δεν χρησιμοποιείται εδώ)
        
    Returns:
        tuple: Κωδικοποιημένη ακμή ως (min(u,v), max(u,v))
    """
    # Εξασφαλίζουμε ότι u ≤ v για συνέπεια
    if u > v:
        u, v = v, u
    return (u, v)

def decode_edge(coord):
    """
    Αποκωδικοποιεί μια συντεταγμένη σε ακμή (u,v).
    
    Args:
        coord: Η κωδικοποιημένη συντεταγμένη
        
    Returns:
        tuple: Η ακμή ως (u, v)
    """
    # Η συντεταγμένη είναι ήδη tuple (u, v)
    return coord

class SimpleUnionFind:
    """
    Απλή υλοποίηση Union-Find για επαλήθευση της ορθότητας.
    Χρησιμοποιείται για τον υπολογισμό συνεκτικών συνιστωσών με τον κλασικό τρόπο.
    """
    
    def __init__(self, n):
        """
        Αρχικοποίηση Union-Find για n κόμβους.
        
        Args:
            n: Αριθμός κόμβων
        """
        # Κάθε κόμβος αρχικά είναι ο γονέας του εαυτού του
        self.parent = list(range(n + 1))
        
        # Rank για balanced union (όλοι ξεκινούν με rank 0)
        self.rank = [0] * (n + 1)
    
    def find(self, x):
        """
        Βρίσκει τον αντιπρόσωπο της συνιστώσας που ανήκει ο κόμβος x.
        Χρησιμοποιεί path compression για βελτίωση απόδοσης.
        
        Args:
            x: Ο κόμβος για τον οποίο ψάχνουμε τον αντιπρόσωπο
            
        Returns:
            int: Ο αντιπρόσωπος της συνιστώσας
        """
        # Path compression: κάνουμε όλους τους κόμβους στο μονοπάτι να δείχνουν στη ρίζα
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """
        Ενώνει τις συνιστώσες που περιέχουν τους κόμβους x και y.
        
        Args:
            x, y: Οι κόμβοι προς ένωση
        """
        # Βρίσκουμε τους αντιπροσώπους των δύο συνιστωσών
        px, py = self.find(x), self.find(y)
        
        # Αν είναι ήδη στην ίδια συνιστώσα, τίποτα να κάνουμε
        if px == py:
            return
        
        # Union by rank: η συνιστώσα με μικρότερο rank γίνεται παιδί της άλλης
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        # Κάνουμε τον py παιδί του px
        self.parent[py] = px
        
        # Αν είχαν ίδιο rank, αυξάνουμε το rank του νέου αντιπροσώπου
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
    
    def get_components(self):
        """
        Επιστρέφει όλες τις συνεκτικές συνιστώσες.
        
        Returns:
            dict: Αντιπρόσωπος -> σύνολο κόμβων της συνιστώσας
        """
        # Dictionary που αντιστοιχεί αντιπρόσωπο σε σύνολο κόμβων
        components = defaultdict(set)
        
        # Για κάθε κόμβο, βρίσκουμε τον αντιπρόσωπό του και τον προσθέτουμε
        for i in range(1, len(self.parent)):
            if i < len(self.parent):
                components[self.find(i)].add(i)
        
        return dict(components)

class BoruvkaGraphWithNonZeroSampler:
    """
    Γράφος που υποστηρίζει τον αλγόριθμο Borůvka με χρήση Non-Zero Samplers.
    Κάθε κόμβος έχει ένα διάνυσμα πρόσπτωσης που αναπαρίσταται με NonZeroSampler.
    """
    
    def __init__(self, n):
        """
        Αρχικοποίηση του γράφου με n κόμβους.
        
        Args:
            n: Αριθμός κόμβων στον γράφο
        """
        # Αποθήκευση αριθμού κόμβων
        self.n = n
        
        # Υπολογισμός παραμέτρου δ για 99% επιτυχία σε 500 queries
        # Συνολική πιθανότητα αποτυχίας ≤ 500*δ ≤ 0.01
        # Άρα δ ≤ 0.01/500 = 0.00002
        delta = 0.00002
        
        # Dictionary που αντιστοιχεί κόμβο σε NonZeroSampler (διάνυσμα πρόσπτωσης)
        self.incident_vectors = {}
        
        # Dictionary που κρατάει τον αριθμό εμφανίσεων κάθε ακμής (για παράλληλες ακμές)
        self.edge_counts = defaultdict(int)
        
        # Μήνυμα αρχικοποίησης
        print("Αρχικοποίηση non-zero samplers...")
        
        # Εκτίμηση μέγιστου αριθμού ακμών για τους samplers
        max_edges = 100000
        
        # Δημιουργία πρώτου sampler για εμφάνιση παραμέτρων
        first_sampler = NonZeroSampler(max_edges, delta)
        print(f"Παράμετροι samplers: {first_sampler.get_params_info()}")
        self.incident_vectors[1] = first_sampler
        
        # Δημιουργία υπόλοιπων samplers
        for i in range(2, n + 1):
            self.incident_vectors[i] = NonZeroSampler(max_edges, delta)
            # Πρόοδος κάθε 20000 samplers
            if i % 20000 == 0:
                print(f"Αρχικοποιήθηκαν {i} samplers...")
        
        print("Ολοκληρώθηκε η αρχικοποίηση!")
    
    def add_edge(self, u, v):
        """
        Προσθέτει μια ακμή (u,v) στον γράφο.
        
        Args:
            u, v: Οι κόμβοι της ακμής
        """
        # Αγνοούμε self-loops
        if u == v:
            return
        
        # Δημιουργία κανονικής μορφής ακμής (με ταξινόμηση)
        edge = tuple(sorted([u, v]))
        
        # Αύξηση μετρητή για αυτήν την ακμή
        self.edge_counts[edge] += 1
        
        # Κωδικοποίηση ακμής για τα διανύσματα πρόσπτωσης
        coord = encode_edge(u, v, self.n)
        
        # Ενημέρωση διανυσμάτων πρόσπτωσης μόνο αν είναι η πρώτη εμφάνιση της ακμής
        if self.edge_counts[edge] == 1:
            # Η ακμή προστίθεται στα διανύσματα πρόσπτωσης των δύο κόμβων
            self.incident_vectors[u].update(coord, 1)
            self.incident_vectors[v].update(coord, 1)
    
    def remove_edge(self, u, v):
        """
        Αφαιρεί μια ακμή (u,v) από τον γράφο.
        
        Args:
            u, v: Οι κόμβοι της ακμής
        """
        # Δημιουργία κανονικής μορφής ακμής
        edge = tuple(sorted([u, v]))
        
        # Έλεγχος αν η ακμή υπάρχει
        if edge not in self.edge_counts or self.edge_counts[edge] == 0:
            return
        
        # Μείωση μετρητή ακμής
        self.edge_counts[edge] -= 1
        
        # Κωδικοποίηση ακμής
        coord = encode_edge(u, v, self.n)
        
        # Ενημέρωση διανυσμάτων πρόσπτωσης μόνο αν δεν υπάρχουν άλλες παράλληλες ακμές
        if self.edge_counts[edge] == 0:
            # Αφαίρεση από τα διανύσματα πρόσπτωσης (προσθήκη -1)
            self.incident_vectors[u].update(coord, -1)
            self.incident_vectors[v].update(coord, -1)
            
            # Διαγραφή από το dictionary των ακμών
            del self.edge_counts[edge]
    
    def get_incident_edges(self, node):
        """
        Επιστρέφει όλες τις ακμές που προσπίπτουν σε έναν κόμβο.
        Χρησιμοποιείται για διαγραφή ακμών.
        
        Args:
            node: Ο κόμβος για τον οποίο ψάχνουμε προσπίπτουσες ακμές
            
        Returns:
            list: Λίστα ακμών που προσπίπτουν στον κόμβο
        """
        edges = []
        
        # Ψάχνουμε σε όλες τις ακμές του γράφου
        for edge, count in self.edge_counts.items():
            if count > 0:  # Η ακμή υπάρχει
                u, v = edge
                # Ελέγχουμε αν ο κόμβος συμμετέχει στην ακμή
                if u == node or v == node:
                    edges.append(edge)
        
        return edges
    
    def get_all_edges(self):
        """
        Επιστρέφει όλες τις ακμές του γράφου για επαλήθευση.
        
        Returns:
            list: Λίστα όλων των ακμών
        """
        return list(self.edge_counts.keys())
    
    def boruvka_connected_components(self):
        """
        Υπολογίζει τις συνεκτικές συνιστώσες χρησιμοποιώντας τον αλγόριθμο Borůvka
        με Non-Zero Samplers.
        
        Returns:
            dict: Αντιπρόσωπος συνιστώσας -> σύνολο κόμβων της συνιστώσας
        """
        # Αρχικοποίηση: κάθε κόμβος αποτελεί ξεχωριστή συνιστώσα
        components = {}  # component_id -> set of nodes
        node_to_component = {}  # node -> component_id  
        component_vectors = {}  # component_id -> NonZeroSampler
        
        # Δημιουργία αρχικών συνιστωσών
        for i in range(1, self.n + 1):
            # Κάθε κόμβος είναι μια συνιστώσα με ID το ίδιο το node ID
            components[i] = {i}
            node_to_component[i] = i
            # Κάθε συνιστώσα παίρνει αντίγραφο του διανύσματος πρόσπτωσης του κόμβου
            component_vectors[i] = self.incident_vectors[i].copy()
        
        # Όριο επαναλήψεων για αποφυγή αέναων βρόχων
        max_iterations = 25
        iteration = 0
        
        # Κύριος βρόχος του αλγορίθμου Borůvka
        while len(components) > 1 and iteration < max_iterations:
            iteration += 1
            merges_to_do = []  # Λίστα συγχωνεύσεων προς εκτέλεση
            
            # Φάση 1: Εύρεση εξερχόμενων ακμών για κάθε συνιστώσα
            for comp_id in list(components.keys()):
                # Έλεγχος ότι η συνιστώσα υπάρχει ακόμη
                if comp_id not in component_vectors:
                    continue
                
                # Δειγματοληψία από το διάνυσμα πρόσπτωσης της συνιστώσας
                sampled_coord = component_vectors[comp_id].sample()
                
                # Αν δεν βρέθηκε ακμή, συνεχίζουμε στην επόμενη συνιστώσα
                if sampled_coord is None:
                    continue
                
                # Αποκωδικοποίηση της ακμής
                u, v = decode_edge(sampled_coord)
                
                # Εύρεση των συνιστωσών των δύο κόμβων της ακμής
                comp_u = node_to_component.get(u)
                comp_v = node_to_component.get(v)
                
                # Έλεγχος ότι η ακμή συνδέει διαφορετικές συνιστώσες (εξερχόμενη ακμή)
                if comp_u != comp_v and comp_u is not None and comp_v is not None:
                    # Κανονικοποίηση: η μικρότερη συνιστώσα πρώτη
                    if comp_u > comp_v:
                        comp_u, comp_v = comp_v, comp_u
                    # Προσθήκη στη λίστα συγχωνεύσεων
                    merges_to_do.append((comp_u, comp_v))
            
            # Φάση 2: Εκτέλεση συγχωνεύσεων
            merges_done = set()  # Για αποφυγή διπλών συγχωνεύσεων
            
            for comp1, comp2 in merges_to_do:
                # Έλεγχος ότι η συγχώνευση δεν έχει γίνει ήδη και οι συνιστώσες υπάρχουν
                if (comp1, comp2) in merges_done or comp1 not in components or comp2 not in components:
                    continue
                
                # Αποθήκευση των παλιών συνόλων κόμβων
                old_comp1_nodes = components[comp1].copy()
                old_comp2_nodes = components[comp2].copy()
                
                # Συγχώνευση: προσθέτουμε τους κόμβους της comp2 στην comp1
                components[comp1].update(components[comp2])
                
                # Ενημέρωση αντιστοίχισης κόμβων σε συνιστώσες
                for node in components[comp2]:
                    node_to_component[node] = comp1
                
                # Συγχώνευση διανυσμάτων πρόσπτωσης
                if comp1 in component_vectors and comp2 in component_vectors:
                    # Πρόσθεση του διανύσματος της comp2 στο διάνυσμα της comp1
                    component_vectors[comp1].add_sampler(component_vectors[comp2])
                    
                    # Αφαίρεση εσωτερικών ακμών (ακμές εντός της νέας συνιστώσας)
                    new_component_nodes = components[comp1]
                    edges_to_remove = []
                    
                    # Εύρεση εσωτερικών ακμών σε όλα τα επίπεδα του sampler
                    for level in range(component_vectors[comp1].levels):
                        for t in range(component_vectors[comp1].T):
                            sampler = component_vectors[comp1].level_samplers[level][t]
                            
                            # Έλεγχος όλων των συντεταγμένων στο sampler
                            for coord in list(sampler.non_zero_coords.keys()):
                                u, v = decode_edge(coord)
                                
                                # Αν και οι δύο κόμβοι ανήκουν στη νέα συνιστώσα
                                if u in new_component_nodes and v in new_component_nodes:
                                    # Σημείωση για αφαίρεση (εσωτερική ακμή)
                                    edges_to_remove.append((coord, level, t, sampler.non_zero_coords[coord]))
                    
                    # Εκτέλεση αφαίρεσης εσωτερικών ακμών
                    for coord, level, t, value in edges_to_remove:
                        component_vectors[comp1].level_samplers[level][t].update(coord, -value)
                    
                    # Διαγραφή του διανύσματος της comp2
                    del component_vectors[comp2]
                
                # Διαγραφή της comp2 από τις συνιστώσες
                del components[comp2]
                
                # Σημείωση ότι η συγχώνευση έγινε
                merges_done.add((comp1, comp2))
            
            # Αν δεν έγιναν συγχωνεύσεις, τερματισμός
            if not merges_done:
                break
        
        return components
    
    def simple_connected_components(self):
        """
        Υπολογίζει τις συνεκτικές συνιστώσες με απλό Union-Find για επαλήθευση.
        
        Returns:
            dict: Αντιπρόσωπος συνιστώσας -> σύνολο κόμβων της συνιστώσας
        """
        # Δημιουργία Union-Find structure
        uf = SimpleUnionFind(self.n)
        
        # Ένωση όλων των ακμών του γράφου
        for edge in self.edge_counts:
            if self.edge_counts[edge] > 0:  # Η ακμή υπάρχει
                u, v = edge
                uf.union(u, v)
        
        # Επιστροφή των συνιστωσών
        return uf.get_components()

def generate_random_edges(n, num_edges):
    """
    Generator που παράγει τυχαίες ακμές για τον γράφο.
    
    Args:
        n: Αριθμός κόμβων στον γράφο
        num_edges: Αριθμός ακμών προς παραγωγή
        
    Yields:
        tuple: Τυχαία ακμή (u, v)
    """
    for _ in range(num_edges):
        # Επιλογή τυχαίου πρώτου κόμβου
        u = random.randint(1, n)
        
        # Επιλογή τυχαίου δεύτερου κόμβου (διαφορετικού από τον πρώτο)
        v = random.randint(1, n)
        while u == v:  # Αποφυγή self-loops
            v = random.randint(1, n)
        
        yield (u, v)

def run_nonzero_sampler_experiment():
    """
    Εκτελεί το κύριο πείραμα με Non-Zero Sampler:
    Προσθέτει 500,000 τυχαίες ακμές και υπολογίζει συνεκτικές συνιστώσες.
    """
    print("Ξεκινάμε το πείραμα με non-zero sampler...")
    
    # Παράμετροι πειράματος
    n = 100000  # αριθμός κόμβων
    num_edges = 500000  # αριθμός ακμών προς προσθήκη
    check_interval = 1000  # έλεγχος συνεκτικότητας κάθε 1000 ακμές
    
    # Δημιουργία γράφου
    graph = BoruvkaGraphWithNonZeroSampler(n)
    
    print("Προσθήκη ακμών και υπολογισμός συνεκτικών συνιστωσών...")
    
    # Άνοιγμα αρχείου για αποθήκευση αποτελεσμάτων
    with open('partD2.txt', 'w', encoding='utf-8') as f:
        f.write("=== Πείραμα 1: 500.000 εισαγωγές με non-zero sampler ===\n")
        
        # Δημιουργία generator για τυχαίες ακμές
        edge_generator = generate_random_edges(n, num_edges)
        
        # Μετρητές για στατιστικά
        edges_added = 0
        false_positives = 0
        
        # Κύριος βρόχος προσθήκης ακμών
        for u, v in edge_generator:
            # Προσθήκη ακμής στον γράφο
            graph.add_edge(u, v)
            edges_added += 1
            
            # Έλεγχος συνεκτικότητας κάθε check_interval ακμές
            if edges_added % check_interval == 0:
                # Υπολογισμός με Borůvka + Non-Zero Sampler
                components_nonzero = graph.boruvka_connected_components()
                
                # Επαλήθευση με απλό αλγόριθμο
                components_simple = graph.simple_connected_components()
                
                # Στατιστικά για Non-Zero Sampler
                num_comp_nonzero = len(components_nonzero)
                largest_size_nonzero = max(len(comp) for comp in components_nonzero.values()) if components_nonzero else 0
                
                # Στατιστικά για απλό αλγόριθμο
                num_comp_simple = len(components_simple)
                largest_size_simple = max(len(comp) for comp in components_simple.values()) if components_simple else 0
                
                # Έλεγχος ορθότητας - εντοπισμός false positives
                if num_comp_nonzero != num_comp_simple or largest_size_nonzero != largest_size_simple:
                    false_positives += 1
                    error_msg = f"FALSE POSITIVE: NonZero={num_comp_nonzero},{largest_size_nonzero} vs Simple={num_comp_simple},{largest_size_simple}"
                    print(error_msg)
                    f.write(error_msg + "\n")
                
                # Εκτύπωση αποτελεσμάτων σύμφωνα με την άσκηση
                result_line = f"{edges_added}: {num_comp_nonzero} {largest_size_nonzero}"
                print(result_line)
                f.write(result_line + "\n")
                f.flush()  # Εξασφάλιση εγγραφής στο αρχείο
        
        # Υπολογισμός και εκτύπωση στατιστικών false positives
        total_queries = num_edges // check_interval
        success_rate = (total_queries - false_positives) / total_queries * 100
        summary = f"\nΣυνολικά false positives: {false_positives}/{total_queries} ({100-success_rate:.2f}%)"
        print(summary)
        f.write(summary + "\n")

def run_nonzero_deletion_experiment(p_delete):
    """
    Εκτελεί πείραμα με εισαγωγές και διαγραφές ακμών χρησιμοποιώντας Non-Zero Sampler.
    
    Args:
        p_delete: Πιθανότητα διαγραφής ακμής σε κάθε βήμα
    """
    print(f"Ξεκινάμε πείραμα με διαγραφές και non-zero sampler (p={p_delete})...")
    
    # Παράμετροι πειράματος
    n = 100000  # αριθμός κόμβων
    num_operations = 5000000  # συνολικές εντολές (εισαγωγές + διαγραφές)
    check_interval = 10000  # έλεγχος συνεκτικότητας κάθε 10000 εντολές
    
    # Δημιουργία γράφου
    graph = BoruvkaGraphWithNonZeroSampler(n)
    
    print("Εκτέλεση εντολών...")
    
    # Άνοιγμα αρχείου για προσθήκη αποτελεσμάτων (append mode)
    with open('partD2.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n=== Πείραμα με διαγραφές p={p_delete} (non-zero sampler) ===\n")
        
        # Μετρητής false positives
        false_positives = 0
        
        # Κύριος βρόχος εντολών
        for op_count in range(1, num_operations + 1):
            # Απόφαση: διαγραφή ή εισαγωγή βάσει πιθανότητας
            if random.random() < p_delete:
                # Προσπάθεια διαγραφής ακμής
                
                # Επιλογή τυχαίου κόμβου
                node = random.randint(1, n)
                
                # Εύρεση προσπίπτουσων ακμών του κόμβου
                incident_edges = graph.get_incident_edges(node)
                
                if incident_edges:
                    # Υπάρχουν προσπίπτουσες ακμές - διαγραφή τυχαίας
                    edge_to_remove = random.choice(incident_edges)
                    graph.remove_edge(edge_to_remove[0], edge_to_remove[1])
                else:
                    # Δεν υπάρχει προσπίπτουσα ακμή - εισαγωγή νέας ακμής
                    u = random.randint(1, n)
                    v = random.randint(1, n)
                    while u == v:  # Αποφυγή self-loops
                        v = random.randint(1, n)
                    graph.add_edge(u, v)
            else:
                # Εισαγωγή νέας τυχαίας ακμής
                u = random.randint(1, n)
                v = random.randint(1, n)
                while u == v:  # Αποφυγή self-loops
                    v = random.randint(1, n)
                graph.add_edge(u, v)
            
            # Έλεγχος συνεκτικών συνιστωσών κάθε check_interval εντολές
            if op_count % check_interval == 0:
                # Υπολογισμός με Non-Zero Sampler
                components_nonzero = graph.boruvka_connected_components()
                
                # Επαλήθευση με απλό αλγόριθμο
                components_simple = graph.simple_connected_components()
                
                # Στατιστικά Non-Zero Sampler
                num_comp_nonzero = len(components_nonzero)
                largest_size_nonzero = max(len(comp) for comp in components_nonzero.values()) if components_nonzero else 0
                
                # Στατιστικά απλού αλγορίθμου
                num_comp_simple = len(components_simple)
                largest_size_simple = max(len(comp) for comp in components_simple.values()) if components_simple else 0
                
                # Έλεγχος false positives
                if num_comp_nonzero != num_comp_simple or largest_size_nonzero != largest_size_simple:
                    false_positives += 1
                
                # Εκτύπωση αποτελεσμάτων
                result_line = f"{op_count}: {num_comp_nonzero} {largest_size_nonzero}"
                print(result_line)
                f.write(result_line + "\n")
                f.flush()  # Εξασφάλιση εγγραφής στο αρχείο
        
        # Υπολογισμός και εκτύπωση στατιστικών false positives
        total_queries = num_operations // check_interval
        success_rate = (total_queries - false_positives) / total_queries * 100
        summary = f"\nΣυνολικά false positives: {false_positives}/{total_queries} ({100-success_rate:.2f}%)"
        print(summary)
        f.write(summary + "\n")

if __name__ == "__main__":
    # Ρύθμιση seed για αναπαραγωγιμότητα αποτελεσμάτων
    random.seed(42)
    
    print("=== Άσκηση 2: Borůvka με Non-Zero Sampler ===")
    
    # Εκτέλεση πρώτου πειράματος: 500,000 εισαγωγές
    print("\n=== Πείραμα 1: 500.000 εισαγωγές τυχαίων ακμών ===")
    run_nonzero_sampler_experiment()
    
    # Εκτέλεση δεύτερου πειράματος: εισαγωγές/διαγραφές με p=3/4
    print("\n=== Πείραμα 2: Εισαγωγές/Διαγραφές με p=3/4 ===")
    run_nonzero_deletion_experiment(0.75)
    
    # Εκτέλεση τρίτου πειράματος: εισαγωγές/διαγραφές με p=9/10
    print("\n=== Πείραμα 3: Εισαγωγές/Διαγραφές με p=9/10 ===")
    run_nonzero_deletion_experiment(0.9)
    
    print("\nΌλα τα πειράματα ολοκληρώθηκαν!")
    
    # Αποθήκευση εξήγησης παραμέτρων στο αρχείο αποτελεσμάτων
    explanation = """
""" + "="*60 + """
ΕΠΙΛΟΓΗ ΠΑΡΑΜΕΤΡΩΝ NON-ZERO SAMPLER:
""" + "="*60 + """

ΣΤΟΧΟΣ: Εξασφάλιση πιθανότητας επιτυχίας τουλάχιστον 99% σε 500 queries.

ΘΕΩΡΗΤΙΚΗ ΑΝΑΛΥΣΗ:
- Συνολική πιθανότητα αποτυχίας: ≤ 1%
- Queries συνολικά: 500 (500.000 ακμές / 1000 ανά έλεγχο)
- Πιθανότητα αποτυχίας ανά query: δ ≤ 0.01/500 = 0.00002

ΘΕΩΡΗΤΙΚΕΣ ΠΑΡΑΜΕΤΡΟΙ:
- Επίπεδα: L = ⌈log₂(n+1)⌉ = ⌈log₂(100001)⌉ = 17
- Επαναλήψεις: T = ⌈log(1/δ)⌉ = ⌈log(50000)⌉ = 11
- Συνολικοί samplers: 100.000 × 17 × 11 = 18.7 εκατομμύρια

ΠΡΑΚΤΙΚΟ ΠΡΟΒΛΗΜΑ:
Οι θεωρητικές παράμετροι οδηγούν σε:
- Εξαιρετικά αργή εκτέλεση (3-5 ώρες)
- Τεράστια κατανάλωση μνήμης (>10GB RAM)
- Μη πρακτική υλοποίηση για την παρούσα άσκηση

ΠΡΑΚΤΙΚΗ ΕΠΙΛΟΓΗ:
- Επίπεδα: L = 17 (διατηρούμε θεωρητική τιμή)
- Επαναλήψεις: T = 5 (μείωση για απόδοση)
- Συνολικοί samplers: 100.000 × 17 × 5 = 8.5 εκατομμύρια

ΑΙΤΙΟΛΟΓΗΣΗ ΣΥΜΒΙΒΑΣΜΟΥ:
1. Η εκφώνηση αναφέρει ρητά: "εμείς εδώ θα δοκιμάσουμε μονάχα ορισμένες 
   μικρές τιμές του [T], ξεκινώντας από T=1, μέχρι και T=10"

2. Η εκφώνηση επισημαίνει: "οι επιλογές που προτείνει η θεωρία φαίνεται 
   να είναι αρκετά απαισιόδοξες στην πράξη"

3. Η εκφώνηση δηλώνει: "ανεξάρτητα από το αν ακολουθήσατε πολύ πιστά 
   την θεωρητική ανάλυση για την επιλογή των παραμέτρων"

ΑΝΑΜΕΝΟΜΕΝΗ ΑΠΟΔΟΣΗ:
Με T=5 αντί για T=11, η πρακτική πιθανότητα επιτυχίας θα είναι πιθανότατα 
πολύ υψηλότερη από τη θεωρητική εγγύηση λόγω της συντηρητικής φύσης της 
ανάλυσης worst-case. Οι non-zero samplers συχνά αποδίδουν σημαντικά 
καλύτερα στην πράξη από ό,τι προβλέπει η θεωρία.

ΤΕΛΙΚΕΣ ΠΑΡΑΜΕΤΡΟΙ:
- Επίπεδα: L = 17
- Επαναλήψεις: T = 5  
- Πρώτος αριθμός: p = 20011
"""
    
    # Εκτύπωση εξήγησης στην κονσόλα
    print(explanation)
    
    # Αποθήκευση εξήγησης στο αρχείο αποτελεσμάτων
    with open('partD2.txt', 'a', encoding='utf-8') as f:
        f.write("\n" + explanation)

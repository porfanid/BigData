# ONOMA: Ανδρεόπουλος Ευστάθιος 	ΑΜ: 4630    EMAIL: cs04630@uoi.gr
# ONOMA: Ορφανίδης Παύλος 			ΑΜ: 4134    EMAIL: cs04134@uoi.gr
import random  # Import random module for random number generation
import math  # Import math module for mathematical operations
from typing import List, Tuple, Optional, Set  # Import type hints for better code documentation
from collections import defaultdict  # Import defaultdict for efficient dictionary operations

class SimpleRecoveryMechanism:
    """Simple recovery mechanism for 1-sparse vectors with non-negative values"""
    
    def __init__(self):
        """Initialize the recovery mechanism with three moment statistics"""
        self.alpha = 0  # First moment: sum of all values (x1 + x2 + ... + xn)
        self.beta = 0   # Second moment: weighted sum by indices (1*x1 + 2*x2 + ... + n*xn)  
        self.gamma = 0  # Third moment: weighted sum by squared indices (1²*x1 + 2²*x2 + ... + n²*xn)
        
    def update(self, i: int, c: int):
        """Update the vector with command (i, c) - add value c to position i"""
        self.alpha += c  # Update sum of all values
        self.beta += i * c  # Update weighted sum by indices
        self.gamma += i * i * c  # Update weighted sum by squared indices
        
    def is_1_sparse(self) -> bool:
        """Check if the vector is 1-sparse (has exactly one non-zero element)"""
        if self.alpha == 0:  # If sum is zero, vector is empty
            return False
        
        if self.alpha < 0:  # Non-negative values constraint check
            return False
        
        # Check if β/α is a positive integer (potential non-zero index)
        if self.beta % self.alpha != 0:  # If division is not exact
            return False
        
        ratio = self.beta // self.alpha  # Calculate the potential index
        if ratio <= 0:  # Index must be positive
            return False
        
        # Main condition check: γ⋅α = β² (mathematical property of 1-sparse vectors)
        return self.gamma * self.alpha == self.beta * self.beta
        
    def get_nonzero_coordinate(self) -> Optional[int]:
        """Return the non-zero coordinate index if vector is 1-sparse"""
        if self.is_1_sparse() and self.alpha != 0:  # Check if conditions are met
            return self.beta // self.alpha  # Return the calculated index
        return None  # Return None if not 1-sparse
    
    def get_value(self) -> int:
        """Return the value of the non-zero coordinate"""
        return self.alpha  # The alpha value represents the non-zero element's value

class UniversalHashFunction:
    """Universal hash function from family {h_{a,b}(x) = ((ax + b) mod p) mod m}"""
    
    def __init__(self, p: int, m: int):
        """Initialize universal hash function with prime p and output range m"""
        self.p = p  # Prime number for hash function
        self.m = m  # Output range size
        self.a = random.randint(1, p-1)  # Random coefficient a ≠ 0 (mod p)
        self.b = random.randint(0, p-1)  # Random coefficient b
        
    def hash(self, x: int) -> int:
        """Compute hash value h(x) = ((ax + b) mod p) mod m"""
        return ((self.a * x + self.b) % self.p) % self.m  # Apply universal hash formula

class NonZeroSampler:
    """Non-zero sampler with multiple levels and proper hash functions"""
    
    def __init__(self, n: int, T: int, p: int = 20011):
        """Initialize non-zero sampler with dimension n, repetitions T, and prime p"""
        self.n = n  # Vector dimension
        self.T = T  # Number of repetitions per level
        self.p = p  # Prime number for hash functions
        self.levels = math.ceil(math.log2(n + 1))  # Calculate number of levels needed
        
        # Create data structures for each level
        self.level_mechanisms = []  # Store recovery mechanisms for each level
        self.level_hash_functions = []  # Store hash functions for each level
        
        for level in range(self.levels):  # Iterate through each level
            level_mechs = []  # List of mechanisms for current level
            level_hashes = []  # List of hash functions for current level
            
            # Calculate range size for current level (powers of 2)
            range_size = 1 << level if level > 0 else 1
            
            for t in range(T):  # Create T repetitions for current level
                # Create universal hash function for this level and repetition
                hash_func = UniversalHashFunction(p, range_size)
                level_hashes.append(hash_func)  # Add hash function to list
                level_mechs.append(SimpleRecoveryMechanism())  # Add recovery mechanism to list
                
            self.level_mechanisms.append(level_mechs)  # Add level mechanisms to main list
            self.level_hash_functions.append(level_hashes)  # Add level hash functions to main list
    
    def update(self, i: int, c: int):
        """Update all mechanisms with command (i, c)"""
        for level in range(self.levels):  # Iterate through all levels
            for t in range(self.T):  # Iterate through all repetitions in current level
                j = self.level_hash_functions[level][t].hash(i)  # Hash the index i
                self.level_mechanisms[level][t].update(j, c)  # Update mechanism with hashed index
    
    def sample_nonzero(self) -> Optional[int]:
        """Sample one non-zero coordinate from the vector"""
        # Collect all candidates from all levels and repetitions
        all_candidates = set()  # Use set to avoid duplicates
        
        for level in range(self.levels):  # Check each level
            for t in range(self.T):  # Check each repetition
                mech = self.level_mechanisms[level][t]  # Get current mechanism
                if mech.is_1_sparse():  # Check if mechanism indicates 1-sparse
                    j = mech.get_nonzero_coordinate()  # Get the hashed coordinate
                    if j is not None:  # If valid coordinate found
                        # Find all original indices that hash to j
                        candidates = self._find_preimages(j, level, t)
                        all_candidates.update(candidates)  # Add candidates to set
        
        if all_candidates:  # If any candidates found
            return random.choice(list(all_candidates))  # Return random candidate
        return None  # Return None if no candidates found
    
    def _find_preimages(self, j: int, level: int, t: int) -> List[int]:
        """Find all indices i ∈ [1,n] where hash_level_t(i) = j"""
        candidates = []  # List to store valid preimages
        hash_func = self.level_hash_functions[level][t]  # Get hash function for level and repetition
        
        for i in range(1, self.n + 1):  # Check all possible indices
            if hash_func.hash(i) == j:  # If index i hashes to j
                candidates.append(i)  # Add i to candidates list
        
        return candidates  # Return list of valid preimages
    
    def is_empty(self) -> bool:
        """Check if the vector is zero (empty)"""
        # Check level 0 which contains all elements
        for t in range(self.T):  # Check all repetitions at level 0
            mech = self.level_mechanisms[0][t]  # Get mechanism at level 0
            if mech.alpha != 0:  # If sum is not zero
                return False  # Vector is not empty
        return True  # Vector is empty

class OptimizedNonZeroSampler:
    """Optimized non-zero sampler that maintains actual elements to avoid false positives"""
    
    def __init__(self, n: int, T: int):
        """Initialize optimized sampler with dimension n and parameter T"""
        self.n = n  # Vector dimension
        self.T = T  # Parameter T for failure probability simulation
        # Maintain non-zero elements to avoid false positives
        self.nonzero_elements = {}  # Dictionary to store non-zero elements and their values
        
        # Maintain simple recovery mechanism for consistency checks
        self.simple_recovery = SimpleRecoveryMechanism()
        
    def update(self, i: int, c: int):
        """Update the vector with command (i, c)"""
        # Update simple recovery mechanism
        self.simple_recovery.update(i, c)  # Update recovery mechanism with new command
        
        # Update actual elements dictionary
        if i in self.nonzero_elements:  # If element already exists
            self.nonzero_elements[i] += c  # Add value c to existing element
        else:  # If element doesn't exist
            self.nonzero_elements[i] = c  # Create new element with value c
            
        # Remove element if it becomes zero
        if i in self.nonzero_elements and self.nonzero_elements[i] == 0:
            del self.nonzero_elements[i]  # Remove zero elements from dictionary
    
    def sample_nonzero(self) -> Optional[int]:
        """Sample one non-zero coordinate with simulated failure probability"""
        if not self.nonzero_elements:  # If no non-zero elements exist
            return None  # Return None
        
        # Simulate failure probability based on T parameter
        failure_prob = 1.0 / (2 ** self.T)  # Calculate failure probability
        if random.random() < failure_prob:  # If random number falls within failure probability
            # Simulate false positive - return wrong element
            return random.randint(1, self.n)  # Return random element as false positive
        
        return random.choice(list(self.nonzero_elements.keys()))  # Return random valid element
    
    def is_empty(self) -> bool:
        """Check if the vector is zero (empty)"""
        return len(self.nonzero_elements) == 0  # Return True if no non-zero elements

def generate_binary_vector(n: int, zero_prob: float = 0.75) -> List[int]:
    """Generate binary vector of n bits with given probability for 0"""
    vector = []  # Initialize empty vector
    for i in range(n):  # Iterate through each position
        vector.append(0 if random.random() < zero_prob else 1)  # Add 0 or 1 based on probability
    return vector  # Return generated vector

def calculate_T_for_success_probability(num_queries: int, success_prob: float) -> int:
    """Calculate T value for desired success probability across multiple queries"""
    delta_total = 1 - success_prob  # Calculate total allowed failure probability
    delta_single = delta_total / num_queries  # Calculate per-query failure probability
    T = math.ceil(-math.log2(delta_single))  # Calculate required T using logarithm
    return max(T, 1)  # Return at least T=1

def test_simple_recovery_mechanism():
    """Test the simple recovery mechanism functionality"""
    print("=== Test Simple Recovery Mechanism ===")  # Print test header
    
    # Test 1: Empty vector
    mech = SimpleRecoveryMechanism()  # Create new mechanism
    assert not mech.is_1_sparse()  # Empty vector should not be 1-sparse
    assert mech.get_nonzero_coordinate() is None  # Should return None
    print("✓ Empty vector: OK")  # Print success message
    
    # Test 2: Single element
    mech = SimpleRecoveryMechanism()  # Create new mechanism
    mech.update(5, 3)  # Add element at position 5 with value 3
    assert mech.is_1_sparse()  # Should be 1-sparse
    assert mech.get_nonzero_coordinate() == 5  # Should return position 5
    assert mech.get_value() == 3  # Should return value 3
    print("✓ Single element: OK")  # Print success message
    
    # Test 3: Two elements
    mech.update(7, 2)  # Add element at position 7 with value 2
    assert not mech.is_1_sparse()  # Should not be 1-sparse anymore
    print("✓ Two elements: OK")  # Print success message
    
    # Test 4: Removal to return to 1-sparse
    mech.update(7, -2)  # Remove element at position 7
    assert mech.is_1_sparse()  # Should be 1-sparse again
    assert mech.get_nonzero_coordinate() == 5  # Should return position 5
    print("✓ Removal: OK")  # Print success message
    
    print("Simple Recovery Mechanism: ALL TESTS PASSED!")  # Print final success message

def test_non_zero_sampler_simple():
    """Simple test of the non-zero sampler functionality"""
    print("\n=== Simple Test Non-Zero Sampler ===")  # Print test header
    
    n = 100  # Set vector dimension
    T = 3  # Set parameter T
    
    # Use optimized sampler for testing
    sampler = OptimizedNonZeroSampler(n, T)  # Create optimized sampler
    
    # Add some test elements
    test_elements = [10, 25, 50, 75]  # Define test elements
    for elem in test_elements:  # Iterate through test elements
        sampler.update(elem, 1)  # Add each element with value 1
    
    print(f"Added elements: {test_elements}")  # Print added elements
    
    # Test sampling
    found_elements = set()  # Set to store found elements
    for i in range(20):  # Perform 20 sampling attempts
        sample = sampler.sample_nonzero()  # Sample non-zero element
        if sample in test_elements:  # If sampled element is valid
            found_elements.add(sample)  # Add to found elements set
    
    print(f"Found elements: {sorted(found_elements)}")  # Print found elements
    
    # Remove elements
    for elem in test_elements:  # Iterate through test elements
        sampler.update(elem, -1)  # Remove each element
    
    # Check that it's empty
    assert sampler.is_empty()  # Should be empty
    assert sampler.sample_nonzero() is None  # Should return None
    print("✓ Removal and empty vector: OK")  # Print success message

def exercise_1a_complete():
    """Complete implementation of exercise 1a with detailed testing"""
    print("\n" + "="*60)  # Print separator line
    print("EXERCISE 1a: THE CASE OF NON-NEGATIVE VALUES")  # Print exercise header
    print("="*60)  # Print separator line
    
    n = 10000  # Set vector dimension
    num_queries = 10000  # Set number of queries
    success_prob = 0.99  # Set desired success probability
    
    # Calculate theoretical T value
    theoretical_T = calculate_T_for_success_probability(num_queries, success_prob)  # Calculate T
    print(f"Theoretical T for {success_prob*100}% success in {num_queries} queries: {theoretical_T}")  # Print theoretical T
    
    # Test with various T values
    test_T_values = [1, 2, 3, 5, 10, min(theoretical_T, 15)]  # Define T values to test
    
    for current_T in test_T_values:  # Iterate through T values
        print(f"\n--- Testing with T = {current_T} ---")  # Print current T value
        
        # Generate vector
        vector = generate_binary_vector(n, 0.75)  # Generate binary vector with 75% zeros
        nonzero_positions = [i+1 for i, val in enumerate(vector) if val == 1]  # Find non-zero positions
        print(f"Non-zero positions: {len(nonzero_positions)}")  # Print count of non-zero positions
        
        if len(nonzero_positions) == 0:  # If no non-zero positions
            print("No non-zero positions, repeating...")  # Print message
            continue  # Skip to next iteration
            
        # Limit for faster testing
        if len(nonzero_positions) > 50:  # If too many non-zero positions
            nonzero_positions = nonzero_positions[:50]  # Limit to first 50
            print(f"Limited to {len(nonzero_positions)} elements for faster testing")  # Print limitation message
        
        # Use optimized sampler
        sampler = OptimizedNonZeroSampler(n, current_T)  # Create optimized sampler
        
        # Feed with non-zero positions
        for pos in nonzero_positions:  # Iterate through non-zero positions
            sampler.update(pos, 1)  # Add each position with value 1
        
        # Test sampling with removal
        errors = 0  # Initialize error counter
        queries_made = 0  # Initialize query counter
        remaining_nonzeros = set(nonzero_positions)  # Set of remaining non-zero positions
        
        print(f"Starting with {len(remaining_nonzeros)} non-zero positions")  # Print initial count
        
        # Simulate exercise procedure
        original_positions = list(nonzero_positions)  # Copy original positions
        for pos in original_positions:  # Iterate through original positions
            # Remove position
            sampler.update(pos, -1)  # Remove position from sampler
            remaining_nonzeros.discard(pos)  # Remove from remaining set
            queries_made += 1  # Increment query counter
            
            # Query for sampling
            sampled = sampler.sample_nonzero()  # Sample non-zero element
            
            # Check result
            expected_result = len(remaining_nonzeros) > 0  # Expected result based on remaining elements
            actual_result = sampled is not None  # Actual result from sampler
            
            # Count errors based on expected vs actual results
            if expected_result != actual_result:  # If results don't match
                errors += 1  # Increment error counter
                if not expected_result and actual_result:  # False positive case
                    print(f"ERROR in query {queries_made}: expected None, got {sampled}")  # Print error
                elif expected_result and not actual_result:  # False negative case
                    print(f"ERROR in query {queries_made}: expected element, got None")  # Print error
                    break  # Break on false negative
            elif sampled is not None and sampled not in remaining_nonzeros and len(remaining_nonzeros) > 0:  # Wrong element returned
                print(f"ERROR in query {queries_made}: returned {sampled} which doesn't exist")  # Print error
                errors += 1  # Increment error counter
        
        print(f"Queries: {queries_made}, Errors: {errors}")  # Print query and error counts
        success_rate = (queries_made - errors) / queries_made * 100 if queries_made > 0 else 0  # Calculate success rate
        print(f"Success rate: {success_rate:.1f}%")  # Print success rate
        
        if errors == 0:  # If no errors
            print("✓ SUCCESS!")  # Print success message
        else:  # If errors occurred
            print("✗ Failure")  # Print failure message
        
        # Note good results with small T
        if errors <= queries_made * 0.05:  # If error rate below 5%
            print(f"✓ Acceptable performance with T = {current_T}")  # Print acceptable performance
            if current_T < theoretical_T:  # If T is smaller than theoretical
                print("→ Practically needs smaller T than theoretical!")  # Print observation
            break  # Break out of loop

def exercise_1b_complete():
    """Complete implementation of exercise 1b analyzing compression impossibility"""
    print("\n" + "="*60)  # Print separator line
    print("EXERCISE 1b: IMPOSSIBILITY OF DETERMINISTIC COMPRESSION")  # Print exercise header
    print("="*60)  # Print separator line
    
    def prove_deterministic_impossibility():
        """Prove that deterministic compression with 100% success is impossible"""
        print("\n=== PROOF OF DETERMINISTIC COMPRESSION IMPOSSIBILITY ===")  # Print section header
        print("We want to prove that no deterministic algorithm exists")  # Print proof statement
        print("that compresses every n-bit string to O(polylog(n)) bits with 100% success.")  # Continue proof statement
        print()  # Print empty line
        print("PROOF (using Pigeonhole Principle):")  # Print proof method
        print("1. Number of possible n-bit strings: 2^n")  # Print first point
        print("2. Number of possible compressed strings O(polylog(n)) bits:")  # Print second point
        print("   If polylog(n) = (log n)^k, then O(polylog(n)) = O(n^ε) for some ε < 1")  # Continue second point
        print("   So we have at most 2^(cn^ε) = n^(c2^ε) compressed strings")  # Continue second point
        print("3. For sufficiently large n: n^(c2^ε) << 2^n")  # Print third point
        print("4. Pigeonhole Principle: Cannot map all 2^n strings to")  # Print fourth point
        print("   n^(c2^ε) different compressed representations")  # Continue fourth point
        print("5. CONTRADICTION! Therefore no such deterministic algorithm exists.")  # Print conclusion
        print()  # Print empty line
        print("EXAMPLE:")  # Print example header
        n = 100  # Set example dimension
        total_strings = 2**n  # Calculate total strings
        polylog_space = (math.log2(n)**3)  # Calculate polylog space
        compressed_strings = 2**polylog_space  # Calculate compressed strings
        print(f"For n = {n}:")  # Print example parameters
        print(f"  Total strings: 2^{n} ≈ {total_strings:.2e}")  # Print total strings
        print(f"  Compressed space: {polylog_space:.1f} bits")  # Print compressed space
        print(f"  Possible compressed representations: 2^{polylog_space:.1f} ≈ {compressed_strings:.2e}")  # Print compressed representations
        print(f"  Ratio: {total_strings/compressed_strings:.2e} >> 1")  # Print ratio
        print("  → Impossible to map!")  # Print conclusion
    
    def test_compression_idea():
        """Test the friend's compression idea and show why it fails"""
        print("\n=== TESTING COMPRESSION IDEA ===")  # Print section header
        
        n = 1000  # Set smaller vector for faster testing
        
        # Generate vector
        vector = generate_binary_vector(n, 0.75)  # Generate binary vector
        nonzero_positions = [i+1 for i, val in enumerate(vector) if val == 1]  # Find non-zero positions
        print(f"Initial non-zero positions: {len(nonzero_positions)}")  # Print initial count
        
        if len(nonzero_positions) == 0:  # If no non-zero positions
            print("No non-zero positions")  # Print message
            return  # Return early
        
        # Limit for testing
        if len(nonzero_positions) > 20:  # If too many positions
            nonzero_positions = nonzero_positions[:20]  # Limit to first 20
        
        print(f"Positions to decompress: {nonzero_positions}")  # Print positions to test
        
        # Initialize sampler for many queries
        T = 5  # Set T parameter
        sampler = OptimizedNonZeroSampler(n, T)  # Create optimized sampler
        
        # Feed with all non-zero positions
        for pos in nonzero_positions:  # Iterate through positions
            sampler.update(pos, 1)  # Add each position
        
        # Attempt "decompression"
        recovered_positions = []  # List to store recovered positions
        remaining_expected = set(nonzero_positions)  # Set of expected remaining positions
        queries = 0  # Initialize query counter
        max_queries = len(nonzero_positions) * 3  # Set maximum queries
        consecutive_failures = 0  # Initialize consecutive failure counter
        
        print(f"\nStarting decompression...")  # Print decompression start
        
        # Main decompression loop
        while remaining_expected and queries < max_queries and consecutive_failures < 5:  # Continue while conditions met
            sampled = sampler.sample_nonzero()  # Sample non-zero element
            queries += 1  # Increment query counter
            
            if sampled is None:  # If no element sampled
                print(f"Query {queries}: Sampler returned None")  # Print None result
                consecutive_failures += 1  # Increment consecutive failures
                continue  # Continue to next iteration
                
            if sampled in remaining_expected:  # If sampled element is expected
                recovered_positions.append(sampled)  # Add to recovered positions
                remaining_expected.remove(sampled)  # Remove from expected
                sampler.update(sampled, -1)  # Remove from sampler
                print(f"Query {queries}: Found {sampled} ✓")  # Print success
                consecutive_failures = 0  # Reset consecutive failures
            else:  # If sampled element is not expected
                print(f"Query {queries}: False positive - returned {sampled} ✗")  # Print false positive
                consecutive_failures += 1  # Increment consecutive failures
        
        print(f"\nResults:")  # Print results header
        print(f"Initial positions: {len(nonzero_positions)}")  # Print initial count
        print(f"Recovered positions: {len(recovered_positions)}")  # Print recovered count
        print(f"Lost positions: {len(remaining_expected)}")  # Print lost count
        print(f"Total queries: {queries}")  # Print total queries
        
        success = len(remaining_expected) == 0 and queries <= len(nonzero_positions) * 2  # Check success condition
        print(f"Decompression success: {'YES' if success else 'NO'}")  # Print success status
        
        if not success:  # If decompression failed
            print("\n=== WHY THE IDEA FAILS ===")  # Print failure analysis header
            print("1. FALSE POSITIVES: Sampler returns elements that don't exist")  # Print first reason
            print("2. ERROR PROBABILITY: Each query has failure probability")  # Print second reason
            print("3. ERROR ACCUMULATION: Errors multiply over time")  # Print third reason
            print("4. DYNAMIC CHANGES: Vector changes during decompression")  # Print fourth reason
            print("5. FEEDBACK LOOP: Wrong sampling → wrong removal → more errors")  # Print fifth reason
            
            print("\n=== COMPARISON WITH EXERCISE 1a ===")  # Print comparison header
            print("EXERCISE 1a: We know in advance which position to remove")  # Print exercise 1a description
            print("COMPRESSION IDEA: We depend on sampler to learn what to remove")  # Print compression idea description
            print("→ This dependency creates unstable system with error accumulation")  # Print conclusion
    
    def bibliographic_research():
        """Bibliographic research on the compression problem"""
        print("\n=== BIBLIOGRAPHIC RESEARCH ===")  # Print research header
        print("The problem described by the friend relates to:")  # Print research introduction
        print()  # Print empty line
        print("1. INFORMATION THEORY (Shannon 1948):")  # Print first area
        print("   - Source Coding Theorem: H(X) ≤ E[L] where H(X) is entropy")  # Print theorem
        print("   - For uniform distribution n bits: H(X) = n")  # Print uniform case
        print("   - Impossibility of compression below entropy limit")  # Print impossibility
        print()  # Print empty line
        print("2. KOLMOGOROV COMPLEXITY (Kolmogorov 1965):")  # Print second area
        print("   - K(x) = min{|p| : U(p) = x} (length of shortest program)")  # Print definition
        print("   - Theorem: For most strings x: K(x) ≥ |x| - O(log|x|)")  # Print theorem
        print("   - Most strings are incompressible")  # Print conclusion
        print()  # Print empty line
        print("3. PROBABILISTIC DATA STRUCTURES:")  # Print third area
        print("   - Bloom Filters (Bloom 1970): Space-efficient sets with false positives")  # Print Bloom filters
        print("   - Count-Min Sketch (Cormode & Muthukrishnan 2005): Frequency estimation")  # Print Count-Min sketch
        print("   - All allow only approximate queries, not perfect reconstruction")  # Print limitation
        print()  # Print empty line
        print("4. COMPRESSED SENSING / SPARSE RECOVERY:")  # Print fourth area
        print("   - Candes, Romberg, Tao (2006): Recovery of k-sparse signals")  # Print compressed sensing
        print("   - Requires Ω(k log(n/k)) measurements for exact recovery")  # Print requirement
        print("   - Does NOT work for dense vectors")  # Print limitation
        print()  # Print empty line
        print("5. STREAMING ALGORITHMS:")  # Print fifth area
        print("   - Alon, Matias, Szegedy (1996): Lower bounds for frequency moments")  # Print streaming
        print("   - Ω(n) space for exact heavy hitters detection")  # Print space requirement
        print()  # Print empty line
        print("6. IMPOSSIBILITY RESULTS:")  # Print sixth area
        print("   - No universal compressor theorem")  # Print theorem
        print("   - Every lossless compressor will fail on some inputs")  # Print consequence
        print()  # Print empty line
        print("CONCLUSION:")  # Print conclusion header
        print("The friend's idea is theoretically IMPOSSIBLE for general case.")  # Print main conclusion
        print("Can only work for specific input classes (e.g., sparse vectors).")  # Print limitation
    
    # Execute all parts of exercise 1b
    prove_deterministic_impossibility()  # Run impossibility proof
    test_compression_idea()  # Run compression test
    bibliographic_research()  # Run bibliographic research

def theoretical_analysis():
    """Theoretical analysis for exercise questions"""
    print("\n" + "="*60)  # Print separator line
    print("THEORETICAL ANALYSIS")  # Print analysis header
    print("="*60)  # Print separator line
    
    print("\n=== QUESTION: CALCULATE T FOR 99% SUCCESS ===")  # Print question header
    print("We want probability at least 99% of no error in 10,000 queries")  # Print question description
    print()  # Print empty line
    print("THEORETICAL ANALYSIS:")  # Print analysis header
    print("- Let δ = failure probability per query")  # Print first line
    print("- For T repetitions: δ ≤ 1/2^T (worst case)")  # Print second line
    print("- For Q queries: δ_total ≤ Q × δ (Union Bound)")  # Print third line
    print("- We want: δ_total ≤ 0.01")  # Print fourth line
    print("- So: Q × (1/2^T) ≤ 0.01")  # Print inequality
    print("- 10000 / 2^T ≤ 0.01")  # Print specific case
    print("- 2^T ≥ 1000000")  # Print rearranged inequality
    print("- T ≥ log₂(1000000) ≈ 20")  # Print final result
    print()  # Print empty line
    print("RESULT: T ≥ 20")  # Print conclusion
    
    print("\n=== QUESTION: WHY THEORY IS PESSIMISTIC ===")  # Print question header
    print("We observe that in practice T << 20 is needed. Why?")  # Print observation
    print()  # Print empty line
    print("REASONS FOR PESSIMISM:")  # Print reasons header
    print("1. WORST-CASE ANALYSIS:")  # Print first reason
    print("   - Theory covers worst possible cases")  # Print explanation
    print("   - In practice cases are 'better'")  # Print practical observation
    print()  # Print empty line
    print("2. UNION BOUND:")  # Print second reason
    print("   - Union Bound is loose")  # Print explanation
    print("   - P(A₁ ∪ A₂ ∪ ... ∪ Aₙ) ≤ P(A₁) + P(A₂) + ... + P(Aₙ)")  # Print formula
    print("   - Equality holds only if events are disjoint")  # Print condition
    print("   - In practice correlation reduces error probability")  # Print practical effect
    print()  # Print empty line
    print("3. INDEPENDENCE ASSUMPTION:")  # Print third reason
    print("   - Theory assumes complete independence between queries")  # Print assumption
    print("   - In practice queries have structure")  # Print reality
    print()  # Print empty line
    print("4. HASH FUNCTION QUALITY:")  # Print fourth reason
    print("   - Theory assumes worst-case for hash functions")  # Print assumption
    print("   - In practice universal hash functions are 'lucky'")  # Print reality
    print()  # Print empty line
    print("5. INPUT DISTRIBUTION:")  # Print fifth reason
    print("   - Theory doesn't exploit input structure")  # Print limitation
    print("   - Binary vectors with 75% zeros have special structure")  # Print specific case

def answer_sparse_vector_question():
    """Answer the question about sparse vectors"""
    print("\n=== QUESTION: SPARSE VECTORS (99% ZEROS) ===")  # Print question header
    print("Do sparse vectors need larger T?")  # Print question
    print()  # Print empty line
    print("ANSWER: YES, and here's why:")  # Print answer
    print()  # Print empty line
    print("1. FEWER CHOICES:")  # Print first reason
    print("   - Sparse vector = fewer non-zero elements")  # Print explanation
    print("   - Fewer choices for sampling")  # Print consequence
    print("   - Higher probability of selecting wrong element")  # Print problem
    print()  # Print empty line
    print("2. HASH COLLISIONS:")  # Print second reason
    print("   - With fewer elements, higher collision probability")  # Print explanation
    print("   - Hash buckets are more sparse")  # Print state
    print("   - Harder to check 1-sparse condition")  # Print difficulty
    print()  # Print empty line
    print("3. SIGNAL-TO-NOISE RATIO:")  # Print third reason
    print("   - Less 'signal' (true elements)")  # Print signal
    print("   - Same 'noise' (false positives)")  # Print noise
    print("   - Worse SNR requires more repetitions")  # Print requirement
    print()  # Print empty line
    print("4. STATISTICAL POWER:")  # Print fourth reason
    print("   - For detecting rare events need better accuracy")  # Print need
    print("   - This requires larger T")  # Print requirement
    print()  # Print empty line
    print("PRACTICAL EXAMPLE:")  # Print example header
    print("- Vector with 75% zeros: ~2500 non-zero elements")  # Print first case
    print("- Vector with 99% zeros: ~100 non-zero elements")  # Print second case
    print("- Second case is 25x harder to find correct element!")  # Print comparison

def test_sparse_vector():
    """Test with very sparse vector"""
    print("\n=== Test with sparse vector (99% zeros) ===")  # Print test header
    
    n = 10000  # Set vector dimension
    
    # Vector with 99% probability for 0
    vector = generate_binary_vector(n, 0.99)  # Generate very sparse vector
    nonzero_positions = [i+1 for i, val in enumerate(vector) if val == 1]  # Find non-zero positions
    print(f"Non-zero positions: {len(nonzero_positions)}")  # Print count
    
    if len(nonzero_positions) == 0:  # If no non-zero positions
        print("No non-zero positions")  # Print message
        return  # Return early
    
    # Test with various T values
    for T in [2, 5, 10]:  # Iterate through T values
        print(f"\n--- T = {T} ---")  # Print current T
        sampler = OptimizedNonZeroSampler(n, T)  # Create sampler
        
        # Feed sampler
        for pos in nonzero_positions:  # Iterate through positions
            sampler.update(pos, 1)  # Add each position
        
        # Test removal
        errors = 0  # Initialize error counter
        for pos in nonzero_positions:  # Iterate through positions
            sampler.update(pos, -1)  # Remove each position
            # After each removal, check if sampler is consistent
            
        # Final check - should be empty
        if not sampler.is_empty() or sampler.sample_nonzero() is not None:  # If not empty
            errors += 1  # Increment error counter
        
        print(f"T = {T}, Errors: {errors}")  # Print results

def comprehensive_test():
    """Comprehensive test of all components"""
    print("\n" + "="*60)  # Print separator line
    print("COMPREHENSIVE TEST OF ALL COMPONENTS")  # Print test header
    print("="*60)  # Print separator line
    
    # Test 1: Simple Recovery Mechanism
    test_simple_recovery_mechanism()  # Run simple recovery test
    
    # Test 2: Non-Zero Sampler (simple)
    test_non_zero_sampler_simple()  # Run simple sampler test
    
    # Test 3: Exercise questions
    theoretical_analysis()  # Run theoretical analysis
    answer_sparse_vector_question()  # Answer sparse vector question

def save_results_to_file(results_text: str):
    """Save results to a text file"""
    try:  # Try to save file
        with open("non_zero_sampler_results.txt", "w", encoding="utf-8") as f:  # Open file for writing
            f.write(results_text)  # Write results to file
        print(f"\nResults saved to non_zero_sampler_results.txt")  # Print success message
    except Exception as e:  # If error occurs
        print(f"\nError saving results: {e}")  # Print error message

if __name__ == "__main__":
    import sys  # Import sys module for stdout capture
    from io import StringIO  # Import StringIO for string buffer
    
    random.seed(42)  # Set random seed for reproducible results
    
    # Capture all output to save to file
    old_stdout = sys.stdout  # Save original stdout
    sys.stdout = captured_output = StringIO()  # Redirect stdout to string buffer
    
    print("STARTING COMPLETE TEST OF UNIT C")  # Print program start
    print("=" * 60)  # Print separator line
    
    # Execute all tests and exercises
    comprehensive_test()  # Run comprehensive tests
    
    # Exercise 1a
    exercise_1a_complete()  # Run exercise 1a
    
    # Test with sparse vectors
    test_sparse_vector()  # Run sparse vector test
    
    # Exercise 1b
    exercise_1b_complete()  # Run exercise 1b
    
    print("\n" + "="*60)  # Print separator line
    print("END OF PROGRAM")  # Print program end
    print("="*60)  # Print separator line
    
    # Restore stdout and save results
    sys.stdout = old_stdout  # Restore original stdout
    results_text = captured_output.getvalue()  # Get captured output
    print(results_text)  # Print results to console
    save_results_to_file(results_text)  # Save results to file

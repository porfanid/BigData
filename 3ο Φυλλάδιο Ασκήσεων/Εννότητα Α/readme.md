# Κύρια Χαρακτηριστικά της Υλοποίησης
1. Αλγόριθμος Γραμμικού Χρόνου (0.25 μονάδες extra για βελτιστοποίηση)

Χρησιμοποιεί BFS με επαναχρησιμοποιούμενο boolean array
Αποφεύγει την αρχικοποίηση όλου του πίνακα σε κάθε κλήση
Καθαρίζει μόνο τις θέσεις που χρησιμοποιήθηκαν

2. Αλγόριθμος Τοπικού Ελέγχου

Υλοποιεί την ρουτίνα με budget B
Τερματίζει όταν εξερευνήσει B+1 κόμβους ή ολοκληρώσει τη διερεύνηση

3. "Απλός" Υπογραμμικός Αλγόριθμος

Χρόνος: O(1/(ε²Δ))
Χρησιμοποιεί μειούμενα ε: ε=1/Δ, ε/2, ε/4, ...

4. "Εκλεπτυσμένος" Υπογραμμικός Αλγόριθμος

Χρόνος: O((1/ε)·log(1/(εΔ))²)
Πιο αποδοτικός για μεγάλα γραφήματα

5. Γρήγορος Αλγόριθμος με Union-Find (0.5 μονάδες)

Σχεδόν γραμμικός χρόνος O(m·α(n)) όπου α η inverse Ackermann
Για τα μεγάλα πειράματα (n=1,000,000)

## Βασικές Λειτουργίες
random_graph_generation_experiment(): Τρέχει το βασικό πείραμα με διαφορετικούς αλγορίθμους
run_experiments(): Εκτελεί το κύριο πείραμα για n=100,000 με 250,000 εισαγωγές
test_fast_algorithm(): Δοκιμάζει τον Union-Find αλγόριθμο για μεγάλα n
Αναμενόμενα Αποτελέσματα

n=100: 200-500 ακμές μέχρι συνεκτικότητα
n=100,000: Γραφική παράσταση που δείχνει αύξηση κλήσεων καθώς το γράφημα πλησιάζει τη συνεκτικότητα
n=1,000,000: Γρήγορη εκτέλεση με Union-Find

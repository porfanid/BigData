class HashFunction:
    def __init__(self, alpha, beta, p, N):
        self.alpha = alpha
        self.beta = beta
        self.p = p
        self.N = N

    def hash(self, X):
        blocks = [int(X[i*20:(i+1)*20], 2) for i in range(5)]
        c = 0
        for Bi in blocks:
            c = (self.alpha * (Bi + c) + self.beta) % self.p
        return c % self.N

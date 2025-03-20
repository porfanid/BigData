from section_3.ex_1.a.bloom_filter import BloomFilter


class Router:
    def __init__(self, router_id, N_bits=10000, k_hashes=1):
        self.id = router_id
        self.bloom_filter = BloomFilter(N_bits, k_hashes)
        self.received_messages = set()  # Για debugging/ιχνηλάτηση αν θες

    def receive_message(self, message):
        self.bloom_filter.add(message)
        self.received_messages.add(message)

    def has_message(self, message):
        return self.bloom_filter.check(message)

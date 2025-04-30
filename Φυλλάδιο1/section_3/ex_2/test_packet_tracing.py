import unittest
import random
from unittest.mock import patch, MagicMock
import tempfile
import os
from main import (
    create_routers, generate_messages, forward_messages, trace_message,
    packet_tracing_simulation, load_graph
)

class TestPacketTracing(unittest.TestCase):
    def setUp(self):
        # Create a simple test graph
        self.test_graph = {
            1: [2, 3],
            2: [4],
            3: [4],
            4: [5],
            5: []
        }
        self.n_nodes = 5

        # Mock router class for testing
        class MockRouter:
            def __init__(self):
                self.messages = set()

            def receive_message(self, message):
                self.messages.add(message)

            def has_message(self, message):
                return message in self.messages

        self.RouterClass = MockRouter

        # Create a temp file with graph data for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(self.temp_file.name, 'w') as f:
            f.write("5\n")  # Number of nodes
            f.write("1 2\n")  # Edge 1->2
            f.write("1 3\n")  # Edge 1->3
            f.write("2 4\n")  # Edge 2->4
            f.write("3 4\n")  # Edge 3->4
            f.write("4 5\n")  # Edge 4->5

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_load_graph(self):
        graph, n = load_graph(self.temp_file.name)
        self.assertEqual(n, 5)
        self.assertEqual(len(graph), 5)
        self.assertEqual(graph[1], [2, 3])
        self.assertEqual(graph[4], [5])
        self.assertEqual(graph[5], [])

    @patch('main.BloomFilter')
    def test_create_routers(self, mock_bloom):
        # Mock the BloomFilter class
        mock_bloom.return_value = MagicMock()

        routers = create_routers(self.test_graph, n_bits=1000, k_hashes=2)

        self.assertEqual(len(routers), 5)
        for i in range(1, 6):
            self.assertIn(i, routers)

        # Verify BloomFilter was called with correct parameters
        self.assertEqual(mock_bloom.call_count, 5)

    def test_generate_messages(self):
        messages = generate_messages(num_messages=100)
        self.assertEqual(len(messages), 100)
        # Verify messages are unique
        self.assertEqual(len(set(messages)), 100)

    def test_forward_messages(self):
        routers = {i: self.RouterClass() for i in range(1, 6)}
        messages = ["test_msg_1", "test_msg_2"]

        with patch('random.randint', return_value=1), \
             patch('random.choice', side_effect=lambda x: x[0]):
            forward_messages(self.test_graph, routers, messages)

            # Check if messages propagated through the network
            for msg in messages:
                self.assertTrue(routers[1].has_message(msg))
                self.assertTrue(routers[2].has_message(msg))
                self.assertFalse(routers[3].has_message(msg))  # Path 1->2->4->5 chosen
                self.assertTrue(routers[4].has_message(msg))
                self.assertTrue(routers[5].has_message(msg))

    def test_trace_message(self):
        routers = {i: self.RouterClass() for i in range(1, 6)}
        message = "test_message"
        sources = {1, 2}

        # Only source 1 has the message
        routers[1].receive_message(message)
        routers[3].receive_message(message)
        routers[4].receive_message(message)

        success = trace_message(self.test_graph, routers, message, 5, sources)
        self.assertTrue(success)

        # Both sources have the message (ambiguous)
        routers[2].receive_message(message)
        success = trace_message(self.test_graph, routers, message, 5, sources)
        self.assertFalse(success)

        # No source has the message
        routers = {i: self.RouterClass() for i in range(1, 6)}
        routers[3].receive_message(message)
        routers[4].receive_message(message)
        success = trace_message(self.test_graph, routers, message, 5, sources)
        self.assertFalse(success)

    @patch('main.load_graph')
    @patch('main.create_routers')
    @patch('main.generate_messages')
    @patch('main.forward_messages')
    @patch('main.trace_message')
    def test_packet_tracing_simulation(self, mock_trace, mock_forward,
                                      mock_generate, mock_create, mock_load):
        # Setup mocks
        mock_load.return_value = (self.test_graph, self.n_nodes)
        mock_create.return_value = {i: MagicMock() for i in range(1, 6)}
        messages = ["msg1", "msg2", "msg3"]
        mock_generate.return_value = messages
        mock_trace.side_effect = [True, False, True]  # 2/3 successful

        # Run simulation
        result = packet_tracing_simulation(self.temp_file.name, k_hashes=2)

        # Verify results
        self.assertEqual(result, 2)
        mock_load.assert_called_once_with(self.temp_file.name)
        mock_create.assert_called_once()
        mock_generate.assert_called_once_with(num_messages=100000)
        mock_forward.assert_called_once()
        self.assertEqual(mock_trace.call_count, 3)


class TestBloomFilterIntegration(unittest.TestCase):
    """Integration tests that require the actual BloomFilter implementation"""

    def setUp(self):
        self.test_graph = {
            1: [2],
            2: [3],
            3: []
        }

    @patch('main.BloomFilter')  # To avoid using the actual BloomFilter
    def test_message_tracing_with_bloom_filters(self, mock_bloom):
        # Create a mock that simulates Bloom filter behavior
        class MockBloom:
            def __init__(self):
                self.items = set()

            def add(self, item):
                self.items.add(item)

            def check(self, item):
                return item in self.items

        # Set up the mock to return our simulated Bloom filter
        mock_bloom.side_effect = MockBloom

        # Create routers with the mock
        routers = create_routers(self.test_graph, n_bits=100, k_hashes=1)

        # Test messages
        msg1 = "test_message_1"
        msg2 = "test_message_2"

        # Simulate message receipt
        routers[1].receive_message(msg1)
        routers[2].receive_message(msg1)
        routers[3].receive_message(msg1)

        routers[2].receive_message(msg2)
        routers[3].receive_message(msg2)

        # Define source routers
        sources = {1, 2}

        # Test tracing from router 3
        success1 = trace_message(self.test_graph, routers, msg1, 3, sources)
        success2 = trace_message(self.test_graph, routers, msg2, 3, sources)

        # Only msg1 should trace uniquely to router 1
        self.assertTrue(success1)
        self.assertTrue(success2)


if __name__ == '__main__':
    unittest.main()
import unittest

import client
import server
from client import create_presence_message
from server import handle_message
from utils import load_configs


class TestChat(unittest.TestCase):
    def setUp(self):
        pass

    def test_config(self):
        config = load_configs()
        self.assertTrue(isinstance(config, dict))

    def test_create_presence_message(self):
        client.CONFIGS = load_configs(is_server=False)
        response = create_presence_message("test")
        eq_response = {'action': 'presence', 'user': {'account_name': 'test'}}
        for i in eq_response:
            self.assertEqual(eq_response.get(i), response.get(i))
        self.assertIsInstance(response.get('time'), float)

    def test_handle_message(self):
        server.CONFIGS = load_configs(is_server=True)
        message = {'action': 'presence', 'time': 1624537883.8739402, 'user': {'account_name': 'Guest'}}
        response = handle_message(message)
        self.assertEqual(response.get('response'), 200)


if __name__ == '__main__':
    unittest.main()
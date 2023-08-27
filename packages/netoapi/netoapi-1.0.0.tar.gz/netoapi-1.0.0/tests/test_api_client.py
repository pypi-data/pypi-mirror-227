import unittest

from api_client import NetoAPIClient


class TestAPIClient(unittest.TestCase):
    def test_timeout_read(self):
        c = NetoAPIClient("http://not/a/url", "testuser", "abc123")

        self.assertEqual(c.timeout, (5, 5))

    def test_timout_set_none(self):
        c = NetoAPIClient("http://not/a/url", "testuser", "abc123")
        c.timeout = None
        self.assertEquals(c.timeout, (None, None))

    def test_timeout_set_int(self):
        c = NetoAPIClient("http://not/a/url", "testuser", "abc123")
        c.timeout = 10
        self.assertEqual(c.timeout, (10, 10))

    def test_timout_set_tuple(self):
        c = NetoAPIClient("http://not/a/url", "testuser", "abc123")
        c.timeout = (6, 7)
        self.assertEqual(c.timeout, (6, 7))

    def test_timout_set_type_error(self):
        c = NetoAPIClient("http://not/a/url", "testuser", "abc123")
        with self.assertRaises(TypeError):
            c.timeout = [1, 2]


unittest.main()

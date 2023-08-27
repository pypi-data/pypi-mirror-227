import unittest

from api_session import RequestsAPISession, get_api_session


class TestRequestsAPISession(unittest.TestCase):
    def test_auth_session(self):
        d = {
            "NETOAPI_USERNAME": "testuser",
            "NETOAPI_KEY": "abc123",
            "Accept": "application/json",
        }
        s = RequestsAPISession()
        h = s.auth_session(d["NETOAPI_USERNAME"], d["NETOAPI_KEY"])
        self.assertDictEqual(s.headers, d)

    def test_send_request(self):
        s = RequestsAPISession()
        # Test the post request

    def test_get_api_session(self):
        s = get_api_session()
        self.assertIsInstance(s, RequestsAPISession)


unittest.main()

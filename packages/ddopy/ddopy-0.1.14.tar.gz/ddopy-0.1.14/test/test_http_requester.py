# write unit tests for database_manager.py

import unittest
from ddopy.http.http_requester import HttpRequester


class TestHttpRequester(unittest.TestCase):
    def test_request(self):
        object = HttpRequester()
        url = "https://httpbin.org/post"
        object.set_endpoint_url(url)
        object.add_header("Content-Type", "application/json")
        payload = {"key1": "value1", "key2": "value2"}
        response = object.post_request(payload)
        self.assertEqual(response["url"], url)
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        self.assertEqual(response["json"], payload)

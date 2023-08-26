"""
This module contains HttpRequester class which is used to send HTTP requests.
"""
import json
import requests


class HttpRequester:
    def __init__(self):
        self._endpoint_url = None
        self._headers = {}

    def set_endpoint_url(self, url):
        self._endpoint_url = url

    def add_header(self, key, value):
        self._headers[key] = value

    def post_request(self, payload):
        if self._endpoint_url is None:
            raise Exception("Endpoint URL is not set. Call set_endpoint_url() method first.")

        response = requests.post(url=self._endpoint_url, data=json.dumps(payload), headers=self._headers, timeout=30)
        response_json = response.json()

        return response_json

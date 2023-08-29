"""
This module contains HttpRequester class which is used to send HTTP requests.
"""
import json
import requests


class HttpRequester:
    def __init__(self):
        self._base_url = None
        self._headers = {}

    def set_base_url(self, url):
        self._base_url = url

    def add_header(self, key, value):
        self._headers[key] = value

    def post_request(self, payload, relative_url=""):
        if self._base_url is None:
            raise Exception("Base URL is not set. Call set_base_url() method first.")

        url = f"{self._base_url}/{relative_url.lstrip('/')}".rstrip("/")
        response = requests.post(url=url, data=json.dumps(payload), headers=self._headers, timeout=30)

        return response

    def get_request(self, relative_url=""):
        if self._base_url is None:
            raise Exception("Base URL is not set. Call set_base_url() method first.")

        url = f"{self._base_url}/{relative_url.lstrip('/')}".rstrip("/")
        response = requests.get(url=url, headers=self._headers, timeout=30)

        return response

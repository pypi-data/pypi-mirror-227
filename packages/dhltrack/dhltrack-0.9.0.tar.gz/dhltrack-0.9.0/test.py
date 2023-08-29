from unittest import TestCase, main
from configparser import ConfigParser

import json

from dhltrack import *

class TestHTTPRequest(TestCase):
    def test_http_request(self):
        http = HTTPRequest("https://httpbin.org/get")
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)

class TestDHL(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.dhl = DHL.from_config(self.config)

    def test_tracking(self):
        tracking_number = "LE650235858DE"
        response = self.dhl.track(tracking_number)
        self.assertEqual(response["shipments"][0]["id"], tracking_number)
        
if __name__ == "__main__":
    main()
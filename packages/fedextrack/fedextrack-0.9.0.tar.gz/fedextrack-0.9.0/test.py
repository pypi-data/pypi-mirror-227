from unittest import TestCase, main
from configparser import ConfigParser

import json

from fedextrack import *

class TestHTTPRequest(TestCase):
    def test_http_request(self):
        http = HTTPRequest("https://httpbin.org/get")
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)

    def test_http_request_with_json_payload(self):
        http = HTTPRequest("https://httpbin.org/post")
        http.add_json_payload({"foo": "bar"})
        response = http.execute()
        self.assertEqual(response["headers"]["User-Agent"], http.USER_AGENT)
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        self.assertEqual(response["json"]["foo"], "bar")

class TestFedEx(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.fedex = FedEx.from_config(self.config)

    def test_tracking(self):
        tracking_number = "702395541585"
        response = self.fedex.track_by_tracking_number(tracking_number)
        self.assertEqual(response["output"]["completeTrackResults"][0]["trackingNumber"], tracking_number)
        
if __name__ == "__main__":
    main()
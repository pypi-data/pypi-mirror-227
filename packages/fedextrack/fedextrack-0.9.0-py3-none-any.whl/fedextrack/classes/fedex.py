from hashlib import md5
from configparser import ConfigParser
from urllib.parse import urlencode

import json

from .http import HTTPRequest


class FedEx:
    BASE_URL = "https://apis.fedex.com/"
    TRACK_BY_NUMBER = "track/v1/trackingnumbers"
    OAUTH_TOKEN = "oauth/token"

    def __init__(self, key: str, secret: str, base_url: str = BASE_URL):
        self.key = key
        self.secret = secret
        self.base_url = base_url

    def get_token(self):
        message = {
            "grant_type": "client_credentials",
            "client_id": self.key,
            "client_secret": self.secret,
        }

        request = self.get_request(self.OAUTH_TOKEN, {}, False)

        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        request.data = urlencode(message).encode("utf-8")

        response = request.execute()
        return response["access_token"]

    @classmethod
    def from_config(cls, config: ConfigParser | str, section: str = "FedEx") -> "FedEx":
        if isinstance(config, str):
            temp_config = ConfigParser()
            temp_config.read(config)
            config = temp_config

        key = config.get(section, "key")
        secret = config.get(section, "secret")
        base_url = config.get(section, "base_url", fallback=cls.BASE_URL)

        return cls(key, secret, base_url)

    def get_request(self, endpoint: str, message: dict = {}, add_token: bool = True) -> HTTPRequest:
        url = self.base_url + endpoint

        request = HTTPRequest(url)

        if message:
            request.add_json_payload(message)

        if add_token:
            request.add_header("Authorization", "Bearer " + self.get_token())

        return request

    def track_by_tracking_number(self, tracking_number: str, include_detailed_scans: bool = True) -> bytes:
        message = {
            "include_detailed_scans": include_detailed_scans,
            "trackingInfo": [
                {
                    "trackingNumberInfo": {
                        "trackingNumber": tracking_number,
                    }
                }
            ]
        }

        request = self.get_request(self.TRACK_BY_NUMBER, message)
        return request.execute()

from hashlib import md5
from configparser import ConfigParser
from urllib.parse import urlencode
from typing import Optional

import json

from .http import HTTPRequest


class DHL:
    BASE_URL = "https://api-eu.dhl.com/track/"
    BASE_URL_SANDBOX = "https://api-test.dhl.com/track/"

    def __init__(self, key: str, secret: str, base_url: str = BASE_URL):
        self.key = key
        self.secret = secret
        self.base_url = base_url

    @classmethod
    def from_config(cls, config: ConfigParser | str, section: str = "DHL") -> "DHL":
        if isinstance(config, str):
            temp_config = ConfigParser()
            temp_config.read(config)
            config = temp_config

        key = config.get(section, "key")
        secret = config.get(section, "secret")
        base_url = config.get(section, "base_url", fallback=cls.BASE_URL)

        return cls(key, secret, base_url)

    def get_request(self, endpoint: str, add_token: bool = True) -> HTTPRequest:
        url = self.base_url + endpoint

        request = HTTPRequest(url)

        if add_token:
            request.add_header("DHL-API-Key", self.key)

        return request

    def track(self, tracking_number: str, **kwargs) -> bytes:
        params = {
            "trackingNumber": tracking_number,
        }

        for key in ("service", "requesterCountryCode", "originCountryCode", "language", "offset", "limit"):
            if key in kwargs:
                params[key] = kwargs[key]

        request = self.get_request(f"shipments?{urlencode(params)}")
        return request.execute()

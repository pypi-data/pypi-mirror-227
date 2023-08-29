from urllib.request import Request, urlopen
from urllib.error import HTTPError
from io import BytesIO

import gzip
import json


class HTTPRequest(Request):
    USER_AGENT = "Mozilla/5.0 (compatible; DHLTrack/dev; +https://kumig.it/kumitterer/dhltrack)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_header("User-Agent", self.USER_AGENT)

    def execute(self, load_json: bool = True, *args, **kwargs):
        try:
            response = urlopen(self, *args, **kwargs).read()
        except HTTPError as e:
            print(e.read())
            raise
        if load_json:
            response = json.loads(response)
        return response

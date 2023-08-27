from urllib.request import Request, urlopen
from urllib.error import HTTPError
from io import BytesIO

import gzip
import json


class HTTPRequest(Request):
    USER_AGENT = "Mozilla/5.0 (compatible; FedExTrack/dev; +https://kumig.it/kumitterer/fedextrack)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_header("User-Agent", self.USER_AGENT)

    @staticmethod
    def read(response):
        if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            return f.read()

        return response.read()

    def execute(self, load_json: bool = True, *args, **kwargs):
        try:
            response = self.read(urlopen(self, *args, **kwargs))
        except HTTPError as e:
            print(self.read(e))
            raise
        if load_json:
            response = json.loads(response)
        return response

    def add_json_payload(self, payload: dict):
        self.add_header("Content-Type", "application/json")
        self.data = json.dumps(payload).encode("utf-8")

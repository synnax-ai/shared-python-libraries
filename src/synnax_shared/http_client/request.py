from typing import Dict

import requests

from synnax_shared.http_client.constants import RETRYABLE_STATUS_CODES
from synnax_shared.http_client.errors import HttpError, HttpRetryableError
from synnax_shared.http_client.http_client import HttpClient


class RequestHttpClient(HttpClient):
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = requests.Session()

    def post(self, endpoint: str, body: Dict, headers: Dict = {}) -> Dict:
        response = self.session.post(
            self.api_url + endpoint,
            json=body,
            headers=headers,
        )
        json_obj = response.json()

        if response.status_code in RETRYABLE_STATUS_CODES:
            raise HttpRetryableError(json_obj["message"], response.status_code)

        if response.status_code < 200 | response.status_code >= 300:
            raise HttpError(json_obj["message"], response.status_code)

        return json_obj

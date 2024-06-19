from typing import Dict

from retry import retry

from synnax_shared.http_client.errors import HttpRetryableError
from synnax_shared.http_client.http_client import HttpClient


class RetryingHttpClient(HttpClient):
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    @retry((HttpRetryableError), tries=5, delay=1, backoff=2)
    def post(self, endpoint: str, body: Dict, headers: Dict = {}) -> Dict:
        response = self.http_client.post(
            endpoint,
            body=body,
            headers=headers,
        )

        return response

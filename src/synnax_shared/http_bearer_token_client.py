from typing import Callable, Dict

import requests


class HttpBearerTokenClient:
    def __init__(self, api_url: str, token_provider: Callable[[], str]):
        self.api_url = api_url
        self.token_provider = token_provider
        self.session = requests.Session()

    def post(self, endpoint: str, request_body: Dict) -> Dict:
        response = self.session.post(
            self.api_url + endpoint,
            json=request_body,
            headers={"Authorization": "Bearer " + self.token_provider()},
        )
        return response.json()

import json
import logging
import time
from typing import Dict, List

import jwt
from mypy_boto3_lambda import LambdaClient

logger = logging.getLogger()


class SystemTokenIssuer:
    def __init__(
        self,
        lambda_client: LambdaClient,
        function_name: str,
        system_id: str,
        permissions: List[Dict[str, str | List[str]]],
        refresh_before_expiry_seconds: int,
    ):
        self.lambda_client = lambda_client
        self.function_name = function_name
        self.system_id = system_id
        self.permissions = permissions
        self.refresh_before_expiry_seconds = refresh_before_expiry_seconds
        self.token: str | None = None

    def get_token(self) -> str:
        if self.token is None:
            return self.refresh_token()

        if self.is_token_expiring(self.token):
            return self.refresh_token()

        return self.token

    def refresh_token(self) -> str:
        logger.info("Refreshing token")
        response = self.lambda_client.invoke(
            FunctionName=self.function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {"systemId": self.system_id, "permissions": self.permissions}
            ),
        )
        payload = json.loads(response["Payload"].read())

        if payload["token"] is None:
            raise Exception("Token not returned from token issuer")

        self.token = payload["token"]
        return payload["token"]

    def is_token_expiring(self, token: str) -> bool:
        payload = jwt.decode(token, options={"verify_signature": False})
        epoch_time = int(time.time())
        if payload["exp"] - epoch_time < self.refresh_before_expiry_seconds:
            return True
        return False

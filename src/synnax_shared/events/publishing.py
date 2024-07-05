import json
import logging
from typing import Generic, TypeVar

from botocore.exceptions import ClientError
from mypy_boto3_sns import SNSClient

from synnax_shared.events.model import DomainEvent

logger = logging.getLogger()
EventT = TypeVar("EventT", bound=DomainEvent)


class EventPublishingClient(Generic[EventT]):
    def __init__(self, sns_client: SNSClient, topic_arn: str) -> None:
        self.sns_client = sns_client
        self.topic_arn = topic_arn

    async def publish_event(self, event: EventT) -> None:
        try:
            response = self.sns_client.publish(
                Message=json.dumps(event),
                TopicArn=self.topic_arn,
                MessageAttributes={
                    "eventType": {"DataType": "String", "StringValue": event["type"]}
                },
            )
            logger.info(
                "Published event to SNS topic",
                extra={"response": response},
            )
        except ClientError as ex:
            logger.error(
                "Error publishing event to SNS topic",
                extra={"error": repr(ex)},
            )

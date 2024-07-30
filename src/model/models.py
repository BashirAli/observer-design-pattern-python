from abc import ABC, abstractmethod
from pydantic import Field, BaseModel
from pydantic_core import ValidationError
from datetime import datetime
from config.logger import logger

class Notification(BaseModel):
    data: dict = Field(..., description="dictionary of data")
    notification_time: datetime
    notification_id: str
    attributes: dict


class abstractSubscriber(ABC):
    @abstractmethod
    def acknowledge_message(self, *args, **kwargs):
        pass


class Subscriber(abstractSubscriber):
    def __init__(self, subscriber_display_name: str, subscriber_id: str):
        self.subscriber_display_name = subscriber_display_name
        self.subscriber_id = subscriber_id

    def acknowledge_message(self, notification: Notification):
        return f"{self.subscriber_display_name} has acknowledged notification {notification.notification_id} with data: {notification.data}, attributes: {notification.attributes} at {notification.notification_time}"

    def __repr__(self):
        return f"{self.subscriber_display_name}"


class Topic:
    def __init__(self, topic_id: str, topic_name: str):
        self.topic_id = topic_id
        self.topic_name: str = topic_name
        self.subscribers: list[Subscriber] = []

    def __repr__(self):
        return f"{self.topic_name}, {self.subscribers}"

    @staticmethod
    def _validate_publish(data: dict) -> Notification | None:
        try:
            validated_model = Notification(**data)
        except ValidationError as ve:
            logger.info(f"Message is invalid {ve}")
            validated_model = None

        return validated_model

    def add_subscriber(self, subscriber: Subscriber) -> None:
        self.subscribers.append(subscriber)

    def publish(self, data: dict) -> None:
        publish_notification = self._validate_publish(data)
        if publish_notification:
            for sub in self.subscribers:
                sub.acknowledge_message(publish_notification)

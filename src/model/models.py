from abc import ABC, abstractmethod
from pydantic import Field, BaseModel
from datetime import datetime


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

    def acknowledge_message(self, notification):
        print(f"Received notification {notification} with data {notification.data}")


class Topic:
    def __init__(self, topic_id: str, topic_name: str):
        self.topic_id = topic_id
        self.topic_name: str = topic_name
        self.subscribers: list[Subscriber] = []

    def _validate_data(self):
        pass

    def add_subscriber(self, subscriber: Subscriber) -> None:
        pass

    def publish(self, ) -> None:
        for sub in self.subscribers:
            sub.acknowledge_message()

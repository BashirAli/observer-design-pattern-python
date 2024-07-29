from abc import ABC, abstractmethod
from pydantic import Field, BaseModel
import datetime


class Notification(BaseModel):
    data: dict = Field(..., description="dictionary of data")
    notification_time: datetime
    notification_id: str
    attributes: dict


class abstractSubscriber(ABC):
    @abstractmethod
    def receive_notification(self, *args, **kwargs):
        pass


class Subscriber(abstractSubscriber):
    def __init__(self, subscriber_display_name: str, subscriber_id: str):
        self.subscriber_display_name = subscriber_display_name
        self.subscriber_id = subscriber_id

    def receive_notification(self, notification):
        print(f"Received notification {notification} with data {notification.data}")


class Topic:
    def __init__(self):
        self.subscribers: list[Subscriber] = []

    def _validate_data(self):
        pass

    def add_subscriber(self, subscriber: Subscriber) -> None:
        pass

    def notify_subscribers(self, ) -> None:
        for sub in self.subscribers:
            sub.receive_notification()

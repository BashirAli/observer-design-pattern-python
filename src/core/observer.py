import random
from config.logger import logger
import pendulum

from model.models import Topic, Subscriber


class Observer:
    def __init__(self):
        self.topics: list[Topic] = []

    def create_infra(self, topic_config: dict) -> None:
        for topic in topic_config:
            sub_list = []
            for sub in topic["subscribers"]:
                subscriber = self._build_subscriber(sub)
                sub_list.append(subscriber)

            self.topics.append(self._build_topic(topic, sub_list))

    @staticmethod
    def _build_subscriber(subscriber_config: dict) -> Subscriber:
        return Subscriber(subscriber_id=subscriber_config["subscriber_id"],
                          subscriber_display_name=subscriber_config["subscriber_display_name"])

    @staticmethod
    def _build_topic(topic_config: dict, subscriber_list: list[Subscriber]) -> Topic:
        new_topic = Topic(topic_id=topic_config["topic_id"], topic_name=topic_config["topic_name"])
        new_topic.set_subscribers(subscriber_list)

        return new_topic

    def notify(self, messages: list[dict]) -> None:
        messages_enriched = (
            list(map(lambda message: {"data": message, "notification_time": pendulum.now("Europe/London"),
                                      "notification_id": str(random.randint(0, 100)),
                                      "attributes": {"test_attributes": ""}}, messages)))
        ack_messages = [
            topic.publish(message)
            for message in messages_enriched
            for topic in self.topics
        ]

        logger.info([ack for ack in ack_messages])

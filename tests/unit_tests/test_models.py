from datetime import datetime

import pytest
from pydantic_core import ValidationError

from model.models import Notification, Subscriber, Topic


@pytest.fixture
def sample_data():
    return {
        "data": {"key": "value"},
        "notification_time": datetime.now(),
        "notification_id": "123",
        "attributes": {"attr_key": "attr_value"}
    }


@pytest.fixture
def invalid_data():
    return {
        "data": {"key": "value"},
        "notification_time": "invalid datetime",  # Invalid datetime
        "notification_id": "123",
        "attributes": {"attr_key": "attr_value"}
    }


@pytest.fixture
def subscriber():
    return Subscriber(subscriber_display_name="John Doe", subscriber_id="sub_123")


@pytest.fixture
def topic():
    return Topic(topic_id="topic_1", topic_name="Test Topic")


def test_add_subscriber(topic, subscriber):
    topic.add_subscriber(subscriber)
    assert subscriber in topic.subscribers


def test_set_subscribers(topic, subscriber):
    subscribers_list = [subscriber]
    topic.set_subscribers(subscribers_list)
    assert topic.subscribers == subscribers_list


def test_publish_valid_data(topic, subscriber, sample_data):
    topic.add_subscriber(subscriber)
    ack_msgs = topic.publish(sample_data)
    assert len(ack_msgs) == 1
    assert "John Doe has acknowledged notification 123" in ack_msgs[0]


def test_publish_invalid_data(topic, invalid_data):
    ack_msgs = topic.publish(invalid_data)
    assert len(ack_msgs) == 0


def test_subscriber_acknowledge_message(subscriber, sample_data):
    notification = Notification(**sample_data)
    ack_msg = subscriber.acknowledge_message(notification)
    expected_msg = "John Doe has acknowledged notification 123 with data: {'key': 'value'}, attributes: {'attr_key': 'attr_value'} at "
    assert ack_msg.startswith(expected_msg)


def test_repr_subscriber(subscriber):
    assert repr(subscriber) == "Subscriber Name: John Doe"


def test_repr_topic(topic, subscriber):
    topic.add_subscriber(subscriber)
    assert repr(topic) == "Topic: Test Topic, Subscribers: [Subscriber Name: John Doe]"


def test_publish_with_no_subscribers(topic, sample_data):
    ack_msgs = topic.publish(sample_data)
    assert len(ack_msgs) == 0  # No subscribers to acknowledge


def test_invalid_notification_raises_validation_error(invalid_data):
    with pytest.raises(ValidationError):
        Notification(**invalid_data)

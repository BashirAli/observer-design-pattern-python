from unittest.mock import patch

import pytest

from core.observer import Observer


@pytest.fixture
def topic_config():
    return [
        {
            "topic_id": "topic_1",
            "topic_name": "Test Topic 1",
            "subscribers": [
                {"subscriber_id": "sub_1", "subscriber_display_name": "Subscriber One"},
                {"subscriber_id": "sub_2", "subscriber_display_name": "Subscriber Two"}
            ]
        },
        {
            "topic_id": "topic_2",
            "topic_name": "Test Topic 2",
            "subscribers": [
                {"subscriber_id": "sub_3", "subscriber_display_name": "Subscriber Three"}
            ]
        }
    ]


@pytest.fixture
def messages():
    return [
        {"key": "value1"},
        {"key": "value2"}
    ]


def test_create_infra(topic_config):
    observer = Observer()
    observer.create_infra(topic_config)

    # Check that the infrastructure was created correctly
    assert len(observer.topics) == 2
    assert observer.topics[0].topic_id == "topic_1"
    assert len(observer.topics[0].subscribers) == 2
    assert observer.topics[1].topic_id == "topic_2"
    assert len(observer.topics[1].subscribers) == 1


def test_build_subscriber():
    subscriber_config = {"subscriber_id": "sub_1", "subscriber_display_name": "Subscriber One"}
    subscriber = Observer._build_subscriber(subscriber_config)
    assert subscriber.subscriber_id == "sub_1"
    assert subscriber.subscriber_display_name == "Subscriber One"


def test_build_topic():
    subscriber_config = {"subscriber_id": "sub_1", "subscriber_display_name": "Subscriber One"}
    subscriber = Observer._build_subscriber(subscriber_config)
    topic_config = {"topic_id": "topic_1", "topic_name": "Test Topic"}
    topic = Observer._build_topic(topic_config, [subscriber])

    assert topic.topic_id == "topic_1"
    assert topic.topic_name == "Test Topic"
    assert len(topic.subscribers) == 1
    assert topic.subscribers[0].subscriber_id == "sub_1"


def test_notify(topic_config, messages):
    observer = Observer()
    observer.create_infra(topic_config)

    with patch('model.models.Topic.publish', return_value=['Acknowledgment message']) as mock_publish:
        observer.notify(messages)

        # Check that publish was called twice per topic (once for each message)
        assert mock_publish.call_count == len(messages) * len(observer.topics)

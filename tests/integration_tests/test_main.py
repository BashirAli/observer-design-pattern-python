from unittest.mock import patch

from core.observer import Observer
from src.main import run_observer

# Mock data for YAML configuration
mock_yaml_data = {
    "topics": [
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
}

# Mock data for JSON messages
mock_json_data = [
    {"key": "value1"},
    {"key": "value2"}
]

def test_run_observer():
    # Patch the read_yaml_config and read_json_file functions to return mock data
    with patch('src.config.parser.read_yaml_config', return_value=mock_yaml_data) as mock_read_yaml, \
         patch('sec.config.parser.read_json_file', return_value=mock_json_data) as mock_read_json, \
         patch('src.config.logger.logger') as mock_logger:

        # Call the run_observer function with mock paths
        run_observer('mock_path_to_yaml', 'mock_path_to_json')

        # Check if the configuration and data files were read
        mock_read_yaml.assert_called_once_with('mock_path_to_yaml')
        mock_read_json.assert_called_once_with('mock_path_to_json')

        # Verify the logger calls
        mock_logger.info.assert_any_call("Created Observer infrastructure: ")
        mock_logger.info.assert_any_call("Publishing test message(s)")

        # Check if observer was set up correctly
        observer_manager = Observer()
        observer_manager.create_infra(mock_yaml_data["topics"])

        # Verify topics and subscribers creation
        assert len(observer_manager.topics) == 2
        assert observer_manager.topics[0].topic_name == "Test Topic 1"
        assert len(observer_manager.topics[0].subscribers) == 2
        assert observer_manager.topics[1].topic_name == "Test Topic 2"
        assert len(observer_manager.topics[1].subscribers) == 1

        # Verify notification is called with mock messages
        with patch('src.core.observer.Observer.notify', return_value=None) as mock_notify:
            observer_manager.notify(mock_json_data)
            mock_notify.assert_called_once_with(mock_json_data)

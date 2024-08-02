import json
from unittest.mock import patch, mock_open

import yaml

from config.parser import read_json_file, read_yaml_config

# Test data
sample_yaml_content = """
key1: value1
key2: value2
"""

sample_json_content = """
[
    {"key1": "value1"},
    {"key2": "value2"}
]
"""

sample_yaml_dict = {
    "key1": "value1",
    "key2": "value2"
}

sample_json_list = [
    {"key1": "value1"},
    {"key2": "value2"}
]


@patch("builtins.open", new_callable=mock_open, read_data=sample_yaml_content)
@patch("yaml.safe_load", return_value=sample_yaml_dict)
def test_read_yaml_config(mock_yaml_load, mock_open_file):
    result = read_yaml_config("dummy_path.yaml")
    mock_open_file.assert_called_once_with("dummy_path.yaml", "r")
    mock_yaml_load.assert_called_once()
    assert result == sample_yaml_dict


@patch("builtins.open", new_callable=mock_open, read_data=sample_json_content)
@patch("json.load", return_value=sample_json_list)
def test_read_json_file(mock_json_load, mock_open_file):
    result = read_json_file("dummy_path.json")
    mock_open_file.assert_called_once_with("dummy_path.json", "r")
    mock_json_load.assert_called_once()
    assert result == sample_json_list


@patch("builtins.open", new_callable=mock_open)
@patch("yaml.safe_load", side_effect=yaml.YAMLError)
def test_read_yaml_config_parsing_error(mock_yaml_load, mock_open_file):
    result = read_yaml_config("dummy_path.yaml")
    mock_open_file.assert_called_once_with("dummy_path.yaml", "r")
    mock_yaml_load.assert_called_once()
    assert result == {}


@patch("builtins.open", new_callable=mock_open)
@patch("json.load", side_effect=json.JSONDecodeError(msg="msg", doc="doc", pos=0))
def test_read_json_file_parsing_error(mock_json_load, mock_open_file):
    result = read_json_file("dummy_path.json")
    mock_open_file.assert_called_once_with("dummy_path.json", "r")
    mock_json_load.assert_called_once()
    assert result == []


@patch("builtins.open", new_callable=mock_open)
def test_read_yaml_config_file_not_found(mock_open_file):
    mock_open_file.side_effect = FileNotFoundError
    result = read_yaml_config("dummy_path.yaml")
    mock_open_file.assert_called_once_with("dummy_path.yaml", "r")
    assert result == {}


@patch("builtins.open", new_callable=mock_open)
def test_read_json_file_file_not_found(mock_open_file):
    mock_open_file.side_effect = FileNotFoundError
    result = read_json_file("dummy_path.json")
    mock_open_file.assert_called_once_with("dummy_path.json", "r")
    assert result == []


@patch("builtins.open", new_callable=mock_open)
def test_read_yaml_config_permission_error(mock_open_file):
    mock_open_file.side_effect = PermissionError
    result = read_yaml_config("dummy_path.yaml")
    mock_open_file.assert_called_once_with("dummy_path.yaml", "r")
    assert result == {}


@patch("builtins.open", new_callable=mock_open)
def test_read_json_file_permission_error(mock_open_file):
    mock_open_file.side_effect = PermissionError
    result = read_json_file("dummy_path.json")
    mock_open_file.assert_called_once_with("dummy_path.json", "r")
    assert result == []

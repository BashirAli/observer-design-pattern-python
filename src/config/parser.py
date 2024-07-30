import json

import yaml

from config.logger import logger


def read_yaml_config(file_path: str) -> dict:
    yaml_data = {}
    try:
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
    except FileNotFoundError as ex:
        logger.warning(f"YAML configuration file not found in {file_path}: {ex}")
    except PermissionError as pe:
        logger.warning(f"YAML configuration file not found in {file_path}: {pe}")
    except yaml.YAMLError as ye:
        logger.warning(f"YAML file parsing failed; {ye}")

    return yaml_data


def read_json_file(file_path: str) -> list:
    json_data = []
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError as ex:
        logger.warning(f"YAML configuration file not found in {file_path}: {ex}")
    except PermissionError as pe:
        logger.warning(f"YAML configuration file not found in {file_path}: {pe}")
    except json.JSONDecodeError as de:
        logger.warning(f"JSON file parsing failed; {de}")

    return json_data

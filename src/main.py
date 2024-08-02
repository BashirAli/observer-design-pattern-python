import argparse
from config.logger import logger
from config.parser import read_yaml_config, read_json_file
from core.observer import Observer


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_path_to_yaml',
        type=str,
        required=True,
        help='Path to YAML config file.'
    )

    parser.add_argument(
        '--input_path_to_data',
        type=str,
        required=True,
        help='Path to JSON notification data.'
    )

    return parser.parse_args()


def run_observer(input_path_to_yaml, input_path_to_data):
    observer_manager = Observer()
    observer_configuration = read_yaml_config(input_path_to_yaml)
    if observer_configuration:
        # create topic and subs
        observer_manager.create_infra(observer_configuration["topics"])
        logger.info("Created Observer infrastructure: ")
        logger.info(f"{topic.__repr__()} \n" for topic in observer_manager.topics)

        dummy_data = read_json_file(input_path_to_data)
        if dummy_data:
            logger.info("Publishing test message(s)")
            # notify subscribers
            observer_manager.notify(dummy_data)


def main():
    system_args = arg_parser()
    run_observer(system_args.input_path_to_yaml, system_args.input_path_to_data)
    # python3 src/main.py --input_path_to_yaml=src/main.yaml --input_path_to_data=src/data/uk_dummy_addresses.json


if __name__ == "__main__":
    main()

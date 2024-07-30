from config.parser import read_yaml_config, read_json_file
from config.logger import logger
import argparse
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


def main():
    system_args = arg_parser()
    observer_manager = Observer()
    observer_configuration = read_yaml_config(system_args.input_path_to_yaml)
    if observer_configuration:
        # create topic and subs
        print(observer_configuration)
        observer_manager.create_infra(observer_configuration["topics"])
        logger.info("Created Observer infrastructure")
        print(f"{topic.__repr__()} \n" for topic in observer_manager.topics)

        dummy_data = read_json_file(system_args.input_path_to_data)
        if dummy_data:
            logger.info("Sending test message(s)")

            # notify subscribers
            observer_manager.notify(dummy_data)
            # print(dummy_data)


if __name__ == "__main__":
    main()

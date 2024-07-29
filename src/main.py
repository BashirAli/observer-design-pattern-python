from config.yaml_parser import read_yaml_config


def main():
    observer_configuration = read_yaml_config("main.yaml")
    print(observer_configuration)



if __name__ == "__main__":
    main()
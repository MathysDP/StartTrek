# Modules
import argparse
import yaml

def get_config():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, required=True,
        help="Path to the YAML configuration file.")

    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

    return config
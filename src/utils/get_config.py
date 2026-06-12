# Modules
from argparse import ArgumentParser
from yaml import safe_load

def get_config():
    parser = ArgumentParser()

    parser.add_argument("--config", type=str, required=True,
        help="Path to the YAML configuration file.")

    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = safe_load(file)

    return config
